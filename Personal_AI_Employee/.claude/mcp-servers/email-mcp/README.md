# Email MCP Server - Setup Guide

## Overview
Gmail email sending and management via Gmail API for Personal AI Employee.

## Features
- ✅ Send emails via Gmail API
- ✅ Create drafts without sending
- ✅ Search emails with query
- ✅ Attachment support
- ✅ DRY_RUN mode for testing

## Setup

### Step 1: Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API:
   - APIs & Services → Library
   - Search "Gmail API"
   - Click Enable

### Step 2: Create OAuth Credentials

1. APIs & Services → Credentials
2. Create Credentials → OAuth 2.0 Client ID
3. Application type: Desktop app
4. Download credentials.json
5. Save to project root: `Personal_AI_Employee/credentials.json`

### Step 3: Install Dependencies

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 4: Configure Environment

Create or update `.env`:
```bash
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_CREDENTIALS_PATH=credentials.json
DRY_RUN=true  # Set to false for production
```

### Step 5: Test the MCP Server

```bash
cd .claude/mcp-servers/email-mcp
python server.py
```

## Usage

### Send Email
```python
{
  "method": "send_email",
  "params": {
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from AI Employee",
    "attachment_path": "/path/to/file.pdf"  # optional
  }
}
```

### Create Draft
```python
{
  "method": "create_draft",
  "params": {
    "to": "recipient@example.com",
    "subject": "Draft Email",
    "body": "This is a draft"
  }
}
```

### Search Emails
```python
{
  "method": "search_emails",
  "params": {
    "query": "from:client@example.com",
    "max_results": 10
  }
}
```

## DRY_RUN Mode

By default, `DRY_RUN=true` means emails are logged but NOT actually sent.

To send real emails:
```bash
export DRY_RUN=false
```

## Integration with AI Employee

The orchestrator automatically uses this MCP when:
1. An approved email file appears in `/Approved/EMAIL_*.md`
2. Reads the email details
3. Calls email MCP to send
4. Logs result to `/Logs/`
5. Moves file to `/Done/`

## Security

- ✅ Credentials stored in `.env` (gitignored)
- ✅ OAuth2 authentication
- ✅ DRY_RUN mode prevents accidental sends
- ✅ All actions logged

## Troubleshooting

### "Credentials not found"
- Ensure `credentials.json` exists in project root
- Check `GMAIL_CREDENTIALS_PATH` in `.env`

### "Permission denied"
- Re-authorize: delete `token.pickle` and run again
- Check OAuth scopes include Gmail send

### "API not enabled"
- Enable Gmail API in Google Cloud Console

## Status

✅ Email MCP Server - Ready for Silver Tier
