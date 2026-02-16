# 📱 WhatsApp Watcher Setup Guide

## Overview
The WhatsApp Watcher monitors WhatsApp Web for urgent messages containing specific keywords and automatically creates action items in your AI Employee system.

## Features
- ✅ Monitors WhatsApp Web every 30 seconds
- ✅ Filters messages with keywords: `urgent`, `invoice`, `payment`, `help`, `asap`
- ✅ Creates action files in `/Needs_Action` folder
- ✅ Persistent browser session (login once, use forever)
- ✅ Comprehensive logging to `/Logs/whatsapp_watcher.log`
- ✅ Priority classification (high/medium)

---

## Prerequisites

### 1. Install Playwright
```bash
pip install playwright
python -m playwright install chromium
```

### 2. Verify Installation
```bash
python -m playwright --version
```

---

## Quick Setup (Automated)

Run the setup script:
```bash
python setup_whatsapp.py
```

This will:
1. Check if Playwright is installed
2. Install Chromium browser if needed
3. Create session directory
4. Guide you through QR code scanning

---

## Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### Step 2: Create Session Directory
The session directory is created automatically, but you can verify:
```bash
mkdir -p sessions/whatsapp
```

### Step 3: First Run (QR Code Scan)
```bash
python watchers/whatsapp_watcher.py
```

**What happens:**
1. Browser window opens with WhatsApp Web
2. QR code appears on screen
3. Scan with your phone (see instructions below)
4. Session is saved for future use

### Step 4: Scan QR Code with Your Phone

**On your phone:**
1. Open WhatsApp
2. Tap **Menu (⋮)** or **Settings**
3. Tap **Linked Devices**
4. Tap **Link a Device**
5. Point camera at QR code on computer screen
6. Wait for confirmation

**On your computer:**
- Browser will show "WhatsApp Web is active"
- Watcher will start monitoring messages
- Session is saved to `sessions/whatsapp/`

---

## Configuration

### Keyword Filtering
Edit `watchers/whatsapp_watcher.py` to customize keywords:
```python
self.keywords = ['urgent', 'invoice', 'payment', 'help', 'asap']
```

Add your own keywords:
```python
self.keywords = ['urgent', 'invoice', 'payment', 'help', 'asap', 'emergency', 'deadline']
```

### Check Interval
Change how often the watcher checks for messages (default: 30 seconds):
```python
watcher = WhatsAppWatcher(check_interval=60)  # Check every 60 seconds
```

### Headless Mode
For production, run browser in background (no visible window):

Edit line 73 in `watchers/whatsapp_watcher.py`:
```python
headless=True,  # Change from False to True
```

---

## Running the Watcher

### Manual Start
```bash
python watchers/whatsapp_watcher.py
```

### Background Process (Linux/Mac)
```bash
nohup python watchers/whatsapp_watcher.py > /dev/null 2>&1 &
```

### Background Process (Windows)
```powershell
Start-Process python -ArgumentList "watchers/whatsapp_watcher.py" -WindowStyle Hidden
```

### Using PM2 (Recommended for 24/7)
```bash
npm install -g pm2
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp-watcher
pm2 save
pm2 startup
```

---

## How It Works

### 1. Message Detection
- Watcher opens WhatsApp Web every 30 seconds
- Scans for unread messages
- Checks message preview text for keywords

### 2. Keyword Matching
If message contains any keyword:
- `urgent` → High priority
- `invoice` → Medium priority
- `payment` → Medium priority
- `help` → Medium priority
- `asap` → High priority

### 3. Action File Creation
Creates file in `/Needs_Action/` with format:
```
WHATSAPP_20260210_143022.md
```

### 4. File Content
```markdown
---
type: whatsapp
from: John Doe
received: 2026-02-10T14:30:22
priority: high
status: pending
keywords: urgent, payment
---

## WhatsApp Message

**From:** John Doe
**Priority:** HIGH
**Matched Keywords:** urgent, payment

### Message Preview
Hi, this is urgent! Need the invoice payment processed ASAP.

## Suggested Actions
- [ ] Review full conversation in WhatsApp
- [ ] Determine urgency and required response
- [ ] Draft appropriate reply
- [ ] Get approval if needed
- [ ] Send response via WhatsApp
- [ ] Archive after processing
```

---

## Monitoring & Logs

