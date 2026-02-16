@echo off
REM Odoo Quick Start Script for Windows

echo ============================================================
echo ODOO 17 COMMUNITY EDITION - QUICK START
echo ============================================================
echo.

REM Check if Docker Desktop is running
echo [1/4] Checking Docker Desktop...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Docker Desktop is not running!
    echo.
    echo Please start Docker Desktop and wait for it to be ready.
    echo Look for the whale icon in your system tray to be steady.
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)
echo     Docker is running!
echo.

REM Navigate to project directory
cd /d "%~dp0.."

REM Pull images
echo [2/4] Pulling Docker images (this may take a few minutes)...
docker-compose pull
if %errorlevel% neq 0 (
    echo     ERROR: Failed to pull images
    pause
    exit /b 1
)
echo     Images pulled successfully!
echo.

REM Start containers
echo [3/4] Starting Odoo and PostgreSQL containers...
docker-compose up -d
if %errorlevel% neq 0 (
    echo     ERROR: Failed to start containers
    pause
    exit /b 1
)
echo     Containers started successfully!
echo.

REM Wait for Odoo to be ready
echo [4/4] Waiting for Odoo to be ready (30 seconds)...
timeout /t 30 /nobreak >nul
echo     Odoo should be ready!
echo.

REM Check container status
echo Container Status:
docker-compose ps
echo.

echo ============================================================
echo ODOO IS READY!
echo ============================================================
echo.
echo Access Odoo at: http://localhost:8069
echo.
echo Next steps:
echo 1. Open http://localhost:8069 in your browser
echo 2. Create a database (see scripts/setup_odoo.md for details)
echo 3. Enable modules: Invoicing, Accounting, Contacts
echo 4. Create API user for external access
echo.
echo To view logs: docker-compose logs -f odoo
echo To stop Odoo: docker-compose down
echo.
pause
