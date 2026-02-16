# CEO Briefing Generator - Usage Guide

## Overview

The CEO Briefing Generator automatically collects data from your AI Employee Vault and generates a comprehensive Monday Morning CEO Briefing using Claude.

## What It Does

### Data Collection

The script collects data from multiple sources:

1. **Business Goals** (`AI_Employee_Vault/Business_Goals.md`)
   - Revenue targets
   - Strategic goals

2. **Completed Tasks** (`AI_Employee_Vault/Done/`)
   - Tasks completed in last 7 days
   - Breakdown by type (email, invoice, social, etc.)

3. **Financial Data** (`AI_Employee_Vault/Accounting/Current_Month.md`)
   - Current revenue
   - Expenses
   - Profit

4. **Activity Logs** (`AI_Employee_Vault/Logs/*.json`)
   - Total actions in last 7 days
   - Error count
   - Bottlenecks (top 3 activities)

5. **Overdue Approvals** (`AI_Employee_Vault/Pending_Approval/`)
   - Items waiting >24 hours

### Output

1. **Data Snapshot**: `AI_Employee_Vault/Plans/briefing_data_[date].json`
2. **CEO Briefing**: `AI_Employee_Vault/Briefings/[YYYY-MM-DD]_Monday_Briefing.md`
3. **Updated Dashboard**: `Dashboard.md` with "Last Briefing" section
4. **Desktop Notification**: "Monday Briefing Ready — check Obsidian"

## Usage

### Manual Execution

```bash
# Run the generator
python scripts/generate_ceo_briefing.py

# Or make it executable and run directly
chmod +x scripts/generate_ceo_briefing.py
./scripts/generate_ceo_briefing.py
```

### Scheduled Execution (Recommended)

**Mac/Linux (cron):**
```bash
# Add to crontab (Sunday 10 PM)
0 22 * * 0 cd /path/to/Personal_AI_Employee && python scripts/generate_ceo_briefing.py >> AI_Employee_Vault/Logs/ceo_briefing.log 2>&1
```

**Windows (Task Scheduler):**
```powershell
# Create scheduled task
$Action = New-ScheduledTaskAction -Execute "python" -Argument "scripts\generate_ceo_briefing.py" -WorkingDirectory "E:\hackathon-0\Personal_AI_Employee"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "22:00"
Register-ScheduledTask -TaskName "AI_Employee_CEO_Briefing" -Action $Action -Trigger $Trigger
```

### Via Setup Scripts

The scheduler setup scripts automatically include this:

```bash
# Mac/Linux
./scripts/setup_scheduler.sh

# Windows
.\scripts\setup_scheduler.ps1
```

## Requirements

### Python Packages

All standard library - no additional packages needed:
- `json`
- `subprocess`
- `pathlib`
- `datetime`
- `re`

### External Dependencies

1. **Claude CLI** (required)
   ```bash
   npm install -g @anthropic-ai/claude-cli
   ```

2. **CEO Briefing Skill** (required)
   - Must exist at: `.claude/skills/ceo_briefing_skill.md`

### Vault Structure

Required directories:
```
AI_Employee_Vault/
├── Business_Goals.md          # Optional but recommended
├── Done/                       # Required
├── Accounting/
│   └── Current_Month.md       # Optional
├── Logs/                       # Optional (*.json files)
├── Pending_Approval/          # Optional
├── Briefings/                 # Created automatically
└── Plans/                     # Created automatically
```

## Configuration

### Lookback Period

Edit `scripts/generate_ceo_briefing.py`:

```python
# Default: 7 days
DAYS_LOOKBACK = 7

# Change to 14 days
DAYS_LOOKBACK = 14
```

### Overdue Threshold

```python
# Default: 24 hours
OVERDUE_HOURS = 24

# Change to 48 hours
OVERDUE_HOURS = 48
```

### Output Location

```python
# Default: AI_Employee_Vault/Briefings/
BRIEFINGS_DIR = VAULT_DIR / 'Briefings'

# Change to different location
BRIEFINGS_DIR = Path('Reports/CEO_Briefings')
```

## Example Output

### Data Snapshot (JSON)

