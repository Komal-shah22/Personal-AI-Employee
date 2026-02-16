# Oracle Cloud Free Tier Deployment Guide

## Overview

This guide walks you through deploying the AI Employee system on Oracle Cloud's Always Free tier, which provides:

- **1 VM**: ARM-based Ampere A1 (4 OCPUs, 24GB RAM) OR AMD (1 OCPU, 1GB RAM)
- **200GB Block Storage**
- **10TB Outbound Data Transfer/month**
- **Always Free**: No time limit, no credit card charges

## Prerequisites

- Oracle Cloud account (free tier)
- SSH client (built-in on Mac/Linux, PuTTY on Windows)
- Git installed locally
- Basic command line knowledge

## Part 1: Create Oracle Cloud VM

### Step 1: Sign Up for Oracle Cloud

1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in details and verify email
4. Complete identity verification

### Step 2: Create Compute Instance

1. Log in to Oracle Cloud Console
2. Click **☰ Menu** → **Compute** → **Instances**
3. Click **Create Instance**

### Step 3: Configure Instance

**Name**: `ai-employee-vm`

**Placement**:
- Availability Domain: (any available)

**Image and Shape**:
1. Click **Change Image**
2. Select **Canonical Ubuntu** → **22.04**
3. Click **Select Image**

4. Click **Change Shape**
5. Select **Ampere** (ARM-based)
6. Choose **VM.Standard.A1.Flex**
7. Set OCPUs: **2** (or up to 4 if available)
8. Set Memory: **12 GB** (or up to 24GB)
9. Click **Select Shape**

**Networking**:
- VCN: Create new VCN (default)
- Subnet: Create new public subnet (default)
- ✓ Assign a public IPv4 address

**Add SSH Keys**:
- Select **Generate a key pair for me**
- Click **Save Private Key** (save as `ai-employee-key.pem`)
- Click **Save Public Key** (optional backup)

**Boot Volume**:
- Size: **100 GB** (or up to 200GB)

### Step 4: Create Instance

1. Review configuration
2. Click **Create**
3. Wait 2-3 minutes for provisioning
4. Note the **Public IP Address** (e.g., 123.45.67.89)

## Part 2: Configure Firewall Rules

### Step 1: Security List Rules

1. On instance details page, click **Subnet** link
2. Click **Default Security List**
3. Click **Add Ingress Rules**

**Rule 1: SSH (Port 22)**
- Source CIDR: `0.0.0.0/0` (or your IP for better security)
- IP Protocol: TCP
- Destination Port: 22
- Description: SSH access

**Rule 2: HTTPS (Port 443)** - Optional, for dashboard
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port: 443
- Description: HTTPS access

4. Click **Add Ingress Rules**

### Step 2: Ubuntu Firewall (UFW)

We'll configure this after SSH connection.

## Part 3: Connect to VM via SSH

### Mac/Linux

```bash
# Set correct permissions
chmod 400 ai-employee-key.pem

# Connect to VM
ssh -i ai-employee-key.pem ubuntu@YOUR_PUBLIC_IP
```

### Windows (PowerShell)

```powershell
# Connect to VM
ssh -i ai-employee-key.pem ubuntu@YOUR_PUBLIC_IP
```

### Windows (PuTTY)

1. Convert `.pem` to `.ppk` using PuTTYgen
2. Open PuTTY
3. Host: `ubuntu@YOUR_PUBLIC_IP`
4. Connection → SSH → Auth → Browse to `.ppk` file
5. Click **Open**

### First Connection

You'll see a warning about host authenticity. Type `yes` to continue.

## Part 4: Initial VM Setup

### Step 1: Update System

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git vim htop
```

### Step 2: Configure Firewall

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (IMPORTANT: do this first!)
sudo ufw allow 22/tcp

# Allow HTTPS (optional, for dashboard)
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### Step 3: Set Timezone

```bash
# Set to UTC (recommended for servers)
sudo timedatectl set-timezone UTC

# Or set to your timezone
sudo timedatectl set-timezone America/New_York

# Verify
timedatectl
```

## Part 5: Install Docker

### Step 1: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Log out and back in for group changes
exit
# Then reconnect via SSH
```

### Step 2: Install Docker Compose

```bash
# Install Docker Compose
sudo apt install -y docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### Step 3: Start Docker

```bash
# Enable Docker to start on boot
sudo systemctl enable docker

# Start Docker
sudo systemctl start docker

# Verify Docker is running
docker ps
```

## Part 6: Clone Repository

### Step 1: Generate SSH Key for GitHub (Optional)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Display public key
cat ~/.ssh/id_ed25519.pub

# Copy and add to GitHub: Settings → SSH Keys → New SSH Key
```

### Step 2: Clone Repository

**Option A: HTTPS (Public Repo)**
```bash
cd ~
git clone https://github.com/yourusername/Personal_AI_Employee.git
cd Personal_AI_Employee
```

