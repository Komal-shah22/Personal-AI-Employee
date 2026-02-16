# AI Employee - Quick Command Reference

Essential commands for running and managing the AI Employee system.

## System Verification

```bash
# Check if everything is set up correctly
python verify_system.py
```

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for email MCP)
cd .claude/mcp-servers/email-mcp
npm install
cd ../../..

# Configure environment
cp .env.template .env
# Edit .env with your credentials
```

## Starting Components

### File Watcher (No Setup Required)
```bash
python watchers/file_watcher.py
```
Drop files into `~/Desktop/AI_Drop_Folder/`

### Gmail Watcher (Requires OAuth Setup)
```bash
# First time: authenticate
python watchers/gmail_watcher.py
# Browser opens, sign in, grant permissions

# Subsequent runs
python watchers/gmail_watcher.py
```

### WhatsApp Watcher (Requires Session Setup)
```bash
python watchers/whatsapp_watcher.py
```

### Orchestrator (Master Controller)
```bash
# Run continuously (checks every 5 minutes)
python orchestrator.py

# Run once and exit
python orchestrator.py --once

# Disable dry-run mode (CAUTION: executes real actions)
python orchestrator.py --no-dry-run
```

### All Watchers at Once
```bash
# Start all watchers
python start_watchers.py all

# Start specific watchers
python start_watchers.py file gmail

# List available watchers
python start_watchers.py --list
```

## Monitoring

### View Logs
```bash
# Orchestrator logs
tail -f AI_Employee_Vault/Logs/orchestrator.log

# File watcher logs
tail -f AI_Employee_Vault/Logs/file_watcher.log

# Gmail watcher logs
tail -f AI_Employee_Vault/Logs/gmail_watcher.log