```json
{
  "generated_at": "2026-02-16T22:00:00",
  "business_goals": {
    "revenue_target": "$100K",
    "strategic_goals": [
      "Increase customer retention by 20%",
      "Launch new product line Q2",
      "Expand to 3 new markets"
    ]
  },
  "completed_tasks": {
    "count": 47,
    "by_type": {
      "email": 23,
      "invoice": 12,
      "social": 8,
      "approval": 4
    }
  },
  "financial": {
    "current_revenue": "87,500",
    "expenses": "45,200",
    "profit": "42,300"
  },
  "activity": {
    "total_actions": 156,
    "errors": 3,
    "bottlenecks": [
      {"type": "email_send", "count": 45},
      {"type": "invoice_generate", "count": 23},
      {"type": "approval_request", "count": 18}
    ]
  },
  "overdue_approvals": {
    "overdue_count": 2,
    "overdue_items": [
      {
        "name": "APPROVAL_payment_20260215.md",
        "hours_overdue": 36.5
      }
    ]
  }
}
```

### CEO Briefing (Markdown)

```markdown
# Monday Morning CEO Briefing
## February 17, 2026

**Generated**: 2026-02-16 22:00:00

## Executive Summary

Strong week with 47 tasks completed and revenue at $87.5K (87.5% of target).
Two approval items require attention. Email processing remains the primary
bottleneck with 45 actions this week.

## Key Metrics

- **Tasks Completed**: 47 (↑ 12% vs last week)
- **Revenue**: $87,500 / $100,000 target (87.5%)
- **Profit**: $42,300 (48% margin)
- **System Errors**: 3 (↓ 2 vs last week)

## Wins This Week

1. **Email Processing**: 23 emails handled automatically
2. **Invoice Generation**: 12 invoices created and sent
3. **Social Media**: 8 posts published on schedule
4. **Approvals**: 4 items approved and executed

## Challenges & Bottlenecks

1. **Email Volume**: 45 email actions (primary bottleneck)
   - Consider automation improvements
   - Review email templates

2. **Overdue Approvals**: 2 items waiting >24 hours
   - Payment approval (36.5 hours overdue)
   - Review approval workflow

3. **System Errors**: 3 errors this week
   - Monitor for patterns
   - Review error logs

## Action Items for Next Week

- [ ] Review and approve 2 overdue items
- [ ] Optimize email processing workflow
- [ ] Investigate system errors
- [ ] Continue progress toward $100K revenue target

## Financial Snapshot

| Metric | Amount | % of Target |
|--------|--------|-------------|
| Revenue | $87,500 | 87.5% |
| Expenses | $45,200 | - |
| Profit | $42,300 | 48% margin |

---

*Auto-generated by AI Employee System*
*Data collected: 2026-02-16 22:00:00*
```

## Troubleshooting

### Script Fails: "Claude CLI not found"

**Solution:**
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-cli

# Verify installation
claude --version
```

### Script Fails: "CEO briefing skill not found"

**Solution:**
```bash
# Check if skill exists
ls -la .claude/skills/ceo_briefing_skill.md

# If missing, create it or check path
```

### No Data Collected

**Symptoms**: JSON file shows empty data

**Causes:**
- Vault directories don't exist
- No files in Done/ folder
- Files are older than 7 days

**Solution:**
```bash
# Check vault structure
ls -la AI_Employee_Vault/

# Check Done folder
ls -la AI_Employee_Vault/Done/

# Check file dates
find AI_Employee_Vault/Done/ -name "*.md" -mtime -7
```

### Briefing Not Generated

**Symptoms**: Script completes but no briefing file

**Causes:**
- Claude CLI failed
- Insufficient API credits
- Network issues

**Solution:**
```bash
# Test Claude CLI manually
claude -p "Test message"

# Check Claude API status
# Review script output for errors

# Run with verbose output
python scripts/generate_ceo_briefing.py 2>&1 | tee briefing_debug.log
```

### Desktop Notification Not Showing

**Symptoms**: Script completes but no notification

**Causes:**
- Platform not supported
- Notification permissions denied
- Notification service not running

**Solution:**
```bash
# Mac: Check notification permissions
# System Preferences → Notifications

# Linux: Check notify-send
notify-send "Test" "Test message"

