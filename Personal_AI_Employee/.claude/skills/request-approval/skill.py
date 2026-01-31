"""
Claude Code Agent Skill: request-approval
Creates approval requests for sensitive actions requiring human review
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import yaml
import argparse
import time
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

def ensure_directories_exist():
    """Ensure required directories exist."""
    dirs_to_create = ["Pending_Approval", "Approved", "Rejected", "Done", "Logs"]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)

def load_company_handbook() -> Dict:
    """Load Company_Handbook.md to get approval thresholds."""
    handbook_path = Path("Company_Handbook.md")

    if not handbook_path.exists():
        # Create a basic handbook if it doesn't exist
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

### Approval Requirements
- All payments over $100 require approval
- New vendor payments always require approval
- Any changes to business-critical systems require approval
- Social media posts about company business require approval
"""
        with open(handbook_path, 'w', encoding='utf-8') as f:
            f.write(handbook_content)

    # For now, return default thresholds
    return {
        "payment_threshold": 500,
        "email_recipients": [],  # Known contacts that don't need approval
        "auto_approve_recurring_payments_under": 100,
        "sensitive_actions": ["file_deletion", "database_modification", "new_vendor_payment"]
    }

def determine_risk_level(action_type: str, details: Dict) -> str:
    """Determine risk level based on action type and details."""
    if action_type == "payment":
        amount_str = details.get("amount", "0")
        # Extract numeric value from amount string (e.g., "$850" -> 850)
        import re
        # Match currency amounts like $850, 850, $850.00, etc.
        match = re.search(r'[\d,]+\.?\d*', str(amount_str).replace(',', ''))
        if match:
            amount = float(match.group().replace(',', ''))
        else:
            amount = 0

        if amount > 1000:
            return "high"
        elif amount > 500:
            return "medium"
        else:
            return "low"
    elif action_type == "email_send":
        recipient = details.get("to", "")
        # If recipient is not in known contacts, higher risk
        handbook = load_company_handbook()
        if recipient not in handbook.get("email_recipients", []):
            return "medium"
        else:
            return "low"
    elif action_type == "social_post":
        return "medium"  # Social posts carry reputational risk
    elif action_type == "file_operation":
        operation = details.get("operation", "")
        if operation == "delete":
            return "high"
        else:
            return "low"
    else:
        return "medium"

def calculate_expiration_time(action_type: str) -> datetime:
    """Calculate expiration time based on action type."""
    now = datetime.now()

    if action_type == "payment":
        return now + timedelta(hours=24)
    elif action_type == "social_post":
        return now + timedelta(hours=72)
    elif action_type == "email_send":
        return now + timedelta(hours=48)
    elif action_type == "file_operation":
        return now + timedelta(hours=24)
    else:
        return now + timedelta(hours=48)  # Default 48 hours

