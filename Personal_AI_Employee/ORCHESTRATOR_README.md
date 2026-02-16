# Orchestrator - AI Employee Master Controller

The orchestrator is the brain of the AI Employee system. It coordinates all components, routes tasks to appropriate skills, manages task lifecycle, and executes approved actions.

## Overview

The orchestrator runs continuously, checking for new tasks every 5 minutes and processing them through the complete workflow:

```
Watchers → Needs_Action → In_Progress → Plans → Pending_Approval → Approved → Done
```

## Key Features

- **Automatic Task Routing**: Reads YAML frontmatter and routes to appropriate Claude Code skills
- **State Management**: Moves tasks through Needs_Action → In_Progress → Done
- **Concurrent Processing**: Handles up to 10 tasks simultaneously
- **Approval Workflow**: Creates approval requests for sensitive actions
- **Dashboard Updates**: Automatically updates Dashboard.md with activity
- **Daily Logging**: Logs all actions to JSON files (YYYY-MM-DD.json)
- **DRY RUN Mode**: Test without executing actual actions (default: enabled)
- **Error Recovery**: Moves failed tasks back to Needs_Action

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set DRY_RUN Mode

Create or edit `.env`:
```
DRY_RUN=true   # Safe mode - no actual execution
# DRY_RUN=false  # Production mode - executes actions
```

### 3. Start the Orchestrator

```bash
# Run continuously (checks every 5 minutes)
python orchestrator.py

# Run once and exit
python orchestrator.py --once

# Disable dry-run mode
python orchestrator.py --no-dry-run
```

## How It Works

### Task Processing Flow

1. **Scan**: Every 5 minutes, scans `AI_Employee_Vault/Needs_Action/` for `.md` files
2. **Parse**: Reads YAML frontmatter to determine task type
3. **Route**: Selects appropriate skill based on type:
   - `type: email` → `email_reply_skill.md`
   - `type: file_drop` → Detects content, routes to `invoice_skill.md` or default
   - `type: whatsapp` → Detects intent, routes to appropriate skill
4. **Move to In_Progress**: Moves file while processing
5. **Call Claude Code**: Invokes Claude with the selected skill
6. **Create Plan**: Claude creates plan in `Plans/` directory
7. **Create Approval**: If needed, creates approval request in `Pending_Approval/`
8. **Move to Done**: Completes task lifecycle
9. **Update Dashboard**: Updates `Dashboard.md` with activity
10. **Log**: Records action in daily JSON log

### Approval Execution Flow

1. **Scan**: Checks `AI_Employee_Vault/Approved/` for approved actions
2. **Parse**: Reads action details from frontmatter
3. **Execute**: Calls appropriate MCP server:
   - `action_type: send_email` → Email MCP server
   - `action_type: payment` → Payment MCP server
   - `action_type: file_operation` → File MCP server
4. **Log**: Records execution in daily JSON log
5. **Move to Done**: Archives approved action

## Task Type Routing

### Email Tasks
```yaml
---
type: email
from: sender@example.com
subject: Question about invoice
priority: high
status: pending
---
```
**Routes to**: `email_reply_skill.md`

### File Drop Tasks
```yaml
---
type: file_drop
original_name: invoice.pdf
detected_type: invoice
size: 245.67 KB
status: pending
---
```
**Routes to**: `invoice_skill.md` (if invoice) or default skill

### WhatsApp Tasks
```yaml
---
type: whatsapp
from: +1234567890
message: Can you send me an invoice?
status: pending
---
```
**Routes to**: `invoice_skill.md` (if mentions invoice) or `email_reply_skill.md`

## Configuration

### Environment Variables

Create `.env` file:
```bash
# Orchestrator settings
DRY_RUN=true                    # Enable dry-run mode (default: true)
CHECK_INTERVAL=300              # Check interval in seconds (default: 300)
MAX_CONCURRENT_TASKS=10         # Max parallel tasks (default: 10)

# Claude Code settings
ANTHROPIC_API_KEY=your_key_here
```

### Directory Structure

The orchestrator expects this structure:
```
AI_Employee_Vault/
├── Needs_Action/       # New tasks from watchers
├── In_Progress/        # Currently processing
├── Done/               # Completed tasks
├── Approved/           # Approved actions ready to execute
├── Pending_Approval/   # Awaiting human approval
├── Plans/              # Generated plans
├── Logs/               # Daily JSON logs
└── Dashboard.md        # Activity dashboard
```

