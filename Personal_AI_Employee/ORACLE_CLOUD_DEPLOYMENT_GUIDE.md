# 🚀 Oracle Cloud Deployment Guide - Personal AI Employee

## **Deploying Your Personal AI Employee for 24/7 Operation**

This guide provides step-by-step instructions to deploy your Personal AI Employee to Oracle Cloud Infrastructure (OCI) for continuous 24/7 operation.

## 📋 **Prerequisites**

### **1. Oracle Cloud Account Setup**
- Sign up for Oracle Cloud account (Free tier available)
- Obtain Oracle Cloud account credentials
- Enable required services (Compute, Networking, Storage)

### **2. Local Environment**
- Oracle Cloud CLI installed
- Terraform installed
- SSH keys generated

### **3. Project Preparation**
- Your Personal AI Employee project ready
- Credentials and configuration files prepared

## 🏗️ **Infrastructure Architecture**

```
Oracle Cloud Infrastructure
├── Virtual Cloud Network (VCN)
│   ├── Public Subnet (for load balancer)
│   ├── Private Subnet (for compute instances)
│   └── Security Lists (firewall rules)
├── Compute Instance (VM.Standard.E4.Flex)
│   ├── Ubuntu 22.04 LTS
│   ├── 2 OCPUs, 8GB Memory
│   └── 50GB Boot Volume
├── Load Balancer (optional)
├── Object Storage (for backups)
└── Monitoring (Observability)
```

## 📁 **Deployment Files Located in `deploy/` Directory**

### **1. Terraform Configuration Files**
- `oracle-terraform.tf` - Main infrastructure
- `variables.tf` - Configuration variables
- `outputs.tf` - Deployment outputs

### **2. Deployment Scripts**
- `deploy-oracle.sh` - Automated deployment
- `setup-production.sh` - Production setup
- `health-monitor.py` - Health monitoring

### **3. Containerization (Optional)**
- `docker-compose.yml` - Multi-container setup
- `Dockerfile` - Application container

## 🚀 **Step-by-Step Deployment Process**

### **Step 1: Install Oracle Cloud CLI**

1. **Install Oracle Cloud CLI:**
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

2. **Configure Oracle Cloud CLI:**
```bash
oci setup config
```
Follow prompts to enter your tenancy OCID, user OCID, region, etc.

3. **Install Terraform:**
```bash
# Download Terraform from https://www.terraform.io/downloads
# Or on Ubuntu:
sudo apt update && sudo apt install terraform
```

### **Step 2: Prepare Deployment Files**

The deployment files are located in the `deploy/` directory:
- Terraform configuration files
- Docker Compose configuration
- Kubernetes deployment files
- Systemd service files
- Health monitoring scripts

### **Step 3: Customize Configuration**

1. **Navigate to deploy directory:**
```bash
cd deploy/
```

2. **Create `terraform.tfvars` file:**
```bash
cp terraform.tfvars.example terraform.tfvars
```

3. **Edit `terraform.tfvars` with your specific values:**
```hcl
compartment_id = "ocid1.compartment.oc1..your_compartment_id_here"
region = "us-ashburn-1"
availability_domain = "1"
ssh_public_key_path = "~/.ssh/id_rsa.pub"
instance_shape = "VM.Standard.E4.Flex"
ocpus = 2
memory_in_gbs = 8
boot_volume_size_in_gbs = 50
display_name_prefix = "ai-employee"
```

4. **Update configuration with your specific values:**
   - `compartment_id`: Your Oracle Cloud compartment OCID
   - `ssh_public_key_path`: Path to your SSH public key
   - `region`: Your preferred Oracle Cloud region

### **Step 4: Deploy Infrastructure**

1. **Initialize Terraform:**
```bash
terraform init
```

2. **Validate configuration:**
```bash
terraform validate
```

3. **Create execution plan:**
```bash
terraform plan -var-file="terraform.tfvars"
```

4. **Apply the configuration:**
```bash
terraform apply -var-file="terraform.tfvars"
```
Confirm with "yes" when prompted.

### **Step 5: Configure Production Environment**

1. **Access the deployed instance:**
```bash
# Get instance IP from Terraform output
terraform output instance_public_ip
ssh ubuntu@<instance_public_ip>
```

2. **Upload your Personal AI Employee project to the instance:**
```bash
# From your local machine, upload the project
scp -r /path/to/personal-ai-employee ubuntu@<instance_ip>:~/ai-employee
```

3. **SSH into the instance and run setup:**
```bash
ssh ubuntu@<instance_ip>
cd ~/ai-employee
chmod +x deploy/setup-production.sh
sudo ./deploy/setup-production.sh
```

### **Step 6: Configure 24/7 Operation**

1. **Start all services:**
```bash
sudo systemctl start ai-employee-orchestrator
sudo systemctl start ai-employee-gmail-watcher
sudo systemctl start ai-employee-filesystem-watcher
sudo systemctl start ai-employee-dashboard
```

