@echo off
REM Setup Windows Task Scheduler for AI Employee Health Monitor
REM Runs health_monitor.py every 5 minutes

setlocal enabledelayedexpansion

echo ============================================================
echo AI EMPLOYEE - HEALTH MONITOR SETUP (Windows)
echo ============================================================
echo.

REM Get current directory
set "PROJECT_DIR=%~dp0.."
cd /d "%PROJECT_DIR%"

echo Project directory: %PROJECT_DIR%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ and try again
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if health_monitor.py exists
if not exist "monitor\health_monitor.py" (
    echo ERROR: monitor\health_monitor.py not found
    pause
    exit /b 1
)

echo [OK] Health monitor script found
echo.

REM Create logs directory
if not exist "monitor\logs" mkdir "monitor\logs"
echo [OK] Logs directory created
echo.

echo === Creating Scheduled Task ===
echo.
echo This will create a task that runs every 5 minutes.
echo Task name: AI_Employee_Health_Monitor
echo.

set /p "CONFIRM=Continue? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Setup cancelled
    pause
    exit /b 0
)

echo.
echo Creating task...
echo.

REM Delete existing task if it exists
schtasks /delete /tn "AI_Employee_Health_Monitor" /f >nul 2>&1

REM Create new task
schtasks /create ^
    /tn "AI_Employee_Health_Monitor" ^
    /tr "cmd /c cd /d \"%PROJECT_DIR%\" && python monitor\health_monitor.py >> monitor\logs\health.log 2>&1" ^
    /sc minute ^
    /mo 5 ^
    /f

if errorlevel 1 (
    echo.
    echo [FAIL] Failed to create scheduled task
    echo.
    echo You may need to run this script as Administrator.
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo [OK] Scheduled task created successfully
echo.

REM Verify task was created
echo === Verifying Task ===
echo.
schtasks /query /tn "AI_Employee_Health_Monitor" /fo LIST

echo.
echo ============================================================
echo SETUP COMPLETE
echo ============================================================
echo.
echo Health monitor will run every 5 minutes automatically.
echo.
echo To view the task:
echo   schtasks /query /tn AI_Employee_Health_Monitor
echo.
echo To run manually:
echo   python monitor\health_monitor.py
echo.
echo To view logs:
echo   type monitor\logs\health.log
echo.
echo To disable the task:
echo   schtasks /change /tn AI_Employee_Health_Monitor /disable
echo.
echo To delete the task:
echo   schtasks /delete /tn AI_Employee_Health_Monitor /f
echo.
echo Next steps:
echo   1. Set ALERT_EMAIL environment variable (optional)
echo   2. Run: python monitor\status_dashboard.py
echo   3. Wait 5 minutes for first health check
echo.
pause