All directories are created automatically on first run.

## Command Line Options

```bash
# Run continuously with dry-run (default)
python orchestrator.py

# Run continuously without dry-run
python orchestrator.py --no-dry-run

# Process once and exit
python orchestrator.py --once

# Show help
python orchestrator.py --help
```

## Logging

### Console Logs
Real-time output to console:
```
2026-02-16 14:30:00 - INFO - Found 3 tasks in Needs_Action
2026-02-16 14:30:01 - INFO - Processing task: EMAIL_invoice_request
2026-02-16 14:30:02 - INFO - Task type: email
2026-02-16 14:30:03 - INFO - DRY RUN: Would call Claude Code with skill...
```

### File Logs
Detailed logs in `AI_Employee_Vault/Logs/orchestrator.log`

### Daily JSON Logs
Structured logs in `AI_Employee_Vault/Logs/YYYY-MM-DD.json`:
```json
{
  "date": "2026-02-16",
  "actions": [
    {
      "timestamp": "2026-02-16T14:30:00",
      "task_id": "EMAIL_invoice_request",
      "type": "email",
      "success": true,
      "frontmatter": {...}
    }
  ],
  "executions": [
    {
      "timestamp": "2026-02-16T14:35:00",
      "action_id": "APPROVAL_email_send",
      "type": "send_email",
      "details": {...}
    }
  ]
}
```

## Dashboard Updates

The orchestrator automatically updates `AI_Employee_Vault/Dashboard.md`:

### Status Counts
```markdown
## Status Overview

- **Pending**: 5
- **In Progress**: 2
- **Completed**: 127
```

### Recent Activity Table
```markdown
## Recent Activity

| Time | Type | Description | Status |
|------|------|-------------|--------|
| 2026-02-16 14:30 | email | Invoice request from client | ✅ Done |
| 2026-02-16 14:25 | file_drop | invoice.pdf | ✅ Done |
```

Only the last 10 activities are shown.

## DRY RUN Mode

**Default: ENABLED** for safety.

### What DRY RUN Does:
- ✅ Scans folders
- ✅ Parses tasks
- ✅ Routes to skills
- ✅ Moves files between folders
- ✅ Updates dashboard
- ✅ Logs actions
- ❌ Does NOT call Claude Code API
- ❌ Does NOT execute approved actions
- ❌ Does NOT send emails/make payments

### Disabling DRY RUN:
```bash
# Option 1: Command line
python orchestrator.py --no-dry-run

# Option 2: Environment variable
# In .env file:
DRY_RUN=false
```

## Concurrent Task Processing

The orchestrator processes up to 10 tasks simultaneously using a thread pool:

```python
MAX_CONCURRENT_TASKS = 10  # Configurable
```

### How It Works:
1. Scans Needs_Action folder
2. Submits up to 10 tasks to thread pool
3. Each task runs independently
4. Waits for all to complete before next cycle

### Benefits:
- Faster processing of multiple tasks
- Efficient resource utilization
- Non-blocking operation

## Error Handling

### Task Processing Errors
If a task fails during processing:
1. Error is logged to console and file
2. Task is moved back to Needs_Action
3. Will be retried on next cycle
4. After 3 failures, human notification (TODO)

### Approval Execution Errors
If an approved action fails:
1. Error is logged
2. Action remains in Approved folder
3. Human can review and retry

## Integration with Other Components

### Watchers
Watchers create tasks in `Needs_Action/`:
- Gmail Watcher → Email tasks
- File Watcher → File drop tasks
- WhatsApp Watcher → WhatsApp tasks

### Skills
Orchestrator invokes Claude Code with skills:
- `email_reply_skill.md` - Email responses
- `invoice_skill.md` - Invoice generation
- Custom skills can be added

### MCP Servers
Orchestrator calls MCP servers for execution:
- Email MCP - Send emails
- Payment MCP - Process payments
- File MCP - File operations

### Dashboard
Orchestrator updates dashboard after each action:
- Status counts
- Recent activity table
- Last updated timestamp

## Running as a Service

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task: "AI Employee Orchestrator"
3. Trigger: At startup
4. Action: Start a program
   - Program: `python`
   - Arguments: `E:\hackathon-0\Personal_AI_Employee\orchestrator.py`
   - Start in: `E:\hackathon-0\Personal_AI_Employee`

