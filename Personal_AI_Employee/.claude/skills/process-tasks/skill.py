"""
Claude Code Agent Skill: process-tasks
Processes pending tasks from Needs_Action folder and creates execution plans
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

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

def create_task_plan(original_file: Path, handbook_rules: Dict[str, Any]) -> Path:
    """Create a detailed plan for a task based on the original file."""
    content = original_file.read_text(encoding='utf-8')
    frontmatter, body = load_yaml_frontmatter(content)

    # Extract information from the original file
    task_id = original_file.stem
    priority = frontmatter.get('priority', 'medium')
    task_type = frontmatter.get('type', 'general')

    # Create descriptive name from subject or first line
    subject = frontmatter.get('subject', '')
    if not subject and body:
        subject = body.split('\n')[0].replace('#', '').strip()[:100]
    if not subject:
        subject = f"Task from {task_id}"

    # Analyze the content to understand what needs to be done
    analysis = f"The task is of type '{task_type}' with priority '{priority}'. "
    if body:
        analysis += f"It contains the following content: {body[:200]}..."

    # Generate action steps based on task type and priority
    action_steps = generate_action_steps(task_type, priority, body, handbook_rules)

    # Create the plan content
    plan_content = f"""---
task_id: {task_id}
source_file: {str(original_file)}
created: {datetime.now().isoformat()}
priority: {priority}
status: planned
---

# Task: {subject}

## Objective
Process and complete the requested task based on the information provided in the original file.

## Analysis
{analysis}

## Action Steps
{chr(10).join(action_steps)}

## Success Criteria
The task is considered complete when all action steps have been executed and documented.

## Notes
Refer to the Company_Handbook.md for additional rules and procedures when executing this task.
"""

    # Create the plan file
    plan_filename = f"PLAN_{task_id}.md"
    plan_path = Path("Plans") / plan_filename
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan_content)

    return plan_path

def generate_action_steps(task_type: str, priority: str, content: str, handbook_rules: Dict[str, Any]) -> List[str]:
    """Generate appropriate action steps based on task type and priority."""
    steps = []

    # Generic steps that apply to most tasks
    steps.append("- [ ] Review the original request in detail")
    steps.append("- [ ] Determine the appropriate priority level based on Company_Handbook.md")

    # Add type-specific steps
    if task_type == 'email':
        steps.extend([
            "- [ ] Draft a response following communication guidelines",
            "- [ ] Check for approval requirements based on content",
            "- [ ] Send response or escalate as needed"
        ])
    elif task_type == 'file_drop':
        steps.extend([
            "- [ ] Review the dropped file content",
            "- [ ] Determine appropriate action based on file type and content",
            "- [ ] Process file according to Company_Handbook.md procedures"
        ])
    elif task_type == 'payment':
        steps.extend([
            "- [ ] Verify payment details and recipient",
            "- [ ] Check approval requirements based on amount",
            "- [ ] Process payment or escalate for approval"
        ])
    else:
        steps.append("- [ ] Analyze the request and determine appropriate action steps")

    # Add priority-specific steps
    if priority == 'high':
        steps.insert(1, "- [ ] Prioritize this task based on high priority status")
        steps.append("- [ ] Escalate to human operator if needed")
    elif priority == 'critical':
        steps.insert(1, "- [ ] Handle immediately as critical priority task")
        steps.append("- [ ] Notify human operator of critical task")

    # Add finalization step
    steps.append("- [ ] Document completion and update status")

    return steps

def update_dashboard(processed_tasks: List[Dict[str, Any]]) -> None:
    """Update the Dashboard.md file with current status."""
    dashboard_path = Path("Dashboard.md")

    if dashboard_path.exists():
        content = dashboard_path.read_text(encoding='utf-8')
    else:
        content = "# Personal AI Employee Dashboard\n\n## Executive Summary\n- **Status**: Operational\n- **Last Update**: {{date}}\n- **Active Tasks**: 0\n- **Pending Approval**: 0\n\n## Recent Activity\n- [No recent activity]\n\n## System Status\n- **Watchers Running**: 0\n- **Last Backup**: Never\n"

    # Count pending tasks
    needs_action_dir = Path("Needs_Action")
    pending_count = len(list(needs_action_dir.glob("*.md")))

    # Find high-priority items
    high_priority_items = []
    for task in processed_tasks:
        if task.get('priority') in ['high', 'critical']:
            high_priority_items.append(task['filename'])

    # Update the content
    lines = content.split('\n')
    updated_lines = []

    for line in lines:
        if line.startswith('- **Active Tasks**:'):
            updated_lines.append(f'- **Active Tasks**: {pending_count}')
        elif line.startswith('- **Last Update**:'):
            updated_lines.append(f'- **Last Update**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}')
        else:
            updated_lines.append(line)

    # Add recent activity section if it exists
    activity_section_found = False
    final_lines = []
    for i, line in enumerate(updated_lines):
        final_lines.append(line)
        if "## Recent Activity" in line:
            # Add the new activity entry after the header
            final_lines.append(f"- [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processed {len(processed_tasks)} tasks from Needs_Action")
            activity_section_found = True
            # Skip the next line if it's a placeholder
            if i + 1 < len(updated_lines) and '[No recent activity]' in updated_lines[i + 1]:
                continue

    if not activity_section_found:
        # If no recent activity section was found, add it
        final_lines.extend(["", "## Recent Activity", f"- [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processed {len(processed_tasks)} tasks from Needs_Action"])

    # Add high priority items section if any exist
    if high_priority_items:
        # Check if high priority section already exists
        high_priority_section_exists = any("## High Priority Items" in line for line in final_lines)

        if not high_priority_section_exists:
            # Find a good place to insert the high priority section
            insert_index = len(final_lines)
            for i, line in enumerate(final_lines):
                if "## Recent Activity" in line:
                    insert_index = i + 3  # Insert after recent activity
                    break

            high_priority_section = ["", "## High Priority Items"]
            for item in high_priority_items:
                high_priority_section.append(f"- {item}")

            final_lines[insert_index:insert_index] = high_priority_section

    updated_content = '\n'.join(final_lines)

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def log_activity(processed_tasks: List[Dict[str, Any]], error_count: int = 0) -> None:
    """Log the activity in the appropriate log file."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = Path("Logs")
    log_dir.mkdir(exist_ok=True)

    log_path = log_dir / f"{today}.txt"

    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] process-tasks skill executed: "
    log_entry += f"processed {len(processed_tasks)} tasks"
    if error_count > 0:
        log_entry += f", encountered {error_count} errors"

    log_entry += "\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def ensure_handbook_exists() -> Dict[str, Any]:
    """Create a basic Company_Handbook.md if it doesn't exist."""
    handbook_path = Path("Company_Handbook.md")

    if not handbook_path.exists():
        handbook_content = """# Company Handbook

## Rules of Engagement

### Communication Guidelines
- Always be polite and professional
- Flag any payment requests over $500 for approval
- Respond to urgent items within 24 hours

### Business Operations
- Prioritize client communication
- Follow approval processes for sensitive actions

### Priority Levels
1. **Critical**: Immediate attention required
2. **High**: Within 24 hours
3. **Medium**: Within 1 week
4. **Low**: As time permits
"""
        with open(handbook_path, 'w', encoding='utf-8') as f:
            f.write(handbook_content)

    # Read and return handbook content (simplified for this skill)
    return {"exists": True}

