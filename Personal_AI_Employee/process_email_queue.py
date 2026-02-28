"""
Email Queue Processor
Processes incoming emails from work_email_queue.json and general_email_queue.json as per requirements
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
import re
import psutil
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
WORK_CHECK_INTERVAL = 180  # seconds for work emails as per requirements
GENERAL_CHECK_INTERVAL = 60  # seconds for general emails
WORK_EMAIL_QUEUE_FILE = Path("work_email_queue.json")
GENERAL_EMAIL_QUEUE_FILE = Path("general_email_queue.json")
APPROVAL_QUEUE_FILE = Path("approval_queue.json")
NEEDS_ACTION_DIR = Path("AI_Employee_Vault/Needs_Action")
PROCESSED_DIR = Path("AI_Employee_Vault/Done")

def get_memory_usage():
    """Get current memory usage percentage"""
    return psutil.virtual_memory().percent

def extract_job_details_from_email(email_body: str) -> Dict[str, Any]:
    """Extract job-related details from email content."""
    # Initialize the details dictionary with empty values
    details = {
        'company_name': '',
        'position': '',
        'employment_type': '',
        'salary': '',
        'location': '',
        'requirements': [],
        'contact_person': '',
        'deadline': ''
    }

    # Extract company name
    company_patterns = [
        r'company[:\s]+([A-Z][a-zA-Z\s]+(?:Inc|LLC|Ltd|Corp|Group)?)',
        r'at\s+([A-Z][a-zA-Z\s]+(?:Inc|LLC|Ltd|Corp|Group)?)',
        r'with\s+([A-Z][a-zA-Z\s]+(?:Inc|LLC|Ltd|Corp|Group)?)',
        r'from\s+([A-Z][a-zA-Z\s]+(?:Inc|LLC|Ltd|Corp|Group)?)',
        r'(?:working\s+)?for\s+([A-Z][a-zA-Z\s]+(?:Inc|LLC|Ltd|Corp|Group)?)'
    ]

    for pattern in company_patterns:
        match = re.search(pattern, email_body, re.IGNORECASE)
        if match:
            details['company_name'] = match.group(1).strip()
            break

    # Extract position
    position_patterns = [
        r'(?:position\s+|role\s+)?(?:as\s+)?([A-Z][a-zA-Z\s]*\b(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Director|Lead|Architect|Coordinator|Assistant|Executive|Officer)\b)',
        r'for\s+a?\s+([A-Z][a-zA-Z\s]*\b(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Director|Lead|Architect|Coordinator|Assistant|Executive|Officer)\b)',
        r'([A-Z][a-zA-Z\s]*\b(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Director|Lead|Architect|Coordinator|Assistant|Executive|Officer)\b)'
    ]

    for pattern in position_patterns:
        matches = re.findall(pattern, email_body)
        if matches:
            # Take the first match that looks like a job title
            for match in matches:
                if match.strip() and len(match.strip()) < 50:  # Reasonable length
                    details['position'] = match.strip()
                    break
            if details['position']:
                break

    # Extract employment type
    emp_type_patterns = [
        r'\b(Contract|Freelance|Full-time|Part-time|Temporary|Permanent|Internship|Remote|Hybrid)\b',
        r'employment\s+type:\s*([A-Za-z-]+)',
        r'job\s+type:\s*([A-Za-z-]+)'
    ]

    for pattern in emp_type_patterns:
        matches = re.findall(pattern, email_body, re.IGNORECASE)
        if matches:
            details['employment_type'] = matches[0].strip()
            break

    # Extract salary
    salary_patterns = [
        r'(\$\d+(?:,\d{3})*(?:\s*-\s*\$\d+(?:,\d{3})*)?)',
        r'([£€]\d+(?:,\d{3})*(?:\s*-\s*[£€]\d+(?:,\d{3})*\b)?)',
        r'(\b\d+(?:,\d{3})*\s*(?:USD|EUR|GBP|PKR|USD|INR)\s*per\s*(?:year|month|hour)\b)',
        r'(salary|compensation|pay):\s*([$\w,\s-]+)',
        r'(?:offering|range):\s*(\$\d+(?:,\d{3})*(?:\s*-\s*\$\d+(?:,\d{3})*)?)'
    ]

    for pattern in salary_patterns:
        matches = re.findall(pattern, email_body, re.IGNORECASE)
        if matches:
            # Take the first match
            if isinstance(matches[0], tuple):
                salary_range = ' - '.join([s for s in matches[0] if s.strip()])
            else:
                salary_range = matches[0]
            details['salary'] = salary_range.strip()
            break

    # Extract location
    location_patterns = [
        r'location[:\s]+([A-Z][a-zA-Z\s,]+)',
        r'based\s+in\s+([A-Z][a-zA-Z\s,]+)',
        r'([A-Z][a-zA-Z\s,]+\s+location)',
        r'work(?:\s+from)?\s+([A-Z][a-zA-Z\s,]+)',
        r'position\s+is\s+([A-Z][a-zA-Z\s,]+)'
    ]

    for pattern in location_patterns:
        match = re.search(pattern, email_body, re.IGNORECASE)
        if match:
            details['location'] = match.group(1).strip()
            break

    # Extract contact person
    contact_patterns = [
        r'(?:contact\s+|reach\s+out\s+to\s+|contact:?\s+)?([A-Z][a-zA-Z\s]*\b(?:Manager|Director|Lead|Recruiter|HR|Hiring)\b)',
        r'(?:contact\s+|reach\s+out\s+to\s+|contact:?\s+)?([A-Z][a-zA-Z\s]*[A-Z][a-zA-Z]+)',
        r'(?:regards|sincerely|thanks)\s+([A-Z][a-zA-Z\s]+)'
    ]

    for pattern in contact_patterns:
        matches = re.findall(pattern, email_body, re.IGNORECASE)
        if matches:
            for match in matches:
                if match.strip() and len(match.strip()) < 50 and ' ' in match.strip():  # Ensure it looks like a name
                    details['contact_person'] = match.strip()
                    break
            if details['contact_person']:
                break

    # Extract deadline
    deadline_patterns = [
        r'(?:deadline|due|apply by|response by|end date|closing):\s*([A-Za-z]+\s+\d{1,2},?\s*\d{4})',
        r'(?:deadline|due|apply by|response by|end date|closing)\s+([A-Za-z]+\s+\d{1,2},?\s*\d{4})',
        r'(?:deadline|due|apply by|response by|end date|closing)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:within\s+)?(\d+\s+(?:days?|weeks?|months?))\s+(?:for|to)?\s*(?:apply|respond|reply)'
    ]

    for pattern in deadline_patterns:
        match = re.search(pattern, email_body, re.IGNORECASE)
        if match:
            details['deadline'] = match.group(1).strip()
            break

    # Extract requirements
    # Look for requirements section
    req_section = re.search(r'(?:requirements?|qualifications?|skills|experience):?\s*(.*?)(?:\n\n|\n[A-Z#]|$)', email_body, re.IGNORECASE | re.DOTALL)
    if req_section:
        req_text = req_section.group(1).strip()
        if req_text and len(req_text) < 500:  # Avoid very long text
            details['requirements'].append(req_text)

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

def generate_professional_response(email_info: Dict[str, Any], job_details: Dict[str, Any]) -> str:
    """Generate a professional response that meets the requirements."""
    sender = email_info.get('from', 'Hiring Manager')
    subject = email_info.get('subject', 'regarding the opportunity')

    # Build the response based on available details
    response_parts = []

    # Opening
    response_parts.append(f"Dear {job_details.get('contact_person', 'Hiring Manager')},")
    response_parts.append("")

    # Thank you and interest
    response_parts.append(f"Thank you for reaching out regarding the {job_details.get('position', 'position')} opportunity at {job_details.get('company_name', 'your company')}.")
    response_parts.append("")

    # Express interest
    response_parts.append(f"I am very interested in this position and believe my skills and experience align well with the requirements.")
    response_parts.append("")

    # Ask for clarification if needed
    missing_info_requests = []
    if not job_details.get('position'):
        missing_info_requests.append("the specific role title")
    if not job_details.get('salary'):
        missing_info_requests.append("the salary range")

    if missing_info_requests:
        and_join = " and " if len(missing_info_requests) > 1 else ""
        response_parts.append(f"Could you please provide more details about {and_join.join(missing_info_requests)}?")

    # General interest statement
    if not missing_info_requests:  # Only add if we didn't already ask for details
        response_parts.append(f"I would appreciate the opportunity to discuss this role further and explore how I can contribute to {job_details.get('company_name', 'your organization')}.")

    response_parts.append("")

    # Closing
    response_parts.append("Thank you for your time and consideration.")
    response_parts.append("")
    response_parts.append("Best regards,")
    response_parts.append("AI Employee Assistant")

    # Join all parts and ensure it's under 150 words
    full_response = "\n".join(response_parts)

    # Truncate if necessary to keep under 150 words
    words = full_response.split()
    if len(words) > 150:
        # Try to keep the most essential parts
        truncated_response = " ".join(words[:150])
        return truncated_response + "..."

    return full_response

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
        if APPROVAL_QUEUE_FILE.exists():
            with open(APPROVAL_QUEUE_FILE, 'r') as f:
                queue_data = json.load(f)
        else:
            queue_data = {"pending_approvals": [], "completed_approvals": [], "last_updated": None}

        queue_data["pending_approvals"].append(approval_data)
        queue_data["last_updated"] = datetime.now().isoformat()

        with open(APPROVAL_QUEUE_FILE, 'w') as f:
            json.dump(queue_data, f, indent=2)

        logger.info(f"Saved approval request for: {company} - {position}")

    except Exception as e:
        logger.error(f"Error saving to approval queue: {e}")

def process_work_email_queue():
    """Process emails from work_email_queue.json every 180 seconds as per requirements."""
    logger.info("Processing work email queue...")

    try:
        if not WORK_EMAIL_QUEUE_FILE.exists():
            logger.info("No work email queue file found")
            return {"status": "success", "message": "No work email queue file", "processed_count": 0}

        with open(WORK_EMAIL_QUEUE_FILE, 'r') as f:
            queue_data = json.load(f)

        emails = queue_data.get("emails", [])

        if not emails:
            logger.info("No work emails in queue")
            return {"status": "success", "message": "No work emails to process", "processed_count": 0}

        processed_count = 0
        error_count = 0

        for email in emails:
            try:
                # Check memory usage before processing to avoid memory issues
                memory_percent = get_memory_usage()
                if memory_percent > 80:  # High memory usage
                    logger.warning(f"High memory usage detected: {memory_percent}%. Skipping response generation.")
                    # Store message about system load
                    save_to_approval_queue(
                        company="System Load High",
                        position="System Maintenance",
                        priority="LOW",
                        draft_response="System load high. Awaiting manual review."
                    )
                    continue

                # Extract job details from email
                email_body = email.get('body', email.get('snippet', ''))
                job_details = extract_job_details_from_email(email_body)

                # Assign priority
                priority = assign_priority(email_body, job_details.get('position'), email.get('subject', ''))

                # Generate professional response
                draft_response = generate_professional_response(email, job_details)

                # Save to approval queue (instead of sending automatically)
                save_to_approval_queue(
                    company=job_details.get('company_name', 'Unknown Company'),
                    position=job_details.get('position', 'Unknown Position'),
                    priority=priority,
                    draft_response=draft_response
                )

                processed_count += 1

            except Exception as e:
                logger.error(f"Error processing work email: {e}")
                error_count += 1
                continue

        # Remove processed emails from the queue
        if processed_count > 0:
            queue_data["emails"] = emails[processed_count:]
            queue_data["total_processed"] = queue_data.get("total_processed", 0) + processed_count

            with open(WORK_EMAIL_QUEUE_FILE, 'w') as f:
                json.dump(queue_data, f, indent=2)

        result = {
            "status": "success",
            "message": f"Processed {processed_count} work emails, {error_count} errors",
            "processed_count": processed_count,
            "error_count": error_count
        }

        logger.info(f"Work email processing result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error processing work email queue: {e}")
        return {"status": "error", "message": str(e)}

def process_general_emails():
    """Process emails using the general email processor."""
    logger.info("Checking for general emails...")

    # For general emails, we'll process the general queue file
    try:
        if GENERAL_EMAIL_QUEUE_FILE.exists():
            with open(GENERAL_EMAIL_QUEUE_FILE, 'r') as f:
                queue_data = json.load(f)

            emails = queue_data.get("emails", [])
            if emails:
                logger.info(f"Found {len(emails)} general emails to process")
                # For now, just log and remove from queue - we'll process them differently if needed
                queue_data["emails"] = []
                queue_data["total_processed"] = queue_data.get("total_processed", 0) + len(emails)

                with open(GENERAL_EMAIL_QUEUE_FILE, 'w') as f:
                    json.dump(queue_data, f, indent=2)

                result = {
                    "status": "success",
                    "message": f"Processed {len(emails)} general emails",
                    "processed_count": len(emails)
                }
                logger.info(f"General email processing result: {result}")
                return result
            else:
                return {"status": "success", "message": "No general emails to process", "processed_count": 0}
        else:
            return {"status": "success", "message": "No general email queue file", "processed_count": 0}
    except Exception as e:
        logger.error(f"Error processing general email queue: {e}")
        return {"status": "error", "message": str(e)}

def run():
    """Main processing loop."""
    logger.info("Email Queue Processor started")
    logger.info(f"Work email check interval: {WORK_CHECK_INTERVAL}s, General email check interval: {GENERAL_CHECK_INTERVAL}s")

    # Create necessary directories
    NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Track the last time general emails were processed
    last_general_check = time.time()

    try:
        while True:
            current_time = time.time()
            logger.debug("Checking email queues...")

            # Process work-related emails (every 180 seconds as per requirements)
            work_result = process_work_email_queue()

            # Process general emails (every 60 seconds, but not every loop)
            if current_time - last_general_check >= GENERAL_CHECK_INTERVAL:
                general_result = process_general_emails()
                last_general_check = current_time
            else:
                general_result = {"status": "skipped", "message": "Interval not reached"}

            # Log summary
            logger.info(f"Processing cycle completed - Work emails: {work_result}, General emails: {general_result}")

            # Wait before next check for work emails (180 seconds as per requirements)
            time.sleep(WORK_CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Email Queue Processor stopped by user")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise

if __name__ == "__main__":
    run()