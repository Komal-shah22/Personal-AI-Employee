#!/usr/bin/env python3
"""
CEO Briefing Generator

Collects data from the AI Employee Vault and generates a comprehensive
Monday Morning CEO Briefing using Claude and the ceo_briefing_skill.

Designed to run via cron every Sunday at 10 PM:
    0 22 * * 0 python scripts/generate_ceo_briefing.py

Data Sources:
- Business_Goals.md: Revenue targets and strategic goals
- Done/: Completed tasks from last 7 days
- Accounting/Current_Month.md: Financial performance
- Logs/*.json: Activity logs and bottlenecks
- Pending_Approval/: Overdue approval requests

Output:
- Briefings/[YYYY-MM-DD]_Monday_Briefing.md
- Plans/briefing_data_[date].json (data snapshot)
- Updated Dashboard.md
- Desktop notification
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
import re

# Configuration
VAULT_DIR = Path('AI_Employee_Vault')
BUSINESS_GOALS_FILE = VAULT_DIR / 'Business_Goals.md'
DONE_DIR = VAULT_DIR / 'Done'
ACCOUNTING_DIR = VAULT_DIR / 'Accounting'
LOGS_DIR = VAULT_DIR / 'Logs'
PENDING_APPROVAL_DIR = VAULT_DIR / 'Pending_Approval'
BRIEFINGS_DIR = VAULT_DIR / 'Briefings'
PLANS_DIR = VAULT_DIR / 'Plans'
DASHBOARD_FILE = Path('Dashboard.md')
CEO_BRIEFING_SKILL = Path('.claude/skills/ceo_briefing_skill.md')

# Lookback period
DAYS_LOOKBACK = 7
OVERDUE_HOURS = 24


def log(message: str, level: str = "INFO"):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def collect_business_goals() -> Dict[str, Any]:
    """Extract revenue targets and strategic goals from Business_Goals.md"""
    log("Collecting business goals...")

    goals = {
        'revenue_target': None,
        'strategic_goals': [],
        'file_exists': False
    }

    if not BUSINESS_GOALS_FILE.exists():
        log(f"Business goals file not found: {BUSINESS_GOALS_FILE}", "WARNING")
        return goals

    goals['file_exists'] = True

    try:
        content = BUSINESS_GOALS_FILE.read_text(encoding='utf-8')

        # Extract revenue target (look for patterns like "$100K", "$1M", "100000")
        revenue_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*[KMB]?',  # $100K, $1M
            r'revenue.*?(\d+(?:,\d{3})*)',  # revenue: 100,000
            r'target.*?(\d+(?:,\d{3})*)',   # target: 100,000
        ]

        for pattern in revenue_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                goals['revenue_target'] = match.group(0)
                break

        # Extract strategic goals (look for bullet points or numbered lists)
        goal_lines = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                # Remove bullet/number prefix
                goal = re.sub(r'^[-*•\d.]+\s*', '', line).strip()
                if goal and len(goal) > 10:  # Ignore very short lines
                    goal_lines.append(goal)

        goals['strategic_goals'] = goal_lines[:5]  # Top 5 goals

        log(f"Found revenue target: {goals['revenue_target']}")
        log(f"Found {len(goals['strategic_goals'])} strategic goals")

    except Exception as e:
        log(f"Error reading business goals: {e}", "ERROR")

    return goals


def collect_completed_tasks() -> Dict[str, Any]:
    """Scan Done/ for files modified in last 7 days"""
    log(f"Collecting completed tasks from last {DAYS_LOOKBACK} days...")

    tasks = {
        'count': 0,
        'by_type': {},
        'recent_files': []
    }

    if not DONE_DIR.exists():
        log(f"Done directory not found: {DONE_DIR}", "WARNING")
        return tasks

    cutoff_date = datetime.now() - timedelta(days=DAYS_LOOKBACK)

    try:
        for file_path in DONE_DIR.glob('*.md'):
            # Check modification time
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

            if mtime >= cutoff_date:
                tasks['count'] += 1
                tasks['recent_files'].append({
                    'name': file_path.name,
                    'modified': mtime.isoformat()
                })

                # Categorize by type (from filename prefix)
                file_type = 'other'
                if file_path.name.startswith('EMAIL_'):
                    file_type = 'email'
                elif file_path.name.startswith('INVOICE_'):
                    file_type = 'invoice'
                elif file_path.name.startswith('APPROVAL_'):
                    file_type = 'approval'
                elif file_path.name.startswith('SOCIAL_') or file_path.name.startswith('LINKEDIN_'):
                    file_type = 'social'
                elif file_path.name.startswith('WHATSAPP_'):
                    file_type = 'whatsapp'

                tasks['by_type'][file_type] = tasks['by_type'].get(file_type, 0) + 1

        log(f"Found {tasks['count']} completed tasks")
        log(f"Breakdown: {tasks['by_type']}")

    except Exception as e:
        log(f"Error collecting completed tasks: {e}", "ERROR")

    return tasks


def collect_financial_data() -> Dict[str, Any]:
    """Extract revenue figures from Accounting/Current_Month.md"""
    log("Collecting financial data...")

    financial = {
        'current_revenue': None,
        'expenses': None,
        'profit': None,
        'file_exists': False
    }

    current_month_file = ACCOUNTING_DIR / 'Current_Month.md'

    if not current_month_file.exists():
        log(f"Accounting file not found: {current_month_file}", "WARNING")
        return financial

    financial['file_exists'] = True

    try:
        content = current_month_file.read_text(encoding='utf-8')

        # Extract revenue (look for patterns)
        revenue_match = re.search(r'revenue.*?\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', content, re.IGNORECASE)
        if revenue_match:
            financial['current_revenue'] = revenue_match.group(1)

        # Extract expenses
        expenses_match = re.search(r'expenses?.*?\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', content, re.IGNORECASE)
        if expenses_match:
            financial['expenses'] = expenses_match.group(1)

        # Extract profit
        profit_match = re.search(r'profit.*?\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', content, re.IGNORECASE)
        if profit_match:
            financial['profit'] = profit_match.group(1)

        log(f"Revenue: {financial['current_revenue']}, Expenses: {financial['expenses']}, Profit: {financial['profit']}")

    except Exception as e:
        log(f"Error reading financial data: {e}", "ERROR")

    return financial


def collect_activity_logs() -> Dict[str, Any]:
    """Scan Logs/*.json files for last 7 days to identify bottlenecks"""
    log(f"Collecting activity logs from last {DAYS_LOOKBACK} days...")

    activity = {
        'total_actions': 0,
        'errors': 0,
        'bottlenecks': [],
        'top_activities': {}
    }

    if not LOGS_DIR.exists():
        log(f"Logs directory not found: {LOGS_DIR}", "WARNING")
        return activity

    cutoff_date = datetime.now() - timedelta(days=DAYS_LOOKBACK)

    try:
        # Look for JSON log files
        for file_path in LOGS_DIR.glob('*.json'):
            # Parse date from filename (YYYY-MM-DD.json)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.name)
            if not date_match:
                continue

            try:
                file_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
            except ValueError:
                continue

            if file_date < cutoff_date:
                continue

            # Parse JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)

                # Count actions
                if isinstance(log_data, list):
                    activity['total_actions'] += len(log_data)

                    for entry in log_data:
                        # Count errors
                        if isinstance(entry, dict):
                            if entry.get('level') == 'ERROR' or entry.get('status') == 'error':
                                activity['errors'] += 1

                            # Track activity types
                            action_type = entry.get('type') or entry.get('action') or 'unknown'
                            activity['top_activities'][action_type] = activity['top_activities'].get(action_type, 0) + 1

            except json.JSONDecodeError:
                log(f"Invalid JSON in {file_path.name}", "WARNING")
                continue

        # Identify bottlenecks (activities with high error rates or frequency)
        if activity['top_activities']:
            sorted_activities = sorted(activity['top_activities'].items(), key=lambda x: x[1], reverse=True)
            activity['bottlenecks'] = [
                {'type': act, 'count': count}
                for act, count in sorted_activities[:3]  # Top 3
            ]

        log(f"Total actions: {activity['total_actions']}, Errors: {activity['errors']}")
        log(f"Top activities: {activity['top_activities']}")

    except Exception as e:
        log(f"Error collecting activity logs: {e}", "ERROR")

    return activity


def collect_overdue_approvals() -> Dict[str, Any]:
    """Check Pending_Approval/ for items older than 24 hours"""
    log(f"Checking for overdue approvals (>{OVERDUE_HOURS}h)...")

    approvals = {
        'overdue_count': 0,
        'overdue_items': []
    }

    if not PENDING_APPROVAL_DIR.exists():
        log(f"Pending Approval directory not found: {PENDING_APPROVAL_DIR}", "WARNING")
        return approvals

    cutoff_time = datetime.now() - timedelta(hours=OVERDUE_HOURS)

    try:
        for file_path in PENDING_APPROVAL_DIR.glob('*.md'):
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

            if mtime < cutoff_time:
                hours_overdue = (datetime.now() - mtime).total_seconds() / 3600
                approvals['overdue_count'] += 1
                approvals['overdue_items'].append({
                    'name': file_path.name,
                    'hours_overdue': round(hours_overdue, 1),
                    'created': mtime.isoformat()
                })

        log(f"Found {approvals['overdue_count']} overdue approvals")

    except Exception as e:
        log(f"Error checking overdue approvals: {e}", "ERROR")

    return approvals


def save_briefing_data(data: Dict[str, Any]) -> Path:
    """Save collected data to JSON file"""
    log("Saving briefing data...")

    PLANS_DIR.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime('%Y-%m-%d')
    output_file = PLANS_DIR / f'briefing_data_{date_str}.json'

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        log(f"Data saved to: {output_file}")
        return output_file

    except Exception as e:
        log(f"Error saving briefing data: {e}", "ERROR")
        raise


def generate_briefing_with_claude(data: Dict[str, Any]) -> Path:
    """Call Claude CLI to generate the briefing"""
    log("Generating briefing with Claude...")

    # Check if Claude CLI is available
    try:
        subprocess.run(['claude', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        log("Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-cli", "ERROR")
        raise RuntimeError("Claude CLI not available")

    # Check if skill file exists
    if not CEO_BRIEFING_SKILL.exists():
        log(f"CEO briefing skill not found: {CEO_BRIEFING_SKILL}", "ERROR")
        raise FileNotFoundError(f"Skill file missing: {CEO_BRIEFING_SKILL}")

    # Prepare output path
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)

    # Next Monday's date
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # If today is Monday, target next Monday
    next_monday = today + timedelta(days=days_until_monday)
    date_str = next_monday.strftime('%Y-%m-%d')

    output_file = BRIEFINGS_DIR / f'{date_str}_Monday_Briefing.md'

    # Build prompt
    data_json = json.dumps(data, indent=2)

    prompt = f"""Read .claude/skills/ceo_briefing_skill.md and generate a Monday Morning CEO Briefing.

Use this collected data:

```json
{data_json}
```

Key points to include:
- Week in review: {data['completed_tasks']['count']} tasks completed
- Financial performance: Revenue {data['financial']['current_revenue'] or 'N/A'}
- Bottlenecks: {len(data['activity']['bottlenecks'])} identified
- Overdue approvals: {data['overdue_approvals']['overdue_count']} items

Save the briefing to: {output_file}

Format as a professional executive briefing with:
1. Executive Summary (2-3 sentences)
2. Key Metrics
3. Wins This Week
4. Challenges & Bottlenecks
5. Action Items for Next Week
6. Financial Snapshot
"""

    log("Calling Claude CLI...")

    try:
        result = subprocess.run(
            ['claude', '-p', prompt],
            capture_output=True,
            text=True,
            check=True
        )

        log("Claude execution completed")
        log(f"Output: {result.stdout[:200]}...")  # First 200 chars

        # Verify output file was created
        if output_file.exists():
            log(f"Briefing generated: {output_file}")
            return output_file
        else:
            log("Warning: Claude completed but output file not found", "WARNING")
            log("Creating placeholder briefing...", "WARNING")

            # Create a basic briefing as fallback
            placeholder_content = f"""# Monday Morning CEO Briefing
## {next_monday.strftime('%B %d, %Y')}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This briefing was auto-generated but Claude did not create the full output.
Please review the data below and generate manually if needed.

## Data Collected

```json
{data_json}
```

## Next Steps

1. Review the collected data
2. Manually generate briefing if needed
3. Check Claude CLI configuration

---

*Auto-generated by generate_ceo_briefing.py*
"""
            output_file.write_text(placeholder_content, encoding='utf-8')
            return output_file

    except subprocess.CalledProcessError as e:
        log(f"Claude execution failed: {e}", "ERROR")
        log(f"Stderr: {e.stderr}", "ERROR")
        raise


def update_dashboard(briefing_file: Path):
    """Update Dashboard.md with last briefing info"""
    log("Updating Dashboard.md...")

    if not DASHBOARD_FILE.exists():
        log(f"Dashboard file not found: {DASHBOARD_FILE}", "WARNING")
        return

    try:
        content = DASHBOARD_FILE.read_text(encoding='utf-8')

        # Prepare update text
        update_text = f"""## Last Briefing

- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **File**: `{briefing_file}`
- **Status**: ✓ Ready for review

[Open Briefing]({briefing_file})
"""

        # Try to find and replace existing "Last Briefing" section
        if '## Last Briefing' in content:
            # Replace existing section (up to next ## or end of file)
            pattern = r'## Last Briefing.*?(?=\n##|\Z)'
            content = re.sub(pattern, update_text.strip(), content, flags=re.DOTALL)
        else:
            # Append to end
            content += f"\n\n{update_text}"

        DASHBOARD_FILE.write_text(content, encoding='utf-8')
        log("Dashboard updated successfully")

    except Exception as e:
        log(f"Error updating dashboard: {e}", "ERROR")


def send_desktop_notification(briefing_file: Path):
    """Send desktop notification that briefing is ready"""
    log("Sending desktop notification...")

    title = "Monday Briefing Ready"
    message = f"CEO briefing generated: {briefing_file.name}\nCheck Obsidian vault"

    try:
        # Detect platform and send notification
        if sys.platform == 'darwin':  # macOS
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=True)
            log("Notification sent (macOS)")

        elif sys.platform == 'linux':  # Linux
            subprocess.run(['notify-send', title, message], check=True)
            log("Notification sent (Linux)")

        elif sys.platform == 'win32':  # Windows
            # Use PowerShell for Windows toast notification
            ps_script = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

            $template = @"
            <toast>
                <visual>
                    <binding template="ToastText02">
                        <text id="1">{title}</text>
                        <text id="2">{message}</text>
                    </binding>
                </visual>
            </toast>
"@

            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AI Employee").Show($toast)
            """
            subprocess.run(['powershell', '-Command', ps_script], check=True)
            log("Notification sent (Windows)")

        else:
            log(f"Desktop notifications not supported on {sys.platform}", "WARNING")

    except Exception as e:
        log(f"Error sending notification: {e}", "WARNING")
        # Don't fail the whole script if notification fails


def main():
    """Main execution flow"""
    log("=" * 60)
    log("CEO BRIEFING GENERATOR - STARTING")
    log("=" * 60)

    try:
        # Step 1: Collect all data
        log("\n--- STEP 1: DATA COLLECTION ---")

        data = {
            'generated_at': datetime.now().isoformat(),
            'business_goals': collect_business_goals(),
            'completed_tasks': collect_completed_tasks(),
            'financial': collect_financial_data(),
            'activity': collect_activity_logs(),
            'overdue_approvals': collect_overdue_approvals()
        }

        # Step 2: Save data snapshot
        log("\n--- STEP 2: SAVE DATA SNAPSHOT ---")
        data_file = save_briefing_data(data)

        # Step 3: Generate briefing with Claude
        log("\n--- STEP 3: GENERATE BRIEFING ---")
        briefing_file = generate_briefing_with_claude(data)

        # Step 4: Update dashboard
        log("\n--- STEP 4: UPDATE DASHBOARD ---")
        update_dashboard(briefing_file)

        # Step 5: Send notification
        log("\n--- STEP 5: SEND NOTIFICATION ---")
        send_desktop_notification(briefing_file)

        # Success!
        log("\n" + "=" * 60)
        log("✓ CEO BRIEFING GENERATION COMPLETE")
        log("=" * 60)
        log(f"Briefing: {briefing_file}")
        log(f"Data: {data_file}")

        return 0

    except Exception as e:
        log("\n" + "=" * 60)
        log(f"✗ BRIEFING GENERATION FAILED: {e}", "ERROR")
        log("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
