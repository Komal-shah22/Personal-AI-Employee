"""
Test script to demonstrate the Personal AI Employee functionality
"""

import os
from datetime import datetime
from pathlib import Path

def create_test_email():
    """Create a test email file to simulate incoming mail"""
    needs_action_dir = Path("Needs_Action")

    # Create a test email that needs action
    email_content = f"""---
type: email
from: client@example.com
subject: Urgent: Invoice Needed for Project Alpha
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## Email Content
Hi, could you please send me the invoice for Project Alpha? We need to process the payment by the end of the week.

## Suggested Actions
- [ ] Generate invoice for Project Alpha
- [ ] Send via email to client@example.com
- [ ] Log transaction in accounting system
"""

    email_file = needs_action_dir / f"TEST_EMAIL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(email_file, 'w') as f:
        f.write(email_content)

    print(f"Created test email: {email_file}")

def create_test_file_drop():
    """Create a test file drop to simulate a file being placed in inbox"""
    inbox_dir = Path("Inbox")

    # Create a test file
    test_file = inbox_dir / "contract_draft.pdf"
    test_file.write_text("This is a sample contract draft that needs review.")

    print(f"Created test file drop: {test_file}")

def create_test_business_goal():
    """Create a test business goal for the AI to track"""
    goals_content = """# Business Goals - Test

---
last_updated: 2026-01-30
review_frequency: weekly
---

## Current Objective
- Complete onboarding of Personal AI Employee
- Process 5 test transactions
- Generate first weekly report
"""

    goals_file = Path("Business_Goals.md")
    with open(goals_file, 'w') as f:
        f.write(goals_content)

    print(f"Updated Business_Goals.md with test content")

if __name__ == "__main__":
    print("Creating test data for Personal AI Employee...")

    # Create test data
    create_test_email()
    create_test_file_drop()
    create_test_business_goal()

    print("\nTest data created successfully!")
    print("You can now run the orchestrator to process these items:")
    print("python orchestrator.py")