2. **Enable services to start on boot:**
```bash
sudo systemctl enable ai-employee-orchestrator
sudo systemctl enable ai-employee-gmail-watcher
sudo systemctl enable ai-employee-filesystem-watcher
sudo systemctl enable ai-employee-dashboard
```

### **Step 7: Set Up Monitoring**

1. **Start health monitoring:**
```bash
cd ~/ai-employee/deploy
python3 health_monitor.py &
```

2. **Configure alerts (optional):**
- Set up Oracle Cloud Monitoring
- Configure email/SMS notifications
- Set up automated recovery procedures

## 🔧 **Configuration Files**

### **Terraform Variables (`terraform.tfvars`):**
```hcl
compartment_id = "ocid1.compartment.oc1..your_compartment_id_here"
region = "us-ashburn-1"
availability_domain = "1"
ssh_public_key_path = "~/.ssh/id_rsa.pub"
instance_shape = "VM.Standard.E4.Flex"
ocpus = 2
memory_in_gbs = 8
boot_volume_size_in_gbs = 50
display_name_prefix = "ai-employee"
```

### **Environment Variables (`env.prod`):**
```env
VAULT_PATH=/opt/ai-employee/AI_Employee_Vault
NODE_ENV=production
NEXT_PUBLIC_REFRESH_INTERVAL=5000
TZ=UTC
```

## 🛡️ **Security Configuration**

### **Firewall Rules:**
- SSH (port 22) - Limited to your IP
- HTTP (port 80) - For dashboard (optional)
- HTTPS (port 443) - For dashboard (optional)
- Dashboard (port 3000) - For Next.js dashboard

### **Security Best Practices:**
- Use IAM policies for access control
- Enable audit logging
- Use private subnets for sensitive components
- Implement SSL/TLS for web interfaces

## 📊 **Monitoring and Maintenance**

### **Health Checks:**
- CPU and memory usage
- Disk space monitoring
- Process uptime tracking
- Network connectivity checks

### **Backup Strategy:**
- Daily vault backups to Object Storage
- Database snapshots
- Configuration backups

### **Maintenance Tasks:**
- Weekly security updates
- Monthly log rotation
- Quarterly performance tuning

## 🚀 **Post-Deployment Verification**

### **Check Services:**
```bash
# Verify all services are running
sudo systemctl status ai-employee-orchestrator
sudo systemctl status ai-employee-gmail-watcher
sudo systemctl status ai-employee-filesystem-watcher
sudo systemctl status ai-employee-dashboard

# Check application logs
journalctl -u ai-employee-orchestrator -f
```

### **Access Dashboard:**
- Open browser to: `http://<instance_ip>:3000`
- Verify real-time data updates
- Check all dashboard components

## 🔄 **Scaling Options**

### **Vertical Scaling:**
- Increase OCPU and memory
- Upgrade to faster shapes
- Increase boot volume size

### **Horizontal Scaling:**
- Load balancing across multiple instances
- Microservices architecture
- Database scaling

## 🆘 **Troubleshooting**

### **Common Issues:**
1. **Instance not accessible:**
   - Check security lists
   - Verify SSH key
   - Confirm VCN configuration

2. **Services not starting:**
   - Check logs: `journalctl -u <service_name>`
   - Verify dependencies
   - Check configuration files

3. **Dashboard not loading:**
   - Verify Node.js installation
   - Check firewall rules
   - Confirm service status

### **Recovery Procedures:**
- Automated health checks and restarts
- Backup restoration procedures
- Rollback strategies

## 📞 **Support and Maintenance**

### **Ongoing Maintenance:**
- Monitor resource utilization
- Update security patches
- Review logs regularly
- Optimize performance

### **Contact Information:**
- Oracle Cloud support: https://cloud.oracle.com/support
- Community forums
- Documentation resources

---

## 🎉 **Congratulations!**

Your Personal AI Employee is now deployed on Oracle Cloud and ready for 24/7 operation. The system is configured for continuous monitoring, automated recovery, and scalable operation.

**Next Steps:**
1. Monitor the system for the first 24 hours
2. Verify all components are functioning
3. Set up automated backups
4. Configure alerts for critical issues
5. Document the production environment

Your Digital FTE is now operational 24/7!

---

## 🚀 **Real Deployment Instructions**

To deploy to Oracle Cloud:

1. **Install required tools:**
```bash
# Install Oracle Cloud CLI
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"

# Install Terraform
# Download from https://www.terraform.io/downloads
```

2. **Configure Oracle Cloud:**
```bash
oci setup config
```

3. **Navigate to deployment directory:**
```bash
cd deploy/
```

4. **Create and configure terraform.tfvars:**
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

5. **Deploy:**
```bash
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

6. **Set up production environment on the deployed instance**

Your Personal AI Employee will be operational 24/7 on Oracle Cloud!