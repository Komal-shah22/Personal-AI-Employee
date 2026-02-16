#!/bin/bash

# Git-Based Vault Synchronization Setup Script
# Sets up Git repository in AI_Employee_Vault for cloud-local sync

set -e

echo "============================================================"
echo "VAULT SYNC SETUP - GIT-BASED SYNCHRONIZATION"
echo "============================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
VAULT_DIR="$PROJECT_DIR/AI_Employee_Vault"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if vault exists
if [ ! -d "$VAULT_DIR" ]; then
    echo -e "${RED}ERROR: AI_Employee_Vault directory not found${NC}"
    exit 1
fi

echo "Vault directory: $VAULT_DIR"
echo ""

# Step 1: Initialize Git repository
echo "=== Step 1: Initialize Git Repository ==="
echo ""

cd "$VAULT_DIR"

if [ -d ".git" ]; then
    echo -e "${YELLOW}Git repository already exists${NC}"
    read -p "Reinitialize? This will preserve history (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping git init"
    fi
else
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi

echo ""

# Step 2: Create .gitignore
echo "=== Step 2: Create .gitignore ==="
echo ""

cat > .gitignore << 'EOF'
# Secrets and Credentials (NEVER COMMIT)
.env
.env.local
.env.cloud
*.key
*.pem
*.p12
*.ovpn
credentials.json
token.json
token.pickle
client_secret*.json

# WhatsApp Sessions (LOCAL ONLY)
sessions/
.whatsapp_processed.json

# Payment Data (LOCAL ONLY)
payments/
transactions/

# Processed IDs (can contain sensitive data)
.processed_ids.json

# Temporary Files
*.tmp
*.temp
_*
.DS_Store
Thumbs.db

# Logs (optional - uncomment if logs contain sensitive data)
# Logs/*.log

# Python
__pycache__/
*.pyc

# Node
node_modules/

# Sync State
.vault_sync_state.json
EOF

echo -e "${GREEN}✓ .gitignore created${NC}"
echo ""

# Step 3: Create pre-commit hook
echo "=== Step 3: Create Pre-Commit Hook (Security) ==="
echo ""

mkdir -p .git/hooks

cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook to prevent committing secrets
# Scans staged files for potential secrets

RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Running security scan..."

# Patterns to detect
PATTERNS=(
    "ANTHROPIC_API_KEY"
    "OPENAI_API_KEY"
    "sk-ant-"
    "sk-proj-"
    "password.*=.*['\"].*['\"]"
    "api_key.*=.*['\"].*['\"]"
    "secret.*=.*['\"].*['\"]"
    "token.*=.*['\"].*['\"]"
    "-----BEGIN.*PRIVATE KEY-----"
    "-----BEGIN RSA PRIVATE KEY-----"
)

# Files that should never be committed
FORBIDDEN_FILES=(
    ".env"
    ".env.local"
    ".env.cloud"
    "credentials.json"
    "token.json"
    "token.pickle"
)

# Check for forbidden files
for file in "${FORBIDDEN_FILES[@]}"; do
    if git diff --cached --name-only | grep -q "^$file$"; then
        echo -e "${RED}ERROR: Attempting to commit forbidden file: $file${NC}"
        echo "This file contains secrets and should never be committed."
        exit 1
    fi
done

# Check for secret patterns in staged files
for pattern in "${PATTERNS[@]}"; do
    if git diff --cached | grep -iE "$pattern" > /dev/null; then
        echo -e "${RED}ERROR: Potential secret detected in staged changes${NC}"
        echo "Pattern matched: $pattern"
        echo ""
        echo "Matched lines:"
        git diff --cached | grep -iE "$pattern" --color=always
        echo ""
        echo "Please remove secrets before committing."
        exit 1
    fi
done

# Check for WhatsApp session files
if git diff --cached --name-only | grep -q "sessions/"; then
    echo -e "${RED}ERROR: Attempting to commit WhatsApp session files${NC}"
    echo "WhatsApp sessions must stay LOCAL only."
    exit 1
fi

# Check for payment-related files
if git diff --cached --name-only | grep -qE "(payments/|transactions/)"; then
    echo -e "${RED}ERROR: Attempting to commit payment data${NC}"
    echo "Payment data must stay LOCAL only."
    exit 1
fi

echo -e "${GREEN}✓ Security scan passed${NC}"
exit 0
EOF

chmod +x .git/hooks/pre-commit
echo -e "${GREEN}✓ Pre-commit hook installed${NC}"
echo ""

# Step 4: Create initial directory structure
echo "=== Step 4: Create Directory Structure ==="
echo ""

mkdir -p Needs_Action
mkdir -p In_Progress/cloud_agent
mkdir -p In_Progress/local_agent
mkdir -p Plans
mkdir -p Drafts
mkdir -p Approved
mkdir -p Done
mkdir -p Pending_Approval
mkdir -p Logs
mkdir -p Briefings
mkdir -p Updates

echo -e "${GREEN}✓ Directory structure created${NC}"
echo ""

# Step 5: Create README
echo "=== Step 5: Create Vault README ==="
echo ""

cat > README.md << 'EOF'
# AI Employee Vault

This directory is synchronized between cloud (Oracle) and local machine using Git.

## Work Zones

### Cloud Owns (Read/Write)
- `Needs_Action/` - Incoming tasks (email triage, social drafts)
- `Plans/` - Task plans and strategies
- `Drafts/` - Draft content (emails, posts)

### Local Owns (Read/Write)
- `Approved/` - Human-approved actions
- `Done/` - Completed tasks
- `Pending_Approval/` - Awaiting human approval
- `Dashboard.md` - Main dashboard (local writes only)