# Windows: Check notification settings
# Settings → System → Notifications
```

## Testing

### Test Data Collection

```bash
# Run script and check JSON output
python scripts/generate_ceo_briefing.py

# View collected data
cat AI_Employee_Vault/Plans/briefing_data_*.json | jq
```

### Test with Sample Data

```bash
# Create sample business goals
cat > AI_Employee_Vault/Business_Goals.md << 'EOF'
# Business Goals 2026

## Revenue Target
$100,000 per month

## Strategic Goals
- Increase customer retention by 20%
- Launch new product line Q2
- Expand to 3 new markets
EOF

# Create sample completed tasks
for i in {1..10}; do
  echo "Task $i completed" > AI_Employee_Vault/Done/TEST_task_$i.md
  touch -t $(date -d "3 days ago" +%Y%m%d%H%M) AI_Employee_Vault/Done/TEST_task_$i.md
done

# Run generator
python scripts/generate_ceo_briefing.py
```

### Test Notification

```bash
# Test notification function separately
python3 << 'EOF'
import subprocess
import sys

title = "Test Notification"
message = "This is a test"

if sys.platform == 'darwin':
    subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
elif sys.platform == 'linux':
    subprocess.run(['notify-send', title, message])
elif sys.platform == 'win32':
    print("Windows notification test - check Task Manager for toast")
EOF
```

## Integration

### With Orchestrator

The briefing generator works alongside the orchestrator:

```bash
# Orchestrator processes daily tasks
python orchestrator.py &

# Briefing generator runs weekly (Sunday night)
# Scheduled via cron/Task Scheduler
```

### With Dashboard

The generator automatically updates `Dashboard.md`:

```markdown
## Last Briefing

- **Generated**: 2026-02-16 22:00:00
- **File**: `AI_Employee_Vault/Briefings/2026-02-17_Monday_Briefing.md`
- **Status**: ✓ Ready for review

[Open Briefing](AI_Employee_Vault/Briefings/2026-02-17_Monday_Briefing.md)
```

### With Obsidian

If using Obsidian for your vault:

1. Briefing appears in `Briefings/` folder
2. Desktop notification alerts you
3. Click notification to open Obsidian
4. Review briefing in Obsidian

## Customization

### Custom Data Sources

Add new data collection functions:

```python
def collect_customer_data() -> Dict[str, Any]:
    """Collect customer metrics"""
    customers = {
        'total': 0,
        'new_this_week': 0,
        'churn_rate': 0
    }

    # Your collection logic here

    return customers

# Add to main data dict
data['customers'] = collect_customer_data()
```

### Custom Briefing Format

Modify the Claude prompt in `generate_briefing_with_claude()`:

```python
prompt = f"""Generate a CEO briefing with these sections:

1. Executive Summary
2. Revenue Analysis
3. Customer Metrics
4. Operational Highlights
5. Strategic Initiatives
6. Action Items

Use this data: {data_json}
"""
```

### Custom Notification

Modify `send_desktop_notification()`:

```python
# Add email notification
import smtplib
from email.message import EmailMessage

def send_email_notification(briefing_file: Path):
    msg = EmailMessage()
    msg['Subject'] = 'Monday Briefing Ready'
    msg['From'] = 'ai-employee@company.com'
    msg['To'] = 'ceo@company.com'
    msg.set_content(f'Briefing generated: {briefing_file}')

    # Send via SMTP
    # ...
```

## Best Practices

1. **Run Weekly**: Schedule for Sunday night (10 PM) so briefing is ready Monday morning
2. **Review Data**: Check JSON snapshot before reviewing briefing
3. **Keep Vault Clean**: Archive old files to keep data collection fast
4. **Monitor Logs**: Check `ceo_briefing.log` for issues
5. **Update Goals**: Keep `Business_Goals.md` current

## Performance

- **Execution Time**: 30-60 seconds (depends on Claude API)
- **Data Collection**: <5 seconds
- **Claude Generation**: 20-40 seconds
- **File I/O**: <1 second

## Security

- **API Keys**: Claude CLI uses your configured API key
- **Data Privacy**: All data stays local (except Claude API call)
- **File Permissions**: Briefings are readable by owner only

---

**Last Updated**: 2026-02-16

**Version**: 1.0.0

**Dependencies**: Python 3.6+, Claude CLI
