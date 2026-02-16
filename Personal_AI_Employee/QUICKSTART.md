# AI Employee - Complete System

## Quick Start Guide

Get your AI Employee up and running in 5 minutes.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the File Watcher (No Setup Required)

```bash
python watchers/file_watcher.py
```

Drop files into `~/Desktop/AI_Drop_Folder/` and they'll be automatically processed.

### 3. Start the Orchestrator (DRY RUN Mode)

```bash
python orchestrator.py
```

The orchestrator will process tasks every 5 minutes in safe DRY RUN mode.

### 4. Optional: Setup Gmail Watcher

Follow `README_gmail_setup.md` to configure Gmail monitoring.

### 5. Optional: Setup WhatsApp Watcher

Follow `WHATSAPP_SETUP_GUIDE.md` to configure WhatsApp monitoring.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        WATCHERS                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐             │
│  │  Gmail   │  │WhatsApp  │  │ File Watcher │             │
│  │ Watcher  │  │ Watcher  │  │              │             │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘             │
│       │             │                │                      │
│       └─────────────┴────────────────┘                      │
│                     │                                        │
└─────────────────────┼────────────────────────────────────────┘
                      ▼
         ┌────────────────────────┐
         │   Needs_Action/        │
         │   (New Tasks)          │
         └────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│                                                              │
│  1. Scan Needs_Action/ every 5 minutes                      │
│  2. Parse YAML frontmatter                                  │
│  3. Route to appropriate skill                              │
│  4. Move to In_Progress/                                    │
│  5. Call Claude Code with skill                             │
│  6. Create Plan in Plans/                                   │
│  7. Create approval request if needed                       │
│  8. Move to Done/                                           │
│  9. Update Dashboard.md                                     │
│  10. Log to daily JSON                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │  Pending_Approval/     │
         │  (Awaiting Human)      │
         └────────┬───────────────┘
                  │
                  │ (Human approves)
                  ▼
         ┌────────────────────────┐
         │     Approved/          │
         │  (Ready to Execute)    │
         └────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR (Execution)                        │
│                                                              │
│  1. Scan Approved/ folder                                   │
│  2. Parse action details                                    │
│  3. Execute via MCP server                                  │
│  4. Log execution                                           │
│  5. Move to Done/                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │       Done/            │
         │   (Completed)          │
         └────────────────────────┘
```

## Directory Structure

```
Personal_AI_Employee/
├── watchers/
│   ├── gmail_watcher.py          # Gmail monitoring
│   ├── whatsapp_watcher.py       # WhatsApp monitoring
│   └── file_watcher.py           # File drop monitoring
│
├── orchestrator.py               # Master controller
├── start_watchers.py             # Unified watcher launcher
│
├── .claude/
│   └── skills/
│       ├── email_reply_skill.md  # Email response generation
│       ├── invoice_skill.md      # Invoice generation
│       └── ...                   # Other skills
│
├── AI_Employee_Vault/
│   ├── Needs_Action/             # New tasks from watchers
│   ├── In_Progress/              # Currently processing
│   ├── Done/                     # Completed tasks
│   ├── Approved/                 # Approved actions
│   ├── Pending_Approval/         # Awaiting approval
│   ├── Plans/                    # Generated plans
│   ├── Logs/                     # Daily JSON logs
│   └── Dashboard.md              # Activity dashboard
│
├── requirements.txt              # Python dependencies
├── .env                          # Configuration (create from .env.template)
├── .env.template                 # Configuration template
│
└── Documentation/
    ├── ORCHESTRATOR_README.md    # Orchestrator guide
    ├── WATCHERS_README.md        # Watchers guide
    ├── README_gmail_setup.md     # Gmail setup
    ├── README_file_watcher.md    # File watcher guide
    └── WHATSAPP_SETUP_GUIDE.md   # WhatsApp setup
