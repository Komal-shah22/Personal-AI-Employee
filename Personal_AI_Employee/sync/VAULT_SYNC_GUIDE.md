# Cloud-Local Vault Synchronization System

## Overview

Git-based synchronization system that enables the AI Employee to work across cloud (Oracle VM) and local machine while maintaining security and preventing conflicts.

## Architecture

### Work Zones

**Cloud Owns (Read/Write)**:
- `Needs_Action/` - Incoming tasks (email triage, social post drafts)
- `Plans/` - Task planning and strategies
- `Drafts/` - Draft content before approval

**Local Owns (Read/Write)**:
- `Approved/` - Human-approved actions ready for execution
- `Done/` - Completed tasks
- `Pending_Approval/` - Tasks awaiting human approval
- `Dashboard.md` - Main dashboard (local writes only)

**Shared (Both)**:
- `In_Progress/` - Currently processing tasks (claim-by-move)
- `Logs/` - Activity logs
- `Briefings/` - CEO briefings

### Sync Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ CLOUD (Oracle VM)                                           │
├─────────────────────────────────────────────────────────────┤
│ 1. Receives email → Creates file in Needs_Action/          │
│ 2. Auto-commits and pushes to Git                          │
│ 3. Processes files it claims from Needs_Action/            │
│ 4. Creates drafts in Drafts/                               │
│ 5. Writes dashboard updates to Updates/[timestamp].md      │
└─────────────────────────────────────────────────────────────┘
                            ↓ Git Push
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ GIT REPOSITORY (Bare Repo on VM or GitHub)                 │
├─────────────────────────────────────────────────────────────┤
│ - Central source of truth                                   │
│ - Conflict resolution via Git                               │
│ - History and audit trail                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓ Git Pull (every 2 min)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ LOCAL (Your Machine)                                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Pulls latest changes every 2 minutes                     │
│ 2. Merges Updates/*.md into Dashboard.md                    │
│ 3. Processes files it claims from Needs_Action/            │
│ 4. Handles WhatsApp, payments (never synced)               │
│ 5. Human approves tasks → moves to Approved/               │
│ 6. Executes approved tasks → moves to Done/                │
│ 7. Commits and pushes changes                              │
└─────────────────────────────────────────────────────────────┘
```

## Claim-by-Move Rule

To prevent conflicts when both agents try to process the same file:

1. **File appears in `Needs_Action/`**
2. **Agent A** moves it to `In_Progress/agent_a/filename.md`
3. **Agent A** commits and pushes immediately
4. **Agent B** pulls and sees file is already claimed
5. **Agent B** skips that file and processes others

**First to move wins** - Git commit timestamp determines ownership.

## Security Model

### What Gets Synced

✓ **Safe to sync**:
- Task files (markdown)
- Plans and strategies
- Draft content
- Logs (if no sensitive data)
- Briefings
- Dashboard updates

### What NEVER Gets Synced

✗ **Never synced** (in .gitignore):
- `.env` files (all variants)
- `sessions/` (WhatsApp authentication)
- `credentials.json` (API credentials)
- `*.key`, `*.pem` (SSH keys, certificates)
- `token.json`, `token.pickle` (OAuth tokens)
- Payment data
- Processed IDs (may contain sensitive data)

### Pre-Commit Hook

Automatically scans for secrets before allowing commits:

```bash
# Blocks commits containing:
- API keys (ANTHROPIC_API_KEY, sk-ant-, etc.)
- Passwords (password=...)
- Private keys (-----BEGIN PRIVATE KEY-----)
- Forbidden files (.env, credentials.json)
- WhatsApp sessions (sessions/)
- Payment data (payments/, transactions/)
```

If secrets are detected, commit is **blocked** with error message.

## Setup

### Prerequisites

- Git installed
- Python 3.6+
- SSH access to Oracle VM (if using VM as remote)

### Step 1: Run Setup Script

**Mac/Linux**:
```bash
chmod +x sync/setup_git_sync.sh
./sync/setup_git_sync.sh
```

**Windows**:
```cmd
sync\setup_git_sync.bat
```

**What it does**:
1. Initializes Git repository in `AI_Employee_Vault/`
2. Creates `.gitignore` with security rules
3. Installs pre-commit hook for secret scanning
4. Creates directory structure
5. Makes initial commit
6. Configures remote repository
7. Sets up auto-pull (cron/Task Scheduler)
8. Creates test file to verify sync

### Step 2: Configure Remote

**Option A: Oracle Cloud VM (Recommended)**

On your Oracle VM:
```bash
# Create bare repository
mkdir -p ~/vault.git
cd ~/vault.git
git init --bare
```

On local machine:
```bash
cd AI_Employee_Vault
git remote add origin ubuntu@YOUR_VM_IP:~/vault.git
git push -u origin main
```

**Option B: GitHub Private Repository**

1. Create private repository on GitHub
2. Add remote:
   ```bash
   cd AI_Employee_Vault
   git remote add origin git@github.com:yourusername/vault.git
   git push -u origin main
   ```

**Option C: GitLab Private Repository**

Similar to GitHub, use GitLab URL.

### Step 3: Start Sync Agents

**On Cloud (Oracle VM)**:
```bash
cd ~/Personal_AI_Employee
python sync/vault_sync.py --mode cloud
```

**On Local Machine**:
```bash
cd Personal_AI_Employee
python sync/vault_sync.py --mode local
```

**Run as background service**:
```bash
# Cloud
nohup python sync/vault_sync.py --mode cloud --interval 120 > sync.log 2>&1 &

# Local
nohup python sync/vault_sync.py --mode local --interval 120 > sync.log 2>&1 &
```

## Usage

### Cloud Agent Workflow

1. **Receives task** (e.g., email arrives)
2. **Creates file** in `Needs_Action/EMAIL_[timestamp].md`
3. **Auto-commits**: `git add . && git commit -m "New email task"`
4. **Auto-pushes**: `git push origin main`
5. **Claims file**: Moves to `In_Progress/cloud_agent/`
6. **Processes**: Creates draft in `Drafts/`
7. **Updates dashboard**: Writes to `Updates/[timestamp].md`
8. **Commits and pushes** all changes

### Local Agent Workflow

1. **Pulls changes** every 2 minutes
2. **Merges dashboard updates**: Combines `Updates/*.md` into `Dashboard.md`
3. **Claims unclaimed files** from `Needs_Action/`
4. **Processes sensitive tasks**: WhatsApp, payments (never synced)
5. **Human approval**: Reviews tasks in `Pending_Approval/`
6. **Executes approved**: Moves to `Approved/` then `Done/`
7. **Commits and pushes** changes

### Manual Operations

**Check sync status**:
```bash
cd AI_Employee_Vault
git status
git log --oneline -10
```

**Manual pull**:
```bash
cd AI_Employee_Vault
git pull --rebase origin main
```

**Manual push**:
```bash
cd AI_Employee_Vault
git add .
git commit -m "Manual update"
git push origin main
```

**View sync logs**:
```bash
tail -f AI_Employee_Vault/Logs/sync.log
```

## Conflict Resolution

### Scenario 1: Both Agents Modify Same File

**Rare** - shouldn't happen due to work zones.

**Resolution**:
1. Git will detect conflict on pull
2. Sync script stashes local changes
3. Pulls remote changes
4. Manual merge required

**Prevention**: Respect work zones.

### Scenario 2: Both Agents Claim Same File

**Prevented** by claim-by-move rule.

**How it works**:
1. Agent A moves file to `In_Progress/agent_a/`
2. Agent A commits and pushes
3. Agent B pulls and sees file is gone from `Needs_Action/`
4. Agent B skips that file

### Scenario 3: Dashboard Conflicts

**Prevented** by Updates/ pattern.

**How it works**:
1. Cloud writes to `Updates/[timestamp].md`
2. Local merges `Updates/*.md` into `Dashboard.md`
3. No direct conflict on `Dashboard.md`

## Monitoring

### Check Sync Health

```bash
# View recent commits
cd AI_Employee_Vault
git log --oneline --graph --all -20

# Check for uncommitted changes
git status

# View sync logs
tail -f Logs/sync.log

# Check last sync time
cat .vault_sync_state.json
```

### Sync Metrics

```bash
# Count commits by agent
git log --all --format='%an' | sort | uniq -c

# View sync frequency
git log --all --format='%ai' | head -20

# Check file distribution
find . -type f -name "*.md" | wc -l
```

## Troubleshooting

### Issue: Sync not working

**Check**:
```bash
# Is Git repo initialized?
cd AI_Employee_Vault
ls -la .git

# Is remote configured?
git remote -v

# Can we reach remote?
git fetch origin

# Are there uncommitted changes?
git status
```

**Fix**:
```bash
# Reinitialize if needed
./sync/setup_git_sync.sh

# Reconfigure remote
git remote set-url origin YOUR_REMOTE_URL

# Commit pending changes
git add .
git commit -m "Pending changes"
git push origin main
```

### Issue: Pre-commit hook blocking valid commit

**Check**:
```bash
# View what's being committed
git diff --cached

# Check for false positives
git diff --cached | grep -i "api_key"
```

**Fix**:
```bash
# If false positive, temporarily disable hook
git commit --no-verify -m "Your message"

# Or edit hook to exclude pattern
nano .git/hooks/pre-commit
```

### Issue: Merge conflicts

**Resolution**:
```bash
# View conflicts
git status

# Edit conflicted files
nano path/to/conflicted/file.md

# Mark as resolved
git add path/to/conflicted/file.md

# Complete merge
git rebase --continue

# Or abort and try again
git rebase --abort
```

### Issue: Secrets accidentally committed

**CRITICAL - Fix immediately**:
```bash
# Remove from history (DANGEROUS)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (overwrites remote)
git push origin --force --all

# Rotate compromised secrets immediately
# Change API keys, passwords, etc.
```

**Prevention**: Pre-commit hook should catch this.

## Best Practices

### 1. Respect Work Zones

- Cloud: Only write to `Needs_Action/`, `Plans/`, `Drafts/`, `Updates/`
- Local: Only write to `Approved/`, `Done/`, `Pending_Approval/`, `Dashboard.md`
- Both: Can write to `In_Progress/[agent_name]/`, `Logs/`, `Briefings/`

### 2. Commit Frequently

- Cloud: After each file creation
- Local: After each approval/completion
- Small, atomic commits are better

### 3. Pull Before Push

- Always pull latest changes before pushing
- Use `git pull --rebase` to avoid merge commits

### 4. Never Force Push

- Except in emergency (secrets leaked)
- Force push loses history and can cause data loss

### 5. Monitor Sync Logs

- Check `Logs/sync.log` daily
- Look for errors or conflicts
- Verify sync frequency

### 6. Test Changes

- Use test files to verify sync
- Check both machines after changes
- Verify claim-by-move works

### 7. Backup Regularly

- Git history is a backup, but not enough
- Regular backups of entire vault
- Store backups off-site

## Performance

### Sync Frequency

- **Cloud**: Immediate (after each file creation)
- **Local**: Every 2 minutes (configurable)

### Network Usage

- **Per sync**: ~10-100 KB (depends on changes)
- **Daily**: ~1-10 MB (typical)
- **Monthly**: ~30-300 MB

### Disk Usage

- **Git repo**: ~50-200 MB (with history)
- **Vault data**: ~100-500 MB (depends on usage)
- **Total**: ~150-700 MB

## Security Checklist

Before going to production:

- [ ] Pre-commit hook installed and tested
- [ ] .gitignore includes all sensitive patterns
- [ ] No .env files in repository
- [ ] No sessions/ directory in repository
- [ ] No credentials.json in repository
- [ ] No API keys in any committed files
- [ ] Remote repository is private (if GitHub/GitLab)
- [ ] SSH keys are secure (if using VM remote)
- [ ] Sync logs don't contain secrets
- [ ] Test secret detection with fake key

## Advanced Configuration

### Custom Sync Interval

```bash
# Sync every 5 minutes instead of 2
python sync/vault_sync.py --mode local --interval 300
```

### Custom Agent Name

```bash
# Use custom agent name
export AGENT_NAME=my_custom_agent
python sync/vault_sync.py --mode local
```

### Sync Specific Zones Only

Edit `vault_sync.py`:
```python
# Only sync certain directories
CLOUD_ZONES = ['Needs_Action']  # Cloud only syncs this
LOCAL_ZONES = ['Done']  # Local only syncs this
```

### Webhook Notifications

Add to `vault_sync.py`:
```python
def notify_sync_complete():
    # Send webhook notification
    requests.post('https://your-webhook-url', json={
        'event': 'sync_complete',
        'agent': self.agent_name,
        'timestamp': datetime.now().isoformat()
    })
```

## Integration with AI Employee

### Orchestrator Integration

```python
# In orchestrator.py
from sync.vault_sync import VaultSync

# After processing file
sync = VaultSync(mode='cloud')
sync.git_commit(f"Processed: {filename}")
sync.git_push()
```

### Watcher Integration

```python
# In watchers/gmail_watcher.py
# After creating action item
subprocess.run(['git', 'add', action_file])
subprocess.run(['git', 'commit', '-m', f'New email: {subject}'])
subprocess.run(['git', 'push', 'origin', 'main'])
```

## Comparison with Alternatives

| Method | Pros | Cons |
|--------|------|------|
| **Git Sync** | Version control, conflict resolution, audit trail | Requires Git knowledge |
| **Rsync** | Fast, simple | No conflict resolution, no history |
| **Dropbox/Drive** | Easy setup | No conflict resolution, privacy concerns |
| **Database** | Real-time, structured | Complex setup, single point of failure |

## Resources

- **Git Documentation**: https://git-scm.com/doc
- **Git Workflows**: https://www.atlassian.com/git/tutorials/comparing-workflows
- **Pre-commit Hooks**: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks

---

**Version**: 1.0.0

**Last Updated**: 2026-02-16

**Status**: Production Ready

**Security**: Hardened with pre-commit hooks and .gitignore
