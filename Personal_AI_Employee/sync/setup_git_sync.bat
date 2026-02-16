@echo off
REM Git-Based Vault Synchronization Setup Script (Windows)
REM Sets up Git repository in AI_Employee_Vault for cloud-local sync

setlocal enabledelayedexpansion

echo ============================================================
echo VAULT SYNC SETUP - GIT-BASED SYNCHRONIZATION
echo ============================================================
echo.

REM Get directories
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
set "VAULT_DIR=%PROJECT_DIR%\AI_Employee_Vault"

REM Check if vault exists
if not exist "%VAULT_DIR%" (
    echo ERROR: AI_Employee_Vault directory not found
    pause
    exit /b 1
)

echo Vault directory: %VAULT_DIR%
echo.

REM Step 1: Initialize Git repository
echo === Step 1: Initialize Git Repository ===
echo.

cd /d "%VAULT_DIR%"

if exist ".git" (
    echo Git repository already exists
    set /p "REINIT=Reinitialize? This will preserve history (y/n): "
    if /i not "!REINIT!"=="y" (
        echo Skipping git init
    )
) else (
    git init
    echo [OK] Git repository initialized
)

echo.

REM Step 2: Create .gitignore
echo === Step 2: Create .gitignore ===
echo.

(
echo # Secrets and Credentials (NEVER COMMIT^)
echo .env
echo .env.local
echo .env.cloud
echo *.key
echo *.pem
echo *.p12
echo *.ovpn
echo credentials.json
echo token.json
echo token.pickle
echo client_secret*.json
echo.
echo # WhatsApp Sessions (LOCAL ONLY^)
echo sessions/
echo .whatsapp_processed.json
echo.
echo # Payment Data (LOCAL ONLY^)
echo payments/
echo transactions/
echo.
echo # Processed IDs
echo .processed_ids.json
echo.
echo # Temporary Files
echo *.tmp
echo *.temp
echo _*
echo .DS_Store
echo Thumbs.db
echo.
echo # Sync State
echo .vault_sync_state.json
) > .gitignore

echo [OK] .gitignore created
echo.

REM Step 3: Create pre-commit hook
echo === Step 3: Create Pre-Commit Hook (Security^) ===
echo.

if not exist ".git\hooks" mkdir ".git\hooks"

(
echo #!/bin/bash
echo # Pre-commit hook to prevent committing secrets
echo.
echo echo "Running security scan..."
echo.
echo # Check for forbidden files
echo if git diff --cached --name-only ^| grep -qE "^\.env"; then
echo     echo "ERROR: Attempting to commit .env file"
echo     exit 1
echo fi
echo.
echo if git diff --cached --name-only ^| grep -q "sessions/"; then
echo     echo "ERROR: Attempting to commit WhatsApp sessions"
echo     exit 1
echo fi
echo.
echo if git diff --cached ^| grep -iE "(ANTHROPIC_API_KEY^|sk-ant-^|password.*=)" ^> /dev/null; then
echo     echo "ERROR: Potential secret detected"
echo     exit 1
echo fi
echo.
echo echo "Security scan passed"
echo exit 0
) > .git\hooks\pre-commit

echo [OK] Pre-commit hook installed
echo.

REM Step 4: Create directory structure
echo === Step 4: Create Directory Structure ===
echo.

mkdir Needs_Action 2>nul
mkdir In_Progress\cloud_agent 2>nul
mkdir In_Progress\local_agent 2>nul
mkdir Plans 2>nul
mkdir Drafts 2>nul
mkdir Approved 2>nul
mkdir Done 2>nul
mkdir Pending_Approval 2>nul
mkdir Logs 2>nul
mkdir Briefings 2>nul
mkdir Updates 2>nul

echo [OK] Directory structure created
echo.

REM Step 5: Create README
echo === Step 5: Create Vault README ===
echo.

(
echo # AI Employee Vault
echo.
echo This directory is synchronized between cloud (Oracle^) and local machine using Git.
echo.
echo ## Work Zones
echo.
echo ### Cloud Owns (Read/Write^)
echo - `Needs_Action/` - Incoming tasks
echo - `Plans/` - Task plans
echo - `Drafts/` - Draft content
echo.
echo ### Local Owns (Read/Write^)
echo - `Approved/` - Human-approved actions
echo - `Done/` - Completed tasks
echo - `Pending_Approval/` - Awaiting approval
echo.
echo ### Shared (Both^)
echo - `In_Progress/` - Currently processing
echo - `Logs/` - Activity logs
echo - `Briefings/` - CEO briefings
echo.
echo ## Security
echo.
echo Files that are NEVER committed:
echo - `.env` files
echo - `sessions/` (WhatsApp^)
echo - `credentials.json`
echo - `*.key`, `*.pem` files
echo.
echo Pre-commit hook scans for secrets.
) > README.md

