"""
Gmail Watcher - Monitors Gmail for unread important emails
Creates action items in AI_Employee_Vault/Needs_Action/
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import base64
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Configuration
CHECK_INTERVAL = 120  # seconds
PROCESSED_IDS_FILE = '.processed_ids.json'
LOG_DIR = Path('AI_Employee_Vault/Logs')
ACTION_DIR = Path('AI_Employee_Vault/Needs_Action')
TOKEN_FILE = 'token.json'

# Setup logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOG_DIR / 'gmail_watcher.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GmailWatcher:
    def __init__(self):
        self.service = None
        self.processed_ids = self.load_processed_ids()
        self.retry_delay = 1  # Initial retry delay in seconds
        self.max_retry_delay = 60

    def load_processed_ids(self) -> set:
        """Load previously processed email IDs"""
        if os.path.exists(PROCESSED_IDS_FILE):
            try:
                with open(PROCESSED_IDS_FILE, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            except Exception as e:
                logger.error(f"Error loading processed IDs: {e}")
                return set()
        return set()

    def save_processed_ids(self):
        """Save processed email IDs to file"""
        try:
            with open(PROCESSED_IDS_FILE, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed IDs: {e}")

    def authenticate(self) -> bool:
        """Authenticate with Gmail API using OAuth2"""
        creds = None

        # Load existing token
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            except Exception as e:
                logger.error(f"Error loading credentials: {e}")

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Credentials refreshed successfully")
                except Exception as e:
                    logger.error(f"Error refreshing credentials: {e}")
                    creds = None

            if not creds:
                try:
                    # Create credentials.json from environment variables
                    client_config = {
                        "installed": {
                            "client_id": os.getenv('GMAIL_CLIENT_ID'),
                            "client_secret": os.getenv('GMAIL_CLIENT_SECRET'),
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "redirect_uris": ["http://localhost"]
                        }
                    }

                    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                    creds = flow.run_local_server(port=0)
                    logger.info("New credentials obtained successfully")
                except Exception as e:
                    logger.error(f"Error obtaining new credentials: {e}")
                    return False

            # Save credentials
            try:
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                logger.error(f"Error saving credentials: {e}")

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error building Gmail service: {e}")
            return False

    def exponential_backoff(self):
        """Implement exponential backoff for retries"""
        time.sleep(self.retry_delay)
        self.retry_delay = min(self.retry_delay * 2, self.max_retry_delay)
        logger.info(f"Backing off for {self.retry_delay}s")

    def reset_retry_delay(self):
        """Reset retry delay after successful operation"""
        self.retry_delay = 1

    def get_unread_important_emails(self) -> List[Dict]:
        """Fetch unread and important emails from Gmail"""
        try:
            # Query for unread AND important emails
            query = 'is:unread is:important'

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                logger.debug("No unread important emails found")
                return []

            logger.info(f"Found {len(messages)} unread important email(s)")
            return messages

        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            self.exponential_backoff()
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching emails: {e}")
            self.exponential_backoff()
            return []

    def get_email_details(self, msg_id: str) -> Optional[Dict]:
        """Get detailed information about an email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            headers = message['payload']['headers']

            # Extract relevant headers
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            from_email = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')

            # Get email body
            body = self.get_email_body(message)

            # Get snippet
            snippet = message.get('snippet', '')

            return {
                'id': msg_id,
                'subject': subject,
                'from': from_email,
                'date': date,
                'body': body,
                'snippet': snippet
            }

        except HttpError as error:
            logger.error(f"Error getting email details for {msg_id}: {error}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting email details: {e}")
            return None

    def get_email_body(self, message: Dict) -> str:
        """Extract email body from message payload"""
        try:
            if 'parts' in message['payload']:
                # Multipart message
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
                    elif part['mimeType'] == 'text/html':
                        # Fallback to HTML if no plain text
                        data = part['body'].get('data', '')
                        if data:
                            html = base64.urlsafe_b64decode(data).decode('utf-8')
                            # Basic HTML stripping
                            text = re.sub('<[^<]+?>', '', html)
                            return text
            else:
                # Simple message
                data = message['payload']['body'].get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')

            return message.get('snippet', '')

        except Exception as e:
            logger.error(f"Error extracting email body: {e}")
            return message.get('snippet', '')

    def sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filename"""
        # Remove or replace invalid filename characters
        text = re.sub(r'[<>:"/\\|?*]', '_', text)
        # Limit length
        return text[:100]

    def create_action_item(self, email: Dict):
        """Create markdown action item for email"""
        try:
            ACTION_DIR.mkdir(parents=True, exist_ok=True)

            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_subject = self.sanitize_filename(email['subject'])
            filename = f"EMAIL_{safe_subject}_{timestamp}.md"
            filepath = ACTION_DIR / filename

            # Determine priority based on subject/content
            priority = 'high' if any(word in email['subject'].lower() for word in ['urgent', 'asap', 'important', 'critical']) else 'normal'

            # Create markdown content
            content = f"""---
type: email
from: {email['from']}
subject: {email['subject']}
received: {email['date']}
priority: {priority}
status: pending
email_id: {email['id']}
---

# Email: {email['subject']}

## From
{email['from']}

## Received
{email['date']}

## Content
{email['snippet']}

---

## Actions Required
- [ ] Reply to this email
- [ ] Forward if necessary
- [ ] Archive after handling

## Notes
Add any notes or context here before taking action.
"""

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Created action item: {filename}")

            # Mark as processed
            self.processed_ids.add(email['id'])
            self.save_processed_ids()

        except Exception as e:
            logger.error(f"Error creating action item for email {email['id']}: {e}")

    def process_emails(self):
        """Main processing loop for emails"""
        messages = self.get_unread_important_emails()

        new_emails = 0
        for msg in messages:
            msg_id = msg['id']

            # Skip if already processed
            if msg_id in self.processed_ids:
                logger.debug(f"Skipping already processed email: {msg_id}")
                continue

            # Get email details
            email = self.get_email_details(msg_id)
            if email:
                self.create_action_item(email)
                new_emails += 1

        if new_emails > 0:
            logger.info(f"Processed {new_emails} new email(s)")

        # Reset retry delay on successful processing
        self.reset_retry_delay()

    def run(self):
        """Main run loop"""
        logger.info("Gmail Watcher started")
        logger.info(f"Checking every {CHECK_INTERVAL} seconds for unread important emails")

        # Authenticate
        if not self.authenticate():
            logger.error("Failed to authenticate with Gmail API")
            return

        # Main loop
        while True:
            try:
                logger.debug("Checking for new emails...")
                self.process_emails()
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                logger.info("Gmail Watcher stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                self.exponential_backoff()


def main():
    watcher = GmailWatcher()
    watcher.run()


if __name__ == '__main__':
    main()
