# Claude Code Hooks - Ralph Wiggum Loop

This directory contains hooks that modify Claude Code's behavior.

## What Are Hooks?

Hooks are scripts that run at specific points in Claude Code's lifecycle:
- **stop_hook.py**: Runs when Claude tries to exit
- **start_hook.py**: Runs when Claude starts (not implemented)
- **error_hook.py**: Runs when an error occurs (not implemented)

## The Ralph Wiggum Stop Hook

Named after Ralph Wiggum's enthusiastic "I'm helping!" attitude, this hook prevents Claude from stopping when there's still work to do.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Claude finishes a task and tries to exit                │
├─────────────────────────────────────────────────────────────┤
│ 2. Stop hook intercepts the exit                           │
├─────────────────────────────────────────────────────────────┤
│ 3. Hook checks AI_Employee_Vault/Needs_Action/ for files   │
├─────────────────────────────────────────────────────────────┤
│ 4. Decision:                                                │
│    • Files exist + iterations < max → Continue working     │
│    • No files OR max iterations → Allow stop               │
├─────────────────────────────────────────────────────────────┤
│ 5. If continuing: inject new prompt and increment counter  │
└─────────────────────────────────────────────────────────────┘
```

### File Structure

```
.claude/hooks/
├── stop_hook.py          # Main hook logic
└── README.md             # This file

AI_Employee_Vault/
├── Needs_Action/         # Unprocessed tasks (hook checks here)
├── In_Progress/          # Currently processing (hook ignores)
├── Done/                 # Completed tasks
└── Plans/
    └── loop_status.md    # Iteration counter and status

scripts/
└── ralph-loop.sh         # Wrapper to start Claude with hook
```

### Loop Status Tracking

The hook tracks iterations in `AI_Employee_Vault/Plans/loop_status.md`:

```yaml
---
iteration: 3
max_iterations: 10
started: 2026-02-16T10:00:00Z
last_updated: 2026-02-16T10:15:00Z
status: running
---
```

**Status values:**
- `running`: Loop is active, processing tasks
- `completed`: All tasks processed successfully
- `no_work`: No tasks found to process
- `max_iterations_reached`: Stopped due to iteration limit

### Usage

#### Method 1: Using the Wrapper Script (Recommended)

```bash
# Process all pending tasks (max 10 iterations)
./scripts/ralph-loop.sh "Process all pending tasks"

# Custom max iterations
./scripts/ralph-loop.sh --max-iterations 20 "Process all emails and invoices"

# Get help
./scripts/ralph-loop.sh --help
```

#### Method 2: Manual Claude Invocation

```bash
# Set max iterations
export RALPH_MAX_ITERATIONS=10

# Start Claude (hook will activate automatically)
claude -p "Process all pending tasks"
```

#### Method 3: Enable Hook Globally

Add to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
export RALPH_MAX_ITERATIONS=10
```

Now every Claude Code session will use the stop hook.

### Configuration

**Environment Variables:**

- `RALPH_MAX_ITERATIONS`: Maximum iterations before stopping (default: 10)

**Hook Behavior:**

The hook considers a file "unprocessed" if:
1. It's in `AI_Employee_Vault/Needs_Action/`
2. It has a `.md` extension
3. It doesn't start with `_` (underscore)
4. It's not already in `AI_Employee_Vault/In_Progress/`

### Examples

#### Example 1: Process All Pending Tasks

```bash
./scripts/ralph-loop.sh "Process all pending tasks"
```

**What happens:**
1. Claude starts and processes first task
2. Moves it to Done/
3. Tries to exit
4. Hook detects more files in Needs_Action/
5. Hook injects: "Continue working. 5 files remain..."
6. Claude continues with next task
7. Repeats until all done or max iterations

#### Example 2: Batch Email Processing

```bash
# Create multiple email tasks
for i in {1..5}; do
  cat > AI_Employee_Vault/Needs_Action/EMAIL_test_$i.md << EOF
---
type: email
to: test$i@example.com
subject: Test Email $i
---
Send a test email.
EOF
done

# Process them all
./scripts/ralph-loop.sh --max-iterations 10 "Process all emails"
```

#### Example 3: Manual Stop

If you need to stop the loop manually:

```bash
# Method 1: Update status file
echo "status: completed" >> AI_Employee_Vault/Plans/loop_status.md

# Method 2: Delete status file
rm AI_Employee_Vault/Plans/loop_status.md

# Method 3: Press Ctrl+C (may leave tasks incomplete)
```

### Troubleshooting

#### Hook Not Running

**Symptom**: Claude stops immediately, hook doesn't trigger

**Solutions:**
1. Check hook exists: `ls -la .claude/hooks/stop_hook.py`
2. Make executable: `chmod +x .claude/hooks/stop_hook.py`
3. Check Claude Code version supports hooks
4. Verify hook syntax: `python3 .claude/hooks/stop_hook.py`

#### Infinite Loop

**Symptom**: Hook keeps running forever

**Causes:**
- Tasks are being created faster than processed
- Tasks are failing and staying in Needs_Action/
- Max iterations set too high

