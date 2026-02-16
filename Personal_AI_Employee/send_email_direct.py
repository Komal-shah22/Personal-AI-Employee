#!/usr/bin/env python3
"""
Direct Email Sender - Send emails immediately via Gmail API
No orchestrator, no queue - instant sending like Gmail compose
"""

import os
import sys
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime

# Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Get authenticated Gmail service"""
    token_path = os.path.join(os.path.dirname(__file__), 'token_send.json')
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    creds = None

    # Load existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                return None, 'credentials.json not found. Please set up Gmail API credentials.'

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds), None

def send_email_direct(to_email, subject, body):
    """Send email directly via Gmail API"""

    try:
        # Get authenticated service
        service, error = get_gmail_service()

        if error:
            return {
                'success': False,
                'error': error
            }

        if not service:
            return {
                'success': False,
                'error': 'Failed to authenticate with Gmail API'
            }

        # Create message
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject
        message['from'] = 'me'

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Send via Gmail API
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return {
            'success': True,
            'message_id': result['id'],
            'to': to_email,
            'subject': subject,
            'sent_at': datetime.now().isoformat(),
            'method': 'gmail_api_direct'
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'fallback': 'queued_for_orchestrator'
        }

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python send_email_direct.py <to> <subject> <body>'
        }))
        sys.exit(1)

    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]

    result = send_email_direct(to_email, subject, body)
    print(json.dumps(result))
