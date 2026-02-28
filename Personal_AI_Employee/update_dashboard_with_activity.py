#!/usr/bin/env python3
"""
Update the AI Employee Dashboard with current status and recent activity
"""

import os
import json
from datetime import datetime
from pathlib import Path

def count_md_files(directory):
    """Count markdown files in a directory"""
    if not os.path.exists(directory):
        return 0
    return len([f for f in os.listdir(directory) if f.lower().endswith('.md')])

def get_recent_activity():
    """Get recent activity from log files"""
    vault_path = "AI_Employee_Vault"
    logs_path = os.path.join(vault_path, "Logs")

    # Get today's log file
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(logs_path, f"{today}.json")

    if not os.path.exists(log_file):
        # Check for other recent log files
        log_files = [f for f in os.listdir(logs_path) if f.endswith('.json') and f.startswith('2026-')]
        if log_files:
            # Get the most recent one
            log_files.sort(reverse=True)
            log_file = os.path.join(logs_path, log_files[0])
        else:
            return []

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        actions = data.get('actions', [])
        # Get most recent 5 actions
        recent_actions = []
        for action in reversed(actions[-5:]):  # Get last 5, reverse to show newest first
            timestamp = datetime.fromisoformat(action['timestamp'])
            recent_actions.append({
                'date': timestamp.strftime('%Y-%m-%d'),
                'time': timestamp.strftime('%H:%M'),
                'action': action.get('type', 'N/A'),
                'subject': action.get('subject', action.get('intent', 'N/A'))[:20]  # Limit description length
            })
        return recent_actions
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []

def update_dashboard():
    # Define vault paths
    vault_path = "AI_Employee_Vault"
    needs_action_path = os.path.join(vault_path, "Needs_Action")
    in_progress_path = os.path.join(vault_path, "In_Progress")
    pending_approval_path = os.path.join(vault_path, "Pending_Approval")
    done_path = os.path.join(vault_path, "Done")
    logs_path = os.path.join(vault_path, "Logs")

    # Count files in each directory
    pending_actions = count_md_files(needs_action_path)
    in_progress = count_md_files(in_progress_path)
    awaiting_approval = count_md_files(pending_approval_path)
    completed = count_md_files(done_path)

    # Get recent activity
    recent_activity = get_recent_activity()

    # Create dashboard content
    dashboard_content = f"""---
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# AI Employee Dashboard

## Current Status

- **Pending Actions**: {pending_actions}
- **In Progress**: {in_progress}
- **Awaiting Approval**: {awaiting_approval}

## Bank Summary

- **Current Balance**: PKR 0.00
- **Last Updated**: Not configured

## Recent Activity

| Date | Time | Action | Status | Details |
|------|------|--------|--------|---------|
"""

    # Add recent activity rows
    if recent_activity:
        for activity in recent_activity:
            dashboard_content += f"| {activity['date']} {activity['time']} | {activity['action']} | {activity['subject']} | ✅ Done | |\n"
    else:
        dashboard_content += "| - | - | - | - | No recent activity |\n"

    dashboard_content += """|------|------|--------|--------|---------|
| - | - | - | - | No recent activity |

## Upcoming Deadlines

| Date | Task | Priority | Status |
|------|------|----------|--------|
| - | - | - | No upcoming deadlines |

---
*Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Write the updated dashboard
    dashboard_file = os.path.join(vault_path, "Dashboard.md")
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(dashboard_content)

    print(f"Dashboard updated successfully!")
    print(f"Current status:")
    print(f"- Pending Actions: {pending_actions}")
    print(f"- In Progress: {in_progress}")
    print(f"- Awaiting Approval: {awaiting_approval}")
    print(f"- Completed: {completed}")
    print(f"Recent activities included: {len(recent_activity)}")
    print(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    update_dashboard()