"""
Cloud orchestrator - DRAFT MODE ONLY
Never performs actual send operations
"""
import os
import time
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path(os.getenv('VAULT_PATH', '/app/AI_Employee_Vault'))
MODE = os.getenv('MODE', 'local')

def cloud_orchestrator():
    """
    Cloud version - creates drafts, never sends
    """
    if MODE != 'cloud':
        print("ERROR: This script only runs in cloud mode")
        return

    print(f"[CLOUD] Starting orchestrator at {datetime.now()}")

    while True:
        try:
            # Check Needs_Action
            needs_action = VAULT_PATH / 'Needs_Action'
            files = list(needs_action.glob('*.md'))

            for file in files:
                # Skip if already being processed
                if file.stem.startswith('_'):
                    continue

                # Mark as in-progress
                in_progress_file = VAULT_PATH / 'In_Progress' / f'CLOUD_{file.name}'
                file.rename(in_progress_file)

                # Read file, determine type
                content = in_progress_file.read_text()

                # Process based on type
                if 'type: email' in content:
                    process_email_draft(in_progress_file)
                elif 'type: social_post' in content:
                    process_social_draft(in_progress_file)

                # Move to Drafts (not Approved - cloud can't approve)
                draft_file = VAULT_PATH / 'Drafts' / f'DRAFT_{file.name}'
                in_progress_file.rename(draft_file)

                print(f"[CLOUD] Created draft: {draft_file.name}")

            time.sleep(60)  # Check every minute

        except Exception as e:
            print(f"[CLOUD] Error: {e}")
            time.sleep(60)

def process_email_draft(file_path):
    """Create email draft without sending"""
    # Read email request
    # Generate reply using Claude
    # Save draft to /Drafts/ folder
    # Add approval request metadata
    pass

def process_social_draft(file_path):
    """Create social media post draft without posting"""
    # Read post request
    # Generate post content
    # Save draft to /Drafts/
    # Add approval metadata
    pass

if __name__ == '__main__':
    cloud_orchestrator()
