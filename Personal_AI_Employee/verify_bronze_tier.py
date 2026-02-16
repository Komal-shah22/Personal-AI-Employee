"""
Bronze Tier Verification Script
Tests all Bronze Tier requirements
"""

import os
import sys
from pathlib import Path
import json

class BronzeTierVerifier:
    def __init__(self):
        self.results = {
            'folder_structure': False,
            'config_file': False,
            'gmail_watcher': False,
            'whatsapp_watcher': False,
            'orchestrator': False,
            'agent_skills': False,
            'dashboard': False
        }
        self.issues = []

    def check_folder_structure(self):
        """Verify all required folders exist"""
        print("\n=== Checking Folder Structure ===")
        required_folders = [
            'AI_Employee_Vault',
            'AI_Employee_Vault/Inbox',
            'AI_Employee_Vault/Needs_Action',
            'AI_Employee_Vault/Done',
            'AI_Employee_Vault/Pending_Approval',
            'AI_Employee_Vault/Approved',
            'AI_Employee_Vault/Plans',
            'AI_Employee_Vault/Logs',
            'AI_Employee_Vault/Briefings',
            'AI_Employee_Vault/Invoices'
        ]

        all_exist = True
        for folder in required_folders:
            path = Path(folder)
            if path.exists():
                print(f"[OK] {folder}")
            else:
                print(f"[FAIL] {folder} - MISSING")
                self.issues.append(f"Missing folder: {folder}")
                all_exist = False

        self.results['folder_structure'] = all_exist
        return all_exist

    def check_config_file(self):
        """Verify config.json exists and is valid"""
        print("\n=== Checking Config File ===")
        config_path = Path('config.json')

        if not config_path.exists():
            print("[FAIL] config.json - MISSING")
            self.issues.append("config.json not found")
            return False

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            required_keys = ['directories', 'watchers', 'mcp_servers', 'ai_settings']
            missing_keys = [key for key in required_keys if key not in config]

            if missing_keys:
                print(f"[FAIL] config.json - Missing keys: {missing_keys}")
                self.issues.append(f"config.json missing keys: {missing_keys}")
                return False

            print("[OK] config.json - Valid")
            self.results['config_file'] = True
            return True

        except json.JSONDecodeError as e:
            print(f"[FAIL] config.json - Invalid JSON: {e}")
            self.issues.append(f"config.json invalid: {e}")
            return False

    def check_gmail_watcher(self):
        """Check if Gmail watcher exists"""
        print("\n=== Checking Gmail Watcher ===")
        watcher_path = Path('watchers/gmail_watcher.py')

        if not watcher_path.exists():
            print("[FAIL] gmail_watcher.py - MISSING")
            self.issues.append("Gmail watcher not found")
            return False

        print("[OK] gmail_watcher.py - EXISTS")

        # Check for credentials
        creds_path = Path('credentials.json')
        token_path = Path('token.json')

        if creds_path.exists():
            print("[OK] credentials.json - EXISTS")
        else:
            print("[WARN]  credentials.json - MISSING (needed for Gmail API)")
            self.issues.append("Gmail credentials.json not configured")

        if token_path.exists():
            print("[OK] token.json - EXISTS")
        else:
            print("[WARN]  token.json - MISSING (will be created on first run)")

        self.results['gmail_watcher'] = True
        return True

    def check_whatsapp_watcher(self):
        """Check if WhatsApp watcher exists"""
        print("\n=== Checking WhatsApp Watcher ===")
        watcher_path = Path('watchers/whatsapp_watcher.py')

        if not watcher_path.exists():
            print("[FAIL] whatsapp_watcher.py - MISSING")
            self.issues.append("WhatsApp watcher not found")
            return False

        print("[OK] whatsapp_watcher.py - EXISTS")

        # Check if playwright is installed
        try:
            import playwright
            print("[OK] playwright - INSTALLED")
        except ImportError:
            print("[FAIL] playwright - NOT INSTALLED")
            print("   Run: pip install playwright && playwright install chromium")
            self.issues.append("playwright not installed")
            return False

        self.results['whatsapp_watcher'] = True
        return True

    def check_orchestrator(self):
        """Check if orchestrator exists"""
        print("\n=== Checking Orchestrator ===")
        orch_path = Path('orchestrator.py')

        if not orch_path.exists():
            print("[FAIL] orchestrator.py - MISSING")
            self.issues.append("orchestrator.py not found")
            return False

        print("[OK] orchestrator.py - EXISTS")

        # Check for key methods
        with open(orch_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_methods = [
            'analyze_content',
            'generate_invoice',
            'create_approval_request',
            'execute_approved_action'
        ]

        for method in required_methods:
            if f"def {method}" in content:
                print(f"[OK] Method: {method}")
            else:
                print(f"[FAIL] Method: {method} - MISSING")
                self.issues.append(f"orchestrator.py missing method: {method}")
                return False

        self.results['orchestrator'] = True
        return True

    def check_agent_skills(self):
        """Check if agent skills exist"""
        print("\n=== Checking Agent Skills ===")
        skills_dir = Path('.claude/skills')

        if not skills_dir.exists():
            print("[FAIL] .claude/skills - MISSING")
            self.issues.append(".claude/skills directory not found")
            return False

        required_skills = [
            'update-dashboard',
            'generate-reports',
            'linkedin-skill',
            'post-social'
        ]

        all_exist = True
        for skill in required_skills:
            skill_path = skills_dir / skill
            if skill_path.exists():
                print(f"[OK] {skill}")
            else:
                print(f"[FAIL] {skill} - MISSING")
                self.issues.append(f"Skill missing: {skill}")
                all_exist = False

        self.results['agent_skills'] = all_exist
        return all_exist

    def check_dashboard(self):
        """Check if dashboard exists"""
        print("\n=== Checking Dashboard ===")
        dashboard_path = Path('Dashboard.md')

        if not dashboard_path.exists():
            print("[FAIL] Dashboard.md - MISSING")
            self.issues.append("Dashboard.md not found")
            return False

        print("[OK] Dashboard.md - EXISTS")
        self.results['dashboard'] = True
        return True

    def run_verification(self):
        """Run all verification checks"""
        print("=" * 60)
        print("BRONZE TIER VERIFICATION")
        print("=" * 60)

        self.check_folder_structure()
        self.check_config_file()
        self.check_gmail_watcher()
        self.check_whatsapp_watcher()
        self.check_orchestrator()
        self.check_agent_skills()
        self.check_dashboard()

        # Summary
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)

        total = len(self.results)
        passed = sum(1 for v in self.results.values() if v)

        for component, status in self.results.items():
            status_icon = "[OK]" if status else "[FAIL]"
            print(f"{status_icon} {component.replace('_', ' ').title()}")

        print(f"\nScore: {passed}/{total} ({int(passed/total*100)}%)")

        if self.issues:
            print("\n[WARN]  ISSUES FOUND:")
            for issue in self.issues:
                print(f"  - {issue}")

        if passed == total:
            print("\n[SUCCESS] BRONZE TIER: CERTIFIED [OK]")
            return True
        else:
            print("\n[FAIL] BRONZE TIER: NOT CERTIFIED")
            print("Please fix the issues above and run verification again.")
            return False

if __name__ == "__main__":
    verifier = BronzeTierVerifier()
    success = verifier.run_verification()
    sys.exit(0 if success else 1)
