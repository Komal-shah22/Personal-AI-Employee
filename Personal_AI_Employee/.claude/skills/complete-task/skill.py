"""
Claude Code Agent Skill: complete-task
Marks a task as completed and moves it to Done folder
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import yaml
import argparse
import re

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

def save_with_yaml_frontmatter(file_path: Path, frontmatter: dict, body: str):
    """Save content with YAML frontmatter."""
    content = "---\n" + yaml.dump(frontmatter, default_flow_style=False) + "---\n" + body
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def find_task_files(task_id: str) -> List[Tuple[Path, str]]:
    """Find all files related to a task across different directories."""
    directories = ["Needs_Action", "Plans", "Pending_Approval", "Approved", "Rejected", "Inbox", "Done"]
    found_files = []

    # Look for files that match the task_id pattern
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            continue

        # Look for exact match first
        for file_path in dir_path.glob("*.md"):
            if task_id.lower() in file_path.stem.lower():
                # Determine the type of file based on its directory
                file_type = directory
                found_files.append((file_path, file_type))

    return found_files

def extract_task_details(content: str, file_path: Path) -> Dict:
    """Extract task details from content."""
    frontmatter, body = load_yaml_frontmatter(content)

    details = {
        'subject': frontmatter.get('subject', file_path.stem),
        'description': body[:200],  # First 200 chars as description
        'priority': frontmatter.get('priority', 'medium'),
        'type': frontmatter.get('type', 'general'),
        'created_at': frontmatter.get('created', None),
        'steps': []
    }

    # Extract steps if they exist in the content
    lines = body.split('\n')
    for line in lines:
        if line.strip().startswith('- [') and '] ' in line:
            # Check if it's a completed or incomplete step
            if '- [x]' in line or '- [X]' in line:
                step = line.strip().replace('- [x]', '').replace('- [X]', '').strip()
                details['steps'].append({'step': step, 'completed': True})
            elif '- [ ]' in line:
                step = line.strip().replace('- [ ]', '').strip()
                details['steps'].append({'step': step, 'completed': False})

    return details

def calculate_duration(created_at: Optional[str]) -> str:
    """Calculate duration between creation and now."""
    if not created_at:
        return "N/A"

    try:
        # Parse the created_at timestamp
        if isinstance(created_at, str):
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            duration = datetime.now() - created_dt
            return str(duration)
        return "N/A"
    except:
        return "N/A"

def create_completion_summary(task_id: str, original_files: List[Tuple[Path, str]], details: Dict) -> str:
    """Create a completion summary for the task."""
    now = datetime.now()

    # Get the first file's details for summary
    if original_files:
        first_file_path, _ = original_files[0]
        original_content = first_file_path.read_text(encoding='utf-8')
        original_details = extract_task_details(original_content, first_file_path)
    else:
        original_details = details

    duration = calculate_duration(original_details.get('created_at'))

    # Format completed steps
    completed_steps = []
    for step_info in original_details.get('steps', []):
        if step_info['completed']:
            completed_steps.append(f"- ✓ {step_info['step']}")

    if not completed_steps:
        completed_steps.append("- ✓ Task completed")

    summary_content = f"""# ✅ Task Completion Summary

**Task:** {original_details['subject']}
**Completed:** {now.isoformat()}
**Duration:** {duration}

## Original Objective
{original_details['description']}

## Steps Taken
{'\\n'.join(completed_steps)}

## Outcome
Task has been successfully completed and archived.

## Notes
Task '{task_id}' was marked as completed by the AI Employee system.

---
*Task archived by AI Employee on {now.strftime('%Y-%m-%d')}*
"""

    return summary_content

def update_dashboard_with_completion(task_subject: str) -> bool:
    """Update the Dashboard.md file to reflect the completed task."""
    dashboard_path = Path("Dashboard.md")

    if not dashboard_path.exists():
        print(f"Dashboard.md not found at {dashboard_path}")
        return False

    try:
        content = dashboard_path.read_text(encoding='utf-8')

        # Update the completed today count in the quick stats table
        lines = content.split('\n')
        updated_lines = []

        for line in lines:
            if '| Completed Today |' in line:
                # Extract the current count and increment it
                match = re.search(r'\| Completed Today \| (\d+) \|', line)
                if match:
                    current_count = int(match.group(1))
                    new_count = current_count + 1
                    updated_line = line.replace(f'| {current_count} |', f'| {new_count} |')
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)
            elif '## ✅ Recently Completed' in line:
                updated_lines.append(line)
                # Add the new completion entry
                updated_lines.append(f"- ✓ {task_subject} - {datetime.now().strftime('%H:%M')}")
            else:
                updated_lines.append(line)

        updated_content = '\n'.join(updated_lines)

        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return True

    except Exception as e:
        print(f"Error updating dashboard: {e}")
        return False

def log_completion(task_id: str, task_subject: str) -> bool:
    """Log the completion to the activity log."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = Path("Logs")
    log_dir.mkdir(exist_ok=True)

    log_path = log_dir / f"{today}.txt"

    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] COMPLETED: {task_id} - {task_subject}\n"

    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        return True
    except Exception as e:
        print(f"Error logging completion: {e}")
        return False

