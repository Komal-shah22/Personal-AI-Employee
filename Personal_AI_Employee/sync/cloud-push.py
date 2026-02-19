#!/usr/bin/env python3
"""
Cloud agent: Pushes vault changes to Git
Runs on Oracle VM - pushes drafts and plans
"""
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path(os.getenv('VAULT_PATH', '/app/vault'))
SYNC_INTERVAL = 120  # 2 minutes

def git_commit_and_push():
    """
    Commit vault changes and push to remote
    """
    os.chdir(VAULT_PATH)

    # Check if there are changes
    status = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )

    if not status.stdout.strip():
        print(f"[{datetime.now()}] No changes to sync")
        return False

    print(f"[{datetime.now()}] Changes detected, syncing...")

    # Add only safe directories
    safe_dirs = [
        'Needs_Action/',
        'In_Progress/CLOUD_*',
        'Plans/',
        'Drafts/',
        'Logs/*.json',
        'Updates/'
    ]

    for pattern in safe_dirs:
        subprocess.run(['git', 'add', pattern], check=False)

    # Commit
    commit_msg = f"[CLOUD] Auto-sync {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    subprocess.run(['git', 'commit', '-m', commit_msg], check=False)

    # Push to remote
    try:
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, timeout=30)
        print(f"[{datetime.now()}] ✓ Pushed to remote")
        return True
    except subprocess.TimeoutExpired:
        print(f"[{datetime.now()}] ✗ Push timeout")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] ✗ Push failed: {e}")
        return False

def main():
    """Main sync loop"""
    print(f"Starting cloud vault sync (interval: {SYNC_INTERVAL}s)")

    while True:
        try:
            git_commit_and_push()
            time.sleep(SYNC_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopping cloud sync...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(SYNC_INTERVAL)

if __name__ == '__main__':
    main()