def create_approval_request(action_type: str, details: Dict) -> str:
    """Create an approval request file."""
    now = datetime.now()
    action_id = f"{action_type}_{now.strftime('%Y%m%d_%H%M%S')}_{details.get('subject', 'action').replace(' ', '_')}"

    # Determine risk level
    risk_level = determine_risk_level(action_type, details)

    # Calculate expiration
    expires = calculate_expiration_time(action_type)

    # Create frontmatter
    frontmatter = {
        "action_type": action_type,
        "action_id": action_id,
        "priority": details.get("priority", "medium"),
        "risk_level": risk_level,
        "created": now.isoformat(),
        "expires": expires.isoformat(),
        "status": "pending_approval",
        "auto_approve": False
    }

    # Create body based on action type
    body_parts = []

    # Title
    action_title = details.get("title", f"{action_type.replace('_', ' ').title()} Request")
    body_parts.append(f"# 🔐 Approval Required: {action_title}\n")

    # Action Summary
    summary = details.get("summary", f"This action requires human approval before proceeding.")
    body_parts.append(f"## Action Summary\n{summary}\n")

    # Details section
    body_parts.append("## Details\n")
    body_parts.append(f"**Type:** {action_type.replace('_', ' ').title()}\n")
    body_parts.append("**Requested by:** AI Employee\n")
    body_parts.append(f"**Reason:** {details.get('reason', 'Standard procedure for sensitive actions')}\n")
    body_parts.append(f"**Impact:** {details.get('impact', 'Will execute the requested action')}\n")
    body_parts.append(f"**Risk:** {risk_level.title()}\n")

    # Specifics section based on action type
    body_parts.append("\n## Specifics\n")

    if action_type == "email_send":
        body_parts.append(f"### Email Details:\n")
        body_parts.append(f"- **To:** {details.get('to', 'Not specified')}\n")
        body_parts.append(f"- **Subject:** {details.get('subject', 'Not specified')}\n")
        body_parts.append(f"- **Content:** See draft below\n")
    elif action_type == "payment":
        body_parts.append(f"### Payment Details:\n")
        body_parts.append(f"- **Amount:** {details.get('amount', 'Not specified')}\n")
        body_parts.append(f"- **To:** {details.get('to', 'Not specified')}\n")
        body_parts.append(f"- **Purpose:** {details.get('purpose', 'Not specified')}\n")
        body_parts.append(f"- **Account:** {details.get('account', 'Not specified')}\n")
    elif action_type == "social_post":
        body_parts.append(f"### Social Post Details:\n")
        body_parts.append(f"- **Platform:** {details.get('platform', 'Not specified')}\n")
        body_parts.append(f"- **Content:** See draft below\n")
        body_parts.append(f"- **Scheduled:** {details.get('scheduled', 'Immediately')}\n")
    elif action_type == "file_operation":
        body_parts.append(f"### File Operation Details:\n")
        body_parts.append(f"- **Operation:** {details.get('operation', 'Not specified')}\n")
        body_parts.append(f"- **File:** {details.get('file_path', 'Not specified')}\n")
        body_parts.append(f"- **Reason:** {details.get('reason', 'Not specified')}\n")
    else:
        body_parts.append(f"### Action Details:\n")
        for key, value in details.items():
            if key not in ["title", "summary", "reason", "impact", "priority"]:
                body_parts.append(f"- **{key.replace('_', ' ').title()}:** {value}\n")

    # Draft/Details section
    body_parts.append(f"\n## Draft/Details\n```\n{details.get('content', 'No content provided')}\n```\n")

    # Approval Instructions
    body_parts.append("## Approval Instructions\n")
    body_parts.append("✅ To Approve:\n")
    body_parts.append("Move this file to /Approved folder\n")
    body_parts.append("❌ To Reject:\n")
    body_parts.append("Move this file to /Rejected folder\n")
    body_parts.append("✏️ To Modify:\n")
    body_parts.append("Edit the content above, then move to /Approved\n")

    # Expiration
    body_parts.append(f"\n## Expiration\n")
    body_parts.append(f"This approval request will expire on: {expires.strftime('%Y-%m-%d %H:%M:%S')}\n")
    body_parts.append("After expiration, action will be automatically cancelled.\n")

    # Notes
    notes = details.get("notes", "No additional notes provided.")
    body_parts.append(f"\n## Notes\n{notes}\n")

    # Footer
    body_parts.append(f"\n---\n*Approval request generated by AI Employee*")

    body = "\n".join(body_parts)

    # Save to Pending_Approval folder
    pending_dir = Path("Pending_Approval")
    pending_dir.mkdir(exist_ok=True)

    file_path = pending_dir / f"APPROVAL_{action_id}.md"
    save_with_yaml_frontmatter(file_path, frontmatter, body)

    return str(file_path)

