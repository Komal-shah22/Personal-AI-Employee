#!/bin/bash

# Cron Job Setup for Personal AI Employee (Linux/Mac)

echo "=========================================="
echo "Setting up Cron Jobs for AI Employee"
echo "=========================================="
echo ""

# Get current directory
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Project directory: $PROJECT_DIR"
echo ""

# Create temporary cron file
TEMP_CRON=$(mktemp)

# Get existing crontab (if any)
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Add AI Employee cron jobs
echo "" >> "$TEMP_CRON"
echo "# Personal AI Employee - Automated Tasks" >> "$TEMP_CRON"
echo "" >> "$TEMP_CRON"

# Every 5 minutes: check Needs_Action
echo "*/5 * * * * cd $PROJECT_DIR && python orchestrator.py --check-once >> AI_Employee_Vault/Logs/cron.log 2>&1" >> "$TEMP_CRON"

# Every day 8:00 AM: morning dashboard update
echo "0 8 * * * cd $PROJECT_DIR && claude -p 'Update Dashboard.md with today summary. Read all /Logs/ from yesterday.' >> AI_Employee_Vault/Logs/cron.log 2>&1" >> "$TEMP_CRON"

# Every Sunday 10:00 PM: generate CEO briefing
echo "0 22 * * 0 cd $PROJECT_DIR && python scripts/generate_ceo_briefing.py >> AI_Employee_Vault/Logs/cron.log 2>&1" >> "$TEMP_CRON"

# Every Monday 8:00 AM: notify briefing ready
echo "0 8 * * 1 cd $PROJECT_DIR && python scripts/notify_briefing.py >> AI_Employee_Vault/Logs/cron.log 2>&1" >> "$TEMP_CRON"

echo "" >> "$TEMP_CRON"

# Install new crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "[OK] Cron jobs installed successfully!"
echo ""
echo "Current crontab:"
crontab -l | grep -A 10 "Personal AI Employee"
echo ""
echo "=========================================="
echo "Cron jobs are now active!"
echo "=========================================="
echo ""
echo "Logs will be written to: AI_Employee_Vault/Logs/cron.log"
echo ""
echo "To view cron jobs: crontab -l"
echo "To edit cron jobs: crontab -e"
echo "To remove AI Employee cron jobs:"
echo "  crontab -l | grep -v 'Personal AI Employee' | grep -v 'orchestrator.py' | grep -v 'generate_ceo_briefing' | crontab -"
echo ""
