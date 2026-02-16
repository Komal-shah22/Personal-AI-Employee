# Production Monitoring System

Comprehensive health monitoring and status dashboard for AI Employee system.

## Components

### 1. Health Monitor (`health_monitor.py`)

Production watchdog that runs every 5 minutes to check system health and auto-restart failed services.

**Checks:**
- ✅ PM2 processes (gmail-watcher, file-watcher, orchestrator)
- ✅ Vault sync (last git commit < 10 minutes)
- ✅ Disk space (> 20% free)
- ✅ Claude Code API (test call)
- ✅ MCP servers (email, social, payment)

**Auto-Recovery:**
- Attempts to restart failed PM2 processes
- Waits 30 seconds and re-checks
- Sends alert email if recovery fails
- Logs all results to `AI_Employee_Vault/Logs/health_[date].json`

**Alert Email Format:**
```
Subject: [ALERT] AI Employee - [service] is down

Body:
- What failed
- What was tried
- What needs manual attention
```

### 2. Status Dashboard (`status_dashboard.py`)

Real-time status display of all services in a formatted table.

**Display:**
```
┌─────────────────────────┬──────────┬─────────────────┐
│ Service                 │ Status   │ Last Active     │
├─────────────────────────┼──────────┼─────────────────┤
│ Gmail Watcher           │  ✅ UP   │ 2 min ago       │
│ WhatsApp Watcher        │  ✅ UP   │ 30 sec ago      │
│ Orchestrator            │  ✅ UP   │ 5 min ago       │
│ Vault Sync              │  ✅ UP   │ 3 min ago       │
│ Email MCP               │  ✅ UP   │ Just now        │
│ Social MCP              │  ✅ UP   │ Just now        │
│ Payment MCP             │  ✅ UP   │ Just now        │
└─────────────────────────┴──────────┴─────────────────┘

Summary: 7 UP, 0 DOWN, 0 STALE
```

## Setup

### Prerequisites

```bash
# Install required Python packages
pip install requests

# Ensure PM2 is installed
npm install -g pm2
```

### Configuration

1. **Set alert email** (optional):
   ```bash
   export ALERT_EMAIL="your-email@example.com"
   ```

2. **Ensure ANTHROPIC_API_KEY is set**:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

### Automated Monitoring Setup

#### Linux/Mac (Cron)

1. **Edit crontab**:
   ```bash
   crontab -e
   ```

2. **Add health monitor** (runs every 5 minutes):
   ```bash
   */5 * * * * cd /path/to/Personal_AI_Employee && python monitor/health_monitor.py >> monitor/logs/health.log 2>&1
   ```

3. **Verify cron job**:
   ```bash
   crontab -l
   ```

#### Windows (Task Scheduler)

1. **Run setup script**:
   ```cmd
   monitor\setup_windows_task.bat
   ```

   Or manually:
   - Open Task Scheduler
   - Create Basic Task: "AI Employee Health Monitor"
   - Trigger: Every 5 minutes
   - Action: Start a program
     - Program: `python`
     - Arguments: `monitor\health_monitor.py`
     - Start in: `E:\hackathon-0\Personal_AI_Employee`

## Usage

### Health Monitor

**Run once** (manual check):
```bash
python monitor/health_monitor.py
```

**Output:**
```
[2026-02-16 10:00:00] [LOCAL] [INFO] Starting health check cycle
[2026-02-16 10:00:01] [LOCAL] [INFO] Checking PM2 process: gmail-watcher
[2026-02-16 10:00:01] [LOCAL] [INFO] Process gmail-watcher is running
[2026-02-16 10:00:02] [LOCAL] [INFO] Checking vault sync...
[2026-02-16 10:00:02] [LOCAL] [INFO] Last commit 3.2 minutes ago
...
[2026-02-16 10:00:10] [LOCAL] [INFO] Health check complete
[2026-02-16 10:00:10] [LOCAL] [INFO] Total checks: 10
[2026-02-16 10:00:10] [LOCAL] [INFO] Failures: 0
[2026-02-16 10:00:10] [LOCAL] [INFO] Alerts sent: 0
```

### Status Dashboard

**Single check**:
```bash
python monitor/status_dashboard.py
```

**Auto-refresh** (every 30 seconds):
```bash
python monitor/status_dashboard.py --watch
```

**Custom refresh interval**:
```bash
python monitor/status_dashboard.py --watch --interval 60
```

**Detailed status**:
```bash
python monitor/status_dashboard.py --details
```

## Health Check Results

Results are saved to `AI_Employee_Vault/Logs/health_[date].json`:

```json
[
  {
    "timestamp": "2026-02-16T10:00:00",
    "checks": {
      "pm2_gmail-watcher": {
        "status": "online",
        "healthy": true,
        "uptime": 1234567890,
        "restarts": 0
      },
      "vault_sync": {
        "status": "active",
        "healthy": true,
        "last_commit": "2026-02-16T09:57:00",
        "age_minutes": 3.2
      },
      "disk_space": {
        "status": "ok",
        "healthy": true,
        "free_percent": 45.2,
        "free_gb": 120
      }
    },
    "failures": [],
    "alerts_sent": []
  }
]
```

