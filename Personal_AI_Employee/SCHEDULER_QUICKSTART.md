# Scheduler Quick Start

Quick commands to set up and manage automated scheduling for the AI Employee system.

## Setup (Choose Your Platform)

### Mac/Linux
```bash
# 1. Make script executable
chmod +x scripts/setup_scheduler.sh

# 2. Run setup
./scripts/setup_scheduler.sh

# 3. Verify installation
crontab -l
```

### Windows
```powershell
# 1. Open PowerShell as Administrator (Win + X → "Terminal (Admin)")

# 2. Navigate to project
cd E:\hackathon-0\Personal_AI_Employee

# 3. Allow script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Run setup
.\scripts\setup_scheduler.ps1

# 5. Verify installation
Get-ScheduledTask -TaskPath "\AI_Employee\*"
```

---

## What Gets Scheduled

| Task | Schedule | Command |
|------|----------|---------|
| Orchestrator | Every 5 min | `python orchestrator.py --check-once` |
| Dashboard | Daily 8 AM | `claude -p "Update Dashboard.md..."` |
| CEO Briefing | Sun 10 PM | `claude -p "Generate briefing..."` |
| Notification | Mon 8 AM | `python scripts/notify_briefing.py` |

---

## Verify It's Working

### Mac/Linux
```bash
# View cron jobs
crontab -l

# Watch orchestrator log (updates every 5 min)
tail -f AI_Employee_Vault/Logs/cron_orchestrator.log

# Check all logs
tail -f AI_Employee_Vault/Logs/cron_*.log

# Test manually
python orchestrator.py --check-once
```

### Windows
```powershell
# List all tasks
Get-ScheduledTask -TaskPath "\AI_Employee\*"

# Check task status
Get-ScheduledTask -TaskPath "\AI_Employee\*" | Select-Object TaskName, State, LastRunTime, NextRunTime

# Watch orchestrator log
Get-Content AI_Employee_Vault\Logs\cron_orchestrator.log -Tail 20 -Wait

# Test manually
Start-ScheduledTask -TaskName "\AI_Employee\Orchestrator_Check"
```

---

## Troubleshooting

### Jobs Not Running?

**Mac/Linux:**
```bash
# Check cron service
# Mac:
sudo launchctl list | grep cron
# Linux:
sudo systemctl status cron

# Test command manually
cd /path/to/Personal_AI_Employee
python orchestrator.py --check-once

# Check system logs
# Mac:
tail -f /var/log/system.log | grep cron
# Linux:
tail -f /var/log/syslog | grep CRON
```

**Windows:**
```powershell
# Open Task Scheduler GUI
taskschd.msc

# Navigate to: Task Scheduler Library > AI_Employee
# Right-click task → "Run" to test
# Check "Last Run Result" (0x0 = success)

# View task history
# Right-click task → Properties → History tab
```

### Common Fixes

**Python not found:**
```bash
# Find Python path
which python3  # Mac/Linux
where python   # Windows

# Update crontab with full path (Mac/Linux)
crontab -e
# Change: python orchestrator.py
# To: /usr/local/bin/python3 orchestrator.py
```

**Permission denied:**
```bash
# Mac/Linux
chmod -R 755 AI_Employee_Vault/Logs/
chmod +x scripts/*.sh scripts/*.py
```

**Claude CLI not found:**
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-cli

# Verify
claude --version
```

---

## Uninstall

### Mac/Linux
```bash
# Remove all AI Employee cron jobs
crontab -l | grep -v 'AI Employee' | crontab -
```

### Windows
```powershell
# Remove all scheduled tasks
Get-ScheduledTask -TaskPath "\AI_Employee\*" | Unregister-ScheduledTask -Confirm:$false
```

---

## Edit Paths (If Needed)

### Mac/Linux
The script auto-detects your project directory. If you need to edit:
```bash
nano scripts/setup_scheduler.sh
# Look for: PROJECT_DIR=
```

### Windows
The script auto-detects paths. If you need to edit:
```powershell
notepad scripts\setup_scheduler.ps1
# Look for: $ProjectDir =
```

---

## Next Steps

1. Run the setup script for your platform
2. Wait 5 minutes for first orchestrator check
3. Check logs: `tail -f AI_Employee_Vault/Logs/cron_orchestrator.log`
4. Create a test action item to verify processing

---

For detailed troubleshooting and customization, see: **SCHEDULER_SETUP_GUIDE.md**
