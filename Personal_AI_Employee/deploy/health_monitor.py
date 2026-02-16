#!/usr/bin/env python3
"""
Cloud VM Health Monitor

Monitors Oracle Cloud VM and AI Employee containers:
- Pings VM every 5 minutes
- Checks container health status
- Sends email alerts if issues detected
- Auto-restarts unhealthy containers

Usage:
    python deploy/health_monitor.py

Configuration:
    Edit the variables below or use environment variables
"""

import subprocess
import time
import smtplib
import sys
from email.message import EmailMessage
from datetime import datetime
import os

# Configuration
VM_IP = os.getenv('VM_IP', '123.45.67.89')  # Your Oracle Cloud VM IP
VM_USER = os.getenv('VM_USER', 'ubuntu')
SSH_KEY = os.getenv('SSH_KEY', '~/.ssh/ai-employee-key.pem')

# Alert configuration
ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'your-email@example.com')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

# Monitoring configuration
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))  # 5 minutes
MAX_FAILURES = int(os.getenv('MAX_FAILURES', '3'))  # Alert after 3 failures

# State tracking
failure_count = 0
last_alert_time = None
ALERT_COOLDOWN = 3600  # 1 hour between alerts


def log(message, level="INFO"):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def send_alert(subject, body):
    """Send email alert"""
    global last_alert_time

    # Check cooldown
    if last_alert_time:
        time_since_last = (datetime.now() - last_alert_time).total_seconds()
        if time_since_last < ALERT_COOLDOWN:
            log(f"Alert cooldown active ({int(time_since_last)}s since last alert)", "WARNING")
            return

    if not SMTP_USER or not SMTP_PASSWORD:
        log("SMTP credentials not configured - cannot send alert", "ERROR")
        log(f"Alert: {subject}", "ERROR")
        log(f"Body: {body}", "ERROR")
        return

    try:
        msg = EmailMessage()
        msg['Subject'] = f"[AI Employee Monitor] {subject}"
        msg['From'] = SMTP_USER
        msg['To'] = ALERT_EMAIL
        msg.set_content(body)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        log(f"Alert sent: {subject}", "INFO")
        last_alert_time = datetime.now()

    except Exception as e:
        log(f"Failed to send alert: {e}", "ERROR")


def ping_vm():
    """Check if VM is reachable via ping"""
    try:
        # Use ping command (works on Windows, Mac, Linux)
        if sys.platform == 'win32':
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '2000', VM_IP],
                capture_output=True,
                timeout=5
            )
        else:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', VM_IP],
                capture_output=True,
                timeout=5
            )

        return result.returncode == 0

    except Exception as e:
        log(f"Ping failed: {e}", "ERROR")
        return False


def check_ssh_connection():
    """Check if SSH connection works"""
    try:
        result = subprocess.run(
            ['ssh', '-i', SSH_KEY, '-o', 'ConnectTimeout=10',
             '-o', 'StrictHostKeyChecking=no',
             f'{VM_USER}@{VM_IP}', 'echo "OK"'],
            capture_output=True,
            timeout=15,
            text=True
        )

        return result.returncode == 0 and 'OK' in result.stdout

    except Exception as e:
        log(f"SSH check failed: {e}", "ERROR")
        return False


def check_container_health():
    """Check Docker container health status"""
    try:
        result = subprocess.run(
            ['ssh', '-i', SSH_KEY, '-o', 'ConnectTimeout=10',
             '-o', 'StrictHostKeyChecking=no',
             f'{VM_USER}@{VM_IP}',
             'cd ~/Personal_AI_Employee && docker compose -f deploy/docker-compose.cloud.yml ps --format json'],
            capture_output=True,
            timeout=15,
            text=True
        )

        if result.returncode != 0:
            return False, "Failed to get container status"

        # Check if container is running
        if 'running' not in result.stdout.lower():
            return False, "Container not running"

        # Check health status
        health_result = subprocess.run(
            ['ssh', '-i', SSH_KEY, '-o', 'ConnectTimeout=10',
             '-o', 'StrictHostKeyChecking=no',
             f'{VM_USER}@{VM_IP}',
             'docker inspect ai_employee_cloud --format="{{.State.Health.Status}}"'],
            capture_output=True,
            timeout=15,
            text=True
        )

        health_status = health_result.stdout.strip()

        if health_status == 'healthy':
            return True, "Container healthy"
        elif health_status == 'unhealthy':
            return False, "Container unhealthy"
        else:
            return True, f"Container status: {health_status}"

    except Exception as e:
        log(f"Container health check failed: {e}", "ERROR")
        return False, str(e)