**Option B: SSH (Private Repo)**
```bash
cd ~
git clone git@github.com:yourusername/Personal_AI_Employee.git
cd Personal_AI_Employee
```

## Part 7: Configure Environment Variables

### Step 1: Create .env File

**CRITICAL**: Never commit `.env` to Git!

```bash
cd ~/Personal_AI_Employee
cp deploy/.env.cloud.template .env
```

### Step 2: Edit .env File

```bash
nano .env
```

**Minimum Required**:
```bash
# Claude API (REQUIRED)
ANTHROPIC_API_KEY=your_actual_api_key_here

# Set to false when ready for production
DRY_RUN=true
```

**Optional Services**:
```bash
# Gmail MCP
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# Social Media MCP
TWITTER_BEARER_TOKEN=your_token
FB_ACCESS_TOKEN=your_token
INSTAGRAM_ACCESS_TOKEN=your_token

# Odoo
ODOO_URL=http://your-odoo-server:8069
ODOO_DB=odoo_production
ODOO_API_USER=api@company.com
ODOO_API_PASSWORD=your_password
```

**Save and exit**: `Ctrl+X`, then `Y`, then `Enter`

### Step 3: Secure .env File

```bash
# Set restrictive permissions
chmod 600 .env

# Verify .env is in .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

## Part 8: Deploy Application

### Step 1: Build Docker Image

```bash
cd ~/Personal_AI_Employee

# Build image (this takes 5-10 minutes)
docker compose -f deploy/docker-compose.cloud.yml build
```

### Step 2: Start Application

```bash
# Start in detached mode
docker compose -f deploy/docker-compose.cloud.yml up -d

# Check status
docker compose -f deploy/docker-compose.cloud.yml ps

# View logs
docker compose -f deploy/docker-compose.cloud.yml logs -f
```

### Step 3: Verify Deployment

```bash
# Check container is running
docker ps

# Check logs for errors
docker compose -f deploy/docker-compose.cloud.yml logs --tail=50

# Check health status
docker inspect ai_employee_cloud | grep -A 5 Health
```

## Part 9: Monitoring & Maintenance

### View Logs

```bash
# All logs
docker compose -f deploy/docker-compose.cloud.yml logs -f

# Last 100 lines
docker compose -f deploy/docker-compose.cloud.yml logs --tail=100

# Specific service
docker compose -f deploy/docker-compose.cloud.yml logs -f ai-employee
```

### Restart Application

```bash
# Restart
docker compose -f deploy/docker-compose.cloud.yml restart

# Stop
docker compose -f deploy/docker-compose.cloud.yml down

# Start
docker compose -f deploy/docker-compose.cloud.yml up -d
```

### Update Application

```bash
# Pull latest code
cd ~/Personal_AI_Employee
git pull

# Rebuild and restart
docker compose -f deploy/docker-compose.cloud.yml down
docker compose -f deploy/docker-compose.cloud.yml build
docker compose -f deploy/docker-compose.cloud.yml up -d
```

### Check Resource Usage

```bash
# System resources
htop

# Docker stats
docker stats

# Disk usage
df -h

# Docker disk usage
docker system df
```

### Backup Vault Data

```bash
# Create backup directory
mkdir -p ~/backups

# Backup vault volume
docker run --rm \
  -v personal_ai_employee_vault-data:/data \
  -v ~/backups:/backup \
  ubuntu tar czf /backup/vault-backup-$(date +%Y%m%d).tar.gz /data

# List backups
ls -lh ~/backups/
```

### Restore Vault Data

```bash
# Restore from backup
docker run --rm \
  -v personal_ai_employee_vault-data:/data \
  -v ~/backups:/backup \
  ubuntu tar xzf /backup/vault-backup-20260216.tar.gz -C /
```

## Part 10: Security Best Practices

### 1. SSH Key Security

```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config

# Set these values:
PasswordAuthentication no
PermitRootLogin no

# Restart SSH
sudo systemctl restart sshd
```

### 2. Automatic Security Updates

```bash
# Install unattended-upgrades
sudo apt install -y unattended-upgrades

# Enable automatic updates
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Fail2Ban (Brute Force Protection)

```bash
# Install fail2ban
sudo apt install -y fail2ban

# Enable and start
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status sshd
```

### 4. Regular Backups

```bash
# Create backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups
DATE=$(date +%Y%m%d)

# Create backup
docker run --rm \
  -v personal_ai_employee_vault-data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu tar czf /backup/vault-backup-$DATE.tar.gz /data

# Keep only last 7 days
find $BACKUP_DIR -name "vault-backup-*.tar.gz" -mtime +7 -delete

echo "Backup completed: vault-backup-$DATE.tar.gz"
EOF

chmod +x ~/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup.sh >> ~/backup.log 2>&1") | crontab -
```

### 5. Monitor Logs