```

## Components

### 1. Watchers (Input Layer)

Monitor external sources and create action items:

- **Gmail Watcher**: Monitors unread important emails
- **WhatsApp Watcher**: Monitors WhatsApp messages
- **File Watcher**: Monitors desktop drop folder

**Output**: Creates `.md` files in `Needs_Action/` with YAML frontmatter

### 2. Orchestrator (Processing Layer)

Coordinates the entire system:

- Scans `Needs_Action/` every 5 minutes
- Routes tasks to appropriate Claude Code skills
- Manages task lifecycle (Needs_Action → In_Progress → Done)
- Creates plans and approval requests
- Executes approved actions via MCP servers
- Updates dashboard and logs

**Key Features**:
- DRY RUN mode (default: enabled)
- Concurrent processing (up to 10 tasks)
- Automatic dashboard updates
- Daily JSON logging

### 3. Skills (Intelligence Layer)

Claude Code skills that process specific task types:

- `email_reply_skill.md` - Generate email responses
- `invoice_skill.md` - Generate invoices
- Custom skills can be added

### 4. MCP Servers (Execution Layer)

Execute approved actions:

- Email MCP - Send emails
- Payment MCP - Process payments
- File MCP - File operations

### 5. Dashboard (Monitoring Layer)

Real-time view of system activity:

- Status counts (Pending, In Progress, Completed)
- Recent activity table
- Last updated timestamp

## Workflow Example

### Example: Invoice Request via Email

1. **Gmail Watcher** detects unread important email: "Can you send me an invoice?"
2. Creates `EMAIL_invoice_request_20260216_143000.md` in `Needs_Action/`
3. **Orchestrator** scans folder (next 5-minute cycle)
4. Reads YAML frontmatter: `type: email`
5. Routes to `email_reply_skill.md`
6. Moves to `In_Progress/`
7. Calls Claude Code with skill
8. Claude creates plan in `Plans/`
9. Claude creates approval request in `Pending_Approval/`
10. Moves to `Done/`
11. Updates `Dashboard.md`
12. Logs to `2026-02-16.json`
13. **Human** reviews approval request
14. Moves approved action to `Approved/`
15. **Orchestrator** detects approved action
16. Executes via Email MCP server
17. Logs execution
18. Moves to `Done/`

## Running the Complete System

### Option 1: Run All Components Separately

```bash
# Terminal 1: File Watcher
python watchers/file_watcher.py

# Terminal 2: Gmail Watcher (if configured)
python watchers/gmail_watcher.py

# Terminal 3: WhatsApp Watcher (if configured)
python watchers/whatsapp_watcher.py

# Terminal 4: Orchestrator
python orchestrator.py
```

### Option 2: Use Unified Launcher

```bash
# Start all watchers
python start_watchers.py all

# In another terminal: Start orchestrator
python orchestrator.py
```

### Option 3: Run as Services

See individual README files for service setup instructions.

## Configuration

### Environment Variables (.env)

```bash
# Orchestrator
DRY_RUN=true                    # Safe mode (default)
CHECK_INTERVAL=300              # 5 minutes
MAX_CONCURRENT_TASKS=10

# Gmail Watcher
GMAIL_CLIENT_ID=your_id
GMAIL_CLIENT_SECRET=your_secret

# Claude Code
ANTHROPIC_API_KEY=your_key
```

## Monitoring

### Real-Time Logs

```bash
# Orchestrator
tail -f AI_Employee_Vault/Logs/orchestrator.log

# File Watcher
tail -f AI_Employee_Vault/Logs/file_watcher.log

# Gmail Watcher
tail -f AI_Employee_Vault/Logs/gmail_watcher.log
```

### Dashboard

View `AI_Employee_Vault/Dashboard.md` for:
- Current status counts
- Recent activity (last 10 items)
- Last update time

### Daily Logs

JSON logs in `AI_Employee_Vault/Logs/YYYY-MM-DD.json`:
```json
{
  "date": "2026-02-16",
  "actions": [...],
  "executions": [...]
}
```

## Safety Features

### DRY RUN Mode (Default: ON)

- Processes tasks without executing actions
- Safe for testing and development
- Disable only when ready for production

### Approval Workflow

- Sensitive actions require human approval
- Review in `Pending_Approval/` folder
- Move to `Approved/` to execute

### Logging

- All actions logged for audit trail
- Daily JSON logs for analysis
- Console and file logging

## Troubleshooting

### No Tasks Being Processed

1. Check if orchestrator is running
2. Check if watchers are running
3. Verify tasks exist in `Needs_Action/`
4. Check logs for errors

### Tasks Stuck in In_Progress

Orchestrator crashed during processing. Move back:
```bash
mv AI_Employee_Vault/In_Progress/*.md AI_Employee_Vault/Needs_Action/
```

### Watchers Not Creating Tasks

1. Check watcher logs
2. Verify configuration (.env)
3. Test manually (drop file, send email, etc.)

## Next Steps

1. **Start with File Watcher**: No setup required
2. **Test with Orchestrator**: DRY RUN mode is safe
3. **Setup Gmail**: Follow `README_gmail_setup.md`
4. **Setup WhatsApp**: Follow `WHATSAPP_SETUP_GUIDE.md`
5. **Disable DRY RUN**: When ready for production

## Documentation

- **Orchestrator**: `ORCHESTRATOR_README.md`
- **Watchers**: `WATCHERS_README.md`
- **Gmail Setup**: `README_gmail_setup.md`
- **File Watcher**: `README_file_watcher.md`
- **WhatsApp Setup**: `WHATSAPP_SETUP_GUIDE.md`

## Support

For issues or questions:
1. Check the logs first
2. Review the appropriate README
3. Verify configuration
4. Check GitHub issues

---

**Ready to start?** Run `python watchers/file_watcher.py` and drop a file into `~/Desktop/AI_Drop_Folder/`!
