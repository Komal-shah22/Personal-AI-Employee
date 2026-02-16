"""
Gold Tier Verification Script
Tests all Gold Tier requirements including error recovery and CEO briefings
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess

class GoldTierVerifier:
    def __init__(self):
        self.results = {
            'ralph_wiggum_loop': False,
            'error_recovery': False,
            'ceo_briefing_daily': False,
            'ceo_briefing_weekly': False,
            'orchestrator_integration': False
        }
        self.issues = []

    def check_ralph_wiggum_loop(self):
        """Verify Ralph Wiggum Loop exists and works"""
        print("\n=== Checking Ralph Wiggum Loop ===")

        # Check if file exists
        ralph_file = Path('ralph_wiggum_loop.py')
        if not ralph_file.exists():
            print("[FAIL] ralph_wiggum_loop.py not found")
            self.issues.append("Ralph Wiggum Loop file missing")
            return False

        print("[OK] ralph_wiggum_loop.py exists")

        # Check for key classes
        try:
            with open(ralph_file, 'r', encoding='utf-8') as f:
                content = f.read()

            required_classes = [
                'ErrorClassifier',
                'RecoveryStrategy',
                'RalphWiggumLoop'
            ]

            for class_name in required_classes:
                if f"class {class_name}" in content:
                    print(f"[OK] Class: {class_name}")
                else:
                    print(f"[FAIL] Class: {class_name} - missing")
                    self.issues.append(f"Missing class: {class_name}")
                    return False

            self.results['ralph_wiggum_loop'] = True
            return True

        except Exception as e:
            print(f"[FAIL] Error reading Ralph Wiggum Loop: {e}")
            self.issues.append(f"Ralph Wiggum Loop read error: {e}")
            return False

    def check_error_recovery(self):
        """Test error recovery functionality"""
        print("\n=== Testing Error Recovery ===")

        try:
            result = subprocess.run(
                ['python', 'ralph_wiggum_loop.py'],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )

            if 'Network error recovery: SUCCESS' in result.stdout:
                print("[OK] Network error recovery works")
            else:
                print("[FAIL] Network error recovery failed")
                self.issues.append("Network error recovery not working")
                return False

            if 'File system error recovery: SUCCESS' in result.stdout:
                print("[OK] File system error recovery works")
            else:
                print("[FAIL] File system error recovery failed")
                self.issues.append("File system error recovery not working")
                return False

            if 'Recovery Statistics' in result.stdout:
                print("[OK] Recovery statistics generated")
            else:
                print("[FAIL] Recovery statistics missing")
                self.issues.append("Recovery statistics not generated")
                return False

            self.results['error_recovery'] = True
            return True

        except subprocess.TimeoutExpired:
            print("[FAIL] Ralph Wiggum Loop test timed out")
            self.issues.append("Error recovery test timeout")
            return False
        except Exception as e:
            print(f"[FAIL] Error testing recovery: {e}")
            self.issues.append(f"Error recovery test failed: {e}")
            return False

    def check_ceo_briefing_daily(self):
        """Verify daily CEO briefing generation"""
        print("\n=== Checking Daily CEO Briefing ===")

        # Check if file exists
        briefing_file = Path('ceo_briefing.py')
        if not briefing_file.exists():
            print("[FAIL] ceo_briefing.py not found")
            self.issues.append("CEO briefing file missing")
            return False

        print("[OK] ceo_briefing.py exists")

        # Test daily briefing generation
        try:
            result = subprocess.run(
                ['python', 'ceo_briefing.py', '--type', 'daily'],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )

            required_sections = [
                'CEO Daily Briefing',
                'Executive Summary',
                'Activity Breakdown',
                'System Health',
                'Next Steps'
            ]

            all_present = True
            for section in required_sections:
                if section in result.stdout:
                    print(f"[OK] Section: {section}")
                else:
                    print(f"[FAIL] Section: {section} - missing")
                    self.issues.append(f"Daily briefing missing section: {section}")
                    all_present = False

            self.results['ceo_briefing_daily'] = all_present
            return all_present

        except subprocess.TimeoutExpired:
            print("[FAIL] Daily briefing generation timed out")
            self.issues.append("Daily briefing timeout")
            return False
        except Exception as e:
            print(f"[FAIL] Error generating daily briefing: {e}")
            self.issues.append(f"Daily briefing error: {e}")
            return False

    def check_ceo_briefing_weekly(self):
        """Verify weekly CEO briefing generation"""
        print("\n=== Checking Weekly CEO Briefing ===")

        try:
            result = subprocess.run(
                ['python', 'ceo_briefing.py', '--type', 'weekly'],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )

            required_sections = [
                'CEO Weekly Briefing',
                'Executive Summary',
                'Weekly Activity',
                'Daily Breakdown',
                'Insights & Trends'
            ]

            all_present = True
            for section in required_sections:
                if section in result.stdout:
                    print(f"[OK] Section: {section}")
                else:
                    print(f"[FAIL] Section: {section} - missing")
                    self.issues.append(f"Weekly briefing missing section: {section}")
                    all_present = False

            self.results['ceo_briefing_weekly'] = all_present
            return all_present

        except subprocess.TimeoutExpired:
            print("[FAIL] Weekly briefing generation timed out")
            self.issues.append("Weekly briefing timeout")
            return False
        except Exception as e:
            print(f"[FAIL] Error generating weekly briefing: {e}")
            self.issues.append(f"Weekly briefing error: {e}")
            return False

    def check_orchestrator_integration(self):
        """Verify Ralph Wiggum Loop is integrated into orchestrator"""
        print("\n=== Checking Orchestrator Integration ===")

        orch_file = Path('orchestrator.py')
        if not orch_file.exists():
            print("[FAIL] orchestrator.py not found")
            self.issues.append("Orchestrator file missing")
            return False

        try:
            with open(orch_file, 'r', encoding='utf-8') as f:
                content = f.read()

            checks = {
                'from ralph_wiggum_loop import': 'Ralph Wiggum import',
                'self.ralph = RalphWiggumLoop': 'Ralph initialization',
                'self.ralph.log_error': 'Error logging',
                'self.ralph.attempt_recovery': 'Recovery attempt',
                'self.ralph.alert_human': 'Human alert'
            }

            all_present = True
            for check_text, description in checks.items():
                if check_text in content:
                    print(f"[OK] {description}")
                else:
                    print(f"[FAIL] {description} - not found")
                    self.issues.append(f"Orchestrator missing: {description}")
                    all_present = False

            self.results['orchestrator_integration'] = all_present
            return all_present

        except Exception as e:
            print(f"[FAIL] Error checking orchestrator: {e}")
            self.issues.append(f"Orchestrator check error: {e}")
            return False

    def run_verification(self):
        """Run all verification checks"""
        print("=" * 60)
        print("GOLD TIER VERIFICATION")
        print("=" * 60)

        self.check_ralph_wiggum_loop()
        self.check_error_recovery()
        self.check_ceo_briefing_daily()
        self.check_ceo_briefing_weekly()
        self.check_orchestrator_integration()

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
            print("\n[SUCCESS] GOLD TIER: CERTIFIED [OK]")
            print("\nAll Gold Tier features are working correctly:")
            print("  - Ralph Wiggum Loop (autonomous error recovery)")
            print("  - Error classification and recovery strategies")
            print("  - CEO daily briefing automation")
            print("  - CEO weekly briefing automation")
            print("  - Orchestrator integration with error recovery")
            return True
        else:
            print("\n[FAIL] GOLD TIER: NOT CERTIFIED")
            print("Please fix the issues above and run verification again.")
            return False

if __name__ == "__main__":
    verifier = GoldTierVerifier()
    success = verifier.run_verification()
    sys.exit(0 if success else 1)
