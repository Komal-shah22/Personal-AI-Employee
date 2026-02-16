#!/usr/bin/env python3
"""
System Verification Script
Checks if all components of the AI Employee system are properly configured
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Tuple

class SystemVerifier:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0

    def print_header(self, text: str):
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")

    def check(self, name: str, condition: bool, error_msg: str = "", warning: bool = False) -> bool:
        """Run a check and print result"""
        if condition:
            print(f"✅ {name}")
            self.checks_passed += 1
            return True
        else:
            if warning:
                print(f"⚠️  {name}")
                if error_msg:
                    print(f"   {error_msg}")
                self.warnings += 1
            else:
                print(f"❌ {name}")
                if error_msg:
                    print(f"   {error_msg}")
                self.checks_failed += 1
            return False

    def verify_python_version(self):
        """Check Python version"""
        version = sys.version_info
        is_valid = version.major == 3 and version.minor >= 8
        self.check(
            "Python 3.8+",
            is_valid,
            f"Found Python {version.major}.{version.minor}, need 3.8+"
        )

    def verify_node_version(self):
        """Check Node.js version"""
        try:
            import subprocess
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            major = int(version.replace('v', '').split('.')[0])
            self.check(
                "Node.js 18+",
                major >= 18,
                f"Found {version}, need v18+"
            )
        except:
            self.check("Node.js 18+", False, "Node.js not found in PATH", warning=True)

    def verify_directories(self):
        """Check required directories exist"""
        dirs = [
            'AI_Employee_Vault/Needs_Action',
            'AI_Employee_Vault/In_Progress',
            'AI_Employee_Vault/Done',
            'AI_Employee_Vault/Approved',
            'AI_Employee_Vault/Pending_Approval',
            'AI_Employee_Vault/Plans',
            'AI_Employee_Vault/Logs',
            'watchers',
            '.claude/skills',
            '.claude/mcp-servers/email-mcp'
        ]

        for dir_path in dirs:
            path = Path(dir_path)
            self.check(
                f"Directory: {dir_path}",
                path.exists() and path.is_dir(),
                f"Create with: mkdir -p {dir_path}"
            )

    def verify_files(self):
        """Check required files exist"""
        files = [
            ('orchestrator.py', False),
            ('watchers/gmail_watcher.py', False),
            ('watchers/file_watcher.py', False),
            ('watchers/whatsapp_watcher.py', True),  # Optional
            ('.claude/skills/email_reply_skill.md', False),
            ('.claude/mcp-servers/email-mcp/index.js', False),
            ('.claude/mcp-servers/email-mcp/package.json', False),
            ('requirements.txt', False),
            ('.env.template', False),
        ]

        for file_path, optional in files:
            path = Path(file_path)
            if optional:
                self.check(
                    f"File: {file_path}",
                    path.exists(),
                    "Optional file",
                    warning=True
                )
            else:
                self.check(
                    f"File: {file_path}",
                    path.exists(),
                    f"File missing: {file_path}"
                )

    def verify_env_file(self):
        """Check .env configuration"""
        env_path = Path('.env')

        if not env_path.exists():
            self.check(
                ".env file exists",
                False,
                "Create from .env.template: cp .env.template .env"
            )
            return

        self.check(".env file exists", True)

        # Check for required variables
        with open(env_path, 'r') as f:
            content = f.read()

        required_vars = ['DRY_RUN']
        optional_vars = ['GMAIL_CLIENT_ID', 'GMAIL_CLIENT_SECRET', 'ANTHROPIC_API_KEY']

        for var in required_vars:
            has_var = var in content and not content.split(var)[1].split('\n')[0].strip().startswith('=your_')
            self.check(
                f"Environment variable: {var}",
                has_var,
                f"Add {var} to .env file"
            )

        for var in optional_vars:
            has_var = var in content and not content.split(var)[1].split('\n')[0].strip().startswith('=your_')
            self.check(
                f"Environment variable: {var}",
                has_var,
                f"Optional: Add {var} to .env for full functionality",
                warning=True
            )

    def verify_python_packages(self):
        """Check Python packages are installed"""
        packages = [
            'google-auth-oauthlib',
            'google-auth-httplib2',
            'google-api-python-client',
            'watchdog',
            'plyer',
            'dotenv'
        ]

        for package in packages:
            try:
                __import__(package.replace('-', '_'))
                self.check(f"Python package: {package}", True)
            except ImportError:
                self.check(
                    f"Python package: {package}",
                    False,
                    f"Install with: pip install {package}"
                )

    def verify_node_packages(self):
        """Check Node.js packages are installed"""
        node_modules = Path('.claude/mcp-servers/email-mcp/node_modules')
        package_json = Path('.claude/mcp-servers/email-mcp/package.json')

        if not package_json.exists():
            self.check(
                "Email MCP package.json",
                False,
                "package.json missing"
            )
            return

        self.check("Email MCP package.json", True)

        if not node_modules.exists():
            self.check(
                "Email MCP dependencies",
                False,
                "Run: cd .claude/mcp-servers/email-mcp && npm install",
                warning=True
            )
        else:
            self.check("Email MCP dependencies", True)

    def verify_gmail_auth(self):
        """Check Gmail authentication"""
        token_path = Path('token.json')

        self.check(
            "Gmail token.json",
            token_path.exists(),
            "Authenticate with: python watchers/gmail_watcher.py",
            warning=True
        )

    def verify_drop_folder(self):
        """Check file watcher drop folder"""
        drop_folder = Path.home() / "Desktop" / "AI_Drop_Folder"

        self.check(
            "File drop folder",
            drop_folder.exists(),
            "Will be created automatically when file watcher starts",
            warning=True
        )

    def print_summary(self):
        """Print verification summary"""
        self.print_header("Verification Summary")

        total = self.checks_passed + self.checks_failed + self.warnings

        print(f"✅ Passed:   {self.checks_passed}/{total}")
        print(f"❌ Failed:   {self.checks_failed}/{total}")
        print(f"⚠️  Warnings: {self.warnings}/{total}")
        print()

        if self.checks_failed == 0:
            print("🎉 System is ready to run!")
            print("\nQuick start:")
            print("  1. python watchers/file_watcher.py")
            print("  2. python orchestrator.py")
        elif self.checks_failed <= 3:
            print("⚠️  System has minor issues. Fix the failed checks above.")
        else:
            print("❌ System has major issues. Please fix the failed checks above.")

        print()

    def run(self):
        """Run all verification checks"""
        self.print_header("AI Employee System Verification")

        print("Checking system requirements...")
        self.verify_python_version()
        self.verify_node_version()

        print("\nChecking directory structure...")
        self.verify_directories()

        print("\nChecking required files...")
        self.verify_files()

        print("\nChecking configuration...")
        self.verify_env_file()

        print("\nChecking Python dependencies...")
        self.verify_python_packages()

        print("\nChecking Node.js dependencies...")
        self.verify_node_packages()

        print("\nChecking authentication...")
        self.verify_gmail_auth()

        print("\nChecking optional components...")
        self.verify_drop_folder()

        self.print_summary()


if __name__ == '__main__':
    verifier = SystemVerifier()
    verifier.run()