### Linux (systemd)

Create `/etc/systemd/system/ai-orchestrator.service`:
```ini
[Unit]
Description=AI Employee Orchestrator
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Personal_AI_Employee
ExecStart=/usr/bin/python3 orchestrator.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-orchestrator
sudo systemctl start ai-orchestrator
sudo systemctl status ai-orchestrator
```

### macOS (launchd)

Create `~/Library/LaunchAgents/com.ai-employee.orchestrator.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-employee.orchestrator</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/orchestrator.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ai-orchestrator.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ai-orchestrator-error.log</string>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.ai-employee.orchestrator.plist
```

## Monitoring

### Check Status
```bash
# View real-time logs
tail -f AI_Employee_Vault/Logs/orchestrator.log

# Check today's actions
cat AI_Employee_Vault/Logs/$(date +%Y-%m-%d).json | jq

# Count pending tasks
ls AI_Employee_Vault/Needs_Action/*.md | wc -l

# Check if running
ps aux | grep orchestrator.py
```

### Health Checks
```bash
# Check last log entry
tail -1 AI_Employee_Vault/Logs/orchestrator.log

# Check dashboard update time
grep "Last updated" AI_Employee_Vault/Dashboard.md
```

## Troubleshooting

### No Tasks Being Processed

**Check:**
1. Is orchestrator running? `ps aux | grep orchestrator`
2. Are there tasks in Needs_Action? `ls AI_Employee_Vault/Needs_Action/`
3. Check logs: `tail -f AI_Employee_Vault/Logs/orchestrator.log`
4. Is DRY_RUN enabled? Check console output

### Tasks Stuck in In_Progress

**Cause**: Orchestrator crashed during processing

**Fix**:
```bash
# Move back to Needs_Action
mv AI_Employee_Vault/In_Progress/*.md AI_Employee_Vault/Needs_Action/
```

### Claude Code Not Being Called

**Check:**
1. Is DRY_RUN enabled? (default: yes)
2. Disable: `python orchestrator.py --no-dry-run`
3. Check ANTHROPIC_API_KEY in .env
4. Verify skill files exist in `.claude/skills/`

### Dashboard Not Updating

**Check:**
1. Does Dashboard.md exist?
2. Check file permissions
3. Review logs for "Dashboard updated" messages
4. Manually create: `touch AI_Employee_Vault/Dashboard.md`

## Performance

- **CPU Usage**: ~5-10% during processing, <1% idle
- **Memory**: ~100-200MB
- **Disk I/O**: Minimal (only during task processing)
- **Network**: Only when calling Claude Code API

## Security Considerations

- **DRY_RUN**: Always enabled by default for safety
- **Approval Required**: Sensitive actions require human approval
- **Logging**: All actions logged for audit trail
- **API Keys**: Stored in .env (excluded from git)
- **File Permissions**: Ensure proper permissions on vault directories

## Customization

### Change Check Interval

Edit `orchestrator.py`:
```python
CHECK_INTERVAL = 300  # Change to desired seconds
```

Or set environment variable:
```bash
CHECK_INTERVAL=600  # 10 minutes
```

### Add Custom Task Types

Edit `TaskProcessor.get_skill_for_task()`:
```python
def get_skill_for_task(self, task_type: str, frontmatter: Dict, body: str):
    if task_type == 'custom_type':
        return '.claude/skills/custom_skill.md'
    # ... existing code
```

### Add Custom Action Types

Edit `Orchestrator.execute_approved_action()`:
```python
if action_type == 'custom_action':
    self.execute_custom_action(frontmatter, body)
```

## Development

### Testing

```bash
# Test with dry-run (safe)
python orchestrator.py --once

# Test without dry-run (caution!)
python orchestrator.py --once --no-dry-run
```

### Debugging

Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Roadmap

Future enhancements:
- [ ] Web UI for monitoring
- [ ] Retry logic with exponential backoff
- [ ] Task priority queue
- [ ] Scheduled tasks
- [ ] Task dependencies
- [ ] Metrics and analytics
- [ ] Health check endpoint
- [ ] Slack/email notifications
- [ ] Task templates
- [ ] Workflow builder

---

**Related Documentation**:
- Watchers: `WATCHERS_README.md`
- Skills: `.claude/skills/*/README.md`
- Dashboard: `AI_Employee_Vault/Dashboard.md`
