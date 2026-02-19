#!/usr/bin/env python3
"""
Claim-by-move rule enforcement
Prevents both agents from processing the same file
"""
from pathlib import Path
import os

VAULT_PATH = Path(os.getenv('VAULT_PATH', os.path.expanduser('~/AI_Employee_Vault')))
AGENT_ID = os.getenv('AGENT_ID', 'LOCAL')  # or 'CLOUD'

def claim_file(filename):
    """
    Try to claim a file from Needs_Action
    Returns: Path to claimed file if successful, None if already claimed
    """
    needs_action = VAULT_PATH / 'Needs_Action' / filename

    if not needs_action.exists():
        return None

    # Move to In_Progress with agent prefix
    in_progress = VAULT_PATH / 'In_Progress' / f'{AGENT_ID}_{filename}'

    if in_progress.exists():
        # Already claimed by this agent
        return in_progress

    # Check if claimed by other agent
    other_agent = 'CLOUD' if AGENT_ID == 'LOCAL' else 'LOCAL'
    other_claim = VAULT_PATH / 'In_Progress' / f'{other_agent}_{filename}'

    if other_claim.exists():
        print(f"File {filename} already claimed by {other_agent}")
        return None

    # Claim it
    try:
        needs_action.rename(in_progress)
        print(f"✓ Claimed {filename}")
        return in_progress
    except FileNotFoundError:
        # Race condition - other agent claimed it
        return None

def release_file(filename, destination='Done'):
    """
    Release a file after processing
    """
    in_progress = VAULT_PATH / 'In_Progress' / f'{AGENT_ID}_{filename}'

    if not in_progress.exists():
        return False

    dest_dir = VAULT_PATH / destination
    dest_file = dest_dir / filename

    in_progress.rename(dest_file)
    print(f"✓ Released {filename} to {destination}")
    return True

# Example usage in orchestrator:
# claimed = claim_file('EMAIL_123.md')
# if claimed:
#     process(claimed)
#     release_file('EMAIL_123.md', 'Done')
