"""
Gmail Watcher for Personal AI Employee

Monitors Gmail for new messages and creates action items in the Needs_Action folder.
"""

import time
import logging
import os
import pickle
import base64
from pathlib import Path
from datetime import datetime
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scopes required for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher:
    def __init__(self, config_path="config.json", credentials_file="credentials.json", check_interval=120):
        self.config = self.load_config(config_path)
        self.credentials_file = credentials_file
        self.check_interval = check_interval

        # Use the configured paths from config.json
        self.needs_action_dir = Path(self.config['directories']['needs_action'])
        self.logs_dir = Path(self.config['directories']['logs'])

        # Create directories if they don't exist
        self.needs_action_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Gmail service
        self.service = self.initialize_gmail_service()
        self.processed_ids = set()

        logger.info("Gmail Watcher initialized")

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def initialize_gmail_service(self):
        """Initialize Gmail API service with OAuth2 authentication"""
        creds = None

        # Token file stores the user's access and refresh tokens
        token_path = Path('token.pickle')

        # Load existing token if available
        if token_path.exists():
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # If there are no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Error refreshing token: {e}")
                    # Delete the old token file and get a new one
                    if token_path.exists():
                        token_path.unlink()
                    creds = None

            if not creds:
                # Get credentials from the downloaded credentials.json
                if not Path(self.credentials_file).exists():
                    raise FileNotFoundError(f"Credentials file {self.credentials_file} not found")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        return service

    def check_for_new_emails(self):
        """Check for new Gmail messages using the API"""
        try:
            # Query for unread emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread'
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                logger.info("No new unread emails found")
                return []

            logger.info(f"Found {len(messages)} new unread emails")

            new_emails = []
            for msg in messages:
                message_id = msg['id']

                # Skip if already processed
                if message_id in self.processed_ids:
                    continue

                # Get full message details
                message = self.service.users().messages().get(
                    userId='me',
                    id=message_id
                ).execute()

                # Parse the email
                email_data = self.parse_email(message)
                if email_data:
                    new_emails.append(email_data)
                    self.processed_ids.add(message_id)

            return new_emails

        except HttpError as error:
            logger.error(f"An error occurred while fetching emails: {error}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while checking emails: {e}")
            return []

    def parse_email(self, message):
        """Parse email message and extract relevant information"""
        try:
            headers = message['payload']['headers']

            # Extract email headers
            email_info = {
                'id': message['id'],
                'threadId': message['threadId'],
                'sizeEstimate': message.get('sizeEstimate', 0)
            }

            for header in headers:
                name = header['name'].lower()
                value = header['value']

                if name == 'from':
                    email_info['from'] = value
                elif name == 'to':
                    email_info['to'] = value
                elif name == 'subject':
                    email_info['subject'] = value
                elif name == 'date':
                    email_info['date'] = value

            # Extract email body
            email_info['body'] = self.extract_body(message)
            email_info['snippet'] = message.get('snippet', '')

            # Determine priority based on keywords
            email_info['priority'] = self.determine_priority(email_info)

            return email_info

        except Exception as e:
            logger.error(f"Error parsing email {message.get('id', 'unknown')}: {e}")
            return None

    def extract_body(self, message):
        """Extract email body from message payload"""
        try:
            body = ""
            payload = message.get('payload', {})
            parts = payload.get('parts', [])

            if not parts:
                # Email might be plain text
                if 'body' in payload and 'data' in payload['body']:
                    body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            else:
                # Process multipart email
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        if 'body' in part and 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
                    elif part.get('mimeType') == 'text/html' and not body:
                        # Fallback to HTML if no plain text found
                        if 'body' in part and 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

            return body if body else message.get('snippet', '')

        except Exception as e:
            logger.error(f"Error extracting email body: {e}")
            return ""

    def determine_priority(self, email_info):
        """Determine email priority based on keywords"""
        subject = email_info.get('subject', '').lower()
        body = email_info.get('body', '').lower()
        snippet = email_info.get('snippet', '').lower()

        # Keywords indicating high priority
        high_priority_keywords = [
            'urgent', 'asap', 'immediate', 'important', 'critical',
            'emergency', 'deadline', 'due', 'invoice', 'payment',
            'billing', 'money', 'financial', 'legal', 'compliance'
        ]

        combined_text = subject + ' ' + body + ' ' + snippet

        for keyword in high_priority_keywords:
            if keyword in combined_text:
                return 'high'

        # Keywords indicating medium priority
        medium_priority_keywords = [
            'follow', 'remind', 'meeting', 'schedule', 'appointment',
            'project', 'report', 'proposal', 'contract', 'agreement'
        ]

        for keyword in medium_priority_keywords:
            if keyword in combined_text:
                return 'medium'

        return 'medium'  # Default priority

    def create_action_file(self, email_info):
        """Create a Markdown file in the Needs_Action folder for a new email."""
        # Create a unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_subject = "".join(c for c in email_info.get('subject', 'untitled') if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_subject:
            safe_subject = "email"
        filename = f"EMAIL_{safe_subject}_{timestamp}.md"
        filepath = self.needs_action_dir / filename

        # Create content for the action file
        content = f"""---
type: email
from: "{email_info.get('from', 'Unknown')}"
to: "{email_info.get('to', 'Unknown')}"
subject: "{email_info.get('subject', 'No Subject')}"
received: "{email_info.get('date', datetime.now().isoformat())}"
priority: {email_info.get('priority', 'medium')}
status: pending
email_id: {email_info.get('id', '')}
thread_id: {email_info.get('threadId', '')}
---

# Email from {email_info.get('from', 'Unknown')}

**Subject:** {email_info.get('subject', 'No Subject')}
**Date:** {email_info.get('date', datetime.now().isoformat())}
**Priority:** {email_info.get('priority', 'medium')}

## Email Content
{email_info.get('body', 'Content not available')}

## Action Required
- [ ] Review email content
- [ ] Determine appropriate response
- [ ] Respond or forward as needed
- [ ] Update status when completed

## Notes
- Original email ID: {email_info.get('id', '')}
- Thread ID: {email_info.get('threadId', '')}
"""

        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created action file: {filepath}")
        return filepath

    def mark_as_read(self, email_id):
        """Mark an email as read to prevent reprocessing"""
        try:
            # Modify the message to remove the 'UNREAD' label
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.debug(f"Marked email {email_id} as read")
        except Exception as e:
            logger.error(f"Error marking email {email_id} as read: {e}")

    def run(self):
        """Main execution loop"""
        logger.info("Starting Gmail Watcher")

        # Log startup
        log_path = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{datetime.now().strftime('%H:%M:%S')}] Gmail Watcher started\n")

        while True:
            try:
                new_emails = self.check_for_new_emails()

                for email_info in new_emails:
                    # Create action file for the email
                    self.create_action_file(email_info)

                    # Mark the email as read to prevent reprocessing
                    self.mark_as_read(email_info['id'])

                # Wait before checking again
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Gmail Watcher stopped by user")

                # Log shutdown
                log_path = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
                with open(log_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"[{datetime.now().strftime('%H:%M:%S')}] Gmail Watcher stopped by user\n")

                break
            except Exception as e:
                logger.error(f"Error in Gmail Watcher: {e}")

                # Log error
                log_path = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
                with open(log_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"[{datetime.now().strftime('%H:%M:%S')}] Gmail Watcher error: {str(e)}\n")

                time.sleep(self.check_interval)


if __name__ == "__main__":
    watcher = GmailWatcher()
    watcher.run()