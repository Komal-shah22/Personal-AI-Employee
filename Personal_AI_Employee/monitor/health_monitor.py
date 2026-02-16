#!/usr/bin/env python3
"""
Production Health Monitor for AI Employee System

Runs every 5 minutes via cron to check system health:
- PM2 processes (gmail-watcher, file-watcher, orchestrator)
- Vault sync (last git commit < 10 minutes)
- Disk space (> 20% free)
- Claude Code API (test call)
- MCP servers (email, social, payment)

Auto-restarts failed services and sends alert emails if recovery fails.

Usage:
    python monitor/health_monitor.py

Cron setup:
    */5 * * * * cd /path/to/Personal_AI_Employee && python monitor/health_monitor.py >> monitor/health.log 2>&1
"""

import os
import sys
import json
import subprocess
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import requests

# Configuration
VAULT_DIR = Path('AI_Employee_Vault')
LOGS_DIR = VAULT_DIR / 'Logs'
HEALTH_LOG_DIR = Path('monitor/logs')
HEALTH_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Services to monitor
PM2_SERVICES = [
    'gmail-watcher',
    'file-watcher',
    'orchestrator'
]

# MCP servers to check
MCP_SERVERS = [
    {'name': 'email-mcp', 'port': 3001},
    {'name': 'social-mcp', 'port': 3002},
    {'name': 'payment-mcp', 'port': 3003}
]

# Thresholds
VAULT_SYNC_MAX_AGE_MINUTES = 10
DISK_SPACE_MIN_PERCENT = 20
MAX_RESTART_ATTEMPTS = 2

# Alert email settings
ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'admin@example.com')


