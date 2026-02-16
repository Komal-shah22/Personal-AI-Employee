#!/bin/bash

# Setup Cron Job for AI Employee Health Monitor
# Runs health_monitor.py every 5 minutes

set -e

echo "============================================================"
echo "AI EMPLOYEE - HEALTH MONITOR SETUP (Linux/Mac)"
echo "============================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Project directory: $PROJECT_DIR"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.6+ and try again"
    exit 1
fi

echo -e "${GREEN}✓ Python found${NC}"
echo ""

# Check if health_monitor.py exists
if [ ! -f "$PROJECT_DIR/monitor/health_monitor.py" ]; then
    echo -e "${RED}ERROR: monitor/health_monitor.py not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Health monitor script found${NC}"
echo ""

# Create logs directory
mkdir -p "$PROJECT_DIR/monitor/logs"
echo -e "${GREEN}✓ Logs directory created${NC}"
echo ""

# Cron job command
CRON_CMD="*/5 * * * * cd $PROJECT_DIR && python3 monitor/health_monitor.py >> monitor/logs/health.log 2>&1"

echo "=== Setting Up Cron Job ==="
echo ""
echo "This will create a cron job that runs every 5 minutes."
echo ""
echo "Cron command:"
echo "  $CRON_CMD"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled"
    exit 0
fi

echo ""
echo "Adding cron job..."
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "health_monitor.py"; then
    echo -e "${YELLOW}Cron job already exists${NC}"
    echo ""
    read -p "Replace existing cron job? (y/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Remove old cron job
        crontab -l 2>/dev/null | grep -v "health_monitor.py" | crontab -
        echo -e "${GREEN}✓ Removed old cron job${NC}"
    else
        echo "Keeping existing cron job"
        exit 0
    fi
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cron job added successfully${NC}"
else
    echo -e "${RED}Failed to add cron job${NC}"
    exit 1
fi

echo ""

# Verify cron job was added
echo "=== Verifying Cron Job ==="
echo ""
echo "Current cron jobs:"
crontab -l | grep "health_monitor.py"
echo ""

echo "============================================================"
echo "SETUP COMPLETE"
echo "============================================================"
echo ""
echo "Health monitor will run every 5 minutes automatically."
echo ""
echo "To view cron jobs:"
echo "  crontab -l"
echo ""
echo "To edit cron jobs:"
echo "  crontab -e"
echo ""
echo "To run manually:"
echo "  python3 monitor/health_monitor.py"
echo ""
echo "To view logs:"
echo "  tail -f monitor/logs/health.log"
echo ""
echo "To remove the cron job:"
echo "  crontab -e  # Then delete the line with health_monitor.py"
echo ""
echo "Next steps:"
echo "  1. Set ALERT_EMAIL environment variable (optional):"
echo "     export ALERT_EMAIL=\"your-email@example.com\""
echo "  2. Run: python3 monitor/status_dashboard.py"
echo "  3. Wait 5 minutes for first health check"
echo ""
