"""
Claude Code Agent Skill: process-emails
Processes incoming emails from Gmail watcher and creates appropriate responses with human approval
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
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

def categorize_email(email_info: Dict[str, Any]) -> str:
    """Categorize email based on sender and content."""
    subject = email_info.get('subject', '').lower()
    sender = email_info.get('from', '').lower()
    body = email_info.get('body', '').lower()

    # Define categories based on keywords
    client_keywords = ['client', 'customer', 'account', 'support', 'service']
    sales_keywords = ['interest', 'inquiry', 'quote', 'price', 'offer', 'buy', 'purchase']
    admin_keywords = ['admin', 'hr', 'office', 'meeting', 'schedule', 'policy', 'procedure']
    team_keywords = ['team', 'internal', 'department', 'colleague', 'staff']
    spam_keywords = ['spam', 'advertisement', 'marketing', 'promotion', 'sale']

    combined_text = f"{subject} {sender} {body}"

    # Check for client emails
    for keyword in client_keywords:
        if keyword in combined_text:
            return 'client'

    # Check for sales leads
    for keyword in sales_keywords:
        if keyword in combined_text:
            return 'sales'

    # Check for admin emails
    for keyword in admin_keywords:
        if keyword in combined_text:
            return 'admin'

    # Check for team emails
    for keyword in team_keywords:
        if keyword in combined_text:
            return 'team'

    # Check for spam
    for keyword in spam_keywords:
        if keyword in combined_text:
            return 'spam'

    # Default to admin if no specific category found
    return 'admin'

def calculate_priority_score(email_info: Dict[str, Any], category: str) -> int:
    """Calculate priority score (0-100) based on keywords and sender."""
    subject = email_info.get('subject', '').lower()
    sender = email_info.get('from', '').lower()
    body = email_info.get('body', '').lower()
    priority = email_info.get('priority', 'medium').lower()

    score = 50  # Base priority

    # High priority keywords
    high_priority_keywords = [
        'urgent', 'asap', 'emergency', 'immediately', 'critical',
        'important', 'deadline', 'due', 'invoice', 'payment', 'bill',
        'money', 'financial', 'legal', 'compliance'
    ]

    # Medium priority keywords
    medium_priority_keywords = [
        'follow', 'remind', 'meeting', 'schedule', 'appointment',
        'project', 'report', 'proposal', 'contract', 'agreement'
    ]

    combined_text = f"{subject} {body}"

    # Add points for high priority keywords
    for keyword in high_priority_keywords:
        if keyword in combined_text:
            score += 20

    # Add points for medium priority keywords
    for keyword in medium_priority_keywords:
        if keyword in combined_text:
            score += 10

    # Adjust based on original priority
    if priority == 'high':
        score += 15
    elif priority == 'critical':
        score += 25
    elif priority == 'low':
        score -= 10

    # Adjust based on category
    if category == 'spam':
        score = max(0, score - 30)  # Reduce spam priority
    elif category in ['client', 'sales']:
        score = min(100, score + 10)  # Boost important categories

    # Cap the score between 0 and 100
    return max(0, min(100, score))

def select_template(category: str) -> str:
    """Select appropriate response template based on category."""
    templates = {
        'client': """Dear [Client Name],

Thank you for reaching out regarding {subject}. We appreciate your inquiry and will address your concerns promptly.

{customized_response}

We value your business and look forward to continuing our partnership.

Best regards,
AI Employee Assistant""",

        'sales': """Dear [Sender Name],

Thank you for your interest in our services/products. We appreciate your inquiry about {subject}.

{customized_response}

We would be happy to discuss how we can help you achieve your goals.

Best regards,
AI Employee Assistant""",

        'admin': """Hello,

Thank you for the information regarding {subject}. This has been noted and will be processed accordingly.

{customized_response}

Have a great day.

Best regards,
AI Employee Assistant""",

        'team': """Hi Team,

Thank you for the update on {subject}. This information has been received and documented.

{customized_response}

Best regards,
AI Employee Assistant""",

        'spam': """This email has been identified as potentially unwanted or irrelevant and will be handled accordingly.