echo [OK] README created
echo.

REM Step 6: Initial commit
echo === Step 6: Initial Commit ===
echo.

git add .
git commit -m "Initial vault setup with security controls" 2>nul

echo [OK] Initial commit created
echo.

REM Step 7: Set up remote
echo === Step 7: Set Up Remote Repository ===
echo.

echo You need to set up a Git remote for synchronization.
echo.
echo Options:
echo   1. Oracle Cloud VM (recommended^)
echo   2. GitHub private repository
echo   3. GitLab private repository
echo.

set /p "SETUP_REMOTE=Configure remote now? (y/n): "

if /i "%SETUP_REMOTE%"=="y" (
    echo.
    echo For Oracle Cloud VM:
    echo   1. SSH to your VM
    echo   2. Create bare repo: mkdir -p ~/vault.git ^&^& cd ~/vault.git ^&^& git init --bare
    echo   3. Use remote URL: ubuntu@YOUR_VM_IP:~/vault.git
    echo.

    set /p "REMOTE_URL=Enter remote URL: "

    if not "!REMOTE_URL!"=="" (
        git remote add origin "!REMOTE_URL!" 2>nul || git remote set-url origin "!REMOTE_URL!"
        echo [OK] Remote configured: !REMOTE_URL!

        set /p "PUSH_NOW=Push to remote now? (y/n): "
        if /i "!PUSH_NOW!"=="y" (
            git push -u origin main 2>nul || git push -u origin master
            echo [OK] Pushed to remote
        )
    )
)

echo.

REM Step 8: Set up auto-pull (Task Scheduler)
echo === Step 8: Set Up Auto-Pull (Local Only^) ===
echo.

set /p "SETUP_TASK=Set up automatic pull every 2 minutes? (y/n): "

if /i "%SETUP_TASK%"=="y" (
    echo.
    echo Creating scheduled task...

    schtasks /create /tn "AI_Employee_Vault_Sync" /tr "cmd /c cd /d %VAULT_DIR% && git pull --rebase origin main >> Logs\sync.log 2>&1" /sc minute /mo 2 /f >nul 2>&1

    if !errorlevel! equ 0 (
        echo [OK] Scheduled task created (pull every 2 minutes^)
        echo.
        echo To view: schtasks /query /tn AI_Employee_Vault_Sync
        echo To remove: schtasks /delete /tn AI_Employee_Vault_Sync /f
    ) else (
        echo [FAIL] Failed to create scheduled task
        echo Run as Administrator to create scheduled tasks
    )
)

echo.

REM Step 9: Test sync
echo === Step 9: Test Sync ===
echo.

set /p "CREATE_TEST=Create test file to verify sync? (y/n): "

if /i "%CREATE_TEST%"=="y" (
    set "TEST_FILE=Needs_Action\TEST_sync_%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.md"
    set "TEST_FILE=!TEST_FILE: =0!"

    (
        echo ---
        echo type: test
        echo priority: low
        echo created: %date% %time%
        echo ---
        echo.
        echo # Sync Test File
        echo.
        echo This is a test file to verify vault synchronization.
        echo.
        echo If you can see this on both machines, sync is working!
    ) > "!TEST_FILE!"

    git add "!TEST_FILE!"
    git commit -m "Test sync file"

    git remote get-url origin >nul 2>&1
    if !errorlevel! equ 0 (
        git push origin main 2>nul || git push origin master
        echo [OK] Test file created and pushed
        echo.
        echo Check the other machine to verify sync.
    ) else (
        echo [OK] Test file created (no remote configured^)
    )
)

echo.

REM Summary
echo ============================================================
echo SETUP COMPLETE
echo ============================================================
echo.
echo [OK] Git repository initialized
echo [OK] .gitignore created (secrets excluded^)
echo [OK] Pre-commit hook installed
echo [OK] Directory structure created
echo [OK] Initial commit created
echo.
echo Next steps:
echo.
echo 1. On CLOUD (Oracle VM^):
echo    python sync/vault_sync.py --mode cloud
echo.
echo 2. On LOCAL machine:
echo    python sync/vault_sync.py --mode local
echo.
echo 3. Monitor sync:
echo    type AI_Employee_Vault\Logs\sync.log
echo.
echo Security reminders:
echo   - Pre-commit hook blocks secrets
echo   - WhatsApp sessions stay LOCAL only
echo   - Payment data stays LOCAL only
echo.
pause