class HealthMonitor:
    def __init__(self):
        self.timestamp = datetime.now()
        self.results = {
            'timestamp': self.timestamp.isoformat(),
            'checks': {},
            'failures': [],
            'alerts_sent': []
        }

    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def run_command(self, command, check=False):
        """Run shell command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=check
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except Exception as e:
            return False, "", str(e)

    def check_pm2_process(self, service_name):
        """Check if PM2 process is running"""
        self.log(f"Checking PM2 process: {service_name}")

        success, stdout, stderr = self.run_command(f"pm2 jlist")

        if not success:
            return {
                'status': 'error',
                'message': f"Failed to query PM2: {stderr}",
                'healthy': False
            }

        try:
            processes = json.loads(stdout)

            # Find the process
            process = None
            for p in processes:
                if p.get('name') == service_name:
                    process = p
                    break

            if not process:
                return {
                    'status': 'not_found',
                    'message': f"Process {service_name} not found in PM2",
                    'healthy': False
                }

            # Check status
            pm2_status = process.get('pm2_env', {}).get('status')

            if pm2_status == 'online':
                return {
                    'status': 'online',
                    'message': f"Process {service_name} is running",
                    'healthy': True,
                    'uptime': process.get('pm2_env', {}).get('pm_uptime'),
                    'restarts': process.get('pm2_env', {}).get('restart_time', 0)
                }
            else:
                return {
                    'status': pm2_status or 'unknown',
                    'message': f"Process {service_name} is {pm2_status}",
                    'healthy': False
                }

        except json.JSONDecodeError:
            return {
                'status': 'error',
                'message': "Failed to parse PM2 output",
                'healthy': False
            }

    def restart_pm2_process(self, service_name):
        """Attempt to restart a PM2 process"""
        self.log(f"Attempting to restart {service_name}...", "WARNING")

        success, stdout, stderr = self.run_command(f"pm2 restart {service_name}")

        if not success:
            self.log(f"Failed to restart {service_name}: {stderr}", "ERROR")
            return False

        # Wait 30 seconds for service to stabilize
        self.log(f"Waiting 30 seconds for {service_name} to stabilize...")
        time.sleep(30)

        # Check if it's running now
        result = self.check_pm2_process(service_name)

        if result['healthy']:
            self.log(f"Successfully restarted {service_name}", "INFO")
            return True
        else:
            self.log(f"Restart failed for {service_name}: {result['message']}", "ERROR")
            return False

    def check_vault_sync(self):
        """Check if vault sync is working (last commit < 10 minutes)"""
        self.log("Checking vault sync...")

        if not (VAULT_DIR / '.git').exists():
            return {
                'status': 'not_initialized',
                'message': "Vault is not a git repository",
                'healthy': False
            }

        # Get last commit time
        success, stdout, stderr = self.run_command(
            f"cd {VAULT_DIR} && git log -1 --format=%ct"
        )

        if not success:
            return {
                'status': 'error',
                'message': f"Failed to get git log: {stderr}",
                'healthy': False
            }

        try:
            last_commit_timestamp = int(stdout.strip())
            last_commit_time = datetime.fromtimestamp(last_commit_timestamp)
            age_minutes = (datetime.now() - last_commit_time).total_seconds() / 60

            if age_minutes <= VAULT_SYNC_MAX_AGE_MINUTES:
                return {
                    'status': 'active',
                    'message': f"Last commit {age_minutes:.1f} minutes ago",
                    'healthy': True,
                    'last_commit': last_commit_time.isoformat(),
                    'age_minutes': age_minutes
                }
            else:
                return {
                    'status': 'stale',
                    'message': f"Last commit {age_minutes:.1f} minutes ago (threshold: {VAULT_SYNC_MAX_AGE_MINUTES})",
                    'healthy': False,
                    'last_commit': last_commit_time.isoformat(),
                    'age_minutes': age_minutes
                }

        except (ValueError, IndexError):
            return {
                'status': 'error',
                'message': "Failed to parse git log output",
                'healthy': False
            }

    def restart_vault_sync(self):
        """Attempt to restart vault sync"""
        self.log("Attempting to restart vault sync...", "WARNING")

        # Try to trigger a sync
        success, stdout, stderr = self.run_command(
            f"cd {VAULT_DIR} && git pull --rebase origin main"
        )

        if not success:
            self.log(f"Failed to pull vault: {stderr}", "ERROR")
            return False

        # Wait 30 seconds
        time.sleep(30)

        # Check if sync is working now
        result = self.check_vault_sync()

        if result['healthy']:
            self.log("Vault sync recovered", "INFO")
            return True
        else:
            self.log(f"Vault sync still failing: {result['message']}", "ERROR")
            return False

    def check_disk_space(self):
        """Check if disk space > 20% free"""
        self.log("Checking disk space...")

        try:
            total, used, free = shutil.disk_usage("/")

            free_percent = (free / total) * 100

            if free_percent >= DISK_SPACE_MIN_PERCENT:
                return {
                    'status': 'ok',
                    'message': f"{free_percent:.1f}% free ({free // (2**30)} GB)",
                    'healthy': True,
                    'free_percent': free_percent,
                    'free_gb': free // (2**30),
                    'total_gb': total // (2**30)
                }
            else:
                return {
                    'status': 'low',
                    'message': f"Only {free_percent:.1f}% free ({free // (2**30)} GB)",
                    'healthy': False,
                    'free_percent': free_percent,
                    'free_gb': free // (2**30),
                    'total_gb': total // (2**30)
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to check disk space: {str(e)}",
                'healthy': False
            }

    def check_claude_api(self):
        """Check if Claude Code API is responding"""
        self.log("Checking Claude Code API...")

        api_key = os.getenv('ANTHROPIC_API_KEY')

        if not api_key:
            return {
                'status': 'not_configured',
                'message': "ANTHROPIC_API_KEY not set",
                'healthy': False
            }

        try:
            # Simple test call
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                },
                json={
                    'model': 'claude-3-5-sonnet-20241022',
                    'max_tokens': 10,
                    'messages': [
                        {'role': 'user', 'content': 'ping'}
                    ]
                },
                timeout=10
            )

            if response.status_code == 200:
                return {
                    'status': 'ok',
                    'message': "API responding normally",
                    'healthy': True,
                    'response_time_ms': response.elapsed.total_seconds() * 1000
                }
            else:
                return {
                    'status': 'error',
                    'message': f"API returned {response.status_code}: {response.text[:100]}",
                    'healthy': False,
                    'status_code': response.status_code
                }

        except requests.exceptions.Timeout:
            return {
                'status': 'timeout',
                'message': "API request timed out",
                'healthy': False
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to reach API: {str(e)}",
                'healthy': False
            }

    def check_mcp_server(self, server_info):
        """Check if MCP server is responding"""
        name = server_info['name']
        port = server_info['port']

        self.log(f"Checking MCP server: {name} on port {port}")

        try:
            # Try to connect to the server
            response = requests.get(
                f"http://localhost:{port}/health",
                timeout=5
            )

            if response.status_code == 200:
                return {
                    'status': 'ok',
                    'message': f"{name} responding on port {port}",
                    'healthy': True,
                    'port': port
                }
            else:
                return {
                    'status': 'error',
                    'message': f"{name} returned {response.status_code}",
                    'healthy': False,
                    'port': port,
                    'status_code': response.status_code
                }

        except requests.exceptions.ConnectionError:
            return {
                'status': 'not_running',
                'message': f"{name} not responding on port {port}",
                'healthy': False,
                'port': port
            }
        except requests.exceptions.Timeout:
            return {
                'status': 'timeout',
                'message': f"{name} timed out",
                'healthy': False,
                'port': port
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to check {name}: {str(e)}",
                'healthy': False,
                'port': port
            }

    def send_alert_email(self, subject, body):
        """Send alert email via Gmail MCP"""
        self.log(f"Sending alert email: {subject}", "WARNING")

        try:
            # Use Gmail MCP to send email
            # This assumes the email MCP server is running
            response = requests.post(
                'http://localhost:3001/send_email',
                json={
                    'to': ALERT_EMAIL,
                    'subject': subject,
                    'body': body
                },
                timeout=10
            )

            if response.status_code == 200:
                self.log("Alert email sent successfully", "INFO")
                return True
            else:
                self.log(f"Failed to send alert email: {response.text}", "ERROR")
                return False

        except Exception as e:
            self.log(f"Failed to send alert email: {str(e)}", "ERROR")
            return False

    def handle_failure(self, service_name, check_result, restart_func=None):
        """Handle a failed check"""
        self.log(f"Handling failure for {service_name}", "WARNING")

        failure_info = {
            'service': service_name,
            'timestamp': datetime.now().isoformat(),
            'check_result': check_result,
            'recovery_attempted': False,
            'recovery_successful': False
        }

        # Attempt restart if function provided
        if restart_func:
            failure_info['recovery_attempted'] = True

            if restart_func():
                failure_info['recovery_successful'] = True
                self.log(f"Successfully recovered {service_name}", "INFO")
                return failure_info

        # Recovery failed or not attempted - send alert
        self.log(f"Sending alert for {service_name}", "WARNING")

        subject = f"[ALERT] AI Employee - {service_name} is down"

        body = f"""AI Employee Health Monitor Alert

