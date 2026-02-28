#!/usr/bin/env python3
"""
Create a queue-based LinkedIn post directly
"""

import json
from datetime import datetime
from pathlib import Path
import os

def create_linkedin_queue_post(content, image_url=None):
    """Create a LinkedIn post in the queue"""
    # Create timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')

    # Get vault path with fallback to parent directory
    vault_path = Path(os.environ.get('VAULT_PATH', Path(__file__).parent / 'AI_Employee_Vault'))
    needs_action_path = vault_path / 'Needs_Action'

    # Create directory if it doesn't exist
    needs_action_path.mkdir(parents=True, exist_ok=True)

    # Create filename
    filename = f"LINKEDIN_DASHBOARD_{timestamp}.md"
    filepath = needs_action_path / filename

    # Create file content
    file_content = f"""---
type: social_post
platform: linkedin
from: direct_script
priority: normal
status: pending
created: {datetime.utcnow().isoformat()}
source: direct_queue_creation
{f"image_url: {image_url}" if image_url else ""}
---

# LinkedIn Post Request from Direct Script

## Post Content

{content}

{f"## Image\n\n![Post Image]({image_url})\n" if image_url else ""}

## Action Required

This LinkedIn post was created via direct script and requires processing by the orchestrator.

**Character Count:** {len(content)} / 3000

---
*Created: {datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}*
"""

    # Write file to Needs_Action
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)

    print(f"Created LinkedIn queue post: {filepath}")
    print(f"Content: {content}")
    return filepath

if __name__ == '__main__':
    content = "Testing AI Employee Dashboard! #AI #Automation"
    filepath = create_linkedin_queue_post(content)
    print(f"\nPost created successfully at: {filepath}")
    print("The orchestrator will process this post automatically.")