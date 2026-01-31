#!/usr/bin/env python3
"""
Test script to run the Personal AI Employee skills
"""

import os
import sys
from pathlib import Path

def run_process_emails():
    """Run the process-emails skill"""
    print("Testing process-emails skill...")

    # Import and run the skill
    try:
        sys.path.append(os.getcwd())
        from claude.skills.process_emails.skill import run_skill
        result = run_skill()
        print(f"process-emails result: {result}")
    except ImportError as e:
        print(f"Could not import process-emails: {e}")
        print("This skill needs to be run via Claude Code CLI")

        # Alternative: run directly if file exists
        skill_path = Path(".claude/skills/process-emails/skill.py")
        if skill_path.exists():
            import subprocess
            try:
                result = subprocess.run([sys.executable, str(skill_path)],
                                      capture_output=True, text=True, timeout=30)
                print(f"Direct execution stdout: {result.stdout}")
                if result.stderr:
                    print(f"Direct execution stderr: {result.stderr}")
                print(f"Return code: {result.returncode}")
            except subprocess.TimeoutExpired:
                print("Skill execution timed out")
        else:
            print("Skill file does not exist at expected location")

def run_process_tasks():
    """Run the process-tasks skill"""
    print("\nTesting process-tasks skill...")

    skill_path = Path(".claude/skills/process-tasks/skill.py")
    if skill_path.exists():
        import subprocess
        try:
            result = subprocess.run([sys.executable, str(skill_path)],
                                  capture_output=True, text=True, timeout=30)
            print(f"process-tasks stdout: {result.stdout}")
            if result.stderr:
                print(f"process-tasks stderr: {result.stderr}")
            print(f"Return code: {result.returncode}")
        except subprocess.TimeoutExpired:
            print("Skill execution timed out")
    else:
        print("process-tasks skill file does not exist")

def run_update_dashboard():
    """Run the update-dashboard skill"""
    print("\nTesting update-dashboard skill...")

    skill_path = Path(".claude/skills/update-dashboard/skill.py")
    if skill_path.exists():
        import subprocess
        try:
            result = subprocess.run([sys.executable, str(skill_path)],
                                  capture_output=True, text=True, timeout=30)
            print(f"update-dashboard stdout: {result.stdout}")
            if result.stderr:
                print(f"update-dashboard stderr: {result.stderr}")
            print(f"Return code: {result.returncode}")
        except subprocess.TimeoutExpired:
            print("Skill execution timed out")
    else:
        print("update-dashboard skill file does not exist")

if __name__ == "__main__":
    print("Running Personal AI Employee skills test...")

    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    run_process_emails()
    run_process_tasks()
    run_update_dashboard()

    print("\nSkills test completed!")
    print("\nTo run the skills properly, use these Claude Code commands:")
    print("claude skill process-emails")
    print("claude skill process-tasks")
    print("claude skill update-dashboard")