**Solutions:**
1. Check loop status: `cat AI_Employee_Vault/Plans/loop_status.md`
2. Lower max iterations: `export RALPH_MAX_ITERATIONS=5`
3. Manually stop: `rm AI_Employee_Vault/Plans/loop_status.md`
4. Check for failing tasks: `ls AI_Employee_Vault/Needs_Action/`

#### Hook Errors

**Symptom**: Hook crashes with Python error

**Solutions:**
1. Check Python version: `python3 --version` (need 3.6+)
2. View hook logs: Check stderr output
3. Test hook manually:
   ```bash
   cd /path/to/project
   python3 .claude/hooks/stop_hook.py
   ```

#### Files Not Being Processed

**Symptom**: Hook says "no work" but files exist in Needs_Action/

**Causes:**
- Files start with underscore (`_temp.md`)
- Files are in In_Progress/ folder
- Files are not `.md` extension

**Solutions:**
1. Check file names: `ls AI_Employee_Vault/Needs_Action/`
2. Rename files: Remove leading underscore
3. Check In_Progress: `ls AI_Employee_Vault/In_Progress/`

### Safety Features

1. **Max Iterations**: Prevents infinite loops (default: 10)
2. **Status Tracking**: Persistent state in loop_status.md
3. **File Filtering**: Ignores temp files (starting with `_`)
4. **Graceful Degradation**: On error, allows Claude to stop normally

### Advanced Usage

#### Custom Hook Logic

Edit `.claude/hooks/stop_hook.py` to customize behavior:

```python
# Change max iterations default
MAX_ITERATIONS = int(os.environ.get('RALPH_MAX_ITERATIONS', '20'))

# Add custom file filtering
def should_process_file(file_path):
    # Skip files older than 7 days
    age_days = (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days
    return age_days < 7

# Add custom completion logic
def on_completion():
    # Send notification, update dashboard, etc.
    pass
```

#### Integration with Orchestrator

The hook works alongside the orchestrator:

```bash
# Start orchestrator in background
python orchestrator.py &

# Start Ralph loop to process tasks
./scripts/ralph-loop.sh "Process all pending tasks"
```

The orchestrator creates tasks in Needs_Action/, and the Ralph loop processes them.

#### Scheduled Ralph Loops

Add to crontab for automated batch processing:

```bash
# Every hour: process any pending tasks (max 5 iterations)
0 * * * * cd /path/to/project && RALPH_MAX_ITERATIONS=5 ./scripts/ralph-loop.sh "Process pending tasks" >> logs/ralph_loop.log 2>&1
```

### Performance Considerations

**Iteration Time**: Each iteration takes 30-120 seconds depending on task complexity

**Resource Usage**:
- CPU: Moderate (Claude API calls)
- Memory: Low (~100MB)
- Network: Moderate (API requests)

**Recommended Limits**:
- Max iterations: 10-20 for interactive use
- Max iterations: 5-10 for scheduled/automated use
- Max iterations: 50+ for overnight batch processing

### Comparison with Other Approaches

| Approach | Pros | Cons |
|----------|------|------|
| **Ralph Hook** | Automatic, no manual intervention | Limited to max iterations |
| **Manual Loop** | Full control | Requires constant monitoring |
| **Orchestrator** | Continuous background processing | Separate process to manage |
| **Scheduled Tasks** | Set and forget | Fixed schedule, not on-demand |

### Best Practices

1. **Start Small**: Use low max iterations (5-10) initially
2. **Monitor Logs**: Check loop_status.md regularly
3. **Clean Up**: Archive completed tasks to keep Needs_Action/ clean
4. **Test First**: Try with a few test tasks before batch processing
5. **Set Limits**: Always use max iterations to prevent runaway loops

### Debugging

Enable verbose logging:

```bash
# Add debug output to hook
export RALPH_DEBUG=1
./scripts/ralph-loop.sh "Process tasks"
```

View hook execution:

```bash
# Hook logs to stderr
./scripts/ralph-loop.sh "Process tasks" 2>&1 | tee ralph_debug.log
```

Check what hook sees:

```bash
# Run hook manually
cd /path/to/project
python3 .claude/hooks/stop_hook.py
```

### FAQ

**Q: Can I disable the hook temporarily?**
A: Yes, rename it: `mv .claude/hooks/stop_hook.py .claude/hooks/stop_hook.py.disabled`

**Q: Does this work on Windows?**
A: Yes, but use PowerShell or WSL. Windows batch script coming soon.

**Q: Can I use this with other Claude Code features?**
A: Yes, it's compatible with all Claude Code features.

**Q: What happens if I press Ctrl+C?**
A: The loop stops immediately. Tasks in progress may be incomplete.

**Q: Can I change max iterations mid-loop?**
A: Yes, edit `AI_Employee_Vault/Plans/loop_status.md` and change `max_iterations`.

**Q: Does this consume API credits?**
A: Yes, each iteration uses Claude API credits. Monitor usage.

---

## Other Hooks (Future)

### start_hook.py (Not Implemented)

Would run when Claude Code starts. Potential uses:
- Load context from previous session
- Check for urgent tasks
- Display dashboard summary

### error_hook.py (Not Implemented)

Would run when Claude encounters an error. Potential uses:
- Log errors to file
- Send notifications
- Attempt recovery

---

**Last Updated**: 2026-02-16

**Version**: 1.0.0

**Author**: AI Employee System
