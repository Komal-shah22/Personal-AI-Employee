#!/usr/bin/env python3
"""
Update the AI Employee Dashboard with current status
"""

import os
from datetime import datetime
from pathlib import Path

def count_md_files(directory):
    """Count markdown files in a directory"""
    if not os.path.exists(directory):
        return 0
    return len([f for f in os.listdir(directory) if f.lower().endswith('.md')])

def update_dashboard():
    # Define vault paths
    vault_path = "AI_Employee_Vault"
    needs_action_path = os.path.join(vault_path, "Needs_Action")
    in_progress_path = os.path.join(vault_path, "In_Progress")
    pending_approval_path = os.path.join(vault_path, "Pending_Approval")
    done_path = os.path.join(vault_path, "Done")
    plans_path = os.path.join(vault_path, "Plans")
    logs_path = os.path.join(vault_path, "Logs")

    # Count files in each directory
    pending_actions = count_md_files(needs_action_path)
    in_progress = count_md_files(in_progress_path)
    awaiting_approval = count_md_files(pending_approval_path)
    completed = count_md_files(done_path)

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
    print(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    update_dashboard()