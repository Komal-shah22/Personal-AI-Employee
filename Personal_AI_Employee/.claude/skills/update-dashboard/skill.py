"""
Claude Code Agent Skill: update-dashboard
Refreshes Dashboard.md with real-time statistics and activity
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import yaml

def load_yaml_frontmatter(content: str) -> tuple:
    """Extract YAML frontmatter from markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return frontmatter or {}, body
            except yaml.YAMLError:
                pass
    return {}, content.strip()

def get_relative_time(dt: datetime) -> str:
    """Convert datetime to relative time string."""
    now = datetime.now()
    diff = now - dt

    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "Just now"

def count_tasks_by_priority(directory: Path) -> Dict[str, List[Dict]]:
    """Count tasks by priority from markdown files in directory."""
    tasks_by_priority = {
        'high': [],
        'medium': [],
        'low': [],
        'critical': []
    }

    if not directory.exists():
        return tasks_by_priority

    for file_path in directory.glob("*.md"):
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, body = load_yaml_frontmatter(content)

            priority = frontmatter.get('priority', 'medium').lower()
            subject = frontmatter.get('subject', file_path.stem)

            # Get brief description from body
            description = body.replace('#', '').replace('*', '').split('\\n')[0][:100]
            if not description:
                description = "No description provided"

            task_info = {
                'name': subject,
                'description': description,
                'file_path': file_path,
                'timestamp': datetime.fromtimestamp(file_path.stat().st_mtime)
            }

            if priority in tasks_by_priority:
                tasks_by_priority[priority].append(task_info)
            else:
                tasks_by_priority['medium'].append(task_info)  # Default to medium

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return tasks_by_priority

def get_recent_logs(today_str: str) -> List[str]:
    """Get recent log entries from today's log file."""
    log_dir = Path("Logs")
    today_log = log_dir / f"{today_str}.txt"

    if not today_log.exists():
        return ["No activity logged yet"]

    try:
        lines = today_log.read_text(encoding='utf-8').strip().split('\n')
        # Take last 10 entries
        recent_entries = [line for line in lines if line.strip()][-10:]
        return recent_entries
    except Exception as e:
        print(f"Error reading log file: {e}")
        return ["Error reading activity log"]

def get_completed_today() -> List[Dict]:
    """Get tasks completed today from the Done folder."""
    done_dir = Path("Done")
    if not done_dir.exists():
        return []

    today = datetime.now().date()
    completed_today = []

    for file_path in done_dir.glob("*.md"):
        try:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mod_time.date() == today:
                content = file_path.read_text(encoding='utf-8')
                frontmatter, body = load_yaml_frontmatter(content)

                task_name = frontmatter.get('subject', file_path.stem)
                completed_today.append({
                    'name': task_name,
                    'file_path': file_path,
                    'completion_time': mod_time.strftime('%H:%M')
                })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Sort by modification time (most recent first)
    completed_today.sort(key=lambda x: x['completion_time'], reverse=True)
    return completed_today[:10]  # Limit to 10 most recent

def calculate_system_stats() -> Dict:
    """Calculate system statistics."""
    stats = {
        'pending_tasks': 0,
        'planned_tasks': 0,
        'completed_today': 0,
        'total_processed': 0,
        'system_status': '🟢 Active',
        'watchers_status': 'Active ✅',
        'last_task_processed': 'Never',
        'avg_response_time': 'N/A'
    }

    # Count pending tasks
    needs_action_dir = Path("Needs_Action")
    if needs_action_dir.exists():
        stats['pending_tasks'] = len(list(needs_action_dir.glob("*.md")))

    # Count planned tasks
    plans_dir = Path("Plans")
    if plans_dir.exists():
        stats['planned_tasks'] = len(list(plans_dir.glob("*.md")))

    # Count completed today
    completed_today_list = get_completed_today()
    stats['completed_today'] = len(completed_today_list)

    # Count total processed (all files in Done folder)
    done_dir = Path("Done")
    if done_dir.exists():
        stats['total_processed'] = len(list(done_dir.glob("*.md")))

    # Determine system status based on pending tasks
    if stats['pending_tasks'] > 10:
        stats['system_status'] = '🟡 Busy'
    elif stats['pending_tasks'] == 0:
        stats['system_status'] = '🟢 Active'
    else:
        stats['system_status'] = '🟢 Active'

    # Get last task processed time
    if done_dir.exists():
        done_files = list(done_dir.glob("*.md"))
        if done_files:
            latest_done = max(done_files, key=lambda f: f.stat().st_mtime)
            mod_time = datetime.fromtimestamp(latest_done.stat().st_mtime)
            stats['last_task_processed'] = f"{mod_time.strftime('%H:%M')} ({get_relative_time(mod_time)})"

    return stats

