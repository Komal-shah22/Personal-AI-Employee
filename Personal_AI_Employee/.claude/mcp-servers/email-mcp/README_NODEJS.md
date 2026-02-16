# Email MCP Server - Node.js Implementation

Gmail integration MCP server for Personal AI Employee system.

## Features

- ✅ **send_email**: Send emails via Gmail API with optional attachments
- ✅ **create_draft**: Create Gmail drafts without sending
- ✅ **search_emails**: Search Gmail with query strings
- ✅ **DRY_RUN mode**: Test without sending actual emails
- ✅ **OAuth2 authentication**: Secure Gmail API access
- ✅ **Attachment support**: Send files with emails

## Prerequisites

- Node.js 18+ installed
- Gmail account
- Google Cloud project with Gmail API enabled

## Setup

### Step 1: Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure OAuth consent screen if prompted:
   - User Type: External
   - App name: "AI Employee"
   - Add your email as test user
4. Application type: "Desktop app"
5. Name: "Email MCP Server"
6. Click "Create"
7. Copy the Client ID and Client Secret

### Step 3: Configure Environment Variables

Add to your `.env` file in the project root:

```bash
# Gmail OAuth2 Credentials
GMAIL_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_client_secret_here

# Optional: Custom token path
TOKEN_PATH=./token.json

# DRY_RUN mode (default: true for safety)
DRY_RUN=true
```

### Step 4: Install Dependencies

```bash
cd .claude/mcp-servers/email-mcp
npm install
```

### Step 5: Authenticate

First time setup requires authentication:

```bash
# Run the Gmail watcher to authenticate
cd ../../..
python watchers/gmail_watcher.py
```

This will:
1. Open a browser window
2. Ask you to sign in with Google
3. Grant permissions
4. Save token to `token.json`

### Step 6: Configure Claude Code MCP

