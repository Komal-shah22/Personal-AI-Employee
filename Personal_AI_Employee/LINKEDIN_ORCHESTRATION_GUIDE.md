# LinkedIn Post Orchestration System

## How the System Works

The AI Employee system processes LinkedIn posts through a multi-stage workflow that includes both queue-based processing and approval workflows:

### 1. Queue Creation (Dashboard → Needs_Action)
- When you submit a post via the dashboard, it creates a file in `AI_Employee_Vault/Needs_Action/`
- The file is named `LINKEDIN_DASHBOARD_[timestamp].md` with frontmatter metadata
- Example: `LINKEDIN_DASHBOARD_2026-02-26T17-59-22.md`

### 2. Processing Queue (Needs_Action → Pending_Approval)
- The script `process_linkedin_queue.py` converts queue files to approval requests
- It moves from `Needs_Action` to `Pending_Approval` folder as `LINKEDIN_APPROVAL_[timestamp].md`
- The orchestrator processes these files automatically

### 3. Approval Workflow (Pending_Approval → Approved → Done)
- Human review is required for LinkedIn posts
- The script `scripts/linkedin_approval_processor.py` processes approved posts
- Posts are moved to `Approved` folder to trigger posting
- After processing, posts are moved to `Done` folder

## Answers to Your Questions

### 1. Is the orchestrator already running automatically?

**Partially.** The orchestrator (`orchestrator.py`) has the capability to:
- Scan `Needs_Action` folder for LinkedIn posts
- Process them through the approval workflow
- However, it may not be running continuously by default

### 2. Do I need to run any command to start it?

**Yes.** You can start the orchestrator with:
```bash
python orchestrator.py
```

Or for a single run:
```bash
python orchestrator.py --once
```

To run in production mode (not dry run):
```bash
python orchestrator.py --no-dry-run
```

### 3. How do I check if a queued post was published?

**Multiple ways:**

#### Check the Done folder:
- Successful posts are moved to `AI_Employee_Vault/Done/`
- Files are timestamped so you can see when they were processed

#### Check the logs:
- `AI_Employee_Vault/Logs/orchestrator.log` - Orchestrator activity
- `AI_Employee_Vault/Logs/linkedin.log` - Specific LinkedIn posting logs

#### Check the dashboard:
- `AI_Employee_Vault/Dashboard.md` - Updates with recent activity

#### Check the approval system:
- Original post moves from `Needs_Action` → `Pending_Approval` → `Done`

### 4. Should I run it manually or is there a background service?

#### For Continuous Operation:
```bash
python orchestrator.py --no-dry-run
```
This runs continuously, checking for new tasks every 5 minutes.

#### For Manual Processing:
```bash
python orchestrator.py --once --no-dry-run
```
This processes any queued items once and then exits.

#### Or run the specific processing scripts:
```bash
# Process LinkedIn queue items
python process_linkedin_queue.py

# Process approved posts
python scripts/linkedin_approval_processor.py
```

## Complete Workflow for Your Posts

1. **Dashboard submission** → Creates file in `Needs_Action`
2. **Orchestrator** → Finds and processes the file
3. **Approval process** → Creates approval request in `Pending_Approval`
4. **Human approval** → Move file to `Approved` folder
5. **Posting execution** → Posts to LinkedIn via MCP server
6. **Completion** → File moved to `Done`, logs updated

## For Your Specific Setup (Without r_liteprofile Scope)

Your system is configured to:
1. Try direct posting with your hardcoded URN: `urn:li:member:komal-shah-0b162a296`
2. When that fails (due to LinkedIn's numeric ID requirement), it falls back to queue-based processing
3. The queue system will still work perfectly - your posts will be processed through the orchestrator workflow
4. You'll need to approve posts when they reach the `Pending_Approval` stage

## Recommended Command to Start Everything

```bash
# Start the orchestrator to handle all tasks
python orchestrator.py --no-dry-run
```

The orchestrator will automatically:
- Process any existing queue files
- Monitor for new files
- Handle the complete LinkedIn posting workflow
- Update logs and dashboard