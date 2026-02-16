# 📅 Automated Scheduling Setup Guide

## Overview

This guide helps you set up automated scheduling for your Personal AI Employee using Windows Task Scheduler.

## 📁 Files Created

1. **`scripts/setup_scheduler.ps1`** - PowerShell script to create scheduled tasks
2. **`scripts/daily_summary.py`** - Python script for daily statistics

## 🚀 Quick Setup

### Step 1: Run the Setup Script

1. **Open PowerShell as Administrator:**
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Navigate to your project:**
   ```powershell
   cd E:\hackathon-0\Personal_AI_Employee
   ```

3. **Run the setup script:**
   ```powershell
   .\scripts\setup_scheduler.ps1
   ```

   If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Step 2: Verify Tasks Were Created

Run this command to see all AI Employee tasks:

```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "AI_Employee*"}
```

You should see 3 tasks:
- `AI_Employee_Orchestrator` - Every 5 minutes
- `AI_Employee_Daily_Summary` - Daily at 8:00 AM
- `AI_Employee_Weekly_Briefing` - Sunday at 10:00 PM

### Step 3: View Task Details

To see detailed information about a specific task:

```powershell
Get-ScheduledTask -TaskName "AI_Employee_Orchestrator" | Format-List *
```

## 📋 Scheduled Tasks

### Task 1: Orchestrator (Every 5 Minutes)

**Name:** `AI_Employee_Orchestrator`

**Schedule:** Every 5 minutes, indefinitely

**Action:** Runs `python orchestrator.py` to process pending tasks

**Purpose:** Continuously monitors and processes tasks in the Needs_Action folder

### Task 2: Daily Summary (8:00 AM Daily)

**Name:** `AI_Employee_Daily_Summary`

**Schedule:** Daily at 8:00 AM

**Action:** Runs `python scripts/daily_summary.py`

**Purpose:**
- Counts files in all vault directories
- Updates Dashboard.md with current statistics
- Logs daily metrics to `Logs/daily_[date].json`
- Appends summary to `Logs/cron.log`

### Task 3: Weekly CEO Briefing (Sunday 10:00 PM)

**Name:** `AI_Employee_Weekly_Briefing`

**Schedule:** Weekly on Sunday at 10:00 PM

**Action:** Runs `claude skill generate-reports --report_type weekly`

**Purpose:** Generates the Monday Morning CEO Briefing with:
- Revenue summary
- Completed tasks
- Bottlenecks
- Proactive suggestions

## 🎮 Managing Tasks

### Manually Run a Task

```powershell
Start-ScheduledTask -TaskName "AI_Employee_Orchestrator"
```

### Disable a Task

```powershell
Disable-ScheduledTask -TaskName "AI_Employee_Orchestrator"
```

### Enable a Task

```powershell
Enable-ScheduledTask -TaskName "AI_Employee_Orchestrator"
```

### View Task History

```powershell
Get-ScheduledTask -TaskName "AI_Employee_Orchestrator" | Get-ScheduledTaskInfo
```

### Remove All AI Employee Tasks

```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "AI_Employee*"} | Unregister-ScheduledTask -Confirm:$false
```

## 🔧 Troubleshooting

### Task Not Running?

1. **Check task status:**
   ```powershell
   Get-ScheduledTask -TaskName "AI_Employee_Orchestrator" | Select-Object State, LastRunTime, LastTaskResult
   ```

2. **View task history in Task Scheduler GUI:**
   - Press `Win + R`, type `taskschd.msc`, press Enter
   - Navigate to Task Scheduler Library
   - Find your AI_Employee tasks
   - Check the "History" tab

3. **Check if Python is in PATH:**
   ```powershell
   python --version
   ```

4. **Check if Claude Code is in PATH:**
   ```powershell
   claude --version
   ```

### Execution Policy Issues?

If you get "cannot be loaded because running scripts is disabled":

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Task Runs But Fails?

Check the logs:
- `AI_Employee_Vault/Logs/cron.log` - Daily summary output
- `AI_Employee_Vault/Logs/[date].txt` - Daily activity logs
- `orchestrator.log` - Orchestrator execution logs

## 📊 Monitoring

### Check Daily Summary Output

```powershell
Get-Content AI_Employee_Vault\Logs\cron.log -Tail 50
```

### View Today's Activity Log

```powershell
$today = Get-Date -Format "yyyy-MM-dd"
Get-Content "AI_Employee_Vault\Logs\$today.txt"
```

### View Daily Statistics JSON

```powershell
$today = Get-Date -Format "yyyy-MM-dd"
Get-Content "AI_Employee_Vault\Logs\daily_$today.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

## 🎯 Testing

### Test Daily Summary Manually

```powershell
python scripts\daily_summary.py
```

Expected output:
- Updates `Dashboard.md`
- Creates/updates `Logs/daily_[date].json`
- Appends to `Logs/[date].txt`

### Test Orchestrator Manually

```powershell
python orchestrator.py
```

### Test Weekly Briefing Manually

```powershell
claude skill generate-reports --report_type weekly
```

## ✅ Verification Checklist

After setup, verify:

- [ ] All 3 tasks appear in Task Scheduler
- [ ] Tasks are enabled (State = Ready)
- [ ] Python path is correct in task actions
- [ ] Claude Code path is correct in task actions
- [ ] Working directory is set to project root
- [ ] Run one task manually to test: `Start-ScheduledTask -TaskName "AI_Employee_Daily_Summary"`
- [ ] Check that Dashboard.md was updated
- [ ] Check that logs were created

## 🎉 Success!

Once setup is complete, your AI Employee will:
- ✅ Process tasks automatically every 5 minutes
- ✅ Generate daily summaries every morning at 8 AM
- ✅ Create weekly CEO briefings every Sunday at 10 PM

Your system is now **fully automated** and ready for **Silver Tier certification**! 🏆

## 📝 Notes

- Tasks run even when you're not logged in (if configured)
- Tasks will start automatically after system reboot
- Logs are kept in `AI_Employee_Vault/Logs/` for audit trail
- You can modify schedules in Task Scheduler GUI if needed

---

**Need help?** Check the troubleshooting section or review task history in Task Scheduler.
