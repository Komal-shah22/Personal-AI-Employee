#!/usr/bin/env python3
"""
System Status Dashboard for AI Employee

Displays current health status of all services in a formatted table.

Usage:
    python monitor/status_dashboard.py
    python monitor/status_dashboard.py --watch  # Auto-refresh every 30 seconds
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
VAULT_DIR = Path('AI_Employee_Vault')
LOGS_DIR = VAULT_DIR / 'Logs'

# Services to display
SERVICES = [
    {'name': 'Gmail Watcher', 'pm2_name': 'gmail-watcher', 'type': 'pm2'},
    {'name': 'WhatsApp Watcher', 'pm2_name': 'whatsapp-watcher', 'type': 'pm2'},
    {'name': 'Orchestrator', 'pm2_name': 'orchestrator', 'type': 'pm2'},
    {'name': 'Vault Sync', 'type': 'git'},
    {'name': 'Email MCP', 'port': 3001, 'type': 'mcp'},
    {'name': 'Social MCP', 'port': 3002, 'type': 'mcp'},
    {'name': 'Payment MCP', 'port': 3003, 'type': 'mcp'},
]


class StatusDashboard:
    def __init__(self):
        self.status_data = []

    def run_command(self, command):
        """Run shell command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    def format_time_ago(self, timestamp):
        """Format timestamp as 'X min ago' or 'X sec ago'"""
        if not timestamp:
            return "Unknown"

        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = datetime.fromtimestamp(timestamp)

            delta = datetime.now() - dt
            seconds = int(delta.total_seconds())

            if seconds < 60:
                return f"{seconds} sec ago"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} min ago"
            elif seconds < 86400:
                hours = seconds // 3600
                return f"{hours} hr ago"
            else:
                days = seconds // 86400
                return f"{days} day ago" if days == 1 else f"{days} days ago"

        except Exception:
            return "Unknown"

    def get_pm2_status(self, pm2_name):
        """Get status of PM2 process"""
        success, stdout, stderr = self.run_command("pm2 jlist")

        if not success:
            return {
                'status': 'DOWN',
                'last_active': 'Error',
                'details': 'PM2 not responding'
            }

        try:
            processes = json.loads(stdout)

            for p in processes:
                if p.get('name') == pm2_name:
                    pm2_status = p.get('pm2_env', {}).get('status')

                    if pm2_status == 'online':
                        uptime = p.get('pm2_env', {}).get('pm_uptime')
                        return {
                            'status': 'UP',
                            'last_active': self.format_time_ago(uptime / 1000) if uptime else 'Running',
                            'details': f"Restarts: {p.get('pm2_env', {}).get('restart_time', 0)}"
                        }
                    else:
                        return {
                            'status': 'DOWN',
                            'last_active': 'Stopped',
                            'details': f"Status: {pm2_status}"
                        }

            return {
                'status': 'DOWN',
                'last_active': 'Not found',
                'details': 'Process not in PM2'
            }

        except json.JSONDecodeError:
            return {
                'status': 'DOWN',
                'last_active': 'Error',
                'details': 'Failed to parse PM2 output'
            }

    def get_vault_sync_status(self):
        """Get status of vault sync"""
        if not (VAULT_DIR / '.git').exists():
            return {
                'status': 'DOWN',
                'last_active': 'Not initialized',
                'details': 'Git not initialized'
            }

        success, stdout, stderr = self.run_command(
            f"cd {VAULT_DIR} && git log -1 --format=%ct"
        )

        if not success:
            return {
                'status': 'DOWN',
                'last_active': 'Error',
                'details': 'Failed to get git log'
            }

        try:
            last_commit_timestamp = int(stdout.strip())
            last_commit_time = datetime.fromtimestamp(last_commit_timestamp)
            age_minutes = (datetime.now() - last_commit_time).total_seconds() / 60

            if age_minutes <= 10:
                return {
                    'status': 'UP',
                    'last_active': self.format_time_ago(last_commit_timestamp),
                    'details': f"Last commit: {age_minutes:.1f} min ago"
                }
            else:
                return {
                    'status': 'STALE',
                    'last_active': self.format_time_ago(last_commit_timestamp),
                    'details': f"Last commit: {age_minutes:.1f} min ago"
                }

        except (ValueError, IndexError):
            return {
                'status': 'DOWN',
                'last_active': 'Error',
                'details': 'Failed to parse git log'
            }

    def get_mcp_status(self, port):
        """Get status of MCP server"""
        try:
            import requests

            response = requests.get(
                f"http://localhost:{port}/health",
                timeout=2
            )

            if response.status_code == 200:
                return {
                    'status': 'UP',
                    'last_active': 'Just now',
                    'details': f"Port {port}"
                }
            else:
                return {
                    'status': 'DOWN',
                    'last_active': 'Error',
                    'details': f"HTTP {response.status_code}"
                }

        except ImportError:
            return {
                'status': 'UNKNOWN',
                'last_active': 'N/A',
                'details': 'requests module not installed'
            }
        except Exception as e:
            return {
                'status': 'DOWN',
                'last_active': 'Not responding',
                'details': f"Port {port}"
            }

    def get_health_log_summary(self):
        """Get summary from latest health log"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"health_{date_str}.json"

        if not log_file.exists():
            return None

        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)

            if logs:
                latest = logs[-1]
                return {
                    'timestamp': latest.get('timestamp'),
                    'failures': len(latest.get('failures', [])),
                    'alerts_sent': len(latest.get('alerts_sent', []))
                }

        except Exception:
            return None

    def collect_status(self):
        """Collect status for all services"""
        self.status_data = []

        for service in SERVICES:
            if service['type'] == 'pm2':
                status = self.get_pm2_status(service['pm2_name'])
            elif service['type'] == 'git':
                status = self.get_vault_sync_status()
            elif service['type'] == 'mcp':
                status = self.get_mcp_status(service['port'])
            else:
                status = {
                    'status': 'UNKNOWN',
                    'last_active': 'N/A',
                    'details': 'Unknown type'
                }

            self.status_data.append({
                'name': service['name'],
                **status
            })

    def print_dashboard(self):
        """Print formatted dashboard"""
        # Clear screen (works on both Windows and Unix)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Header
        print()
        print("=" * 70)
        print("  AI EMPLOYEE - SYSTEM STATUS DASHBOARD")
        print("=" * 70)
        print()

        # Timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  Last Updated: {now}")
        print()

        # Table header
        print("+-------------------------+----------+-----------------+")
        print("| Service                 | Status   | Last Active     |")
        print("+-------------------------+----------+-----------------+")

        # Table rows
        for item in self.status_data:
            name = item['name'].ljust(23)
            status = item['status'].ljust(8)
            last_active = item['last_active'].ljust(15)

            print(f"| {name} | {status} | {last_active} |")

        # Table footer
        print("+-------------------------+----------+-----------------+")
        print()

        # Summary
        up_count = sum(1 for item in self.status_data if item['status'] == 'UP')
        down_count = sum(1 for item in self.status_data if item['status'] == 'DOWN')
        stale_count = sum(1 for item in self.status_data if item['status'] == 'STALE')

        print(f"  Summary: {up_count} UP, {down_count} DOWN, {stale_count} STALE")
        print()

        # Health log summary
        health_summary = self.get_health_log_summary()
        if health_summary:
            print(f"  Last Health Check: {self.format_time_ago(health_summary['timestamp'])}")
            if health_summary['failures'] > 0:
                print(f"  ⚠️  {health_summary['failures']} failures detected")
            if health_summary['alerts_sent'] > 0:
                print(f"  📧 {health_summary['alerts_sent']} alerts sent")
        else:
            print("  No health check logs found for today")

        print()
        print("=" * 70)
        print()

    def print_details(self):
        """Print detailed status information"""
        print()
        print("DETAILED STATUS:")
        print("-" * 70)

        for item in self.status_data:
            print(f"\n{item['name']}:")
            print(f"  Status: {item['status']}")
            print(f"  Last Active: {item['last_active']}")
            print(f"  Details: {item['details']}")

        print()

    def run(self, watch=False, interval=30):
        """Run dashboard"""
        try:
            while True:
                self.collect_status()
                self.print_dashboard()

                if not watch:
                    break

                print(f"  Auto-refresh in {interval} seconds... (Ctrl+C to exit)")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n  Dashboard stopped by user.\n")
            sys.exit(0)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Status Dashboard')
    parser.add_argument('--watch', action='store_true',
                        help='Auto-refresh every 30 seconds')
    parser.add_argument('--interval', type=int, default=30,
                        help='Refresh interval in seconds (default: 30)')
    parser.add_argument('--details', action='store_true',
                        help='Show detailed status information')

    args = parser.parse_args()

    dashboard = StatusDashboard()

    if args.details:
        dashboard.collect_status()
        dashboard.print_dashboard()
        dashboard.print_details()
    else:
        dashboard.run(watch=args.watch, interval=args.interval)


if __name__ == '__main__':
    main()