No response will be sent."""
    }

    return templates.get(category, templates['admin'])

def draft_response(email_info: Dict[str, Any], category: str) -> str:
    """Draft a response based on email content and category."""
    subject = email_info.get('subject', 'No Subject')
    body = email_info.get('body', 'No content provided')

    # Create a customized response based on the email content
    customized_response = f"Regarding your email with subject '{subject}', we acknowledge receipt and will take appropriate action based on your request."

    if category != 'spam':
        # Extract key points from the email body
        sentences = body.split('.')
        if len(sentences) > 0:
            # Use the first substantial sentence as part of the response
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 10:  # Only use if it's substantial
                customized_response = f"I've reviewed your request about '{first_sentence[:50]}...' and will handle it accordingly."

    template = select_template(category)
    return template.format(subject=subject, customized_response=customized_response)

def create_approval_request(email_info: Dict[str, Any], response_draft: str, priority_score: int) -> Path:
    """Create an approval request for the email response."""
    pending_approval_dir = Path("AI_Employee_Vault/Pending_Approval")
    pending_approval_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_subject = "".join(c for c in email_info.get('subject', 'email') if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not safe_subject:
        safe_subject = "email"

    filename = f"APPROVAL_email_response_{timestamp}_{safe_subject}.md"
    filepath = pending_approval_dir / filename

    # Determine risk level based on priority score
    if priority_score >= 80:
        risk_level = 'high'
    elif priority_score >= 50:
        risk_level = 'medium'
    else:
        risk_level = 'low'

    approval_content = f"""---
action_type: email_send
action_id: email_response_{timestamp}
priority: {priority_score}
risk_level: {risk_level}
created: {datetime.now().isoformat()}
expires: {(datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=1)).isoformat()}
status: pending_approval
email_thread_id: {email_info.get('thread_id', email_info.get('email_id', 'unknown'))}
---

# 🔐 Approval Required: Email Response

## Action Summary
Send response to email from {email_info.get('from', 'Unknown')} regarding "{email_info.get('subject', 'No Subject')}"

## Details

**Type:** Email Response
**Requested by:** AI Employee
**Reason:** Process incoming email
**Impact:** Send professional response
**Risk:** {risk_level}

## Draft Response
```
{response_draft}
```

## Approval Instructions
✅ To Approve: Move this file to /Approved folder
❌ To Reject: Move this file to /Rejected folder
✏️ To Modify: Edit the response above, then move to /Approved

