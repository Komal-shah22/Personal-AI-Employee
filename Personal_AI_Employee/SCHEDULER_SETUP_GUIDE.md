# Scheduler Setup Guide

Complete guide for setting up automated scheduling for the AI Employee system.

## Overview

The AI Employee system can run automatically on a schedule using:
- **Mac/Linux**: Cron jobs
- **Windows**: Task Scheduler

This guide covers setup for both platforms.

---

## What Gets Scheduled

Four automated tasks:

| Task | Schedule | Purpose |
|------|----------|---------|
| **Orchestrator Check** | Every 5 minutes | Processes items in `Needs_Action/` folder |
| **Dashboard Update** | Daily at 8:00 AM | Updates `Dashboard.md` with yesterday's summary |
| **CEO Briefing** | Sunday at 10:00 PM | Generates weekly Monday morning briefing |
| **Briefing Notification** | Monday at 8:00 AM | Notifies when briefing is ready |

---

## Mac/Linux Setup (Cron)

### Step 1: Edit Paths

Open the setup script:
```bash
nano scripts/setup_scheduler.sh
```

The script auto-detects your project directory, but verify these paths are correct:
- `$PROJECT_DIR` - Should point to your Personal_AI_Employee directory
- `$PYTHON_CMD` - Should be `python` or `python3`

### Step 2: Make Script Executable

```bash
chmod +x scripts/setup_scheduler.sh
```

### Step 3: Run Setup

```bash
./scripts/setup_scheduler.sh
```

The script will:
1. Detect your project directory
2. Check for Python and Claude CLI
3. Show you the cron jobs it will create
4. Ask for confirmation
5. Install the cron jobs

### Step 4: Verify Installation

Check that cron jobs were created:
```bash
crontab -l
```

You should see 4 entries with "AI Employee" comments.

### Step 5: Monitor Logs

Watch for activity:
```bash
# Watch orchestrator log (updates every 5 minutes)
tail -f AI_Employee_Vault/Logs/cron_orchestrator.log

# Watch all cron logs
tail -f AI_Employee_Vault/Logs/cron_*.log
```

### Troubleshooting (Mac/Linux)

**Cron jobs not running?**

1. Check cron service is running:
   ```bash
   # Mac
   sudo launchctl list | grep cron

   # Linux
   sudo systemctl status cron
   ```

2. Check log files exist and are writable:
   ```bash
   ls -la AI_Employee_Vault/Logs/
   ```

3. Test commands manually:
   ```bash
   cd /path/to/Personal_AI_Employee
   python orchestrator.py --check-once
   ```

4. Check cron logs:
   ```bash
   # Mac
   tail -f /var/log/system.log | grep cron

   # Linux
   tail -f /var/log/syslog | grep CRON
   ```

**Remove all cron jobs:**
```bash
crontab -l | grep -v 'AI Employee' | crontab -
```

**Edit cron jobs manually:**
```bash
crontab -e
```

---

## Windows Setup (Task Scheduler)

### Step 1: Edit Paths

Open the setup script in a text editor:
```powershell
notepad scripts\setup_scheduler.ps1
```

Find these lines near the top and update if needed:
```powershell
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
```

The script auto-detects paths, but verify they're correct for your system.

### Step 2: Run as Administrator

**IMPORTANT**: You must run PowerShell as Administrator.

1. Press `Win + X`
2. Select "Windows PowerShell (Admin)" or "Terminal (Admin)"
3. Navigate to your project:
   ```powershell
   cd E:\hackathon-0\Personal_AI_Employee
   ```

### Step 3: Allow Script Execution

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Run Setup

```powershell
.\scripts\setup_scheduler.ps1
```

The script will:
1. Detect your project directory
2. Check for Python and Claude CLI
3. Show you the tasks it will create
4. Ask for confirmation
5. Create the scheduled tasks

### Step 5: Verify Installation

Check that tasks were created:
```powershell
Get-ScheduledTask -TaskPath "\AI_Employee\*"
```

