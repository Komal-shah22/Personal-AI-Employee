# Vault Sync System - Quick Start

## ✓ Sync Scripts Created

All sync components are ready in `sync/`:
- `cloud-push.py` - Cloud agent pushes drafts/plans to GitHub
- `local-pull.py` - Local agent pulls updates and processes approvals
- `claim-handler.py` - Prevents race conditions with claim-by-move
- `conflict-resolver.py` - Auto-resolves merge conflicts
- `vault-init.sh` - Initializes vault as git repo
- `.gitignore` - Protects sensitive files from syncing

## Current Status

Your vault is already a Git repository. Next steps:

### 1. Add Security .gitignore

```bash
# Copy the secure .gitignore to vault
cp sync/.gitignore AI_Employee_Vault/.gitignore

# Commit it
cd AI_Employee_Vault
git add .gitignore
git commit -m "Add secure .gitignore for vault sync"
```

### 2. Set Up GitHub Remote (if not done)

```bash
# Create private repo on GitHub: ai-employee-vault
# Then add remote:
cd AI_Employee_Vault
git remote add origin git@github.com:YOUR_USERNAME/ai-employee-vault.git

# Or if using HTTPS:
git remote add origin https://github.com/YOUR_USERNAME/ai-employee-vault.git

# Push initial state
git push -u origin main
```

### 3. Test Local Sync (Manual)

```bash
# Set vault path
export VAULT_PATH="E:/hackathon-0/Personal_AI_Employee/AI_Employee_Vault"

# Test pull (dry run - won't loop)
cd sync
python3 local-pull.py
```

### 4. Test Claim-by-Move Logic

```bash
# Create test file in Needs_Action
echo "Test task from dashboard" > AI_Employee_Vault/Needs_Action/TEST_TASK.md

# Claim it as LOCAL agent
export AGENT_ID=LOCAL
export VAULT_PATH="E:/hackathon-0/Personal_AI_Employee/AI_Employee_Vault"
python3 -c "from sync.claim_handler import claim_file; print(claim_file('TEST_TASK.md'))"

# Should move to In_Progress/LOCAL_TEST_TASK.md
ls AI_Employee_Vault/In_Progress/
```

## For Cloud VM Setup

Once local is working, on your Oracle VM:

```bash
# Clone vault
cd /app
git clone git@github.com:YOUR_USERNAME/ai-employee-vault.git vault

# Set up cloud sync service
export VAULT_PATH=/app/vault
export AGENT_ID=CLOUD

# Add to PM2 ecosystem
pm2 start sync/cloud-push.py --name vault-sync --interpreter python3
```

## Security Notes

The .gitignore prevents syncing:
- ✗ .env files
- ✗ SSH keys (.pem, .key)
- ✗ WhatsApp sessions
- ✗ Banking/payment logs
- ✗ Credentials files

Only task files, plans, and drafts sync between agents.

## Next: Test It!

1. Copy .gitignore to vault
2. Push to GitHub
3. Run local-pull.py once to test
4. Try claim-by-move with a test file

Report back when ready for cloud setup!
