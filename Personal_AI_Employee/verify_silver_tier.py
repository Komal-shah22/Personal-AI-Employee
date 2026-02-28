"""
Silver Tier Verification Script
Tests all Silver Tier requirements including intelligent reasoning and HITL workflow
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess

class SilverTierVerifier:
    def __init__(self):
        self.results = {
            'intelligent_reasoning': False,
            'invoice_generation': False,
            'approval_workflow': False,
            'audit_trail': False,
            'dry_run_mode': False
        }
        self.issues = []
        self.test_email_created = False

    def cleanup_test_files(self):
        """Clean up any existing test files"""
        print("\n=== Cleaning up previous test files ===")

        test_patterns = [
            'AI_Employee_Vault/Needs_Action/SILVER_TEST_*.md',
            'AI_Employee_Vault/Done/SILVER_TEST_*.md',
            'AI_Employee_Vault/Plans/PLAN_SILVER_TEST_*.md',
            'AI_Employee_Vault/Pending_Approval/EMAIL_invoice_silver_test_verification_com_*.md',
            'AI_Employee_Vault/Approved/EMAIL_invoice_silver_test_verification_com_*.md',
            'AI_Employee_Vault/Invoices/INVOICE_silver_test_verification_com_*.md'
        ]

        import glob
        for pattern in test_patterns:
            for file in glob.glob(pattern):
                try:
                    os.remove(file)
                    print(f"[OK] Removed: {file}")
                except Exception as e:
                    print(f"[WARN] Could not remove {file}: {e}")

    def create_test_email(self):
        """Create a test invoice request email"""
        print("\n=== Creating Test Email ===")

        timestamp = datetime.now().isoformat()
        test_content = f"""---
type: email
from: silver.test@verification.com
subject: Invoice Request for Silver Tier Test
received: {timestamp}
priority: high
status: pending
---

Hi,

Could you please send me the invoice for Silver Tier verification?

The agreed amount was $999 for the testing services.

