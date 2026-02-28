#!/usr/bin/env python3
"""
Create a new test post to verify the complete LinkedIn queue workflow works with your configuration
"""
import json
from datetime import datetime
from pathlib import Path
import os

def create_new_test_post():
    """Create a new LinkedIn test post to verify the complete workflow"""

    # Create timestamp
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    # Get vault path with fallback to parent directory
    vault_path = Path(os.environ.get('VAULT_PATH', Path(__file__).parent))
    needs_action_path = vault_path / 'AI_Employee_Vault' / 'Needs_Action'

    # Create directory if it doesn't exist
    needs_action_path.mkdir(parents=True, exist_ok=True)

    # Create filename
    filename = f"LINKEDIN_DASHBOARD_{timestamp}.md"
    filepath = needs_action_path / filename

    # Create test post content
    test_content = "Testing AI Employee Dashboard with direct posting fallback! #AI #Automation #LinkedIn"

    file_content = f"""---
type: social_post
platform: linkedin
from: dashboard_test
priority: normal
status: pending
created: {datetime.now().isoformat()}
source: dashboard_queue_test
---

# LinkedIn Post Request from Dashboard

## Post Content

{test_content}

## Action Required

This LinkedIn post was created via the dashboard queue test and requires processing by the orchestrator.

**Character Count:** {len(test_content)} / 3000

---
*Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Write file to Needs_Action
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)

    print(f"Created test queue post: {filepath}")
    print(f"Content: {test_content}")
    return filepath

if __name__ == '__main__':
    print("Creating test LinkedIn post for workflow verification...")
    filepath = create_new_test_post()
    print(f"\nTest post created successfully at: {filepath}")
    print("The orchestrator should process this through the complete workflow.")