def complete_task(task_id: str) -> Dict:
    """Main function to complete a task."""
    print(f"Attempting to complete task: {task_id}")

    # Find all related files
    found_files = find_task_files(task_id)

    if not found_files:
        # Try to suggest similar tasks
        suggestions = []
        directories = ["Needs_Action", "Plans", "Pending_Approval", "Done"]
        for directory in directories:
            dir_path = Path(directory)
            if dir_path.exists():
                for file_path in dir_path.glob("*.md"):
                    if task_id.lower() in file_path.stem.lower() or levenshtein_distance(task_id.lower(), file_path.stem.lower()) <= 2:
                        suggestions.append(file_path.stem)

        if suggestions:
            return {
                "status": "not_found_with_suggestions",
                "message": f"Task '{task_id}' not found. Did you mean: {', '.join(suggestions[:5])}?",
                "suggestions": suggestions[:5]
            }
        else:
            return {
                "status": "not_found",
                "message": f"Task '{task_id}' not found. Please check the task name and try again.",
                "suggestions": []
            }

    # Check if task is already completed (in Done folder)
    already_completed = any(file_type == "Done" for _, file_type in found_files)
    if already_completed:
        # Find the completion date from one of the done files
        done_file = next((file_path for file_path, file_type in found_files if file_type == "Done"), None)
        if done_file:
            try:
                content = done_file.read_text(encoding='utf-8')
                frontmatter, _ = load_yaml_frontmatter(content)
                completed_at = frontmatter.get('completed_at', 'unknown date')
                return {
                    "status": "already_completed",
                    "message": f"Task '{task_id}' was already completed on {completed_at}",
                    "completed_date": completed_at
                }
            except:
                return {
                    "status": "already_completed",
                    "message": f"Task '{task_id}' was already completed",
                    "completed_date": "unknown"
                }

    # Process each found file
    processed_files = []
    task_details = {}

    for file_path, file_type in found_files:
        try:
            # Read the current content
            content = file_path.read_text(encoding='utf-8')

            # Extract details before modification
            if not task_details:
                task_details = extract_task_details(content, file_path)

            # Load frontmatter and body
            frontmatter, body = load_yaml_frontmatter(content)

            # Update frontmatter with completion info
            frontmatter['status'] = 'completed'
            frontmatter['completed_at'] = datetime.now().isoformat()
            frontmatter['completed_by'] = 'claude_skill'

            # Add completion note to the body
            completion_note = f"\n\n## Completion Note\nTask completed by AI Employee on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
            updated_body = body + completion_note

            # Save the updated content to Done folder
            done_dir = Path("Done")
            done_dir.mkdir(exist_ok=True)

            new_file_path = done_dir / file_path.name
            save_with_yaml_frontmatter(new_file_path, frontmatter, updated_body)

            # Remove the original file
            file_path.unlink()

            processed_files.append({
                "original_path": str(file_path),
                "new_path": str(new_file_path),
                "type": file_type
            })

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    if not processed_files:
        return {
            "status": "error",
            "message": f"Failed to process any files for task '{task_id}'",
            "processed_count": 0
        }

    # Create completion summary
    summary_content = create_completion_summary(task_id, [(Path(pf['new_path']), pf['type']) for pf in processed_files], task_details)

    # Save the summary as a separate file in Done
    summary_file_path = Path("Done") / f"SUMMARY_{task_id}.md"
    with open(summary_file_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    # Update dashboard
    dashboard_updated = update_dashboard_with_completion(task_details.get('subject', task_id))

    # Log completion
    log_success = log_completion(task_id, task_details.get('subject', task_id))

    # Calculate duration
    duration = calculate_duration(task_details.get('created_at'))

    # Prepare result
    result = {
        "status": "completed",
        "message": f"Task '{task_id}' has been completed successfully",
        "processed_count": len(processed_files),
        "duration": duration,
        "dashboard_updated": dashboard_updated,
        "log_recorded": log_success,
        "task_subject": task_details.get('subject', task_id),
        "summary_file": str(summary_file_path)
    }

    return result

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def run_skill(task_identifier: Optional[str] = None):
    """
    Main function for the complete-task skill
    """
    if not task_identifier:
        return {
            "status": "missing_param",
            "message": "Please specify which task to complete. Example: complete task invoice_reminder",
            "suggestions": []
        }

    print(f"Starting complete-task skill for: {task_identifier}")

    # Call the complete_task function
    result = complete_task(task_identifier)

    # Print confirmation message based on result
    if result["status"] == "completed":
        print(f"Task Completed: {result['task_subject']}")
        print(f"Files archived: {result['processed_count']}")
        print(f"Duration: {result['duration']}")
        print(f"Dashboard updated: {'Yes' if result['dashboard_updated'] else 'No'}")
        print(f"Logged to activity log: {'Yes' if result['log_recorded'] else 'No'}")
        print(f"Original task has been moved to Done folder with completion metadata.")
    elif result["status"] == "not_found_with_suggestions":
        print(result["message"])
    elif result["status"] == "already_completed":
        print(result["message"])
    elif result["status"] == "not_found":
        print(result["message"])
    else:
        print(f"Error: {result['message']}")

    return result

def main():
    parser = argparse.ArgumentParser(description='Complete a task and archive it')
    parser.add_argument('task_id', nargs='?', help='The task identifier to complete')
    args = parser.parse_args()

    result = run_skill(args.task_id)
    return result

if __name__ == "__main__":
    result = main()
    print(f"\nSkill execution completed: {result}")