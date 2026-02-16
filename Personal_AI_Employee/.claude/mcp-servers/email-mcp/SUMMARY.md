# Email MCP Server - Complete Setup Summary

## What Was Created

### Core Files

1. **index.js** - Main MCP server implementation
   - Implements MCP protocol via stdio
   - Three tools: send_email, create_draft, search_emails
   - Gmail API integration with OAuth2
   - DRY_RUN mode support
   - Reads credentials from .env ONLY

2. **package.json** - Node.js dependencies
   - @modelcontextprotocol/sdk - MCP protocol
   - googleapis - Gmail API client
   - dotenv - Environment variables

3. **test.js** - Test suite
   - Tests all three tools
   - Always runs in DRY_RUN mode
   - Validates MCP protocol communication

### Documentation

4. **README_NODEJS.md** - Complete user guide
   - Features overview
   - Setup instructions
   - Usage examples
   - Troubleshooting
   - Security notes

5. **INSTALL.md** - Quick installation guide
   - Step-by-step setup
   - Configuration examples
   - Verification checklist
   - Production deployment

6. **mcp.example.json** - MCP configuration template
   - Example for ~/.config/claude-code/mcp.json
   - Shows absolute paths
   - Environment variables

## Features Implemented

### 1. send_email Tool
```javascript
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body text",
  "attachment_path": "/path/to/file.pdf"  // optional
}
```

**Behavior**:
- Creates draft first (for logging)
- If DRY_RUN=true: Logs but doesn't send
- If DRY_RUN=false: Sends via Gmail API
- Returns: {success, message_id, timestamp}

### 2. create_draft Tool
```javascript
{
  "to": "recipient@example.com",
  "subject": "Draft Subject",
  "body": "Draft body"
}
```

**Behavior**:
- Creates Gmail draft without sending
- Returns: {success, draft_id}

### 3. search_emails Tool
```javascript
{
  "query": "from:user@example.com is:unread",
  "max_results": 10
}
```

**Behavior**:
- Searches Gmail with query string
- Returns: {success, count, results[]}

## Configuration

### Environment Variables (.env)
```bash
GMAIL_CLIENT_ID=your_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_secret
TOKEN_PATH=./token.json
DRY_RUN=true
```

### MCP Configuration (~/.config/claude-code/mcp.json)
```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["E:\\path\\to\\index.js"],
      "env": {
        "GMAIL_CLIENT_ID": "...",
        "GMAIL_CLIENT_SECRET": "...",
        "TOKEN_PATH": "E:\\path\\to\\token.json",
        "DRY_RUN": "true"
      }
    }
  }
}
```

## Installation Steps

1. **Install Dependencies**
   ```bash
   cd .claude/mcp-servers/email-mcp
   npm install
   ```

2. **Configure .env**
   - Add GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET
   - Set DRY_RUN=true for testing

3. **Authenticate**
   ```bash
   python watchers/gmail_watcher.py
   ```
   - Creates token.json

4. **Configure MCP**
   - Edit ~/.config/claude-code/mcp.json
   - Use absolute paths
   - Copy from mcp.example.json

5. **Test**
   ```bash
   npm test
   ```

6. **Verify in Claude Code**
   - Restart Claude Code
   - Check for email tools

## Integration with Orchestrator

The orchestrator now calls the email MCP server when:

1. Approved email action appears in `Approved/`
2. File has `action_type: send_email`
3. Orchestrator reads email details
4. Calls email MCP via subprocess (in production, would use MCP client)
5. Logs result
6. Moves to Done/

### Example Approved Action

File: `AI_Employee_Vault/Approved/EMAIL_invoice_20260216.md`

```markdown
---
action_type: send_email
to: client@example.com
subject: Invoice for January 2026
attachment: AI_Employee_Vault/Invoices/INVOICE_client.pdf
---

Dear Client,

Please find attached the invoice for January 2026.

Best regards,
AI Employee
```