def restart_container():
    """Restart unhealthy container"""
    try:
        log("Attempting to restart container...", "WARNING")

        result = subprocess.run(
            ['ssh', '-i', SSH_KEY, '-o', 'ConnectTimeout=10',
             '-o', 'StrictHostKeyChecking=no',
             f'{VM_USER}@{VM_IP}',
             'cd ~/Personal_AI_Employee && docker compose -f deploy/docker-compose.cloud.yml restart'],
            capture_output=True,
            timeout=60,
            text=True
        )

        if result.returncode == 0:
            log("Container restarted successfully", "INFO")
            send_alert(
                "Container Restarted",
                f"AI Employee container was unhealthy and has been restarted.\n\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"VM: {VM_IP}\n\n"
                f"Please check logs for any issues."
            )
            return True
        else:
            log(f"Container restart failed: {result.stderr}", "ERROR")
            return False

    except Exception as e:
        log(f"Failed to restart container: {e}", "ERROR")
        return False


def perform_health_check():
    """Perform complete health check"""
    global failure_count

    log("Starting health check...", "INFO")

    # Step 1: Ping VM
    log("Checking VM reachability...", "INFO")
    if not ping_vm():
        log("VM is not reachable via ping", "ERROR")
        failure_count += 1

        if failure_count >= MAX_FAILURES:
            send_alert(
                "VM Unreachable",
                f"Oracle Cloud VM is not responding to ping.\n\n"
                f"VM IP: {VM_IP}\n"
                f"Failed checks: {failure_count}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Please check:\n"
                f"1. VM is running in Oracle Cloud Console\n"
                f"2. Network connectivity\n"
                f"3. Firewall rules\n"
                f"4. VM hasn't been stopped or terminated"
            )
            failure_count = 0  # Reset after alert

        return False

    log("✓ VM is reachable", "INFO")

    # Step 2: Check SSH
    log("Checking SSH connection...", "INFO")
    if not check_ssh_connection():
        log("SSH connection failed", "ERROR")
        failure_count += 1

        if failure_count >= MAX_FAILURES:
            send_alert(
                "SSH Connection Failed",
                f"Cannot connect to VM via SSH.\n\n"
                f"VM IP: {VM_IP}\n"
                f"SSH User: {VM_USER}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Please check:\n"
                f"1. SSH service is running\n"
                f"2. SSH key is correct\n"
                f"3. Firewall allows port 22\n"
                f"4. User account is active"
            )
            failure_count = 0

        return False

    log("✓ SSH connection successful", "INFO")

    # Step 3: Check container health
    log("Checking container health...", "INFO")
    is_healthy, status_message = check_container_health()

    if not is_healthy:
        log(f"Container unhealthy: {status_message}", "ERROR")

        # Attempt auto-restart
        if restart_container():
            log("Container restarted successfully", "INFO")
            failure_count = 0
            return True
        else:
            failure_count += 1

            if failure_count >= MAX_FAILURES:
                send_alert(
                    "Container Unhealthy - Restart Failed",
                    f"AI Employee container is unhealthy and auto-restart failed.\n\n"
                    f"VM IP: {VM_IP}\n"
                    f"Status: {status_message}\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"Manual intervention required.\n\n"
                    f"To investigate:\n"
                    f"1. SSH to VM: ssh -i {SSH_KEY} {VM_USER}@{VM_IP}\n"
                    f"2. Check logs: docker compose -f deploy/docker-compose.cloud.yml logs\n"
                    f"3. Check status: docker compose -f deploy/docker-compose.cloud.yml ps\n"
                    f"4. Restart manually: docker compose -f deploy/docker-compose.cloud.yml restart"
                )
                failure_count = 0

            return False

    log(f"✓ Container healthy: {status_message}", "INFO")

    # All checks passed
    failure_count = 0
    log("Health check completed successfully", "INFO")
    return True


def main():
    """Main monitoring loop"""
    log("=" * 60)
    log("AI EMPLOYEE CLOUD HEALTH MONITOR")
    log("=" * 60)
    log(f"VM IP: {VM_IP}")
    log(f"Check interval: {CHECK_INTERVAL} seconds")
    log(f"Alert email: {ALERT_EMAIL}")
    log(f"Max failures before alert: {MAX_FAILURES}")
    log("=" * 60)

    if not SMTP_USER or not SMTP_PASSWORD:
        log("WARNING: SMTP credentials not configured - alerts will not be sent", "WARNING")
        log("Set SMTP_USER and SMTP_PASSWORD environment variables", "WARNING")

    check_count = 0

    try:
        while True:
            check_count += 1
            log(f"\n--- Health Check #{check_count} ---")

            perform_health_check()

            log(f"Next check in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log("\nMonitoring stopped by user", "INFO")
    except Exception as e:
        log(f"Unexpected error: {e}", "ERROR")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
