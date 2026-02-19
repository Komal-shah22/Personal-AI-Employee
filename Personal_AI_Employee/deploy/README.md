# Cloud Deployment Guide

## Overview

This directory contains everything needed to deploy your Personal AI Employee to Oracle Cloud Free Tier for 24/7 operation.

## Architecture

**Cloud VM (Oracle):**
- Email monitoring (Gmail API)
- Social media draft generation
- File processing
- Plan creation
- READ-ONLY operations + DRAFT creation

**Local Machine:**
- WhatsApp session (NEVER goes to cloud)
- Payment/banking credentials
- Final "send" actions
- Human approvals
- Dashboard access

## Files

- `Dockerfile` - Container image definition
- `docker-compose.cloud.yml` - Cloud deployment configuration
- `.env.cloud.example` - Template for cloud environment variables
- `oracle-cloud-setup.md` - Step-by-step Oracle Cloud setup
- `SECURITY.md` - Security checklist and best practices

## Quick Start

### 1. Prepare Local Environment

```bash
# Copy environment template
cp deploy/.env.cloud.example deploy/.env.cloud

# Edit with your API keys (Gmail, LinkedIn, social media)
# DO NOT add WhatsApp, banking, or payment credentials
nano deploy/.env.cloud
```

### 2. Test Build Locally (Optional)

```bash
# Build the Docker image
cd deploy
docker build -t ai-employee-cloud -f Dockerfile ..

# Test run (won't work fully without cloud setup)
docker-compose -f docker-compose.cloud.yml up
```

### 3. Deploy to Oracle Cloud

Follow the complete guide in `oracle-cloud-setup.md`:

1. Create Oracle Cloud Free Tier account
2. Provision VM instance (VM.Standard.E2.1.Micro)
3. Configure firewall rules
4. Install Docker on VM
5. Clone project to VM
6. Configure .env.cloud with API keys
7. Start services with docker-compose
8. Verify health checks

### 4. Monitor

```bash
# SSH into VM
ssh -i ~/.ssh/oracle_key ubuntu@<VM_IP>

# Check logs
cd ai-employee
docker-compose -f deploy/docker-compose.cloud.yml logs -f

# Check health
docker exec ai-employee-cloud node scripts/health-check.js

# Restart if needed
docker-compose -f deploy/docker-compose.cloud.yml restart
```

## Security

**CRITICAL:** Review `SECURITY.md` before deploying.

Key points:
- ✅ Cloud has Gmail, LinkedIn, social media APIs
- ❌ Cloud NEVER has WhatsApp session
- ❌ Cloud NEVER has banking/payment credentials
- ✅ Cloud creates drafts only
- ✅ Local machine performs all "send" actions

## Troubleshooting

### Container won't start
```bash
docker logs ai-employee-cloud
# Check for missing environment variables
```

### Out of memory
```bash
free -h
docker stats
# Oracle Free Tier has 1GB RAM - may need to optimize
```

### Health check failing
```bash
docker exec ai-employee-cloud node scripts/health-check.js
# Check vault is accessible and logs are being written
```

## Next Steps

After deployment:
- Set up vault sync between cloud and local (Agent P2)
- Configure monitoring and alerts (Agent P3)
- Test end-to-end workflow
- Set up automated backups

## Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Review SECURITY.md checklist
3. Verify .env.cloud has correct API keys
4. Check Oracle Cloud firewall rules