```bash
# Check for errors daily
grep -i error ~/Personal_AI_Employee/AI_Employee_Vault/Logs/*.log

# Check Docker logs
docker compose -f deploy/docker-compose.cloud.yml logs --since 24h | grep -i error
```

## Part 11: Troubleshooting

### Issue: Container won't start

```bash
# Check logs
docker compose -f deploy/docker-compose.cloud.yml logs

# Check .env file
cat .env | grep -v "^#" | grep -v "^$"

# Rebuild image
docker compose -f deploy/docker-compose.cloud.yml build --no-cache
docker compose -f deploy/docker-compose.cloud.yml up -d
```

### Issue: Out of memory

```bash
# Check memory usage
free -h

# Check Docker memory
docker stats

# Reduce container memory limit in docker-compose.cloud.yml
# Or upgrade to larger VM shape
```

### Issue: Out of disk space

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a

# Remove old logs
find ~/Personal_AI_Employee/AI_Employee_Vault/Logs -name "*.log" -mtime +30 -delete
```

### Issue: Can't connect via SSH

```bash
# Check VM is running in Oracle Console
# Check security list allows port 22
# Check UFW allows port 22: sudo ufw status
# Verify SSH key permissions: chmod 400 ai-employee-key.pem
```

### Issue: Git pull fails

```bash
# Check Git status
git status

# Discard local changes
git reset --hard origin/main

# Pull again
git pull
```

## Part 12: Advanced Configuration

### Set Up Swap (Recommended for 1GB RAM VMs)

```bash
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify
free -h
```

### Set Up Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/ai-employee

# Add this content:
/home/ubuntu/Personal_AI_Employee/AI_Employee_Vault/Logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}

# Test
sudo logrotate -f /etc/logrotate.d/ai-employee
```

### Set Up Monitoring (Optional)

```bash
# Install monitoring tools
sudo apt install -y prometheus-node-exporter

# Enable and start
sudo systemctl enable prometheus-node-exporter
sudo systemctl start prometheus-node-exporter
```

## Part 13: Cost Optimization

### Always Free Tier Limits

- **Compute**: 2 VMs (ARM) or 2 VMs (AMD)
- **Storage**: 200GB total
- **Outbound Transfer**: 10TB/month
- **No time limit**: Runs forever for free

### Tips to Stay Within Free Tier

1. **Use ARM shape**: More resources for free
2. **Monitor usage**: Check Oracle Console regularly
3. **Clean up**: Remove unused Docker images/volumes
4. **Optimize logs**: Rotate and compress logs
5. **Backup externally**: Use external storage for long-term backups

## Part 14: Security Checklist

Before going to production:

- [ ] SSH key-only authentication enabled
- [ ] Password authentication disabled
- [ ] UFW firewall configured
- [ ] Only necessary ports open (22, 443)
- [ ] .env file has restrictive permissions (600)
- [ ] .env file is in .gitignore
- [ ] Automatic security updates enabled
- [ ] Fail2ban installed and configured
- [ ] Regular backups scheduled
- [ ] DRY_RUN=false only after testing
- [ ] Strong passwords for all services
- [ ] WhatsApp sessions NOT on cloud
- [ ] Payment MCP NOT on cloud
- [ ] Monitoring and alerting set up

## Part 15: What NOT to Deploy to Cloud

### NEVER Deploy These to Cloud:

1. **WhatsApp Sessions**
   - Contains authentication data
   - Must stay on local machine only
   - Security risk if compromised

2. **Payment MCP**
   - Handles financial transactions
   - Must stay on local machine only
   - Requires human oversight

3. **Credentials in Git**
   - Never commit .env files
   - Never commit API keys
   - Use Oracle Vault or environment variables

4. **Personal Data**
   - Customer payment information
   - Personal identification data
   - Sensitive business data

### Safe to Deploy:

- ✓ Email processing (with proper credentials)
- ✓ Social media posting (with proper credentials)
- ✓ Invoice generation (non-payment)
- ✓ Task orchestration
- ✓ CEO briefing generation
- ✓ File processing
- ✓ Logging and monitoring

## Summary

You now have a fully deployed AI Employee system on Oracle Cloud Free Tier:

✓ Ubuntu 22.04 VM with Docker
✓ Secure SSH access
✓ Firewall configured
✓ Application running 24/7
✓ Automatic restarts
✓ Health monitoring
✓ Backup system
✓ Security hardened

**Access**: SSH to `ubuntu@YOUR_PUBLIC_IP`

**Manage**: `docker compose -f deploy/docker-compose.cloud.yml [command]`

**Logs**: `docker compose -f deploy/docker-compose.cloud.yml logs -f`

**Monitor**: `htop` and `docker stats`

---

**Last Updated**: 2026-02-16

**Oracle Cloud**: Always Free Tier

**OS**: Ubuntu 22.04 LTS

**Docker**: Latest stable

**Security**: Hardened for production
