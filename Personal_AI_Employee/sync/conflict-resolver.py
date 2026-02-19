#!/usr/bin/env python3
"""
Automatic conflict resolution for vault sync
"""
import os
import subprocess
from pathlib import Path

VAULT_PATH = Path(os.getenv('VAULT_PATH'))

def resolve_conflicts():
    """
    Resolve common sync conflicts automatically
    """
    os.chdir(VAULT_PATH)

    # Check for conflicts
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=U'],
        capture_output=True,
        text=True
    )

    conflicted_files = result.stdout.strip().split('\n')

    if not conflicted_files or conflicted_files == ['']:
        return

    print(f"Found {len(conflicted_files)} conflicts")

    for file in conflicted_files:
        resolve_file_conflict(file)

def resolve_file_conflict(filepath):
    """
    Resolve conflict for a single file

    Strategy:
    - Dashboard.md: Always keep local version
    - Logs/*.json: Merge both (append)
    - Approved/*, Rejected/*: Keep local
    - Plans/*, Drafts/*: Keep cloud (newer)
    """
    file_path = VAULT_PATH / filepath

    if not file_path.exists():
        return

    # Read conflict markers
    content = file_path.read_text()

    if 'Dashboard.md' in filepath:
        # Keep local version (ours)
        subprocess.run(['git', 'checkout', '--ours', filepath])
        subprocess.run(['git', 'add', filepath])
        print(f"✓ Resolved {filepath} (kept local)")

    elif filepath.startswith('Approved/') or filepath.startswith('Rejected/'):
        # Keep local version
        subprocess.run(['git', 'checkout', '--ours', filepath])
        subprocess.run(['git', 'add', filepath])
        print(f"✓ Resolved {filepath} (kept local)")

    elif filepath.startswith('Plans/') or filepath.startswith('Drafts/'):
        # Keep cloud version (theirs)
        subprocess.run(['git', 'checkout', '--theirs', filepath])
        subprocess.run(['git', 'add', filepath])
        print(f"✓ Resolved {filepath} (kept cloud)")

    elif filepath.startswith('Logs/'):
        # Merge both versions
        merge_log_file(file_path)
        subprocess.run(['git', 'add', filepath])
        print(f"✓ Resolved {filepath} (merged)")

def merge_log_file(file_path):
    """
    Merge log file conflicts by combining both versions
    """
    content = file_path.read_text()

    # Extract both versions from conflict markers
    # <<<<<<< HEAD
    # local content
    # =======
    # cloud content
    # >>>>>>> branch

    parts = content.split('=======')
    if len(parts) != 2:
        return

    local_part = parts[0].split('<<<<<<< HEAD')[1] if '<<<<<<< HEAD' in parts[0] else ''
    cloud_part = parts[1].split('>>>>>>>')[0] if '>>>>>>>' in parts[1] else ''

    # Combine both (append cloud to local)
    merged = local_part.strip() + '\n' + cloud_part.strip()

    file_path.write_text(merged)

if __name__ == '__main__':
    resolve_conflicts()