Thanks,
Silver Test
"""

        test_file = Path('AI_Employee_Vault/Needs_Action/SILVER_TEST_invoice_request.md')

        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            print(f"[OK] Test email created: {test_file}")
            self.test_email_created = True
            return True
        except Exception as e:
            print(f"[FAIL] Could not create test email: {e}")
            self.issues.append(f"Failed to create test email: {e}")
            return False

    def run_orchestrator(self):
        """Run orchestrator to process the test email"""
        print("\n=== Running Orchestrator ===")

        try:
            result = subprocess.run(
                ['python', 'orchestrator.py', '--process-once'],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )

            if 'Analysis: intent=invoice_request' in result.stdout:
                print("[OK] Orchestrator detected invoice request")
                return True
            else:
                print("[FAIL] Orchestrator did not detect invoice request")
                print(f"Output: {result.stdout[:500]}")
                self.issues.append("Orchestrator failed to detect invoice intent")
                return False

        except subprocess.TimeoutExpired:
            print("[FAIL] Orchestrator timed out")
            self.issues.append("Orchestrator execution timed out")
            return False
        except Exception as e:
            print(f"[FAIL] Error running orchestrator: {e}")
            self.issues.append(f"Orchestrator error: {e}")
            return False

    def check_intelligent_reasoning(self):
        """Verify intelligent content analysis"""
        print("\n=== Checking Intelligent Reasoning ===")

        # Check if plan was created with proper analysis
        plan_files = list(Path('AI_Employee_Vault/Plans').glob('PLAN_SILVER_TEST_*.md'))

        if not plan_files:
            print("[FAIL] No plan file created")
            self.issues.append("Plan file not created")
            return False

        plan_file = plan_files[0]
        print(f"[OK] Plan file found: {plan_file.name}")

        try:
            with open(plan_file, 'r', encoding='utf-8') as f:
                plan_content = f.read()

            # Check for key elements
            checks = {
                'intent: invoice_request': 'Intent detection',
                'action_type: send_email_with_invoice': 'Action type identification',
                'Generate invoice document': 'Invoice generation step',
                'Create approval request': 'Approval workflow step'
            }

            all_passed = True
            for check_text, description in checks.items():
                if check_text in plan_content:
                    print(f"[OK] {description}")
                else:
                    print(f"[FAIL] {description} - not found")
                    self.issues.append(f"Plan missing: {description}")
                    all_passed = False

            self.results['intelligent_reasoning'] = all_passed
            return all_passed

        except Exception as e:
            print(f"[FAIL] Error reading plan: {e}")
            self.issues.append(f"Plan read error: {e}")
            return False

    def check_invoice_generation(self):
        """Verify invoice was generated"""
        print("\n=== Checking Invoice Generation ===")

        # Note: The orchestrator replaces @ and . with _ in filenames
        # So silver.test@verification.com becomes silver_test_verification_com
        invoice_files = list(Path('AI_Employee_Vault/Invoices').glob('INVOICE_silver_test_verification_com_*.md'))

        if not invoice_files:
            print("[FAIL] No invoice file created")
            self.issues.append("Invoice not generated")
            return False

        invoice_file = invoice_files[0]
        print(f"[OK] Invoice file found: {invoice_file.name}")

        try:
            with open(invoice_file, 'r', encoding='utf-8') as f:
                invoice_content = f.read()

            # Check invoice contents
            checks = {
                'INVOICE': 'Invoice header',
                'Invoice Number': 'Invoice number',
                'silver.test@verification.com': 'Customer email',
                '$999': 'Amount',
                'Payment Terms': 'Payment terms'
            }

            all_passed = True
            for check_text, description in checks.items():
                if check_text in invoice_content:
                    print(f"[OK] {description}")
                else:
                    print(f"[FAIL] {description} - not found")
                    self.issues.append(f"Invoice missing: {description}")
                    all_passed = False

            self.results['invoice_generation'] = all_passed
            return all_passed

        except Exception as e:
            print(f"[FAIL] Error reading invoice: {e}")
            self.issues.append(f"Invoice read error: {e}")
            return False

    def check_approval_workflow(self):
        """Verify HITL approval workflow"""
        print("\n=== Checking Approval Workflow ===")

        # Note: The orchestrator replaces @ and . with _ in filenames
        approval_files = list(Path('AI_Employee_Vault/Pending_Approval').glob('EMAIL_invoice_silver_test_verification_com_*.md'))

        if not approval_files:
            print("[FAIL] No approval request created")
            self.issues.append("Approval request not created")
            return False

        approval_file = approval_files[0]
        print(f"[OK] Approval request found: {approval_file.name}")

        try:
            with open(approval_file, 'r', encoding='utf-8') as f:
                approval_content = f.read()

            # Check approval request contents
            checks = {
                'action_type: send_email': 'Action type',
                'silver.test@verification.com': 'Recipient',
                'Approval Required': 'Approval header',
                'Proposed Action': 'Proposed action section',
                'Invoice': 'Invoice attachment reference'
            }

            all_passed = True
            for check_text, description in checks.items():
                if check_text in approval_content:
                    print(f"[OK] {description}")
                else:
                    print(f"[FAIL] {description} - not found")
                    self.issues.append(f"Approval request missing: {description}")
                    all_passed = False

            self.results['approval_workflow'] = all_passed
            return all_passed

        except Exception as e:
            print(f"[FAIL] Error reading approval request: {e}")
            self.issues.append(f"Approval request read error: {e}")
            return False

    def check_audit_trail(self):
        """Verify audit trail logging"""
        print("\n=== Checking Audit Trail ===")

        today = datetime.now().strftime('%Y-%m-%d')
        log_file = Path(f'AI_Employee_Vault/Logs/{today}.json')

        if not log_file.exists():
            print(f"[FAIL] Log file not found: {log_file}")
            self.issues.append("Daily log file not created")
            return False

        print(f"[OK] Log file found: {log_file}")

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            # Find our test action - look for SILVER_TEST in task_id
            test_action = None
            for action in log_data.get('actions', []):
                if 'SILVER_TEST' in action.get('task_id', '') or 'silver_test' in action.get('task_id', ''):
                    test_action = action
                    break

            if not test_action:
                print("[FAIL] Test action not logged")
                print(f"  Available actions: {[a.get('task_id', '') for a in log_data.get('actions', [])]}")
                self.issues.append("Test action not found in logs")
                return False

            print("[OK] Test action found in logs")

            # Check log entry fields
            checks = {
                'timestamp': 'Timestamp',
                'task_id': 'Task ID',
                'type': 'Type',
                'success': 'Success flag'
            }

            all_passed = True
            for field, description in checks.items():
                if field in test_action:
                    print(f"[OK] {description}: {test_action[field]}")
                else:
                    print(f"[FAIL] {description} - missing")
                    self.issues.append(f"Log entry missing: {description}")
                    all_passed = False

            self.results['audit_trail'] = all_passed
            return all_passed

        except Exception as e:
            print(f"[FAIL] Error reading log: {e}")
            self.issues.append(f"Log read error: {e}")
            return False

    def check_dry_run_mode(self):
        """Verify DRY RUN mode is active"""
        print("\n=== Checking DRY RUN Mode ===")

        # Check environment variable
        dry_run = os.getenv('DRY_RUN', 'true').lower()

        if dry_run == 'true':
            print("[OK] DRY_RUN environment variable is set to 'true'")
        else:
            print(f"[WARN] DRY_RUN is set to '{dry_run}' (should be 'true' for testing)")

        # Check orchestrator code
        try:
            with open('orchestrator.py', 'r', encoding='utf-8') as f:
                orch_content = f.read()

            if 'self.dry_run' in orch_content and 'DRY RUN:' in orch_content:
                print("[OK] Orchestrator has DRY RUN mode implemented")
                self.results['dry_run_mode'] = True
                return True
            else:
                print("[FAIL] DRY RUN mode not found in orchestrator")
                self.issues.append("DRY RUN mode not implemented")
                return False

        except Exception as e:
            print(f"[FAIL] Error checking orchestrator: {e}")
            self.issues.append(f"Orchestrator check error: {e}")
            return False

    def run_verification(self):
        """Run all verification checks"""
        print("=" * 60)
        print("SILVER TIER VERIFICATION")
        print("=" * 60)

        # Cleanup previous test files
        self.cleanup_test_files()

        # Create test email
        if not self.create_test_email():
            print("\n[FAIL] Cannot proceed without test email")
            return False

        # Run orchestrator
        if not self.run_orchestrator():
            print("\n[FAIL] Orchestrator failed to process test email")
            return False

        # Run all checks
        self.check_intelligent_reasoning()
        self.check_invoice_generation()
        self.check_approval_workflow()
        self.check_audit_trail()
        self.check_dry_run_mode()

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
            print("\n[WARN] ISSUES FOUND:")
            for issue in self.issues:
                print(f"  - {issue}")

        if passed == total:
            print("\n[SUCCESS] SILVER TIER: CERTIFIED [OK]")
            print("\nAll Silver Tier features are working correctly:")
            print("  - Intelligent email analysis with intent detection")
            print("  - Automated invoice generation")
            print("  - Human-in-the-loop approval workflow")
            print("  - Complete audit trail with JSON logging")
            print("  - DRY RUN mode for safe testing")
            return True
        else:
            print("\n[FAIL] SILVER TIER: NOT CERTIFIED")
            print("Please fix the issues above and run verification again.")
            return False

if __name__ == "__main__":
    verifier = SilverTierVerifier()
    success = verifier.run_verification()
    sys.exit(0 if success else 1)