Add to `~/.config/claude-code/mcp.json` (or `%APPDATA%\claude-code\mcp.json` on Windows):

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": [
        "E:\\hackathon-0\\Personal_AI_Employee\\.claude\\mcp-servers\\email-mcp\\index.js"
      ],
      "env": {
        "GMAIL_CLIENT_ID": "your_client_id.apps.googleusercontent.com",
        "GMAIL_CLIENT_SECRET": "your_client_secret",
        "TOKEN_PATH": "E:\\hackathon-0\\Personal_AI_Employee\\token.json",
        "DRY_RUN": "true"
      }
    }
  }
}
```

**Important**: Use absolute paths for both the script and token file.

### Step 7: Test the Server

```bash
# Test in dry-run mode (safe)
node index.js
```

The server will start and wait for MCP requests via stdio.

## Usage

### From Claude Code

Once configured, Claude Code can use these tools:

#### Send Email

```javascript
// Claude will call this tool when needed
{
  "tool": "send_email",
  "arguments": {
    "to": "recipient@example.com",
    "subject": "Invoice for January 2026",
    "body": "Dear Client,\n\nPlease find attached the invoice...",
    "attachment_path": "/absolute/path/to/invoice.pdf"
  }
}
```

#### Create Draft

```javascript
{
  "tool": "create_draft",
  "arguments": {
    "to": "recipient@example.com",
    "subject": "Draft Email",
    "body": "This is a draft that won't be sent yet."
  }
}
```

#### Search Emails

```javascript
{
  "tool": "search_emails",
  "arguments": {
    "query": "from:client@example.com is:unread",
    "max_results": 10
  }
}
```

### From Orchestrator

The orchestrator automatically uses this MCP server when:

1. An approved email action appears in `AI_Employee_Vault/Approved/`
2. File has `action_type: send_email` in frontmatter
3. Orchestrator calls the email MCP server
4. Email is sent (or logged in DRY_RUN mode)
5. Result is logged to daily JSON
6. File is moved to `Done/`

## DRY_RUN Mode

**Default: ENABLED** for safety.

### What DRY_RUN Does:
- ✅ Validates all parameters
- ✅ Creates email message
- ✅ Logs what would be sent
- ❌ Does NOT actually send email
- ❌ Does NOT create drafts
- ❌ Does NOT call Gmail API

### Disabling DRY_RUN:

**Option 1**: Environment variable
```bash
export DRY_RUN=false
```

**Option 2**: Update `.env`
```bash
DRY_RUN=false
```

**Option 3**: Update `mcp.json`
```json
{
  "env": {
    "DRY_RUN": "false"
  }
}
```

## Gmail Search Query Syntax

Examples:
- `from:user@example.com` - Emails from specific sender
- `to:me` - Emails sent to you
- `subject:invoice` - Emails with "invoice" in subject
- `is:unread` - Unread emails
- `is:starred` - Starred emails
- `has:attachment` - Emails with attachments
- `after:2026/01/01` - Emails after date
- `newer_than:7d` - Emails from last 7 days

Combine with AND/OR:
- `from:client@example.com subject:invoice`
- `is:unread OR is:starred`

## Response Format

### Success Response

```json
{
  "success": true,
  "message_id": "18d4f2a3b5c6d7e8",
  "timestamp": "2026-02-16T14:30:00Z",
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "note": "Email sent successfully"
}
```

### DRY_RUN Response

```json
{
  "success": true,
  "message_id": "dry_run_1708095000000",
  "timestamp": "2026-02-16T14:30:00Z",
  "dry_run": true,
  "note": "Email not sent (DRY_RUN=true)"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Invalid credentials",
  "timestamp": "2026-02-16T14:30:00Z"
}
```

## Troubleshooting

### "GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set"

**Solution**: Add credentials to `.env` file:
```bash
GMAIL_CLIENT_ID=your_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_secret
```

### "Token not found at token.json"

**Solution**: Authenticate first:
```bash
python watchers/gmail_watcher.py
```
This will create the token file.

### "Permission denied" or "Invalid credentials"

**Solution**:
1. Delete `token.json`
2. Re-authenticate: `python watchers/gmail_watcher.py`
3. Grant all requested permissions

### "Gmail API has not been used in project"

**Solution**: Enable Gmail API in Google Cloud Console:
1. Go to APIs & Services > Library
2. Search "Gmail API"
3. Click Enable

### MCP Server Not Responding

**Check**:
1. Is Node.js installed? `node --version`
2. Are dependencies installed? `npm install`
3. Is the path in `mcp.json` absolute?
4. Check Claude Code logs for errors

### Emails Not Being Sent

**Check**:
1. Is `DRY_RUN=true`? (default)
2. Set `DRY_RUN=false` to send real emails
3. Check token is valid
4. Verify Gmail API quota not exceeded

## Security

- ✅ OAuth2 authentication (no password storage)
- ✅ Credentials in `.env` (gitignored)
- ✅ Token stored locally (gitignored)
- ✅ DRY_RUN mode prevents accidental sends
- ✅ All actions logged
- ✅ Scoped permissions (only send/compose/read)

## Logging

All operations are logged to stderr:
```
[Email MCP] Server initialized (DRY_RUN: true)
[Email MCP] Creating draft: To=client@example.com, Subject=Invoice
[Email MCP] DRY RUN MODE - Email not actually sent
[Email MCP] Would send to: client@example.com
```

## Integration with AI Employee

### Workflow

1. **Watcher** detects email request
2. **Orchestrator** processes and creates approval request
3. **Human** reviews and approves
4. **Orchestrator** calls email MCP server
5. **Email MCP** sends email via Gmail API
6. **Result** logged to daily JSON
7. **Dashboard** updated with activity

### Example Approved Action

File: `AI_Employee_Vault/Approved/EMAIL_invoice_20260216_143000.md`

```markdown
---
action_type: send_email
to: client@example.com
subject: Invoice for January 2026
attachment: AI_Employee_Vault/Invoices/INVOICE_client_20260216.pdf
---

# Approved: Send Invoice Email

Dear Client,

Please find attached the invoice for January 2026.

Best regards,
AI Employee
```

## Development

### Testing

```bash
# Test with dry-run (safe)
DRY_RUN=true node index.js

# Test without dry-run (sends real emails!)
DRY_RUN=false node index.js
```

### Debugging

Enable verbose logging:
```javascript
// In index.js, add more console.error() statements
console.error('[Email MCP] Debug info:', data);
```

## API Limits

Gmail API quotas (free tier):
- **Send**: 100 emails/day
- **Read**: 1 billion quota units/day (very high)
- **Drafts**: Unlimited

For higher limits, request quota increase in Google Cloud Console.

## Roadmap

Future enhancements:
- [ ] HTML email support
- [ ] Multiple attachments
- [ ] CC/BCC support
- [ ] Email templates
- [ ] Scheduled sending
- [ ] Read receipts
- [ ] Email threading
- [ ] Signature management

---

**Status**: ✅ Ready for Production

**Last Updated**: 2026-02-16