Service: {service_name}
Status: {check_result.get('status', 'unknown')}
Message: {check_result.get('message', 'No details available')}

What was tried:
"""

        if failure_info['recovery_attempted']:
            body += f"- Attempted automatic restart: FAILED\n"
        else:
            body += f"- No automatic recovery available\n"

        body += f"""
What needs manual attention:
- Check service logs for errors
- Verify configuration and credentials
- Restart service manually if needed

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
AI Employee Health Monitor
"""

        if self.send_alert_email(subject, body):
            failure_info['alert_sent'] = True
            self.results['alerts_sent'].append(service_name)
        else:
            failure_info['alert_sent'] = False

        self.results['failures'].append(failure_info)

        return failure_info

    def run_all_checks(self):
        """Run all health checks"""
        self.log("=" * 60)
        self.log("Starting health check cycle")
        self.log("=" * 60)

        # Check PM2 processes
        for service in PM2_SERVICES:
            result = self.check_pm2_process(service)
            self.results['checks'][f'pm2_{service}'] = result

            if not result['healthy']:
                self.handle_failure(
                    service,
                    result,
                    lambda s=service: self.restart_pm2_process(s)
                )

        # Check vault sync
        result = self.check_vault_sync()
        self.results['checks']['vault_sync'] = result

        if not result['healthy']:
            self.handle_failure(
                'vault_sync',
                result,
                self.restart_vault_sync
            )

        # Check disk space
        result = self.check_disk_space()
        self.results['checks']['disk_space'] = result

        if not result['healthy']:
            self.handle_failure('disk_space', result)

        # Check Claude API
        result = self.check_claude_api()
        self.results['checks']['claude_api'] = result

        if not result['healthy']:
            self.handle_failure('claude_api', result)

        # Check MCP servers
        for server in MCP_SERVERS:
            result = self.check_mcp_server(server)
            self.results['checks'][f"mcp_{server['name']}"] = result

            if not result['healthy']:
                self.handle_failure(
                    f"mcp_{server['name']}",
                    result
                )

        # Save results
        self.save_results()

        # Summary
        self.log("=" * 60)
        self.log("Health check complete")
        self.log(f"Total checks: {len(self.results['checks'])}")
        self.log(f"Failures: {len(self.results['failures'])}")
        self.log(f"Alerts sent: {len(self.results['alerts_sent'])}")
        self.log("=" * 60)

    def save_results(self):
        """Save health check results to log file"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"health_{date_str}.json"

        # Load existing logs for today
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        else:
            logs = []

        # Append new results
        logs.append(self.results)

        # Save
        try:
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)

            self.log(f"Results saved to {log_file}")
        except Exception as e:
            self.log(f"Failed to save results: {str(e)}", "ERROR")


def main():
    """Main entry point"""
    monitor = HealthMonitor()

    try:
        monitor.run_all_checks()
        sys.exit(0)
    except Exception as e:
        monitor.log(f"Health monitor crashed: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