def run_skill():
    """
    Main function for the process-tasks skill
    """
    print("Starting process-tasks skill...")

    # 1. Read the Company_Handbook.md file
    handbook_rules = ensure_handbook_exists()
    print("Company handbook verified.")

    # 2. Scan the /Needs_Action folder for all .md files
    needs_action_dir = Path("Needs_Action")
    if not needs_action_dir.exists():
        print("No Needs_Action directory found. Creating it...")
        needs_action_dir.mkdir(parents=True, exist_ok=True)

    task_files = list(needs_action_dir.glob("*.md"))

    if not task_files:
        print("No pending tasks found")
        return {"status": "success", "message": "No pending tasks found", "processed_count": 0}

    print(f"Found {len(task_files)} pending tasks to process.")

    processed_tasks = []
    error_count = 0

    # 3. Process each file
    for task_file in task_files:
        try:
            print(f"Processing: {task_file.name}")

            # Create a plan for the task
            plan_path = create_task_plan(task_file, handbook_rules)

            # Get priority from the original file
            content = task_file.read_text(encoding='utf-8')
            frontmatter, _ = load_yaml_frontmatter(content)
            priority = frontmatter.get('priority', 'medium')

            processed_tasks.append({
                "filename": task_file.name,
                "plan_path": str(plan_path),
                "priority": priority
            })

            print(f"Created plan: {plan_path.name}")

        except Exception as e:
            print(f"Error processing {task_file.name}: {str(e)}")
            error_count += 1
            continue

    # 4. Update the Dashboard.md file
    try:
        update_dashboard(processed_tasks)
        print("Dashboard updated successfully.")
    except Exception as e:
        print(f"Error updating dashboard: {str(e)}")
        error_count += 1

    # 5. Log the activity
    try:
        log_activity(processed_tasks, error_count)
        print("Activity logged successfully.")
    except Exception as e:
        print(f"Error logging activity: {str(e)}")

    # Prepare result
    result_message = f"Processed {len(processed_tasks)} tasks"
    if error_count > 0:
        result_message += f" with {error_count} errors"

    result = {
        "status": "success",
        "message": result_message,
        "processed_count": len(processed_tasks),
        "error_count": error_count
    }

    print(result_message)
    return result

if __name__ == "__main__":
    result = run_skill()
    print(f"\nSkill execution completed: {result}")