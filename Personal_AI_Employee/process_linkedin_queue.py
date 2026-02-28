#!/usr/bin/env python3
"""
Process LinkedIn posts from dashboard queue
Integrates dashboard with existing LinkedIn skill
"""

import os
import json
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path('AI_Employee_Vault')
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
PENDING_APPROVAL = VAULT_PATH / 'Pending_Approval'
DONE = VAULT_PATH / 'Done'

# Ensure directories exist
PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)
DONE.mkdir(parents=True, exist_ok=True)

def process_linkedin_posts():
    """Process LinkedIn posts from dashboard queue"""
    
    linkedin_files = list(NEEDS_ACTION.glob('LINKEDIN_DASHBOARD_*.md'))
    
    if not linkedin_files:
        print("No LinkedIn posts in queue")
        return
    
    print(f"Found {len(linkedin_files)} LinkedIn posts to process")
    
    for file_path in linkedin_files:
        print(f"\nProcessing: {file_path.name}")
        
        # Read the post
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract post content
        lines = content.split('\n')
        post_content = []
        in_content = False
        
        for line in lines:
            if line.strip() == '## Post Content':
                in_content = True
                continue
            elif line.strip().startswith('##') and in_content:
                break
            elif in_content and line.strip():
                post_content.append(line.strip())
        
        post_text = '\n'.join(post_content)
        
        if not post_text or post_text == 'hello':
            print(f"  [SKIP] Test post: {file_path.name}")
            # Move to done
            done_path = DONE / file_path.name
            file_path.rename(done_path)
            continue
        
        # Create approval file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        approval_file = PENDING_APPROVAL / f'LINKEDIN_APPROVAL_{timestamp}.md'
        
        approval_content = f"""---
type: linkedin_post
source: dashboard
status: pending_approval
created: {datetime.now().isoformat()}
original_file: {file_path.name}
---

# LinkedIn Post - Pending Approval

## Post Content

{post_text}

## Validation

- Character count: {len(post_text)}
- Source: Dashboard Quick Action
- Status: Ready for review

## Approval Instructions

[OK] To Approve: Run `python post_linkedin_direct.py "content"`
[X] To Reject: Delete this file
[EDIT] To Edit: Modify content above, then approve

---
*Queued from Dashboard: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(approval_file, 'w', encoding='utf-8') as f:
            f.write(approval_content)
        
        # Move original to done
        done_path = DONE / file_path.name
        file_path.rename(done_path)
        
        print(f"  [OK] Moved to approval: {approval_file.name}")
        print(f"  [OK] Original archived: {done_path.name}")

    print(f"\n[SUCCESS] Processed {len(linkedin_files)} posts")
    print(f"[INFO] Check: {PENDING_APPROVAL}")

if __name__ == '__main__':
    process_linkedin_posts()
