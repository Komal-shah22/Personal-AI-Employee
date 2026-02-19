#!/usr/bin/env python3
"""
Local agent: Pulls vault changes from Git
Runs on your laptop - pulls drafts from cloud
"""
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path(os.getenv('VAULT_PATH', os.path.expanduser('~/AI_Employee_Vault')))
SYNC_INTERVAL = 120  # 2 minutes

def git_pull():
    """
    Pull latest changes from remote
    """
    os.chdir(VAULT_PATH)

    try:
        # Fetch latest
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True, timeout=30)

        # Check if there are updates
        result = subprocess.run(
            ['git', 'rev-list', 'HEAD...origin/main', '--count'],
            capture_output=True,
            text=True,
            check=True
        )

        commits_behind = int(result.stdout.strip())

        if commits_behind == 0:
            print(f"[{datetime.now()}] Already up to date")
            return False

        print(f"[{datetime.now()}] Pulling {commits_behind} commits...")

        # Pull (rebase to avoid merge commits)
        subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=True)

        print(f"[{datetime.now()}] ✓ Pulled updates")

        # Process new drafts
        process_new_drafts()

        return True

    except subprocess.TimeoutExpired:
        print(f"[{datetime.now()}] ✗ Pull timeout")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] ✗ Pull failed: {e}")
        return False

def process_new_drafts():
    """
    Check for new drafts from cloud and create approval requests
    """
    drafts_dir = VAULT_PATH / 'Drafts'

    if not drafts_dir.exists():
        return

    draft_files = list(drafts_dir.glob('DRAFT_*.md'))

    for draft in draft_files:
        # Read draft content
        content = draft.read_text()

        # Create approval request
        approval_file = VAULT_PATH / 'Pending_Approval' / draft.name.replace('DRAFT_', 'APPROVAL_')

        if approval_file.exists():
            continue  # Already has approval request

        # Copy draft to pending approval
        approval_file.write_text(content)

        print(f"[{datetime.now()}] Created approval request: {approval_file.name}")

def git_commit_local_changes():
    """
    Commit local changes (approvals, done files, dashboard updates)
    """
    os.chdir(VAULT_PATH)

    # Add only local-owned directories
    local_dirs = [
        'Approved/',
        'Rejected/',
        'Done/',
        'Dashboard.md',
        'Logs/local_*.json'
    ]

    for pattern in local_dirs:
        subprocess.run(['git', 'add', pattern], check=False)

    # Commit if there are changes
    status = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )

    if status.stdout.strip():
        commit_msg = f"[LOCAL] Auto-sync {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=False)

        # Push
        try:
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, timeout=30)
            print(f"[{datetime.now()}] ✓ Pushed local changes")
        except:
            print(f"[{datetime.now()}] ✗ Push failed")

def main():
    """Main sync loop"""
    print(f"Starting local vault sync (interval: {SYNC_INTERVAL}s)")

    while True:
        try:
            # Pull from cloud
            git_pull()

            # Push local changes
            git_commit_local_changes()

            time.sleep(SYNC_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopping local sync...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(SYNC_INTERVAL)

if __name__ == '__main__':
    main()
