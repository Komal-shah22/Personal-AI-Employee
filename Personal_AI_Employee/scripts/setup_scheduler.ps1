# AI Employee Scheduler Setup Script (Windows)
# This script sets up Windows Task Scheduler jobs to automate the AI Employee system

# Requires Administrator privileges
#Requires -RunAsAdministrator

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "AI EMPLOYEE - SCHEDULER SETUP (WINDOWS)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get the project directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "Detected project directory: $ProjectDir" -ForegroundColor Green
Write-Host ""

# Check if Python is available
$PythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonCmd = "python3"
} else {
    Write-Host "ERROR: Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if Claude CLI is available
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Host "WARNING: Claude CLI not found. Some tasks may fail." -ForegroundColor Yellow
    Write-Host "Install with: npm install -g @anthropic-ai/claude-cli" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "This script will create the following scheduled tasks:" -ForegroundColor White
Write-Host ""
Write-Host "1. AI_Employee_Orchestrator - Every 5 minutes" -ForegroundColor White
Write-Host "   Checks Needs_Action folder and processes tasks"
Write-Host ""
Write-Host "2. AI_Employee_Dashboard - Daily at 8:00 AM" -ForegroundColor White
Write-Host "   Updates Dashboard.md with daily summary"
Write-Host ""
Write-Host "3. AI_Employee_CEO_Briefing - Sunday at 10:00 PM" -ForegroundColor White
Write-Host "   Generates weekly CEO briefing"
Write-Host ""
Write-Host "4. AI_Employee_Briefing_Notify - Monday at 8:00 AM" -ForegroundColor White
Write-Host "   Sends briefing notification"
Write-Host ""

$Confirm = Read-Host "Continue with setup? (y/n)"
if ($Confirm -ne 'y' -and $Confirm -ne 'Y') {
    Write-Host "Setup cancelled." -ForegroundColor Yellow
    exit 0
}

# Task Scheduler folder
$TaskFolder = "\AI_Employee\"

# Create task folder if it doesn't exist
try {
    $Schedule = New-Object -ComObject Schedule.Service
    $Schedule.Connect()
    $RootFolder = $Schedule.GetFolder("\")

    try {
        $RootFolder.GetFolder($TaskFolder)
        Write-Host "Task folder already exists." -ForegroundColor Yellow
    } catch {
        $RootFolder.CreateFolder($TaskFolder)
        Write-Host "Created task folder: $TaskFolder" -ForegroundColor Green
    }
} catch {
    Write-Host "ERROR: Failed to access Task Scheduler: $_" -ForegroundColor Red
    exit 1
}

# Function to create scheduled task
function New-AIEmployeeTask {
    param(
        [string]$TaskName,
        [string]$Description,
        [string]$Command,
        [string]$Arguments,
        [string]$WorkingDirectory,
        [string]$TriggerType,
        [hashtable]$TriggerParams
    )

    Write-Host "Creating task: $TaskName..." -ForegroundColor Cyan

    # Remove existing task if it exists
    try {
        Unregister-ScheduledTask -TaskName "$TaskFolder$TaskName" -Confirm:$false -ErrorAction SilentlyContinue
    } catch {}

    # Create action
    $Action = New-ScheduledTaskAction -Execute $Command -Argument $Arguments -WorkingDirectory $WorkingDirectory

    # Create trigger based on type
    $Trigger = switch ($TriggerType) {
        "Interval" {
            $TriggerObj = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval $TriggerParams.Interval -RepetitionDuration ([TimeSpan]::MaxValue)
            $TriggerObj
        }
        "Daily" {
            New-ScheduledTaskTrigger -Daily -At $TriggerParams.Time
        }
        "Weekly" {
            New-ScheduledTaskTrigger -Weekly -DaysOfWeek $TriggerParams.DayOfWeek -At $TriggerParams.Time
        }
    }

    # Create settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    # Register task
    try {
        Register-ScheduledTask -TaskName "$TaskFolder$TaskName" -Action $Action -Trigger $Trigger -Settings $Settings -Description $Description -ErrorAction Stop
        Write-Host "✓ Task created: $TaskName" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to create task: $TaskName - $_" -ForegroundColor Red
    }
}

# 1. Orchestrator Check (every 5 minutes)
New-AIEmployeeTask `
    -TaskName "Orchestrator_Check" `
    -Description "AI Employee - Check Needs_Action folder every 5 minutes" `
    -Command $PythonCmd `
    -Arguments "`"$ProjectDir\orchestrator.py`" --check-once >> `"$ProjectDir\AI_Employee_Vault\Logs\cron_orchestrator.log`" 2>&1" `
    -WorkingDirectory $ProjectDir `
    -TriggerType "Interval" `
    -TriggerParams @{ Interval = (New-TimeSpan -Minutes 5) }

# 2. Dashboard Update (daily 8 AM)
New-AIEmployeeTask `
    -TaskName "Dashboard_Update" `
    -Description "AI Employee - Update Dashboard.md daily at 8:00 AM" `
    -Command "claude" `
    -Arguments "-p `"Update Dashboard.md with today's summary. Read all /Logs/ from yesterday.`" >> `"$ProjectDir\AI_Employee_Vault\Logs\cron_dashboard.log`" 2>&1" `
    -WorkingDirectory $ProjectDir `
    -TriggerType "Daily" `
    -TriggerParams @{ Time = "08:00" }

# 3. CEO Briefing (Sunday 10 PM)
New-AIEmployeeTask `
    -TaskName "CEO_Briefing" `
    -Description "AI Employee - Generate CEO briefing every Sunday at 10:00 PM" `
    -Command $PythonCmd `
    -Arguments "`"$ProjectDir\scripts\generate_ceo_briefing.py`" >> `"$ProjectDir\AI_Employee_Vault\Logs\cron_briefing.log`" 2>&1" `
    -WorkingDirectory $ProjectDir `
    -TriggerType "Weekly" `
    -TriggerParams @{ DayOfWeek = "Sunday"; Time = "22:00" }

# 4. Briefing Notification (Monday 8 AM)
New-AIEmployeeTask `
    -TaskName "Briefing_Notify" `
    -Description "AI Employee - Send briefing notification every Monday at 8:00 AM" `
    -Command $PythonCmd `
    -Arguments "`"$ProjectDir\scripts\notify_briefing.py`" >> `"$ProjectDir\AI_Employee_Vault\Logs\cron_notify.log`" 2>&1" `
    -WorkingDirectory $ProjectDir `
    -TriggerType "Weekly" `
    -TriggerParams @{ DayOfWeek = "Monday"; Time = "08:00" }

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ SCHEDULED TASKS CREATED SUCCESSFULLY" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verify installation:" -ForegroundColor White
Write-Host "  Get-ScheduledTask -TaskPath '$TaskFolder*'" -ForegroundColor Gray
Write-Host ""
Write-Host "View task details:" -ForegroundColor White
Write-Host "  Get-ScheduledTask -TaskPath '$TaskFolder*' | Get-ScheduledTaskInfo" -ForegroundColor Gray
Write-Host ""
Write-Host "View logs:" -ForegroundColor White
Write-Host "  Get-Content AI_Employee_Vault\Logs\cron_*.log -Tail 20 -Wait" -ForegroundColor Gray
Write-Host ""
Write-Host "Remove all AI Employee tasks:" -ForegroundColor White
Write-Host "  Get-ScheduledTask -TaskPath '$TaskFolder*' | Unregister-ScheduledTask -Confirm:`$false" -ForegroundColor Gray
Write-Host ""
Write-Host "Open Task Scheduler GUI:" -ForegroundColor White
Write-Host "  taskschd.msc" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Wait 5 minutes for first orchestrator check"
Write-Host "2. Check logs to verify tasks are running"
Write-Host "3. Adjust schedule if needed in Task Scheduler"
Write-Host ""
