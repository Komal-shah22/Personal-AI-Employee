# Vault Sync Setup Guide

## Prerequisites
- Git installed on both local and cloud
- GitHub account (or GitLab/Bitbucket)
- SSH keys configured for GitHub

## Step 1: Create GitHub Repository
```bash
# On GitHub.com
1. Create new private repository: "ai-employee-vault"
2. Don't initialize with README (we'll push existing)
3. Copy the SSH URL: git@github.com:yourusername/ai-employee-vault.git
```

## Step 2: Initialize Local Vault
```bash
# On your laptop
cd ~/AI_Employee_Vault

# Run init script
bash ../sync/vault-init.sh

# Add GitHub remote
git remote add origin git@github.com:yourusername/ai-employee-vault.git

# Push initial state
git push -u origin main
```

## Step 3: Clone Vault on Cloud VM
```bash
# SSH to Oracle VM
ssh ubuntu@<VM_IP>

# Clone vault
cd /app
git clone git@github.com:yourusername/ai-employee-vault.git vault

# Verify
cd vault
ls -la
```

## Step 4: Configure SSH Keys for Cloud VM
```bash
# On cloud VM, generate SSH key
ssh-keygen -t ed25519 -C "ai-employee-cloud"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings > SSH Keys > Add
```

## Step 5: Test Sync

### From Cloud:
```bash
# Create test file
echo "test from cloud" > /app/vault/Drafts/test.md

# Run cloud push
python3 sync/cloud-push.py

# Should commit and push to GitHub
```

### From Local:
```bash
# Run local pull
python3 sync/local-pull.py

# Should pull the test file
cat ~/AI_Employee_Vault/Drafts/test.md
```

## Step 6: Set Up Auto-Sync

### Cloud (in Docker):
Add to ecosystem.config.js:
```javascript
{
  name: 'vault-sync',
  script: 'sync/cloud-push.py',
  interpreter: 'python3',
  autorestart: true
}
```

### Local (cron):
```bash
# Edit crontab
crontab -e

# Add (every 2 minutes):
*/2 * * * * cd ~/AI_Employee_Vault && python3 sync/local-pull.py >> ~/vault-sync.log 2>&1
```

## Troubleshooting

### Sync conflicts
```bash
# If git pull fails with conflicts
git stash
git pull --rebase
git stash pop
# Manually resolve conflicts
```

### SSH authentication failed
```bash
# Test SSH to GitHub
ssh -T git@github.com

# If fails, check SSH key is added to GitHub
```

### Large files causing issues
```bash
# Git LFS for large files (optional)
git lfs install
git lfs track "*.pdf"
git add .gitattributes
```
