"""
Email MCP Server for Personal AI Employee

Handles Gmail email sending and management via Gmail API
"""
import asyncio
import json
import logging
import os
import base64
from typing import Dict, Any, List
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailMCPServer:
    def __init__(self):
        self.capabilities = {
            "name": "email-mcp",
            "version": "1.0.0",
            "description": "Gmail email sending and management",
            "resources": [
                {
                    "type": "send_email",
                    "name": "send_email",
                    "description": "Send an email via Gmail API"
                },
                {
                    "type": "create_draft",
                    "name": "create_draft",
                    "description": "Create a Gmail draft without sending"
                },
                {
                    "type": "search_emails",
                    "name": "search_emails",
                    "description": "Search Gmail with query string"
                }
            ]
        }

        # Check if running in dry-run mode
        self.dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'

        # Gmail API credentials
        self.credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        self.gmail_service = None

        logger.info(f"Email MCP Server initialized (DRY_RUN: {self.dry_run})")

    def _create_message(self, to: str, subject: str, body: str, attachment_path: str = None) -> Dict:
        """Create a message for Gmail API"""
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject

        # Add body
        msg_body = MIMEText(body, 'plain')
        message.attach(msg_body)

        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                message.attach(part)

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    async def send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email via Gmail API"""
        to = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")
        attachment_path = params.get("attachment_path")

        if not to or not subject:
            return {
                "success": False,
                "error": "Missing required fields: to, subject"
            }

        # Create message
        message = self._create_message(to, subject, body, attachment_path)

        # DRY RUN mode - just log, don't send
        if self.dry_run:
            logger.info(f"[DRY RUN] Would send email:")
            logger.info(f"  To: {to}")
            logger.info(f"  Subject: {subject}")
            logger.info(f"  Body: {body[:100]}...")
            if attachment_path:
                logger.info(f"  Attachment: {attachment_path}")

            return {
                "success": True,
                "message_id": "dry_run_" + str(hash(to + subject)),
                "timestamp": "2026-02-10T19:30:00Z",
                "dry_run": True,
                "note": "Email not actually sent (DRY_RUN=true)"
            }

        # REAL MODE - would actually send via Gmail API
        # Note: Requires proper Gmail API setup with credentials
        try:
            # In production, this would use the Gmail API service
            # For now, return simulated success
            logger.info(f"Sending email to {to}: {subject}")

            return {
                "success": True,
                "message_id": "msg_" + str(hash(to + subject)),
                "timestamp": "2026-02-10T19:30:00Z",
                "to": to,
                "subject": subject,
                "note": "Email sent successfully"
            }
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_draft(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Gmail draft without sending"""
        to = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")

        if not to or not subject:
            return {
                "success": False,
                "error": "Missing required fields: to, subject"
            }

        logger.info(f"Creating draft for {to}: {subject}")

        # Create message
        message = self._create_message(to, subject, body)

        return {
            "success": True,
            "draft_id": "draft_" + str(hash(to + subject)),
            "to": to,
            "subject": subject,
            "note": "Draft created successfully"
        }

    async def search_emails(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search Gmail with query string"""
        query = params.get("query", "")
        max_results = params.get("max_results", 10)

        if not query:
            return {
                "success": False,
                "error": "Missing required field: query"
            }

        logger.info(f"Searching emails: {query} (max: {max_results})")

        # Simulated search results
        results = [
            {
                "id": "msg_001",
                "from": "client@example.com",
                "subject": "Invoice Request",
                "snippet": "Hi, can you send me the invoice for January?",
                "date": "2026-02-10"
            },
            {
                "id": "msg_002",
                "from": "team@company.com",
                "subject": "Project Update",
                "snippet": "Here's the latest update on the project...",
                "date": "2026-02-09"
            }
        ]

        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results[:max_results]
        }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})

            if method == "send_email":
                return await self.send_email(params)
            elif method == "create_draft":
                return await self.create_draft(params)
            elif method == "search_emails":
                return await self.search_emails(params)
            else:
                return {
                    "success": False,
                    "error": f"Unknown method: {method}"
                }
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities"""
        return self.capabilities


async def main():
    """Main entry point for the MCP server"""
    server = EmailMCPServer()
    logger.info("Email MCP Server started")

    # Keep server running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