### Shared (Both)
- `In_Progress/` - Currently processing (claim-by-move)
- `Logs/` - Activity logs
- `Briefings/` - CEO briefings

## Sync Rules

1. **Claim-by-Move**: First agent to move file from `Needs_Action/` to `In_Progress/[agent_name]/` owns it
2. **Dashboard Updates**: Cloud writes to `Updates/[timestamp].md`, local merges into `Dashboard.md`
3. **Security**: Secrets, WhatsApp sessions, and payment data NEVER synced

## Security

Files that are NEVER committed:
- `.env` files
- `sessions/` (WhatsApp)
- `credentials.json`
- `*.key`, `*.pem` files
- Payment data

Pre-commit hook scans for secrets before allowing commits.

## Sync Frequency

- **Cloud**: Auto-commit and push after file creation
- **Local**: Pull every 2 minutes

## Usage

See `sync/vault_sync.py` for sync script.
EOF

echo -e "${GREEN}✓ README created${NC}"
echo ""

# Step 6: Initial commit
echo "=== Step 6: Initial Commit ==="
echo ""

git add .
git commit -m "Initial vault setup with security controls" || echo "No changes to commit"

echo -e "${GREEN}✓ Initial commit created${NC}"
echo ""

# Step 7: Set up remote
echo "=== Step 7: Set Up Remote Repository ==="
echo ""

echo "You need to set up a Git remote for synchronization."
echo ""
echo "Options:"
echo "  1. Oracle Cloud VM (recommended for this setup)"
echo "  2. GitHub private repository"
echo "  3. GitLab private repository"
echo "  4. Self-hosted Git server"
echo ""

read -p "Do you want to configure a remote now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "=== Remote Configuration ==="
    echo ""
    echo "For Oracle Cloud VM:"
    echo "  1. SSH to your VM"
    echo "  2. Create bare repo: mkdir -p ~/vault.git && cd ~/vault.git && git init --bare"
    echo "  3. Use this remote URL: ubuntu@YOUR_VM_IP:~/vault.git"
    echo ""
    echo "For GitHub/GitLab:"
    echo "  1. Create a PRIVATE repository"
    echo "  2. Use the provided Git URL"
    echo ""

    read -p "Enter remote URL: " REMOTE_URL

    if [ -n "$REMOTE_URL" ]; then
        git remote add origin "$REMOTE_URL" || git remote set-url origin "$REMOTE_URL"
        echo -e "${GREEN}✓ Remote configured: $REMOTE_URL${NC}"

        read -p "Push to remote now? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push -u origin main || git push -u origin master
            echo -e "${GREEN}✓ Pushed to remote${NC}"
        fi
    fi
fi

echo ""

# Step 8: Set up local auto-pull (cron)
echo "=== Step 8: Set Up Auto-Pull (Local Only) ==="
echo ""

read -p "Set up automatic pull every 2 minutes on this machine? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    CRON_CMD="*/2 * * * * cd $VAULT_DIR && git pull --rebase origin main >> $VAULT_DIR/Logs/sync.log 2>&1"

    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "vault.*git pull"; then
        echo -e "${YELLOW}Cron job already exists${NC}"
    else
        (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
        echo -e "${GREEN}✓ Cron job added (pull every 2 minutes)${NC}"
    fi

    echo ""
    echo "To view cron jobs: crontab -l"
    echo "To remove: crontab -e (then delete the line)"
fi

echo ""

# Step 9: Test sync
echo "=== Step 9: Test Sync ==="
echo ""

read -p "Create a test file to verify sync? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    TEST_FILE="Needs_Action/TEST_sync_$(date +%Y%m%d_%H%M%S).md"

    cat > "$TEST_FILE" << EOF
---
type: test
priority: low
created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
---

# Sync Test File

This is a test file to verify vault synchronization is working.

Created: $(date)

If you can see this file on both cloud and local machines, sync is working!
EOF

    git add "$TEST_FILE"
    git commit -m "Test sync file"

    if git remote get-url origin >/dev/null 2>&1; then
        git push origin main || git push origin master
        echo -e "${GREEN}✓ Test file created and pushed${NC}"
        echo ""
        echo "Check the other machine to verify sync is working."
    else
        echo -e "${YELLOW}Test file created but not pushed (no remote configured)${NC}"
    fi
fi

echo ""

# Summary
echo "============================================================"
echo "SETUP COMPLETE"
echo "============================================================"
echo ""
echo -e "${GREEN}✓ Git repository initialized${NC}"
echo -e "${GREEN}✓ .gitignore created (secrets excluded)${NC}"
echo -e "${GREEN}✓ Pre-commit hook installed (security scan)${NC}"
echo -e "${GREEN}✓ Directory structure created${NC}"
echo -e "${GREEN}✓ Initial commit created${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. On CLOUD (Oracle VM):"
echo "   cd ~/Personal_AI_Employee"
echo "   python sync/vault_sync.py --mode cloud"
echo ""
echo "2. On LOCAL machine:"
echo "   python sync/vault_sync.py --mode local"
echo ""
echo "3. Or run continuously:"
echo "   python sync/vault_sync.py --mode local --interval 120"
echo ""
echo "4. Monitor sync:"
echo "   tail -f AI_Employee_Vault/Logs/sync.log"
echo ""
echo "Security reminders:"
echo "  - Pre-commit hook will block secrets"
echo "  - WhatsApp sessions stay LOCAL only"
echo "  - Payment data stays LOCAL only"
echo "  - Always review changes before pushing"
echo ""
