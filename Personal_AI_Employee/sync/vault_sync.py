#!/usr/bin/env python3
"""
Cloud-Local Vault Synchronization System

Synchronizes AI Employee Vault between cloud (Oracle) and local machine using Git.

Work Zones:
- CLOUD owns: /Needs_Action/, /Plans/, /Drafts/ (triage, drafts, no real actions)
- LOCAL owns: /Approved/, /Done/, Dashboard.md (approvals, sensitive ops)

Sync Strategy:
- Cloud: Auto-commit and push after file creation
- Local: Pull every 2 minutes
- Claim-by-move: First to move file to /In_Progress/[agent_name]/ owns it

Usage:
    python sync/vault_sync.py --mode [cloud|local]

Configuration:
    Set SYNC_MODE environment variable or use --mode flag
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
import argparse
import hashlib

# Configuration
VAULT_DIR = Path('AI_Employee_Vault')
SYNC_STATE_FILE = Path('.vault_sync_state.json')
AGENT_NAME = os.getenv('AGENT_NAME', 'local')  # 'cloud' or 'local'

# Work zone definitions
CLOUD_ZONES = ['Needs_Action', 'Plans', 'Drafts']
LOCAL_ZONES = ['Approved', 'Done', 'Pending_Approval']
SHARED_ZONES = ['In_Progress', 'Logs', 'Briefings']

# Files that should never be synced
NEVER_SYNC = [
    '.env',
    '.env.local',
    '.env.cloud',
    'sessions/',
    'credentials/',
    '*.key',
    '*.pem',
    '*.p12',
    'token.json',
    'token.pickle',
    '.whatsapp_processed.json',
    '.processed_ids.json'
]


class VaultSync:
    def __init__(self, mode='local'):
        self.mode = mode
        self.agent_name = f"{mode}_agent"
        self.vault_dir = VAULT_DIR
        self.state = self.load_state()

    def load_state(self):
        """Load sync state from file"""
        if SYNC_STATE_FILE.exists():
            try:
                with open(SYNC_STATE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.log(f"Failed to load state: {e}", "WARNING")

        return {
            'last_sync': None,
            'claimed_files': {},
            'last_commit': None
        }

    def save_state(self):
        """Save sync state to file"""
        try:
            with open(SYNC_STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            self.log(f"Failed to save state: {e}", "ERROR")

    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.mode.upper()}] [{level}] {message}")

    def run_git_command(self, command, check=True):
        """Run git command in vault directory"""
        try:
            result = subprocess.run(
                command,
                cwd=self.vault_dir,
                capture_output=True,
                text=True,
                check=check
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except Exception as e:
            return False, "", str(e)

    def check_git_repo(self):
        """Check if vault is a git repository"""
        git_dir = self.vault_dir / '.git'
        if not git_dir.exists():
            self.log("Vault is not a git repository", "ERROR")
            self.log("Run sync/setup_git_sync.sh first", "ERROR")
            return False
        return True

    def git_pull(self):
        """Pull latest changes from remote"""
        self.log("Pulling latest changes...")

        # Fetch first
        success, stdout, stderr = self.run_git_command(['git', 'fetch', 'origin'])
        if not success:
            self.log(f"Git fetch failed: {stderr}", "ERROR")
            return False

        # Check for conflicts
        success, stdout, stderr = self.run_git_command(['git', 'status', '--porcelain'])
        if stdout.strip():
            self.log("Local changes detected, stashing...", "WARNING")
            self.run_git_command(['git', 'stash'])

        # Pull with rebase
        success, stdout, stderr = self.run_git_command(['git', 'pull', '--rebase', 'origin', 'main'])

        if not success:
            self.log(f"Git pull failed: {stderr}", "ERROR")
            # Try to recover
            self.run_git_command(['git', 'rebase', '--abort'], check=False)
            return False

        self.log("Pull completed successfully")
        return True

    def git_push(self):
        """Push local changes to remote"""
        self.log("Pushing changes to remote...")

        success, stdout, stderr = self.run_git_command(['git', 'push', 'origin', 'main'])

        if not success:
            self.log(f"Git push failed: {stderr}", "ERROR")
            return False

        self.log("Push completed successfully")
        return True

    def git_commit(self, message):
        """Commit changes with message"""
        # Add all changes in vault
        success, stdout, stderr = self.run_git_command(['git', 'add', '.'])
        if not success:
            self.log(f"Git add failed: {stderr}", "ERROR")
            return False

        # Check if there are changes to commit
        success, stdout, stderr = self.run_git_command(['git', 'status', '--porcelain'])
        if not stdout.strip():
            self.log("No changes to commit", "INFO")
            return True

        # Commit
        commit_message = f"[{self.agent_name}] {message}"
        success, stdout, stderr = self.run_git_command(['git', 'commit', '-m', commit_message])

        if not success:
            self.log(f"Git commit failed: {stderr}", "ERROR")
            return False

        self.log(f"Committed: {message}")
        self.state['last_commit'] = datetime.now().isoformat()
        self.save_state()
        return True

    def can_access_zone(self, zone_name):
        """Check if this agent can write to a zone"""
        if self.mode == 'cloud':
            return zone_name in CLOUD_ZONES or zone_name in SHARED_ZONES
        else:  # local
            return zone_name in LOCAL_ZONES or zone_name in SHARED_ZONES

    def claim_file(self, file_path):
        """Attempt to claim a file by moving to In_Progress"""
        if not file_path.exists():
            return False

        # Create In_Progress directory for this agent
        in_progress_dir = self.vault_dir / 'In_Progress' / self.agent_name
        in_progress_dir.mkdir(parents=True, exist_ok=True)

        # Target path
        target_path = in_progress_dir / file_path.name

        # Check if already claimed by another agent
        for agent_dir in (self.vault_dir / 'In_Progress').glob('*'):
            if agent_dir.is_dir() and agent_dir.name != self.agent_name:
                claimed_file = agent_dir / file_path.name
                if claimed_file.exists():
                    self.log(f"File already claimed by {agent_dir.name}: {file_path.name}", "INFO")
                    return False

        # Move file to claim it
        try:
            file_path.rename(target_path)
            self.log(f"Claimed file: {file_path.name}", "INFO")

            # Record claim
            self.state['claimed_files'][str(target_path)] = {
                'claimed_at': datetime.now().isoformat(),
                'original_path': str(file_path)
            }
            self.save_state()

            # Commit the claim
            self.git_commit(f"Claim file: {file_path.name}")

            return True
        except Exception as e:
            self.log(f"Failed to claim file: {e}", "ERROR")
            return False

    def process_needs_action(self):
        """Process files in Needs_Action directory"""
        needs_action_dir = self.vault_dir / 'Needs_Action'

        if not needs_action_dir.exists():
            return

        # Find files to process
        for file_path in needs_action_dir.glob('*.md'):
            # Skip files starting with underscore (temp files)
            if file_path.name.startswith('_'):
                continue

            # Attempt to claim
            if self.claim_file(file_path):
                self.log(f"Processing: {file_path.name}", "INFO")
                # File is now in In_Progress/[agent_name]/
                # Orchestrator will pick it up from there

    def merge_dashboard_updates(self):
        """Merge Updates/*.md into Dashboard.md (LOCAL ONLY)"""
        if self.mode != 'local':
            return

        updates_dir = self.vault_dir / 'Updates'
        dashboard_file = Path('Dashboard.md')

        if not updates_dir.exists():
            return

        # Find update files
        update_files = sorted(updates_dir.glob('*.md'))

        if not update_files:
            return

        self.log(f"Merging {len(update_files)} dashboard updates...", "INFO")

        # Read current dashboard
        if dashboard_file.exists():
            dashboard_content = dashboard_file.read_text(encoding='utf-8')
        else:
            dashboard_content = "# AI Employee Dashboard\n\n"

        # Append updates
        for update_file in update_files:
            update_content = update_file.read_text(encoding='utf-8')

            # Add separator
            dashboard_content += f"\n\n---\n\n"
            dashboard_content += f"## Update: {update_file.stem}\n\n"
            dashboard_content += update_content

            # Move to processed
            processed_dir = updates_dir / 'processed'
            processed_dir.mkdir(exist_ok=True)
            update_file.rename(processed_dir / update_file.name)

        # Write updated dashboard
        dashboard_file.write_text(dashboard_content, encoding='utf-8')

        self.log("Dashboard updates merged", "INFO")

        # Commit
        self.git_commit("Merge dashboard updates")

    def sync_cloud_mode(self):
        """Sync in cloud mode"""
        self.log("Starting cloud sync cycle...")

        # Pull latest changes
        if not self.git_pull():
            self.log("Pull failed, skipping this cycle", "ERROR")
            return

        # Process files in Needs_Action
        self.process_needs_action()

        # Push any changes
        self.git_push()

        self.state['last_sync'] = datetime.now().isoformat()
        self.save_state()

    def sync_local_mode(self):
        """Sync in local mode"""
        self.log("Starting local sync cycle...")

        # Pull latest changes
        if not self.git_pull():
            self.log("Pull failed, skipping this cycle", "ERROR")
            return

        # Merge dashboard updates
        self.merge_dashboard_updates()

        # Process files in Needs_Action
        self.process_needs_action()

        # Push any changes
        self.git_push()

        self.state['last_sync'] = datetime.now().isoformat()
        self.save_state()

    def run_once(self):
        """Run one sync cycle"""
        if not self.check_git_repo():
            return False

        try:
            if self.mode == 'cloud':
                self.sync_cloud_mode()
            else:
                self.sync_local_mode()

            return True
        except Exception as e:
            self.log(f"Sync cycle failed: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False

    def run_continuous(self, interval=120):
        """Run continuous sync loop"""
        self.log(f"Starting continuous sync (interval: {interval}s)")

        try:
            while True:
                self.run_once()
                self.log(f"Next sync in {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            self.log("Sync stopped by user", "INFO")
        except Exception as e:
            self.log(f"Sync loop failed: {e}", "ERROR")
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Vault Sync System')
    parser.add_argument('--mode', choices=['cloud', 'local'], required=True,
                        help='Sync mode: cloud or local')
    parser.add_argument('--once', action='store_true',
                        help='Run once and exit (default: continuous)')
    parser.add_argument('--interval', type=int, default=120,
                        help='Sync interval in seconds (default: 120)')

    args = parser.parse_args()

    # Set agent name based on mode
    os.environ['AGENT_NAME'] = f"{args.mode}_agent"

    # Create sync instance
    sync = VaultSync(mode=args.mode)

    # Run
    if args.once:
        success = sync.run_once()
        sys.exit(0 if success else 1)
    else:
        sync.run_continuous(interval=args.interval)


if __name__ == '__main__':
    main()