def log_approval_request(action_id: str, action_type: str, reason: str):
    """Log the approval request to the activity log."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = Path("Logs")
    log_dir.mkdir(exist_ok=True)

    log_path = log_dir / f"{today}.txt"

    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] APPROVAL_REQUESTED: {action_id} - {action_type} - {reason}\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def monitor_approval_request(file_path: str, timeout_minutes: int = 60*24*2):  # 2 days default
    """Monitor the approval request file for changes."""
    file_path_obj = Path(file_path)
    start_time = time.time()

    while time.time() - start_time < timeout_minutes * 60:
        # Check if the file has been moved to Approved or Rejected
        pending_dir = Path("Pending_Approval")

        # If the file no longer exists in Pending_Approval, it has been moved
        if not file_path_obj.exists():
            # Determine where it was moved
            approved_path = Path("Approved") / file_path_obj.name
            rejected_path = Path("Rejected") / file_path_obj.name

            if approved_path.exists():
                return "approved", str(approved_path)
            elif rejected_path.exists():
                return "rejected", str(rejected_path)

        # Check if the file has expired
        content = file_path_obj.read_text(encoding='utf-8')
        frontmatter, _ = load_yaml_frontmatter(content)

        if 'expires' in frontmatter:
            try:
                expires_at = datetime.fromisoformat(frontmatter['expires'])
                if datetime.now() > expires_at:
                    # Move to Rejected as it expired
                    rejected_dir = Path("Rejected")
                    rejected_dir.mkdir(exist_ok=True)
                    expired_path = rejected_dir / file_path_obj.name
                    file_path_obj.rename(expired_path)

                    # Log expiration
                    action_id = frontmatter.get('action_id', 'unknown')
                    log_approval_decision(action_id, 'expired', 'Approval request timed out')

                    return "expired", str(expired_path)
            except ValueError:
                pass  # If parsing fails, continue monitoring

        # Wait 5 minutes before checking again
        time.sleep(300)

    # If we've reached here, the timeout occurred
    if file_path_obj.exists():
        rejected_dir = Path("Rejected")
        rejected_dir.mkdir(exist_ok=True)
        timeout_path = rejected_dir / file_path_obj.name
        file_path_obj.rename(timeout_path)

        # Log timeout
        content = file_path_obj.read_text(encoding='utf-8')
        frontmatter, _ = load_yaml_frontmatter(content)
        action_id = frontmatter.get('action_id', 'unknown')
        log_approval_decision(action_id, 'timeout', 'Approval request timed out')

        return "timeout", str(timeout_path)

    return "unknown", ""

def log_approval_decision(action_id: str, decision: str, reason: str):
    """Log the approval decision to the activity log."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = Path("Logs")
    log_dir.mkdir(exist_ok=True)

    log_path = log_dir / f"{today}.txt"

    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] APPROVAL_DECISION: {action_id} - {decision} - {reason}\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def request_approval(action_type: str, details: Dict) -> Dict:
    """Main function to request approval for an action."""
    print(f"Requesting approval for action: {action_type}")

    # Ensure directories exist
    ensure_directories_exist()

    # Create approval request file
    file_path = create_approval_request(action_type, details)

    # Log the request
    reason = details.get("reason", f"Sensitive {action_type} action")
    log_approval_request(details.get("action_id", action_type), action_type, reason)

    # Determine expiration time for the response
    expires_at = calculate_expiration_time(action_type)
    expires_relative = expires_at - datetime.now()
    expires_hours = int(expires_relative.total_seconds() // 3600)

    # Prepare result
    result = {
        "status": "approval_requested",
        "message": f"Approval required for {action_type}",
        "file_path": file_path,
        "action_id": details.get("action_id", action_type),
        "expires_in_hours": expires_hours,
        "priority": details.get("priority", "medium")
    }

    return result

def run_skill(action_type: str = None, details_json: str = None):
    """
    Main function for the request-approval skill
    """
    if not action_type:
        return {
            "status": "error",
            "message": "Please specify action type and details for approval request"
        }

    # Parse details if provided as JSON string
    if details_json:
        try:
            details = json.loads(details_json)
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "Invalid JSON in details parameter"
            }
    else:
        # Use defaults if no details provided
        details = {
            "title": f"{action_type.replace('_', ' ').title()} Request",
            "summary": "This action requires human approval before proceeding.",
            "reason": "Standard procedure for sensitive actions",
            "impact": "Will execute the requested action",
            "priority": "medium",
            "content": "No specific content provided."
        }

    print(f"Starting request-approval skill for: {action_type}")

    # Call the request_approval function
    result = request_approval(action_type, details)

    # Print confirmation message
    print("[LOCK] Approval Required")
    print(f"I've created an approval request for:")
    print(f"{details.get('title', action_type.replace('_', ' ').title())}")
    print(f"[FOLDER] Location: {result['file_path']}")
    print(f"[TIME] Expires: in {result['expires_in_hours']} hours")
    print(f"[TARGET] Priority: {result['priority']}")
    print("To approve: Move the file to /Approved folder")
    print("To reject: Move the file to /Rejected folder")
    print("I'll monitor for your decision and execute if approved.")

    return result

def main():
    parser = argparse.ArgumentParser(description='Request approval for sensitive actions')
    parser.add_argument('action_type', nargs='?', help='The type of action requiring approval')
    parser.add_argument('--details', help='JSON string with action details')
    args = parser.parse_args()

    if not args.action_type:
        print("Usage: python skill.py <action_type> --details '{\"key\": \"value\"}'")
        return {
            "status": "error",
            "message": "Please specify action type for approval request"
        }

    result = run_skill(args.action_type, args.details)
    return result

if __name__ == "__main__":
    result = main()
    print(f"\nSkill execution completed: {result}")