## Security Features

✅ **OAuth2 Authentication**: No password storage
✅ **Credentials in .env**: Gitignored
✅ **Token stored locally**: Gitignored
✅ **DRY_RUN default**: Prevents accidental sends
✅ **All actions logged**: Audit trail
✅ **Scoped permissions**: Only send/compose/read

## Testing

### Test in DRY_RUN Mode (Safe)

```bash
cd .claude/mcp-servers/email-mcp
npm test
```

Expected output:
```
[Email MCP] Server initialized (DRY_RUN: true)
[Email MCP] DRY RUN MODE - Email not actually sent
[Email MCP] Would send to: test@example.com
✅ All tests completed successfully!
```

### Test with Orchestrator

```bash
# Create test approval
cat > AI_Employee_Vault/Approved/TEST_EMAIL.md << 'EOF'
---
action_type: send_email
to: test@example.com
subject: Test Email
---
This is a test.
EOF

# Run orchestrator once
python orchestrator.py --once

# Check logs
tail AI_Employee_Vault/Logs/orchestrator.log
```

## Production Deployment

When ready to send real emails:

1. **Disable DRY_RUN**
   ```bash
   # In .env
   DRY_RUN=false
   ```

2. **Update mcp.json**
   ```json
   {
     "env": {
       "DRY_RUN": "false"
     }
   }
   ```

3. **Test with your own email first**
   ```bash
   # Send to yourself
   to: your_email@example.com
   ```

4. **Monitor logs**
   ```bash
   tail -f AI_Employee_Vault/Logs/orchestrator.log
   ```

## Verification Checklist

Before going to production:

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Dependencies installed (`npm install` completed)
- [ ] `.env` configured with Gmail credentials
- [ ] `token.json` exists (authenticated via Gmail watcher)
- [ ] `mcp.json` configured with absolute paths
- [ ] Test script passes (`npm test`)
- [ ] Claude Code shows email tools
- [ ] Test email sent to yourself successfully
- [ ] Logs show successful delivery
- [ ] Gmail API quota checked in Google Cloud Console

## Troubleshooting

### Common Issues

1. **"Cannot find module"**
   - Run `npm install` in email-mcp directory

2. **"Token not found"**
   - Run `python watchers/gmail_watcher.py` to authenticate

3. **"GMAIL_CLIENT_ID must be set"**
   - Add credentials to `.env` file

4. **MCP server not showing in Claude Code**
   - Check `mcp.json` location and syntax
   - Use absolute paths
   - Restart Claude Code

5. **Emails not sending**
   - Check `DRY_RUN=true` (default)
   - Set to `false` for production
   - Verify token is valid

## File Structure

```
.claude/mcp-servers/email-mcp/
├── index.js              # Main MCP server
├── package.json          # Dependencies
├── test.js               # Test suite
├── mcp.example.json      # Config template
├── README_NODEJS.md      # User guide
├── INSTALL.md            # Installation guide
└── SUMMARY.md            # This file
```

## Next Steps

1. **Install**: `cd .claude/mcp-servers/email-mcp && npm install`
2. **Configure**: Add credentials to `.env`
3. **Authenticate**: Run Gmail watcher once
4. **Test**: `npm test`
5. **Deploy**: Update `mcp.json` and restart Claude Code

## Status

✅ **Email MCP Server**: Complete and ready for testing
✅ **Documentation**: Complete
✅ **Test Suite**: Complete
✅ **Orchestrator Integration**: Complete
✅ **DRY_RUN Mode**: Enabled by default (safe)

## Support

- **Installation**: See `INSTALL.md`
- **Usage**: See `README_NODEJS.md`
- **Testing**: Run `npm test`
- **Logs**: Check `AI_Employee_Vault/Logs/orchestrator.log`

---

**Created**: 2026-02-16
**Status**: ✅ Production Ready (with DRY_RUN enabled)