You should see 4 tasks:
- `Orchestrator_Check`
- `Dashboard_Update`
- `CEO_Briefing`
- `Briefing_Notify`

### Step 6: View Task Details

```powershell
Get-ScheduledTask -TaskPath "\AI_Employee\*" | Get-ScheduledTaskInfo
```

### Step 7: Monitor Logs

Watch for activity:
```powershell
# Watch orchestrator log (updates every 5 minutes)
Get-Content AI_Employee_Vault\Logs\cron_orchestrator.log -Tail 20 -Wait

# View all cron logs
Get-ChildItem AI_Employee_Vault\Logs\cron_*.log | ForEach-Object { Get-Content $_ -Tail 10 }
```

### Troubleshooting (Windows)

**Tasks not running?**

1. Open Task Scheduler GUI:
   ```powershell
   taskschd.msc
   ```

2. Navigate to: `Task Scheduler Library > AI_Employee`

3. Right-click a task and select "Run" to test manually

4. Check "Last Run Result" column:
   - `0x0` = Success
   - Other codes = Error (Google the code)

5. View task history:
   - Right-click task → "Properties"
   - Go to "History" tab

**Test a task manually:**
```powershell
Start-ScheduledTask -TaskName "\AI_Employee\Orchestrator_Check"
```

**Check task status:**
```powershell
Get-ScheduledTask -TaskPath "\AI_Employee\*" | Select-Object TaskName, State, LastRunTime, NextRunTime
```

**Remove all tasks:**
```powershell
Get-ScheduledTask -TaskPath "\AI_Employee\*" | Unregister-ScheduledTask -Confirm:$false
```

**Re-enable a disabled task:**
```powershell
Enable-ScheduledTask -TaskName "\AI_Employee\Orchestrator_Check"
```

---

## Common Issues (Both Platforms)

### Issue: Python not found

**Symptoms**: Tasks fail with "python: command not found"

**Solution**:
1. Verify Python is installed:
   ```bash
   python --version
   # or
   python3 --version
   ```

2. Update script to use full path:
   ```bash
   # Mac/Linux: Edit crontab
   crontab -e
   # Change: python orchestrator.py
   # To: /usr/local/bin/python3 orchestrator.py

   # Windows: Edit task in Task Scheduler GUI
   # Change command to full path: C:\Python39\python.exe
   ```

### Issue: Claude CLI not found

**Symptoms**: Dashboard and briefing tasks fail

**Solution**:
1. Install Claude CLI:
   ```bash
   npm install -g @anthropic-ai/claude-cli
   ```

2. Verify installation:
   ```bash
   claude --version
   ```

3. If still not found, use full path in scheduled tasks

### Issue: Permission denied

**Symptoms**: Tasks fail with permission errors

**Solution (Mac/Linux)**:
```bash
# Make sure log directory is writable
chmod -R 755 AI_Employee_Vault/Logs/

# Make sure scripts are executable
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

**Solution (Windows)**:
- Run Task Scheduler as Administrator
- Ensure tasks run with appropriate user account

### Issue: Working directory wrong

**Symptoms**: Tasks can't find files (orchestrator.py, Dashboard.md, etc.)

**Solution**:
- Verify the working directory in your scheduled task
- All tasks should run from the project root directory
- Check paths in crontab or Task Scheduler

---

## Customizing Schedules

### Change Orchestrator Check Interval

**Mac/Linux** (edit crontab):
```bash
crontab -e

# Change from every 5 minutes:
*/5 * * * * cd /path/to/project && python orchestrator.py --check-once

# To every 10 minutes:
*/10 * * * * cd /path/to/project && python orchestrator.py --check-once
```

**Windows** (PowerShell):
```powershell
# Get the task
$Task = Get-ScheduledTask -TaskName "\AI_Employee\Orchestrator_Check"

# Create new trigger (every 10 minutes)
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration ([TimeSpan]::MaxValue)

