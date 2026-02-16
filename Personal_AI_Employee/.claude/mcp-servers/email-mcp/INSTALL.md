# Email MCP Server - Installation Guide

Quick setup guide for the Node.js Email MCP Server.

## Prerequisites

- Node.js 18+ installed
- Gmail account
- Google Cloud project with Gmail API enabled

## Installation Steps

### 1. Install Node.js Dependencies

```bash
cd .claude/mcp-servers/email-mcp
npm install
```

This installs:
- `@modelcontextprotocol/sdk` - MCP protocol implementation
- `googleapis` - Google APIs client library
- `dotenv` - Environment variable management

### 2. Configure Environment Variables

Add to your `.env` file in the project root:

```bash
# Gmail OAuth2 Credentials (from Google Cloud Console)
GMAIL_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_client_secret_here

# Token path (where OAuth token is stored)
TOKEN_PATH=./token.json

# DRY_RUN mode (default: true for safety)
DRY_RUN=true
```

### 3. Authenticate with Gmail

The email MCP server uses the same OAuth token as the Gmail watcher.

**Option A: Use Gmail Watcher to Authenticate**
```bash
cd ../../..
python watchers/gmail_watcher.py
```

**Option B: Manual Authentication**
1. Run the watcher once to trigger OAuth flow
2. Browser opens automatically
3. Sign in with Google
4. Grant permissions
5. Token saved to `token.json`

### 4. Configure Claude Code MCP

**Windows**: Edit `%APPDATA%\claude-code\mcp.json`
**Mac/Linux**: Edit `~/.config/claude-code/mcp.json`

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

**Important**:
- Use **absolute paths** for both the script and token file
- Replace backslashes with forward slashes on Mac/Linux
- Update the paths to match your installation directory

### 5. Test the Server

```bash
# Test with dry-run (safe - no emails sent)
npm test

# Or manually test
node index.js
```

Expected output:
```
[Email MCP] Server initialized (DRY_RUN: true)
[Email MCP] Server running on stdio
```

### 6. Verify in Claude Code

Open Claude Code and check if the email MCP server is available:

```bash
# In Claude Code, you should see:
# - send_email tool
# - create_draft tool
# - search_emails tool
```

## Quick Test

Create a test file to verify the setup:

```bash
# Create test approval file
cat > AI_Employee_Vault/Approved/TEST_EMAIL.md << 'EOF'
---
action_type: send_email
to: test@example.com
subject: Test Email
---

This is a test email from the AI Employee system.
EOF

# Run orchestrator once
python orchestrator.py --once
```

Check logs:
```bash
tail -f AI_Employee_Vault/Logs/orchestrator.log
```

You should see:
```
[Email MCP] DRY RUN MODE - Email not actually sent
[Email MCP] Would send to: test@example.com
```

## Troubleshooting

### "Cannot find module '@modelcontextprotocol/sdk'"

**Solution**: Install dependencies
```bash
cd .claude/mcp-servers/email-mcp
npm install
```

### "GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set"

**Solution**: Add credentials to `.env`
```bash
GMAIL_CLIENT_ID=your_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_secret
```

### "Token not found at token.json"

**Solution**: Authenticate first
```bash
python watchers/gmail_watcher.py
```

### "Module not found" or "Cannot find package"

**Solution**: Ensure you're using Node.js 18+
```bash
node --version  # Should be v18.0.0 or higher
```

### MCP Server Not Showing in Claude Code

**Check**:
1. Is `mcp.json` in the correct location?
   - Windows: `%APPDATA%\claude-code\mcp.json`
   - Mac/Linux: `~/.config/claude-code/mcp.json`
2. Are paths absolute (not relative)?
3. Restart Claude Code after editing `mcp.json`
4. Check Claude Code logs for errors

## Verification Checklist

- [ ] Node.js 18+ installed
- [ ] Dependencies installed (`npm install`)
- [ ] `.env` configured with Gmail credentials
- [ ] `token.json` exists (authenticated)
- [ ] `mcp.json` configured with absolute paths
- [ ] Test script runs successfully (`npm test`)
- [ ] Claude Code shows email tools

## Next Steps

1. **Test in DRY_RUN mode**: Verify everything works without sending emails
2. **Review logs**: Check `AI_Employee_Vault/Logs/orchestrator.log`
3. **Disable DRY_RUN**: When ready, set `DRY_RUN=false` in `.env`
4. **Monitor usage**: Check Gmail API quota in Google Cloud Console

## Production Deployment

When ready for production:

1. **Disable DRY_RUN**:
   ```bash
   # In .env
   DRY_RUN=false
   ```

2. **Update mcp.json**:
   ```json
   {
     "env": {
       "DRY_RUN": "false"
     }
   }
   ```

3. **Test with real email**:
   - Send to your own email first
   - Verify delivery
   - Check formatting

4. **Monitor logs**:
   ```bash
   tail -f AI_Employee_Vault/Logs/orchestrator.log
   ```

## Support

For issues:
1. Check logs: `AI_Employee_Vault/Logs/orchestrator.log`
2. Verify configuration: `.env` and `mcp.json`
3. Test authentication: `python watchers/gmail_watcher.py`
4. Review README: `README_NODEJS.md`

---

**Status**: ✅ Installation Complete

**Last Updated**: 2026-02-16