## Troubleshooting

### Health Monitor Not Running

**Check cron job** (Linux/Mac):
```bash
crontab -l | grep health_monitor
```

**Check Task Scheduler** (Windows):
```cmd
schtasks /query /tn "AI_Employee_Health_Monitor"
```

### Alert Emails Not Sending

1. **Check Email MCP is running**:
   ```bash
   curl http://localhost:3001/health
   ```

2. **Check Gmail credentials**:
   ```bash
   cat .claude/mcp-servers/email-mcp/.env
   ```

3. **Test email manually**:
   ```bash
   curl -X POST http://localhost:3001/send_email \
     -H "Content-Type: application/json" \
     -d '{"to":"test@example.com","subject":"Test","body":"Test"}'
   ```

### PM2 Process Not Detected

**Check PM2 is running**:
```bash
pm2 list
```

**Restart PM2**:
```bash
pm2 restart all
```

### Vault Sync Showing Stale

**Check Git status**:
```bash
cd AI_Employee_Vault
git status
git log -1
```

**Manual sync**:
```bash
cd AI_Employee_Vault
git pull --rebase origin main
```

## Monitoring Best Practices

1. **Check dashboard daily**:
   ```bash
   python monitor/status_dashboard.py
   ```

2. **Review health logs weekly**:
   ```bash
   cat AI_Employee_Vault/Logs/health_$(date +%Y-%m-%d).json | jq
   ```

3. **Monitor disk space**:
   - Keep > 20% free
   - Clean old logs if needed

4. **Test alert emails monthly**:
   - Temporarily stop a service
   - Wait for alert email
   - Verify email received

5. **Update alert email**:
   ```bash
   export ALERT_EMAIL="new-email@example.com"
   ```

## Integration with Existing System

### Orchestrator Integration

Add health check before processing:

```python
# In orchestrator.py
import subprocess

def check_system_health():
    result = subprocess.run(
        ['python', 'monitor/health_monitor.py'],
        capture_output=True
    )
    return result.returncode == 0

# Before main loop
if not check_system_health():
    print("System health check failed, review logs")
```

### Dashboard in Web UI

Add status endpoint to dashboard API:

```python
# In ai-employee-dashboard/src/app/api/health/route.ts
import { exec } from 'child_process';

export async function GET() {
  const result = await new Promise((resolve) => {
    exec('python monitor/status_dashboard.py --json', (error, stdout) => {
      resolve(JSON.parse(stdout));
    });
  });

  return Response.json(result);
}
```

## Performance

### Resource Usage

- **CPU**: < 1% (during checks)
- **Memory**: ~50 MB
- **Disk**: ~1 MB/day (logs)
- **Network**: ~100 KB/check (API calls)

### Check Duration

- PM2 processes: ~1 second
- Vault sync: ~2 seconds
- Disk space: < 1 second
- Claude API: ~2 seconds
- MCP servers: ~3 seconds
- **Total**: ~10 seconds per cycle

## Security

### Credentials

- Never log API keys or passwords
- Alert emails don't contain sensitive data
- Health logs exclude credentials

### Access Control

- Health monitor runs as current user
- No elevated privileges required
- Logs stored in vault (Git-ignored if sensitive)

## Advanced Configuration

### Custom Check Intervals

Edit cron job for different intervals:

```bash
# Every 2 minutes
*/2 * * * * cd /path/to/Personal_AI_Employee && python monitor/health_monitor.py

# Every 10 minutes
*/10 * * * * cd /path/to/Personal_AI_Employee && python monitor/health_monitor.py

# Every hour
0 * * * * cd /path/to/Personal_AI_Employee && python monitor/health_monitor.py
```

### Custom Thresholds

Edit `monitor/health_monitor.py`:

```python
# Vault sync threshold
VAULT_SYNC_MAX_AGE_MINUTES = 15  # Default: 10

# Disk space threshold
DISK_SPACE_MIN_PERCENT = 15  # Default: 20

# Max restart attempts
MAX_RESTART_ATTEMPTS = 3  # Default: 2
```

### Additional Services

Add custom services to monitor:

```python
# In monitor/health_monitor.py
SERVICES.append({
    'name': 'Custom Service',
    'pm2_name': 'custom-service',
    'type': 'pm2'
})
```

## Summary

✅ **Health Monitor**: Automated watchdog with auto-restart and alerts
✅ **Status Dashboard**: Real-time system status display
✅ **Cron Integration**: Runs every 5 minutes automatically
✅ **Alert System**: Email notifications for failures
✅ **Comprehensive Logging**: JSON logs for analysis
✅ **Auto-Recovery**: Attempts to restart failed services

**Next Steps:**
1. Run `python monitor/status_dashboard.py` to check current status
2. Set up cron job for automated monitoring
3. Configure alert email address
4. Test alert system by stopping a service

---

**Version**: 1.0.0
**Last Updated**: 2026-02-16
**Status**: Production Ready