## Expiration
This approval request will expire on: {(datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')}
After expiration, the response will be cancelled.

---
*Approval request generated by AI Employee*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(approval_content)

    return filepath

def update_dashboard(processed_emails: List[Dict[str, Any]]) -> None:
    """Update the Dashboard.md file with email statistics."""
    dashboard_path = Path("Dashboard.md")

    if dashboard_path.exists():
        content = dashboard_path.read_text(encoding='utf-8')
    else:
        content = "# Personal AI Employee Dashboard\n\n## Executive Summary\n- **Status**: Operational\n- **Last Update**: {{date}}\n- **Active Tasks**: 0\n- **Pending Approval**: 0\n\n## Recent Activity\n- [No recent activity]\n\n## System Status\n- **Watchers Running**: 0\n- **Last Backup**: Never\n"

    # Count email statistics
    email_categories = {'client': 0, 'sales': 0, 'admin': 0, 'team': 0, 'spam': 0}
    for email in processed_emails:
        category = email.get('category', 'admin')
        if category in email_categories:
            email_categories[category] += 1

    # Update the content
    lines = content.split('\n')
    updated_lines = []
    email_stats_added = False

    for line in lines:
        if "## System Status" in line and not email_stats_added:
            updated_lines.append(line)
            updated_lines.append("")
            updated_lines.append("## Email Statistics")
            for category, count in email_categories.items():
                if count > 0:
                    updated_lines.append(f"- **{category.title()} Emails**: {count}")
            email_stats_added = True
        elif line.startswith('- **Last Update**:'):
            updated_lines.append(f'- **Last Update**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}')
        else:
            updated_lines.append(line)

    # Add email stats section if not found
    if not email_stats_added:
        # Find a good place to add email stats
        final_lines = []
        for line in updated_lines:
            final_lines.append(line)
            if "## Recent Activity" in line:
                # Add email stats after recent activity section
                final_lines.append("")
                final_lines.append("## Email Statistics")
                for category, count in email_categories.items():
                    if count > 0:
                        final_lines.append(f"- **{category.title()} Emails**: {count}")
                break

        updated_content = '\n'.join(final_lines)
    else:
        updated_content = '\n'.join(updated_lines)

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def log_activity(processed_emails: List[Dict[str, Any]], error_count: int = 0) -> None:
    """Log the email processing activity."""
    today = datetime.now().strftime("%Y-%m-%d")
    logs_dir = Path("AI_Employee_Vault/Logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_path = logs_dir / f"{today}.txt"

    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] process-emails skill executed: "
    log_entry += f"processed {len(processed_emails)} emails"
    if error_count > 0:
        log_entry += f", encountered {error_count} errors"

    for email in processed_emails:
        log_entry += f"\n  - {email['category']} email from {email.get('from', 'Unknown')}: {email.get('subject', 'No Subject')} (Priority: {email.get('priority_score', 0)})"

    log_entry += "\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def run_skill():
    """
    Main function for the process-emails skill
    """
    from datetime import timedelta  # Import here to avoid conflicts

    print("Starting process-emails skill...")

    # 1. Scan the /Needs_Action folder for EMAIL_*.md files
    needs_action_dir = Path("AI_Employee_Vault/Needs_Action")
    if not needs_action_dir.exists():
        print("No Needs_Action directory found.")
        return {"status": "success", "message": "No email files to process", "processed_count": 0}

    email_files = list(needs_action_dir.glob("EMAIL_*.md"))

    if not email_files:
        print("No email files found to process")
        return {"status": "success", "message": "No email files to process", "processed_count": 0}

    print(f"Found {len(email_files)} email files to process.")

    processed_emails = []
    error_count = 0

    # 2. Process each email file
    for email_file in email_files:
        try:
            print(f"Processing email: {email_file.name}")

            # Read the email file content
            content = email_file.read_text(encoding='utf-8')
            frontmatter, body = load_yaml_frontmatter(content)

            # Create email info dictionary
            email_info = {
                'id': frontmatter.get('email_id', ''),
                'thread_id': frontmatter.get('thread_id', ''),
                'from': frontmatter.get('from', 'Unknown'),
                'to': frontmatter.get('to', 'Unknown'),
                'subject': frontmatter.get('subject', 'No Subject'),
                'received': frontmatter.get('received', ''),
                'priority': frontmatter.get('priority', 'medium'),
                'type': frontmatter.get('type', 'email'),
                'body': body
            }

            # Categorize the email
            category = categorize_email(email_info)
            print(f"  - Categorized as: {category}")

            # Calculate priority score
            priority_score = calculate_priority_score(email_info, category)
            print(f"  - Priority score: {priority_score}")

            # Draft a response
            response_draft = draft_response(email_info, category)
            print(f"  - Response drafted")

            # Create approval request
            approval_file = create_approval_request(email_info, response_draft, priority_score)
            print(f"  - Approval request created: {approval_file.name}")

            # Store processed email info
            processed_email_info = {
                'filename': email_file.name,
                'category': category,
                'priority_score': priority_score,
                'from': email_info.get('from', 'Unknown'),
                'subject': email_info.get('subject', 'No Subject')
            }
            processed_emails.append(processed_email_info)

            # Optionally, move the processed email file to indicate it's been handled
            # For now, we'll keep it but you could move it to a processed folder

        except Exception as e:
            print(f"Error processing {email_file.name}: {str(e)}")
            error_count += 1
            continue

    # 3. Update the Dashboard.md file
    try:
        update_dashboard(processed_emails)
        print("Dashboard updated successfully.")
    except Exception as e:
        print(f"Error updating dashboard: {str(e)}")
        error_count += 1

    # 4. Log the activity
    try:
        log_activity(processed_emails, error_count)
        print("Activity logged successfully.")
    except Exception as e:
        print(f"Error logging activity: {str(e)}")

    # Prepare result
    result_message = f"Processed {len(processed_emails)} emails"
    if error_count > 0:
        result_message += f" with {error_count} errors"

    result = {
        "status": "success",
        "message": result_message,
        "processed_count": len(processed_emails),
        "error_count": error_count
    }

    print(result_message)
    return result

if __name__ == "__main__":
    result = run_skill()
    print(f"\nSkill execution completed: {result}")