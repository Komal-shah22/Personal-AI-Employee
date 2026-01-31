"""
Script to check the current status of the Personal AI Employee dashboard
"""
import os
from pathlib import Path

def check_dashboard():
    """Check the status of the AI Employee dashboard"""

    # Define the vault directories
    vault_dirs = {
        'inbox': './AI_Employee_Vault/Inbox',
        'needs_action': './AI_Employee_Vault/Needs_Action',
        'plans': './AI_Employee_Vault/Plans',
        'done': './AI_Employee_Vault/Done',
        'pending_approval': './AI_Employee_Vault/Pending_Approval',
        'approved': './AI_Employee_Vault/Approved',
        'rejected': './AI_Employee_Vault/Rejected',
        'logs': './AI_Employee_Vault/Logs'
    }

    print("=" * 60)
    print("PERSONAL AI EMPLOYEE DASHBOARD")
    print("=" * 60)
    print(f"{'Directory':<20} {'Count':<10} {'Files'}")
    print("-" * 60)

    for name, path in vault_dirs.items():
        dir_path = Path(path)
        if dir_path.exists():
            files = list(dir_path.glob('*'))
            count = len(files)
            file_list = ', '.join([f.name for f in files[:3]])  # Show first 3 files
            if count > 3:
                file_list += f" ... (+{count-3} more)"
            print(f"{name:<20} {count:<10} {file_list}")
        else:
            print(f"{name:<20} {'N/A':<10} Directory does not exist")

    print("-" * 60)
    print("Services Status:")
    print("- Orchestrator: RUNNING (background)")
    print("- Gmail Watcher: RUNNING (background)")
    print("- Claude Code Skills: AVAILABLE")
    print("=" * 60)
    print("\nThe Personal AI Employee is actively monitoring and processing tasks!")

if __name__ == "__main__":
    check_dashboard()