# Today's action log (JSON)
cat AI_Employee_Vault/Logs/$(date +%Y-%m-%d).json | jq
```

### Check Status
```bash
# Count pending tasks
ls AI_Employee_Vault/Needs_Action/*.md 2>/dev/null | wc -l

# Count in-progress tasks
ls AI_Employee_Vault/In_Progress/*.md 2>/dev/null | wc -l

# Count completed tasks
ls AI_Employee_Vault/Done/*.md 2>/dev/null | wc -l

# View dashboard
cat AI_Employee_Vault/Dashboard.md
```

### Check Running Processes
```bash
# Linux/Mac
ps aux | grep -E "orchestrator|watcher"

# Windows
tasklist | findstr python
```

## Testing

### Test Email MCP Server
```bash
cd .claude/mcp-servers/email-mcp
npm test
cd ../../..
```

### Test File Watcher
```bash
# Start watcher
python watchers/file_watcher.py

# In another terminal, drop a test file
echo "Test content" > ~/Desktop/AI_Drop_Folder/test.txt

# Check logs
tail AI_Employee_Vault/Logs/file_watcher.log
```

### Test Orchestrator
```bash
# Create test task
cat > AI_Employee_Vault/Needs_Action/TEST_TASK.md << 'EOF'
---
type: email
from: test@example.com
subject: Test Task
priority: normal
status: pending
---

This is a test task.
EOF

# Run orchestrator once
python orchestrator.py --once

# Check logs
tail AI_Employee_Vault/Logs/orchestrator.log
```

## Configuration

### Enable/Disable DRY_RUN Mode
```bash
# In .env file
DRY_RUN=true   # Safe mode (default)
DRY_RUN=false  # Production mode

# Or via command line
python orchestrator.py --no-dry-run
```

### Change Check Interval
```bash
# Edit orchestrator.py
CHECK_INTERVAL = 300  # 5 minutes (default)
CHECK_INTERVAL = 600  # 10 minutes
```

### Configure Gmail Watcher
```bash
# Edit .env
GMAIL_CLIENT_ID=your_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_secret
```

## Troubleshooting

### Reset Gmail Authentication
```bash
rm token.json
python watchers/gmail_watcher.py
```

### Move Stuck Tasks Back to Needs_Action
```bash
mv AI_Employee_Vault/In_Progress/*.md AI_Employee_Vault/Needs_Action/
```

### Clear Processed Email IDs
```bash
rm .processed_ids.json
```

### Reinstall Dependencies
```bash
# Python
pip install -r requirements.txt --force-reinstall

# Node.js
cd .claude/mcp-servers/email-mcp
rm -rf node_modules package-lock.json
npm install
```

### Check for Errors
```bash
# Recent errors in orchestrator
grep ERROR AI_Employee_Vault/Logs/orchestrator.log | tail -20

# Recent errors in watchers
grep ERROR AI_Employee_Vault/Logs/*.log
```

## Maintenance

### Clean Up Old Logs
```bash
# Archive logs older than 30 days
find AI_Employee_Vault/Logs -name "*.log" -mtime +30 -exec gzip {} \;
find AI_Employee_Vault/Logs -name "*.json" -mtime +30 -exec gzip {} \;
```

### Backup Configuration
```bash
# Backup .env and tokens
tar -czf backup_$(date +%Y%m%d).tar.gz .env token.json AI_Employee_Vault/
```

### Update System
```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade
cd .claude/mcp-servers/email-mcp && npm update
```

## Production Deployment

### Run as Services

**Linux (systemd)**
```bash
# Create service files
sudo nano /etc/systemd/system/ai-orchestrator.service
sudo nano /etc/systemd/system/ai-file-watcher.service

# Enable and start
sudo systemctl enable ai-orchestrator ai-file-watcher
sudo systemctl start ai-orchestrator ai-file-watcher

# Check status
sudo systemctl status ai-orchestrator
```

**Windows (Task Scheduler)**
```powershell
# Create scheduled tasks via GUI
# Trigger: At startup
# Action: python E:\path\to\orchestrator.py
```

**macOS (launchd)**
```bash
# Create plist files
nano ~/Library/LaunchAgents/com.ai-employee.orchestrator.plist

# Load
launchctl load ~/Library/LaunchAgents/com.ai-employee.orchestrator.plist
```

## Emergency Commands

### Stop All Components
```bash
# Linux/Mac
pkill -f "orchestrator.py"
pkill -f "watcher.py"

# Windows
taskkill /F /IM python.exe
```

### Emergency Disable
```bash
# Set DRY_RUN to prevent any actions
echo "DRY_RUN=true" >> .env
```

### Rollback Last Action
```bash
# Check last action
tail -1 AI_Employee_Vault/Logs/$(date +%Y-%m-%d).json

# Move from Done back to Needs_Action
mv AI_Employee_Vault/Done/LAST_FILE.md AI_Employee_Vault/Needs_Action/
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# AI Employee aliases
alias ai-verify='python verify_system.py'
alias ai-start='python orchestrator.py'
alias ai-watch='python start_watchers.py all'
alias ai-logs='tail -f AI_Employee_Vault/Logs/orchestrator.log'
alias ai-status='cat AI_Employee_Vault/Dashboard.md'
alias ai-pending='ls AI_Employee_Vault/Needs_Action/*.md | wc -l'
```

## Quick Diagnostics

```bash
# One-liner system check
python verify_system.py && \
ls AI_Employee_Vault/Needs_Action/*.md 2>/dev/null | wc -l && \
tail -5 AI_Employee_Vault/Logs/orchestrator.log
```

## Documentation

- **System Overview**: `QUICKSTART.md`
- **Orchestrator**: `ORCHESTRATOR_README.md`
- **Watchers**: `WATCHERS_README.md`
- **Gmail Setup**: `README_gmail_setup.md`
- **File Watcher**: `README_file_watcher.md`
- **Email MCP**: `.claude/mcp-servers/email-mcp/README_NODEJS.md`

---

**Tip**: Bookmark this file for quick reference!

**Last Updated**: 2026-02-16
