# Security Checklist for Cloud Deployment

## ✅ BEFORE DEPLOYING

### Secrets Management
- [ ] All sensitive credentials in .env files
- [ ] .env files in .gitignore
- [ ] No credentials in Dockerfile
- [ ] No credentials in docker-compose.yml (use env_file)
- [ ] Separate .env.cloud and .env.local files

### Cloud vs Local Separation
- [ ] WhatsApp session NEVER synced to cloud
- [ ] Banking credentials NEVER synced to cloud
- [ ] Payment tokens NEVER synced to cloud
- [ ] Cloud .env does NOT contain sensitive credentials
- [ ] Cloud has DRY_RUN=false ONLY for safe operations

### Code Security
- [ ] No API keys hardcoded in scripts
- [ ] All file operations use environment variables for paths
- [ ] Input validation on all user inputs
- [ ] No eval() or exec() with user data
- [ ] Dependencies up to date (npm audit, pip check)

### Network Security
- [ ] Firewall allows only necessary ports (22, 8080)
- [ ] SSH key-based authentication (no password login)
- [ ] Oracle Cloud security lists properly configured
- [ ] No public endpoints for sensitive operations

## ✅ AFTER DEPLOYING

### Access Control
- [ ] SSH access restricted to your IP (if possible)
- [ ] Docker containers not accessible from internet
- [ ] Logs do not contain sensitive data
- [ ] Health check endpoint doesn't leak information

### Monitoring
- [ ] Set up alerts for container restarts
- [ ] Monitor disk space usage
- [ ] Check logs for unauthorized access attempts
- [ ] Verify vault sync is working

### Backup
- [ ] Regular backups of vault data
- [ ] Backup stored securely (encrypted)
- [ ] Tested restore procedure

## 🚨 NEVER DO THIS

- ❌ Store WhatsApp session in cloud
- ❌ Store banking credentials in cloud
- ❌ Commit .env files to git
- ❌ Use same .env for cloud and local
- ❌ Give cloud permission to make payments
- ❌ Allow cloud to send WhatsApp messages
- ❌ Expose Docker ports to public internet
- ❌ Run as root user in container
- ❌ Disable health checks
- ❌ Ignore failed health checks

## 📋 INCIDENT RESPONSE

If credentials are compromised:
1. Immediately rotate all API tokens
2. Stop cloud container: `docker stop ai-employee-cloud`
3. Review logs for unauthorized access
4. Update .env with new credentials
5. Restart with new credentials
6. Monitor for 24 hours

If VM is compromised:
1. Snapshot VM (evidence)
2. Destroy VM instance
3. Create new VM
4. Deploy from scratch with new SSH key
5. Rotate all credentials
