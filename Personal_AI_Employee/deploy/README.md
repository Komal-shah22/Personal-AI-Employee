# 🚀 Oracle Cloud Deployment - Personal AI Employee

This directory contains all the necessary files and scripts to deploy your Personal AI Employee to Oracle Cloud for 24/7 operation.

## 📁 Directory Structure

```
deploy/
├── oracle-terraform.tf         # Main Terraform configuration
├── variables.tf                # Terraform variables
├── outputs.tf                  # Terraform outputs
├── docker-compose.yml          # Docker configuration
├── kubernetes-deployment.yaml  # Kubernetes configuration
├── health_monitor.py           # Health monitoring script
├── systemd/                    # Systemd service files
│   ├── ai-employee-orchestrator.service
│   ├── ai-employee-gmail-watcher.service
│   ├── ai-employee-filesystem-watcher.service
│   └── ai-employee-dashboard.service
├── deploy-oracle.sh            # Oracle Cloud deployment script
├── deploy-docker.sh            # Docker deployment script
├── setup-production.sh         # Production setup script
├── setup-oracle-cloud.sh       # Oracle Cloud setup helper script
├── oracle-cloud-deployment.md  # Detailed deployment guide
├── README.md                   # This file
└── terraform.tfvars.example    # Example Terraform variables
```

## 🚀 Quick Start - Oracle Cloud Deployment

### **Step 1: Prerequisites**

1. **Install Oracle Cloud CLI:**
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

2. **Configure Oracle Cloud CLI:**
```bash
oci setup config
```

3. **Install Terraform:**
```bash
# Download from https://www.terraform.io/downloads
# Or on Ubuntu:
sudo apt update && sudo apt install terraform
```

### **Step 2: Setup Oracle Cloud Deployment**

1. **Navigate to deploy directory:**
```bash
cd deploy/
```

2. **Run the setup script:**
```bash
./setup-oracle-cloud.sh
```

3. **The script will:**
   - Check prerequisites
   - Validate your OCI configuration
   - Create `terraform.tfvars` file
   - Show you the deployment plan
   - Execute the deployment

### **Step 3: Configure Terraform Variables**

1. **Copy the example variables file:**
```bash
cp terraform.tfvars.example terraform.tfvars
```

2. **Edit `terraform.tfvars` with your values:**
   - `compartment_id`: Your Oracle Cloud compartment OCID
   - `ssh_public_key_path`: Path to your SSH public key
   - `region`: Your preferred Oracle Cloud region

### **Step 4: Deploy to Oracle Cloud**

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

## 🏗️ Infrastructure Components

### **Virtual Cloud Network (VCN)**
- Isolated network environment
- Public and private subnets
- Internet gateway
- Route tables
- Security lists (firewall rules)

### **Compute Instance**
- Shape: `VM.Standard.E4.Flex`
- 2 OCPUs, 8GB Memory
- 50GB Boot Volume
- Ubuntu 22.04 LTS
- SSH access configured

### **Services Deployed**
- AI Employee Orchestrator
- Gmail Watcher
- Filesystem Watcher
- Premium Dashboard (Next.js)
- MCP Servers (Social, Browser, Payment, ERP)

## 🔧 Production Setup

After the infrastructure is deployed:

1. **SSH to your instance:**
```bash
ssh ubuntu@<INSTANCE_PUBLIC_IP>
```

2. **Upload your Personal AI Employee project:**
```bash
scp -r /path/to/your/project ubuntu@<INSTANCE_IP>:~/ai-employee
```

3. **Run production setup:**
```bash
cd ~/ai-employee
chmod +x deploy/setup-production.sh
sudo ./deploy/setup-production.sh
```

4. **Verify all services are running:**
```bash
sudo systemctl status ai-employee-*
```

## 🛡️ Security Features

- **Isolated VCN**: Network isolation
- **Security Lists**: Firewall rules limiting access
- **SSH Keys**: Secure authentication
- **Private Subnets**: Internal services
- **Monitoring**: Health checks and alerts

## 📊 Monitoring and Health Checks

The deployment includes health monitoring:

```bash
# Check service status
sudo systemctl status ai-employee-*

# View service logs
journalctl -u ai-employee-orchestrator -f

# Run health monitoring script
python3 deploy/health_monitor.py
```

## 🔄 Scaling Options

### **Vertical Scaling:**
- Update `ocpus` and `memory_in_gbs` in variables
- Apply changes with Terraform

### **Horizontal Scaling:**
- Use the Kubernetes configuration
- Deploy multiple instances behind a load balancer

## 🆘 Troubleshooting

### **Common Issues:**

1. **Instance not accessible:**
   - Check security lists allow SSH access
   - Verify SSH key is correct
   - Confirm VCN routing

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

## 📞 Support Resources

- [Oracle Cloud Documentation](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [Terraform Oracle Cloud Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)
- [Oracle Cloud Support](https://cloud.oracle.com/support)

## 🎉 Next Steps

1. **Monitor the system** for the first 24 hours
2. **Verify all components** are functioning
3. **Set up automated backups**
4. **Configure alerts** for critical issues
5. **Document the production environment**

---

**Your Personal AI Employee is now ready for 24/7 operation on Oracle Cloud! 🚀**

Enjoy your Digital FTE operating 168 hours per week!