# Update task
Set-ScheduledTask -TaskName "\AI_Employee\Orchestrator_Check" -Trigger $Trigger
```

### Change Dashboard Update Time

**Mac/Linux**:
```bash
# Change from 8:00 AM to 9:00 AM
0 9 * * * cd /path/to/project && claude -p "Update Dashboard.md..."
```

**Windows**:
```powershell
$Trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
Set-ScheduledTask -TaskName "\AI_Employee\Dashboard_Update" -Trigger $Trigger
```

### Change CEO Briefing Day/Time

**Mac/Linux**:
```bash
# Change from Sunday 10 PM to Friday 5 PM
0 17 * * 5 cd /path/to/project && claude -p "Generate CEO briefing..."
```

**Windows**:
```powershell
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "17:00"
Set-ScheduledTask -TaskName "\AI_Employee\CEO_Briefing" -Trigger $Trigger
```

---

## Testing Your Setup

### 1. Test Orchestrator Manually

```bash
# Mac/Linux
cd /path/to/Personal_AI_Employee
python orchestrator.py --check-once

# Windows
cd E:\hackathon-0\Personal_AI_Employee
python orchestrator.py --check-once
```

Expected: Should process any items in `Needs_Action/` folder

### 2. Create Test Action Item

```bash
# Create a test file
cat > AI_Employee_Vault/Needs_Action/TEST_scheduler.md << 'EOF'
---
type: test
priority: low
status: pending
---

# Test Action Item

This is a test to verify the scheduler is working.

Please acknowledge this test item.
EOF
```

Wait 5 minutes, then check logs:
```bash
tail AI_Employee_Vault/Logs/cron_orchestrator.log
```

### 3. Test Notification Script

```bash
python scripts/notify_briefing.py
```

Expected: Creates notification in `Needs_Action/` if briefing exists

---

## Monitoring & Maintenance

### Daily Checks

```bash
# View today's activity
tail -50 AI_Employee_Vault/Logs/cron_orchestrator.log

# Check for errors
grep -i error AI_Employee_Vault/Logs/cron_*.log
```

### Weekly Checks

```bash
# Verify all tasks ran this week
ls -lt AI_Employee_Vault/Logs/cron_*.log

# Check briefing was generated
ls -lt AI_Employee_Vault/Briefings/
```

### Log Rotation

Logs can grow large over time. Set up log rotation:

**Mac/Linux** (create `/etc/logrotate.d/ai-employee`):
```
/path/to/Personal_AI_Employee/AI_Employee_Vault/Logs/*.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
}
```

**Windows** (PowerShell script to run monthly):
```powershell
# Archive old logs
$LogDir = "AI_Employee_Vault\Logs"
$ArchiveDir = "AI_Employee_Vault\Logs\Archive"

Get-ChildItem $LogDir -Filter "cron_*.log" | Where-Object {
    $_.LastWriteTime -lt (Get-Date).AddDays(-30)
} | ForEach-Object {
    Move-Item $_.FullName -Destination $ArchiveDir
}
```

---

## Uninstalling

### Mac/Linux

Remove all AI Employee cron jobs:
```bash
crontab -l | grep -v 'AI Employee' | crontab -
```

### Windows

Remove all scheduled tasks:
```powershell
Get-ScheduledTask -TaskPath "\AI_Employee\*" | Unregister-ScheduledTask -Confirm:$false
```

Or use Task Scheduler GUI:
1. Open `taskschd.msc`
2. Navigate to `AI_Employee` folder
3. Delete all tasks
4. Delete the folder

---

## Next Steps

After setup is complete:

1. **Wait 5 minutes** for first orchestrator check
2. **Check logs** to verify tasks are running
3. **Create test action items** to verify processing
4. **Adjust schedules** if needed for your timezone/workflow
5. **Set up log rotation** to prevent disk space issues

---

## Support

If you encounter issues:

1. Check the troubleshooting sections above
2. Review log files for error messages
3. Test commands manually to isolate the problem
4. Verify paths and permissions are correct

---

**Last Updated**: 2026-02-16
