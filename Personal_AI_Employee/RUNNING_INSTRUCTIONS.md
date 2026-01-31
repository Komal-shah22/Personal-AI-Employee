# Running the Personal AI Employee

The Personal AI Employee system is currently running with the following components:

## Active Services

1. **Orchestrator** - Running in background (PID: b9710ab)
   - Monitors the vault directories
   - Processes items in the Needs_Action folder
   - Creates plans and moves items through the workflow

2. **Gmail Watcher** - Running in background (PID: b0cfebe)
   - Monitors Gmail for new emails
   - Creates action items from unread emails
   - Marks processed emails as read

## Managing the System

### Check Current Status
```bash
python check_dashboard.py
```

### View Service Outputs
To check the orchestrator output:
```bash
# On Linux/Mac
cat /tmp/orchestrator_output.log

# On Windows (use the TaskOutput tool in Claude Code)
```

### Stopping the Services
To stop the background services, you can kill the processes:
```bash
# If running in Python directly, press Ctrl+C in the respective terminals
```

### Using Claude Code Skills
The system includes several custom skills that can be run with Claude Code:

- `claude skill process-tasks` - Process pending tasks
- `claude skill update-dashboard` - Update dashboard statistics
- `claude skill complete-task` - Mark tasks as complete
- `claude skill request-approval` - Request approval for actions
- `claude skill process-emails` - Process incoming emails

## How to Interact with the System

1. **Adding New Tasks**: Place files in `AI_Employee_Vault/Inbox/` or create new items in `AI_Employee_Vault/Needs_Action/`

2. **Monitoring Progress**: Check the dashboard using `python check_dashboard.py` or review the various vault directories

3. **Reviewing Plans**: Completed plans are stored in `AI_Employee_Vault/Plans/`

4. **Checking Logs**: System logs are available in `AI_Employee_Vault/Logs/`

## Troubleshooting

- If services aren't running, check that all dependencies are installed (`pip install -r requirements.txt`)
- Verify that `credentials.json` exists for Gmail integration
- Check that the vault directory structure exists and is writable
- Review the configuration in `config.json`