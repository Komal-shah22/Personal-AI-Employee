#!/bin/bash

# AI Employee Scheduler Setup Script (Mac/Linux)
# This script sets up cron jobs to automate the AI Employee system

set -e

echo "=========================================="
echo "AI EMPLOYEE - SCHEDULER SETUP"
echo "=========================================="
echo ""

# Get the project directory (parent of scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "Detected project directory: $PROJECT_DIR"
echo ""
echo "This script will set up the following cron jobs:"
echo ""
echo "1. Every 5 minutes: Check Needs_Action folder"
echo "   */5 * * * * cd $PROJECT_DIR && python orchestrator.py --check-once"
echo ""
echo "2. Every day at 8:00 AM: Morning dashboard update"
echo "   0 8 * * * cd $PROJECT_DIR && claude -p \"Update Dashboard.md with today's summary\""
echo ""
echo "3. Every Sunday at 10:00 PM: Generate CEO briefing"
echo "   0 22 * * 0 cd $PROJECT_DIR && claude -p \"Generate this week's CEO briefing\""
echo ""
echo "4. Every Monday at 8:00 AM: Daily briefing notification"
echo "   0 8 * * 1 cd $PROJECT_DIR && python scripts/notify_briefing.py"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found. Please install Python first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

# Check if Claude CLI is available
if ! command -v claude &> /dev/null; then
    echo "WARNING: Claude CLI not found. Some jobs may fail."
    echo "Install with: npm install -g @anthropic-ai/claude-cli"
    echo ""
fi

# Ask for confirmation
read -p "Continue with setup? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Create temporary cron file
TEMP_CRON=$(mktemp)

# Get existing crontab (if any)
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Check if our jobs already exist
if grep -q "AI Employee - Orchestrator Check" "$TEMP_CRON"; then
    echo ""
    echo "WARNING: AI Employee cron jobs already exist."
    read -p "Remove existing jobs and reinstall? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Remove existing AI Employee jobs
        sed -i.bak '/# AI Employee/d' "$TEMP_CRON"
        sed -i.bak '/orchestrator.py/d' "$TEMP_CRON"
        sed -i.bak '/Dashboard.md/d' "$TEMP_CRON"
        sed -i.bak '/CEO.*[Bb]riefing/d' "$TEMP_CRON"
        sed -i.bak '/notify_briefing.py/d' "$TEMP_CRON"
        echo "Existing jobs removed."
    else
        echo "Setup cancelled."
        rm "$TEMP_CRON"
        exit 0
    fi
fi

# Add new cron jobs
cat >> "$TEMP_CRON" << EOF

# AI Employee - Orchestrator Check (every 5 minutes)
*/5 * * * * cd "$PROJECT_DIR" && $PYTHON_CMD orchestrator.py --check-once >> "$PROJECT_DIR/AI_Employee_Vault/Logs/cron_orchestrator.log" 2>&1

# AI Employee - Morning Dashboard Update (daily 8 AM)
0 8 * * * cd "$PROJECT_DIR" && claude -p "Update Dashboard.md with today's summary. Read all /Logs/ from yesterday." >> "$PROJECT_DIR/AI_Employee_Vault/Logs/cron_dashboard.log" 2>&1

# AI Employee - CEO Briefing Generation (Sunday 10 PM)
0 22 * * 0 cd "$PROJECT_DIR" && $PYTHON_CMD "$PROJECT_DIR/scripts/generate_ceo_briefing.py" >> "$PROJECT_DIR/AI_Employee_Vault/Logs/cron_briefing.log" 2>&1

# AI Employee - Briefing Notification (Monday 8 AM)
0 8 * * 1 cd "$PROJECT_DIR" && $PYTHON_CMD "$PROJECT_DIR/scripts/notify_briefing.py" >> "$PROJECT_DIR/AI_Employee_Vault/Logs/cron_notify.log" 2>&1

EOF

# Install new crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo ""
echo "=========================================="
echo "✓ CRON JOBS INSTALLED SUCCESSFULLY"
echo "=========================================="
echo ""
echo "Verify installation:"
echo "  crontab -l"
echo ""
echo "View logs:"
echo "  tail -f AI_Employee_Vault/Logs/cron_*.log"
echo ""
echo "Remove all AI Employee cron jobs:"
echo "  crontab -l | grep -v 'AI Employee' | crontab -"
echo ""
echo "Manual crontab edit:"
echo "  crontab -e"
echo ""
echo "Next steps:"
echo "1. Wait 5 minutes for first orchestrator check"
echo "2. Check logs to verify jobs are running"
echo "3. Adjust schedule if needed with: crontab -e"
echo ""
