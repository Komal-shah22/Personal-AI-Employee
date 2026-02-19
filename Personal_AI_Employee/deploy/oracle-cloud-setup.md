# Oracle Cloud Free Tier Setup

## Step 1: Create Free Oracle Cloud Account
1. Go to: https://www.oracle.com/cloud/free/
2. Sign up (requires credit card but won't charge)
3. Verify email

## Step 2: Create VM Instance
1. Go to: Compute > Instances > Create Instance
2. Name: ai-employee-production
3. Image: Ubuntu 22.04 (Canonical)
4. Shape: VM.Standard.E2.1.Micro (Always Free)
5. Add SSH key (generate on your local machine)
6. Networking: Use default VCN
7. Click "Create"

## Step 3: Configure Firewall
1. Go to: Networking > Virtual Cloud Networks
2. Click your VCN > Security Lists > Default
3. Add Ingress Rules:
   - Port 22 (SSH)
   - Port 8080 (Health check - optional)
4. Save

## Step 4: Connect via SSH
```bash
ssh -i ~/.ssh/oracle_key ubuntu@<VM_PUBLIC_IP>
```

## Step 5: Install Docker on VM
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version
```

## Step 6: Clone Project to VM
```bash
# Install git
sudo apt install git -y

# Clone your project
git clone https://github.com/yourusername/ai-employee.git
cd ai-employee

# Create .env.cloud file
cp deploy/.env.cloud.example deploy/.env.cloud
nano deploy/.env.cloud
# Add your API keys (Gmail, LinkedIn, etc.)
# DO NOT add WhatsApp, banking, payment credentials
```

## Step 7: Start Services
```bash
cd deploy
docker-compose -f docker-compose.cloud.yml up -d

# Check logs
docker-compose -f docker-compose.cloud.yml logs -f

# Check health
docker ps
```

## Step 8: Set Up Auto-restart on Boot
```bash
# Enable Docker to start on boot
sudo systemctl enable docker

# Docker Compose will auto-restart containers (restart: unless-stopped)
```

## Step 9: Monitor
```bash
# View logs
docker-compose -f docker-compose.cloud.yml logs -f ai-employee-cloud

# Check health
docker exec ai-employee-cloud node scripts/health-check.js

# Restart if needed
docker-compose -f docker-compose.cloud.yml restart
```

## Troubleshooting

### Container keeps restarting
```bash
docker logs ai-employee-cloud
# Check for missing env variables or errors
```

### Out of memory
```bash
# Check memory usage
free -h
docker stats

# Oracle Free Tier has 1GB RAM - may need to limit processes
```

### Can't connect to VM
```bash
# Check security list has port 22 open
# Verify SSH key is correct
# Check VM is running in Oracle Console
```
