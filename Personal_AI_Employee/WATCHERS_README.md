# AI Employee Watchers

Automated monitoring systems that detect and process incoming tasks from various sources.

## Overview

The AI Employee system includes three watchers that monitor different input channels:

| Watcher | Monitors | Creates | Status |
|---------|----------|---------|--------|
| **Gmail Watcher** | Unread important emails | Email action items | Requires setup |
| **WhatsApp Watcher** | WhatsApp messages | Message action items | Requires setup |
| **File Watcher** | Desktop drop folder | File action items | Ready to use |

## Quick Start

### Option 1: Start Individual Watchers

```bash
# File watcher (no setup required)
python watchers/file_watcher.py

# Gmail watcher (requires OAuth setup)
python watchers/gmail_watcher.py

# WhatsApp watcher (requires session setup)
python watchers/whatsapp_watcher.py
```

### Option 2: Use Unified Launcher

```bash
# Start specific watchers
python start_watchers.py file
python start_watchers.py gmail file
python start_watchers.py all

# List available watchers
python start_watchers.py --list
```

## Watcher Details

### 1. Gmail Watcher

**Purpose**: Monitors Gmail for unread important emails and creates action items.

**Features**:
- Checks every 120 seconds for `is:unread is:important` emails
- OAuth2 authentication via .env credentials
- Exponential backoff on API errors (1s → 60s max)
- Tracks processed emails to avoid duplicates
- Logs to `AI_Employee_Vault/Logs/gmail_watcher.log`

**Setup Required**: Yes
- Google Cloud Console OAuth2 credentials
- See: `README_gmail_setup.md`

**Action Items Created**:
```
AI_Employee_Vault/Needs_Action/EMAIL_[subject]_[timestamp].md
```

**YAML Frontmatter**:
```yaml
type: email
from: sender@example.com
subject: Email subject
received: Date
priority: high/normal
status: pending
email_id: gmail_message_id
```

### 2. WhatsApp Watcher

**Purpose**: Monitors WhatsApp Web for new messages.

**Features**:
- Real-time message monitoring
- Keyword filtering support
- Session persistence (stays logged in)
- Desktop notifications
- Logs to `AI_Employee_Vault/Logs/whatsapp_watcher.log`

**Setup Required**: Yes
- WhatsApp Web session authentication
- See: `WHATSAPP_SETUP_GUIDE.md`

**Action Items Created**:
```
AI_Employee_Vault/Needs_Action/WHATSAPP_[contact]_[timestamp].md
```

### 3. File Watcher

**Purpose**: Monitors desktop drop folder for new files.

**Features**:
- Real-time file detection using watchdog
- Automatic file type detection (.pdf=invoice, .csv=data, etc.)
- Handles locked files with retry logic
- Duplicate detection with timestamp suffixes
- Desktop notifications via plyer
- Logs to `AI_Employee_Vault/Logs/file_watcher.log`

**Setup Required**: No (creates drop folder automatically)

**Drop Folder**: `~/Desktop/AI_Drop_Folder/`

**Action Items Created**:
```
AI_Employee_Vault/Needs_Action/FILE_[filename]_[timestamp].md
```

**YAML Frontmatter**:
```yaml
type: file_drop
original_name: filename.pdf
size: 245.67 KB
size_bytes: 251584
date_added: 2026-02-16T14:30:22
detected_type: invoice
file_location: filename.pdf
status: pending
```

**Supported File Types**:
- `.pdf` → invoice
- `.csv`, `.xlsx`, `.xls` → data
- `.jpg`, `.jpeg`, `.png` → image
- `.docx`, `.doc`, `.txt` → document

## Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:
- `google-auth-httplib2` - Gmail API authentication
- `google-auth-oauthlib` - OAuth2 flow
- `google-api-python-client` - Gmail API client
- `python-dotenv` - Environment variable management
- `watchdog` - File system monitoring
- `plyer` - Desktop notifications
- `playwright` - WhatsApp Web automation

## Configuration

### Gmail Watcher

1. Copy `.env.template` to `.env`
2. Add Google OAuth credentials:
   ```
   GMAIL_CLIENT_ID=your_client_id.apps.googleusercontent.com
   GMAIL_CLIENT_SECRET=your_client_secret
   ```
3. Follow `README_gmail_setup.md` for detailed setup

### WhatsApp Watcher

1. Run setup script:
   ```bash
   python setup_whatsapp.py
   ```
2. Scan QR code with WhatsApp mobile app
3. Session persists across restarts

### File Watcher