def generate_dashboard_content() -> str:
    """Generate the complete dashboard content."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # Calculate stats
    stats = calculate_system_stats()

    # Get high priority tasks
    tasks_by_priority = count_tasks_by_priority(Path("Needs_Action"))
    high_priority_tasks = tasks_by_priority.get('high', [])[:5]  # Limit to 5
    critical_tasks = tasks_by_priority.get('critical', [])[:5]
    all_high_priority = critical_tasks + high_priority_tasks  # Critical first

    # Get completed today
    completed_today = get_completed_today()

    # Get recent activity
    recent_activity = get_recent_logs(today_str)

    # Format dashboard
    dashboard_content = f"""# 🏠 AI Employee Dashboard

**Last Updated:** {now.isoformat()}
**System Status:** {stats['system_status']}

---

## 📊 Quick Stats

| Metric | Count |
|--------|-------|
| Pending Tasks | {stats['pending_tasks']} |
| In Progress | {stats['planned_tasks']} |
| Completed Today | {stats['completed_today']} |
| Total Processed | {stats['total_processed']} |

---

## 🔥 High Priority Tasks
"""

    if all_high_priority:
        for i, task in enumerate(all_high_priority, 1):
            priority_label = "🚨 Critical" if task in critical_tasks else "🔥 High"
            dashboard_content += f"{i}. **{task['name']}** - {task['description']}\n"
    else:
        dashboard_content += "*No high-priority tasks at the moment* ✅\n\n"

    dashboard_content += "---\n\n## ✅ Recently Completed\n"

    if completed_today:
        for task in completed_today:
            dashboard_content += f"- ✓ {task['name']} - {task['completion_time']}\n"
    else:
        dashboard_content += "*No tasks completed today yet*\n\n"

    dashboard_content += "---\n\n## 📋 Pending Tasks by Priority\n"

    # Add pending tasks by priority
    dashboard_content += f"\n### High Priority ({len(high_priority_tasks)})\n"
    if high_priority_tasks:
        for task in high_priority_tasks:
            dashboard_content += f"- {task['name']}\n"
    else:
        dashboard_content += "*None*\n"

    dashboard_content += f"\n### Medium Priority ({len(tasks_by_priority.get('medium', []))})\n"
    medium_tasks = tasks_by_priority.get('medium', [])
    if medium_tasks:
        for task in medium_tasks[:10]:  # Limit to 10
            dashboard_content += f"- {task['name']}\n"
    else:
        dashboard_content += "*None*\n"

    dashboard_content += f"\n### Low Priority ({len(tasks_by_priority.get('low', []))})\n"
    low_tasks = tasks_by_priority.get('low', [])
    if low_tasks:
        for task in low_tasks[:10]:  # Limit to 10
            dashboard_content += f"- {task['name']}\n"
    else:
        dashboard_content += "*None*\n"

    dashboard_content += f"\n---\n\n## 📝 Today's Activity Log\n"

    for entry in recent_activity:
        if entry.strip():
            dashboard_content += f"- {entry}\n"

    dashboard_content += f"\n---\n\n## 🎯 System Health\n\n"
    dashboard_content += f"- **Watchers:** {stats['watchers_status']}\n"
    dashboard_content += f"- **Last Task Processed:** {stats['last_task_processed']}\n"
    dashboard_content += f"- **Average Response Time:** {stats['avg_response_time']}\n\n"

    dashboard_content += "---\n\n*Dashboard automatically generated by AI Employee*\n"

    return dashboard_content

def ensure_directories_exist():
    """Ensure required directories exist."""
    dirs_to_create = ["Needs_Action", "Plans", "Done", "Logs", "Pending_Approval", "Approved", "Rejected", "Inbox"]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)

def run_skill():
    """
    Main function for the update-dashboard skill
    """
    print("Starting update-dashboard skill...")

    # Ensure required directories exist
    ensure_directories_exist()
    print("Verified directory structure.")

    # Generate dashboard content
    dashboard_content = generate_dashboard_content()
    print("Dashboard content generated.")

    # Write to Dashboard.md
    dashboard_path = Path("Dashboard.md")
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_content)

    print(f"Dashboard updated successfully at {dashboard_path}")

    # Prepare result
    result = {
        "status": "success",
        "message": "Dashboard updated with current system status",
        "dashboard_path": str(dashboard_path)
    }

    print("Dashboard update completed successfully.")
    return result

if __name__ == "__main__":
    result = run_skill()
    print(f"\nSkill execution completed: {result}")