### View Real-time Logs
```bash
tail -f AI_Employee_Vault/Logs/whatsapp_watcher.log
```

### Log Format
```
2026-02-10 14:30:22 - WhatsAppWatcher - INFO - Starting WhatsApp Watcher
2026-02-10 14:30:25 - WhatsAppWatcher - INFO - ✅ Already logged in to WhatsApp Web
2026-02-10 14:30:28 - WhatsAppWatcher - INFO - Found 3 unread chat(s)
2026-02-10 14:30:29 - WhatsAppWatcher - INFO - ✅ Found urgent message from John Doe
2026-02-10 14:30:29 - WhatsAppWatcher - INFO - ✅ Created action file: WHATSAPP_20260210_143029.md
```

---

## Troubleshooting

### Issue: QR Code Not Appearing
**Solution:**
1. Close all Chrome/Chromium windows
2. Delete session: `rm -rf sessions/whatsapp`
3. Run watcher again

### Issue: "Session Expired" Error
**Solution:**
1. Delete session: `rm -rf sessions/whatsapp`
2. Scan QR code again

### Issue: Browser Crashes
**Solution:**
1. Update Playwright: `pip install --upgrade playwright`
2. Reinstall browsers: `python -m playwright install chromium`

### Issue: No Messages Detected
**Solution:**
1. Check keywords match your messages
2. Verify messages are actually unread
3. Check logs: `tail -f AI_Employee_Vault/Logs/whatsapp_watcher.log`

### Issue: Permission Denied
**Solution:**
```bash
chmod +x watchers/whatsapp_watcher.py
```

---

## Security Considerations

### Session Storage
- Session stored in `sessions/whatsapp/`
- Contains login credentials
- **Add to .gitignore**: `sessions/`
- **Never commit to Git**

### Privacy
- Watcher only reads message previews
- Does not store full message content
- Does not send messages automatically
- All actions require human approval

### Best Practices
1. ✅ Run on trusted computer only
2. ✅ Use strong device password
3. ✅ Enable 2FA on WhatsApp
4. ✅ Regularly review linked devices
5. ✅ Log out when not in use (optional)

---

## Integration with AI Employee

### Automatic Processing
Once action files are created, Claude Code can:
1. Read the WhatsApp message details
2. Analyze urgency and context
3. Draft appropriate response
4. Create approval request
5. Wait for human approval
6. Log the interaction

### Using Claude Skills
```bash
# Process WhatsApp messages
claude skill process-tasks

# Update dashboard with WhatsApp stats
claude skill update-dashboard
```

---

## Advanced Configuration

### Multiple Phone Numbers
To monitor multiple WhatsApp accounts:
1. Create separate session directories
2. Run multiple watcher instances
3. Use different ports/profiles

### Custom Filters
Add sender-based filtering:
```python
# In check_for_updates() method
if chat_name in ['Important Client', 'Boss', 'VIP']:
    priority = 'critical'
```

### Integration with MCP
Connect to WhatsApp MCP server for sending responses:
```json
{
  "servers": [
    {
      "name": "whatsapp",
      "command": "node",
      "args": ["path/to/whatsapp-mcp/index.js"]
    }
  ]
}
```

---

## Status Check

### Verify Watcher is Running
```bash
ps aux | grep whatsapp_watcher
```

### Check Recent Activity
```bash
ls -lt AI_Employee_Vault/Needs_Action/WHATSAPP_*.md | head -5
```

### View Statistics
```bash
grep "Found urgent message" AI_Employee_Vault/Logs/whatsapp_watcher.log | wc -l
```

---

## Stopping the Watcher

### Manual Stop
Press `Ctrl+C` in the terminal

### PM2 Stop
```bash
pm2 stop whatsapp-watcher
```

### Kill Process
```bash
pkill -f whatsapp_watcher.py
```

---

## Next Steps

After setup:
1. ✅ Test with a sample message containing keywords
2. ✅ Verify action file is created in `/Needs_Action`
3. ✅ Process the action with Claude Code
4. ✅ Set up automated scheduling (cron/PM2)
5. ✅ Configure for 24/7 operation

---

## Support

For issues or questions:
- Check logs: `AI_Employee_Vault/Logs/whatsapp_watcher.log`
- Review this guide
- Test with manual run first
- Verify Playwright installation

---

**🎉 Congratulations! Your WhatsApp Watcher is now set up and ready to monitor urgent messages 24/7!**