No configuration needed. Drop folder created automatically at:
- Windows: `C:\Users\[username]\Desktop\AI_Drop_Folder\`
- Mac/Linux: `~/Desktop/AI_Drop_Folder/`

## Running as Services

### Windows (Task Scheduler)

Create scheduled tasks for each watcher:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start a program
   - Program: `python`
   - Arguments: `E:\hackathon-0\Personal_AI_Employee\watchers\[watcher_name].py`
   - Start in: `E:\hackathon-0\Personal_AI_Employee`

### Linux (systemd)

Create service files in `/etc/systemd/system/`:

```ini
[Unit]
Description=AI Employee File Watcher
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Personal_AI_Employee
ExecStart=/usr/bin/python3 watchers/file_watcher.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-file-watcher
sudo systemctl start ai-file-watcher
```

### macOS (launchd)

Create plist files in `~/Library/LaunchAgents/`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-employee.file-watcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/watchers/file_watcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.ai-employee.file-watcher.plist
```

## Integration with AI Employee

All watchers create action items in `AI_Employee_Vault/Needs_Action/` that can be processed by:

1. **Orchestrator** (`orchestrator.py`):
   - Automatically picks up new action items
   - Routes to appropriate skills
   - Handles approval workflows

2. **Dashboard** (`ai-employee-dashboard`):
   - Displays action items in real-time
   - Shows activity feed
   - Provides approval interface

3. **Skills** (`.claude/skills/`):
   - `email_reply_skill.md` - Processes email action items
   - `invoice_skill.md` - Processes invoice files
   - Custom skills can be added for specific file types

## Monitoring and Logs

### View Logs

```bash
# File watcher
tail -f AI_Employee_Vault/Logs/file_watcher.log

# Gmail watcher
tail -f AI_Employee_Vault/Logs/gmail_watcher.log

# WhatsApp watcher
tail -f AI_Employee_Vault/Logs/whatsapp_watcher.log
```

### Check Running Watchers

```bash
# Linux/Mac
ps aux | grep watcher

# Windows
tasklist | findstr python
```

### Stop Watchers

Press `Ctrl+C` in the terminal running the watcher, or:

```bash
# Linux/Mac
pkill -f file_watcher.py

# Windows
taskkill /F /IM python.exe
```

## Troubleshooting

### Gmail Watcher

**"Authentication failed"**:
- Check `.env` credentials are correct
- Ensure Gmail API is enabled in Google Cloud Console
- Delete `token.json` and re-authenticate

**"No emails found"**:
- Mark emails as important in Gmail (click "!" icon)
- Check emails are unread
- Verify watcher is running without errors

### WhatsApp Watcher

**"Session not found"**:
- Run `python setup_whatsapp.py` to create session
- Scan QR code with WhatsApp mobile app

**"Connection lost"**:
- Check internet connection
- Restart watcher
- Re-authenticate if needed

### File Watcher

**"No notifications"**:
- Check OS notification settings
- Ensure `plyer` is installed correctly

**"Permission denied"**:
- Check write permissions on `AI_Employee_Vault/Needs_Action/`
- Run with appropriate user permissions

**"Files not detected"**:
- Verify drop folder path exists
- Check watcher is running
- Review logs for errors

## Security Considerations

- **Gmail**: OAuth tokens stored in `token.json` (excluded from git)
- **WhatsApp**: Session data stored locally (excluded from git)
- **Files**: Copied to action folder (originals remain in drop folder)
- **Logs**: May contain sensitive information (review before sharing)
- **Credentials**: Never commit `.env`, `token.json`, or session files

## Performance

- **CPU Usage**: Minimal when idle (<1%)
- **Memory**: ~50-100MB per watcher
- **Network**: Periodic API calls (Gmail: every 120s)
- **Disk**: Logs rotate automatically (not implemented yet - TODO)

## Customization

### Change Check Intervals

Edit the watcher files:

```python
# Gmail watcher
CHECK_INTERVAL = 120  # seconds

# File watcher
# Real-time, no interval needed
```

### Add Custom File Types

Edit `watchers/file_watcher.py`:

```python
FILE_TYPE_MAP = {
    '.pdf': 'invoice',
    '.py': 'code',  # Add custom type
    # ... more types
}

SUGGESTED_ACTIONS = {
    'code': [
        '- [ ] Review code',
        '- [ ] Run tests'
    ],
    # ... more actions
}
```

### Customize Email Queries

Edit `watchers/gmail_watcher.py`:

```python
# Change from 'is:unread is:important' to:
query = 'is:unread from:boss@company.com'
query = 'is:unread subject:invoice'
query = 'is:starred newer_than:1d'
```

## Roadmap

Future enhancements:
- [ ] Slack watcher
- [ ] Calendar watcher (Google Calendar, Outlook)
- [ ] Database watcher (monitor tables for changes)
- [ ] API webhook receiver
- [ ] Log rotation and archiving
- [ ] Health check endpoints
- [ ] Metrics and analytics
- [ ] Web UI for watcher management

## Support

For issues or questions:
1. Check the logs first
2. Review the specific watcher's README
3. Verify setup requirements are met
4. Check GitHub issues

---

**Documentation**:
- Gmail Setup: `README_gmail_setup.md`
- File Watcher: `README_file_watcher.md`
- WhatsApp Setup: `WHATSAPP_SETUP_GUIDE.md`
