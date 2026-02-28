"""
Claude Code Agent Skill: work-email-handler
Specialized skill for detecting, processing, and responding to work-related emails
with automatic classification and approval workflow for job opportunities.
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re
import psutil

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

def is_work_related_email(email_info: Dict[str, Any]) -> bool:
    """Check if an email is work/employment related based on keywords."""
    subject = email_info.get('subject', '').lower()
    sender = email_info.get('from', '').lower()
    body = email_info.get('body', '').lower()

    # Work-related keywords
    work_keywords = [
        'job', 'work', 'employment', 'opportunity', 'hire', 'contract',
        'freelance', 'position', 'role', 'application', 'candidate',
        'recruit', 'hiring', 'vacancy', 'opening', 'interview',
        'company', 'role', 'position', 'project', 'engagement',
        'consultant', 'consulting', 'freelancer', 'contractor', 'offer',
        'salary', 'pay', 'compensation'
    ]

    combined_text = f"{subject} {sender} {body}"

    # Check for work-related keywords
    for keyword in work_keywords:
        if keyword in combined_text:
            return True

    return False

def extract_job_details(email_info: Dict[str, Any]) -> Dict[str, Any]:
    """Extract job-related details from email content."""
    body = email_info.get('body', '')

    # Extract details using regex patterns
    details = {
        'company_name': '',
        'job_title': '',
        'salary_range': '',
        'location': '',
        'requirements': [],
        'deadline': '',
        'employment_type': '',
        'contact_person': ''
    }

    # Try to find company name
    company_patterns = [
        r'company[:\s]+([A-Z][a-zA-Z\s]+)',
        r'at\s+([A-Z][a-zA-Z\s]+)',
        r'with\s+([A-Z][a-zA-Z\s]+)',
        r'from\s+([A-Z][a-zA-Z\s]+)'
    ]

    for pattern in company_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            details['company_name'] = match.group(1).strip()
            break

    # Try to find job title
    job_title_patterns = [
        r'for\s+a?\s+([A-Z][a-zA-Z\s]*\b(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Director|Lead|Architect|Coordinator|Assistant|Executive|Officer)\b)',
        r'(?:position\s+|role\s+)?(?:as\s+a?\s+)?([A-Z][a-zA-Z\s]*\b(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Director|Lead|Architect|Coordinator|Assistant|Executive|Officer)\b)',
        r'([A-Z][a-zA-Z\s]*\b(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Director|Lead|Architect|Coordinator|Assistant|Executive|Officer)\b)'
    ]

    for pattern in job_title_patterns:
        matches = re.findall(pattern, body)
        if matches:
            # Take the first match that looks like a job title
            for match in matches:
                if match.strip() and len(match.strip()) < 50:  # Reasonable length
                    details['job_title'] = match.strip()
                    break
            if details['job_title']:
                break

    # Try to find salary info
    salary_patterns = [
        r'(\$\d+(?:,\d{3})*(?:\s*-\s*\$\d+(?:,\d{3})*)?)',
        r'([£€]\d+(?:,\d{3})*(?:\s*-\s*[£€]\d+(?:,\d{3})*\b)?)',
        r'(\b\d+(?:,\d{3})*\s*(?:USD|EUR|GBP|PKR|USD|INR)\s*per\s*(?:year|month|hour)\b)',
        r'(salary|compensation|pay):\s*([$\w,\s-]+)'
    ]

    for pattern in salary_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            # Take the first match
            if isinstance(matches[0], tuple):
                salary_range = ' - '.join([s for s in matches[0] if s.strip()])
            else:
                salary_range = matches[0]
            details['salary_range'] = salary_range.strip()
            break

    # Try to find location
    location_patterns = [
        r'location[:\s]+([A-Z][a-zA-Z\s,]+)',
        r'based\s+in\s+([A-Z][a-zA-Z\s,]+)',
        r'([A-Z][a-zA-Z\s,]+\s+location)',
        r'work(?:\s+from)?\s+([A-Z][a-zA-Z\s,]+)'
    ]

    for pattern in location_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            details['location'] = match.group(1).strip()
            break

    # Try to find employment type
    emp_type_patterns = [
        r'\b(Contract|Freelance|Full-time|Part-time|Temporary|Permanent|Internship|Remote|Hybrid)\b',
        r'employment\s+type:\s*([A-Za-z-]+)',
        r'job\s+type:\s*([A-Za-z-]+)'
    ]

    for pattern in emp_type_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            details['employment_type'] = matches[0].strip()
            break

    # Try to find application deadline
    deadline_patterns = [
        r'(?:deadline|due|apply by|response by):\s*([A-Za-z]+\s+\d{1,2},?\s*\d{4})',
        r'(?:deadline|due|apply by|response by)\s+([A-Za-z]+\s+\d{1,2},?\s*\d{4})',
        r'(?:deadline|due|apply by|response by)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    ]

    for pattern in deadline_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            details['deadline'] = match.group(1).strip()
            break

    # Try to find contact person
    contact_patterns = [
        r'(?:contact\s+|reach\s+out\s+to\s+|contact:?\s+)?([A-Z][a-zA-Z\s]*\b(?:Manager|Director|Lead|Recruiter|HR|Hiring)\b)',
        r'(?:contact\s+|reach\s+out\s+to\s+|contact:?\s+)?([A-Z][a-zA-Z\s]*[A-Z][a-zA-Z]+)',
        r'(?:regards|sincerely|thanks)\s+([A-Z][a-zA-Z\s]+)'
    ]

    for pattern in contact_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            for match in matches:
                if match.strip() and len(match.strip()) < 50 and ' ' in match.strip():  # Ensure it looks like a name
                    details['contact_person'] = match.strip()
                    break
            if details['contact_person']:
                break

    # Extract requirements if any
    requirements_keywords = re.findall(r'(?:requirements?|qualifications?|skills|experience):\s*([^.\n]+)', body, re.IGNORECASE)
    if requirements_keywords:
        for req in requirements_keywords:
            req = req.strip()
            if req and len(req) < 200:  # Avoid very long text
                details['requirements'].append(req)

    return details

def assign_priority(email_body: str, position: str, subject: str) -> str:
    """Assign priority level based on email content"""
    body_lower = email_body.lower()
    subject_lower = subject.lower()
    position_lower = position.lower() if position else ""

    # HIGH priority: job offer or interview
    high_keywords = ['offer', 'interview', 'selected', 'congratulations', 'hiring manager', 'next steps', 'final round']
    for keyword in high_keywords:
        if keyword in body_lower or keyword in subject_lower or keyword in position_lower:
            return 'HIGH'

    # MEDIUM priority: freelance or recruiter message
    medium_keywords = ['freelance', 'contract', 'recruiter', 'agency', 'talent', 'hiring']
    for keyword in medium_keywords:
        if keyword in body_lower or keyword in subject_lower:
            return 'MEDIUM'

    # LOW priority: hiring newsletter
    low_keywords = ['newsletter', 'update', 'digest', 'opportunities', 'jobs this week']
    for keyword in low_keywords:
        if keyword in body_lower or keyword in subject_lower:
            return 'LOW'

    # Default to MEDIUM if it's work-related
    return 'MEDIUM'

def create_work_email_response(email_info: Dict[str, Any], job_details: Dict[str, Any]) -> str:
    """Create a professional response for work-related emails."""
    subject = email_info.get('subject', 'Work Opportunity')

    # Build response considering the requirements: under 150 words, professional tone
    greeting = f"Dear {job_details.get('contact_person', 'Hiring Manager')},"

    body_parts = [
        f"Thank you for reaching out regarding the {job_details.get('job_title', 'position')} opportunity at {job_details.get('company_name', 'your company')}.",
        "I am very interested in this position and believe my skills and experience align well with the requirements.",
    ]

    # Ask for clarification if needed
    missing_info_requests = []
    if not job_details.get('job_title'):
        missing_info_requests.append("the specific role title")
    if not job_details.get('salary_range'):
        missing_info_requests.append("the salary range")

    if missing_info_requests:
        and_join = " and " if len(missing_info_requests) > 1 else ""
        body_parts.append(f"Could you please provide more details about {and_join.join(missing_info_requests)}?")

    body_parts.append("I would appreciate the opportunity to discuss this role further and explore how I can contribute to your organization.")

    closing = [
        "Thank you for your time and consideration.",
        "Best regards,",
        "AI Employee Assistant"
    ]

    response_parts = [greeting, ""] + body_parts + [""] + closing
    response = "\n".join(response_parts)

    # Truncate if necessary to keep under 150 words
    words = response.split()
    if len(words) > 150:
        # Try to keep the most essential parts
        truncated_response = " ".join(words[:150])
        return truncated_response + "..."

    return response

def save_to_approval_queue(company: str, position: str, priority: str, draft_response: str):
    """Save draft response to approval queue."""
    approval_data = {
        "company": company,
        "position": position,
        "priority": priority,
        "draft_response": draft_response,
        "status": "AWAITING USER APPROVAL",
        "timestamp": datetime.now().isoformat()
    }

    try:
        approval_queue_file = Path("approval_queue.json")
        if approval_queue_file.exists():
            with open(approval_queue_file, 'r') as f:
                queue_data = json.load(f)
        else:
            queue_data = {"pending_approvals": [], "completed_approvals": [], "last_updated": None}

        queue_data["pending_approvals"].append(approval_data)
        queue_data["last_updated"] = datetime.now().isoformat()

        with open(approval_queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)

        return True

    except Exception as e:
        print(f"Error saving to approval queue: {e}")
        return False

def run_skill():
    """
    Main function for the work-email-handler skill
    """
    from datetime import timedelta  # Import here to avoid conflicts

    print("Starting work-email-handler skill...")

    # Check memory usage first
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 80:  # High memory usage
        print(f"High memory usage detected: {memory_percent}%. Skipping processing.")
        # Store message about system load
        save_to_approval_queue(
            company="System Load High",
            position="System Maintenance",
            priority="LOW",
            draft_response="System load high. Awaiting manual review."
        )
        return {"status": "success", "message": "High memory usage - processing skipped", "processed_count": 0}

    # Load work email queue
    work_email_queue_file = Path("work_email_queue.json")
    if not work_email_queue_file.exists():
        print("No work email queue file found.")
        return {"status": "success", "message": "No work email queue file", "processed_count": 0}

    try:
        with open(work_email_queue_file, 'r') as f:
            queue_data = json.load(f)
    except Exception as e:
        print(f"Error loading work email queue: {str(e)}")
        return {"status": "error", "message": f"Error loading work email queue: {str(e)}", "processed_count": 0}

    emails = queue_data.get("emails", [])

    if not emails:
        print("No emails in work queue to process")
        return {"status": "success", "message": "No emails to process", "processed_count": 0}

    print(f"Found {len(emails)} work-related emails to process.")
    processed_emails = []
    error_count = 0

    # Process each email in the work queue
    for i, email in enumerate(emails):
        try:
            print(f"Processing email {i+1}/{len(emails)}: {email.get('subject', 'No Subject')}")

            # Extract job details
            job_details = extract_job_details(email)
            print(f"  - Job details extracted: {job_details.get('job_title', 'N/A')} at {job_details.get('company_name', 'N/A')}")

            # Assign priority
            priority = assign_priority(email.get('body', email.get('snippet', '')),
                                     job_details.get('job_title', ''),
                                     email.get('subject', ''))
            print(f"  - Priority assigned: {priority}")

            # Create a response draft
            response_draft = create_work_email_response(email, job_details)
            print(f"  - Response drafted")

            # Save to approval queue
            saved = save_to_approval_queue(
                company=job_details.get('company_name', 'Unknown Company'),
                position=job_details.get('job_title', 'Unknown Position'),
                priority=priority,
                draft_response=response_draft
            )

            if saved:
                # Store processed email info
                work_email_info = {
                    'id': email.get('id', 'Unknown'),
                    'from': email.get('from', 'Unknown'),
                    'subject': email.get('subject', 'No Subject'),
                    'company': job_details.get('company_name', 'Unknown'),
                    'position': job_details.get('job_title', 'Unknown'),
                    'priority': priority
                }
                processed_emails.append(work_email_info)
            else:
                error_count += 1

        except Exception as e:
            print(f"Error processing work email: {str(e)}")
            error_count += 1
            continue

    # Update the queue file by removing processed emails
    remaining_emails = emails[len(processed_emails):]
    queue_data["emails"] = remaining_emails
    queue_data["total_processed"] = queue_data.get("total_processed", 0) + len(processed_emails)

    try:
        with open(work_email_queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)
    except Exception as e:
        print(f"Error updating work email queue: {str(e)}")

    # Prepare result
    result_message = f"Processed {len(emails)} work email files, identified {len(processed_emails)} emails, {error_count} errors"

    result = {
        "status": "success",
        "message": result_message,
        "total_emails_processed": len(emails),
        "work_related_emails": len(processed_emails),
        "work_emails_list": processed_emails,
        "errors": error_count
    }

    print(result_message)
    return result

if __name__ == "__main__":
    result = run_skill()
    print(f"\nSkill execution completed: {result}")