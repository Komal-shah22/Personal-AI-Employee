"""
Cloud Deployment Setup for Personal AI Employee

Configuration and scripts for deploying to cloud platforms
"""

import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys
from typing import Dict, Any, List

class CloudDeploymentSetup:
    def __init__(self):
        self.deployment_configs = {
            "oracle_cloud": {
                "provider": "oracle",
                "region": "us-ashburn-1",
                "shape": "VM.Standard.E4.Flex",
                "memory_gb": 8,
                "ocpus": 2,
                "image": "Canonical Ubuntu 22.04",
                "services": ["compute", "network", "storage"]
            },
            "aws": {
                "provider": "aws",
                "region": "us-east-1",
                "instance_type": "t3.medium",
                "ami": "ami-0abcdef1234567890",
                "services": ["ec2", "vpc", "iam", "rds"]
            },
            "gcp": {
                "provider": "gcp",
                "region": "us-central1",
                "machine_type": "e2-medium",
                "image": "ubuntu-2204-lts",
                "services": ["compute", "vpc", "firewall"]
            }
        }

    def generate_oracle_terraform_config(self) -> str:
        """Generate Terraform configuration for Oracle Cloud deployment"""
        terraform_config = '''
# Oracle Cloud Infrastructure - Personal AI Employee
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 5.0.0"
    }
  }
}

# Provider configuration
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# Variables
variable "tenancy_ocid" {
  description = "OCID of the tenancy"
  type        = string
}

variable "user_ocid" {
  description = "OCID of the user"
  type        = string
}

variable "fingerprint" {
  description = "Fingerprint of the API key"
  type        = string
}

variable "private_key_path" {
  description = "Path to the private key file"
  type        = string
}

variable "region" {
  description = "Region where resources will be created"
  type        = string
  default     = "us-ashburn-1"
}

# VCN
resource "oci_core_virtual_network" "ai_employee_vcn" {
  compartment_id = var.compartment_id
  cidr_block     = "10.0.0.0/16"
  display_name   = "ai-employee-vcn"
  dns_label      = "aiemployee"
}

# Internet Gateway
resource "oci_core_internet_gateway" "ai_employee_ig" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_virtual_network.ai_employee_vcn.id
  display_name   = "ai-employee-ig"
}

# Route Table
resource "oci_core_route_table" "ai_employee_rt" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_virtual_network.ai_employee_vcn.id
  display_name   = "ai-employee-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.ai_employee_ig.id
  }
}

# Security List
resource "oci_core_security_list" "ai_employee_sl" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_virtual_network.ai_employee_vcn.id
  display_name   = "ai-employee-security-list"

  # Ingress rules
  ingress_security_rules {
    protocol    = "6"  # TCP
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"

    tcp_options {
      min = 22
      max = 22
    }
  }

  ingress_security_rules {
    protocol    = "6"  # TCP
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"

    tcp_options {
      min = 80
      max = 80
    }
  }

  ingress_security_rules {
    protocol    = "6"  # TCP
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"

    tcp_options {
      min = 443
      max = 443
    }
  }

  # Egress rules
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
    destination_type = "CIDR_BLOCK"
  }
}

# Subnet
resource "oci_core_subnet" "ai_employee_subnet" {
  compartment_id        = var.compartment_id
  vcn_id               = oci_core_virtual_network.ai_employee_vcn.id
  availability_domain  = data.oci_identity_availability_domains.ads.availability_domains[0].name
  cidr_block           = "10.0.1.0/24"
  display_name         = "ai-employee-subnet"
  dns_label            = "aisubnet"
  route_table_id       = oci_core_route_table.ai_employee_rt.id
  security_list_ids    = [oci_core_security_list.ai_employee_sl.id]
  dhcp_options_id      = oci_core_virtual_network.ai_employee_vcn.default_dhcp_options_id
}

# Instance
resource "oci_core_instance" "ai_employee_instance" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_id
  display_name        = "ai-employee-instance"
  shape               = "VM.Standard.E4.Flex"
  subnet_id           = oci_core_subnet.ai_employee_subnet.id

  create_vnic_details {
    assign_public_ip = true
    subnet_id        = oci_core_subnet.ai_employee_subnet.id
  }

  source_details {
    source_type = "image"
    source_id   = "ocid1.image.oc1..aaaaaaaayourimageid"
  }

  shape_config {
    ocpus         = 2
    memory_in_gbs = 8
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)
  }
}

# Outputs
output "instance_public_ip" {
  value = oci_core_instance.ai_employee_instance.public_ip
}

output "instance_private_ip" {
  value = oci_core_instance.ai_employee_instance.private_ip
}
'''
        return terraform_config

    def generate_docker_compose_config(self) -> str:
        """Generate Docker Compose configuration for containerized deployment"""
        docker_compose = '''
version: '3.8'

services:
  ai-employee-orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.orchestrator
    container_name: ai-employee-orchestrator
    volumes:
      - ./AI_Employee_Vault:/app/AI_Employee_Vault
      - ./config.json:/app/config.json
      - ./credentials.json:/app/credentials.json
    environment:
      - VAULT_PATH=/app/AI_Employee_Vault
      - PYTHONPATH=/app
    restart: unless-stopped
    networks:
      - ai_employee_net

  ai-employee-dashboard:
    build:
      context: ./ai-employee-dashboard
      dockerfile: Dockerfile
    container_name: ai-employee-dashboard
    ports:
      - "3000:3000"
    volumes:
      - ./AI_Employee_Vault:/app/public/AI_Employee_Vault
    environment:
      - VAULT_PATH=../AI_Employee_Vault
      - NEXT_PUBLIC_REFRESH_INTERVAL=5000
    restart: unless-stopped
    networks:
      - ai_employee_net

  ai-employee-watchers:
    build:
      context: .
      dockerfile: Dockerfile.watchers
    container_name: ai-employee-watchers
    volumes:
      - ./AI_Employee_Vault:/app/AI_Employee_Vault
      - ./config.json:/app/config.json
    environment:
      - VAULT_PATH=/app/AI_Employee_Vault
    restart: unless-stopped
    networks:
      - ai_employee_net

  ai-employee-mcp-servers:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    container_name: ai-employee-mcp-servers
    volumes:
      - ./AI_Employee_Vault:/app/AI_Employee_Vault
      - ./.claude/mcp-servers:/app/.claude/mcp-servers
    environment:
      - VAULT_PATH=/app/AI_Employee_Vault
    restart: unless-stopped
    networks:
      - ai_employee_net

networks:
  ai_employee_net:
    driver: bridge

volumes:
  vault_data:
  dashboard_data:
'''
        return docker_compose

    def generate_kubernetes_deployment(self) -> str:
        """Generate Kubernetes deployment configuration"""
        k8s_config = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-employee-orchestrator
  labels:
    app: ai-employee-orchestrator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-employee-orchestrator
  template:
    metadata:
      labels:
        app: ai-employee-orchestrator
    spec:
      containers:
      - name: orchestrator
        image: ai-employee/orchestrator:latest
        volumeMounts:
        - name: vault-storage
          mountPath: /app/AI_Employee_Vault
        - name: config-volume
          mountPath: /app/config.json
          subPath: config.json
        env:
        - name: VAULT_PATH
          value: /app/AI_Employee_Vault
        - name: PYTHONPATH
          value: /app
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: vault-storage
        persistentVolumeClaim:
          claimName: vault-pvc
      - name: config-volume
        configMap:
          name: ai-employee-config

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-employee-dashboard
  labels:
    app: ai-employee-dashboard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-employee-dashboard
  template:
    metadata:
      labels:
        app: ai-employee-dashboard
    spec:
      containers:
      - name: dashboard
        image: ai-employee/dashboard:latest
        ports:
        - containerPort: 3000
        env:
        - name: VAULT_PATH
          value: /app/AI_Employee_Vault
        - name: NEXT_PUBLIC_REFRESH_INTERVAL
          value: "5000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"

---
apiVersion: v1
kind: Service
metadata:
  name: ai-employee-dashboard-service
spec:
  selector:
    app: ai-employee-dashboard
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vault-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
'''
        return k8s_config

    def generate_health_monitoring_config(self) -> str:
        """Generate health monitoring configuration"""
        monitoring_config = '''
# Health monitoring script for AI Employee
import os
import time
import logging
from datetime import datetime
from pathlib import Path
import psutil
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HealthMonitor:
    def __init__(self, vault_path="../AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.alert_recipients = os.environ.get('ALERT_RECIPIENTS', '').split(',')

    def check_system_health(self):
        """Check overall system health"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'vault_accessible': self.check_vault_access(),
            'processes': self.check_processes(),
            'network': self.check_network_connectivity()
        }

        return health_status

    def check_vault_access(self):
        """Check if vault directories are accessible"""
        try:
            # Check if vault exists and is readable
            if not self.vault_path.exists():
                return False

            # Check if we can write to logs directory
            logs_dir = self.vault_path / 'Logs'
            logs_dir.mkdir(exist_ok=True)

            # Create a test file
            test_file = logs_dir / f'health_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tmp'
            test_file.touch()
            test_file.unlink()

            return True
        except Exception as e:
            logger.error(f"Vault access error: {e}")
            return False

    def check_processes(self):
        """Check if critical processes are running"""
        critical_processes = ['orchestrator', 'gmail_watcher', 'filesystem_watcher']
        running_processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else proc.info['name']
                if any(crit_proc in cmdline.lower() for crit_proc in critical_processes):
                    running_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return running_processes

    def check_network_connectivity(self):
        """Check network connectivity"""
        try:
            # Try to reach a reliable endpoint
            response = requests.get('https://httpbin.org/get', timeout=5)
            return response.status_code == 200
        except:
            return False

    def evaluate_health_status(self, health_data):
        """Evaluate overall health status"""
        issues = []

        if health_data['cpu_percent'] > 80:
            issues.append(f"High CPU usage: {health_data['cpu_percent']}%")

        if health_data['memory_percent'] > 85:
            issues.append(f"High memory usage: {health_data['memory_percent']}%")

        if health_data['disk_usage'] > 90:
            issues.append(f"High disk usage: {health_data['disk_usage']}%")

        if not health_data['vault_accessible']:
            issues.append("Vault not accessible")

        if not health_data['network']:
            issues.append("Network connectivity issues")

        if len(health_data['processes']) == 0:
            issues.append("No critical processes running")

        return {
            'status': 'healthy' if len(issues) == 0 else 'unhealthy',
            'issues': issues,
            'health_data': health_data
        }

    def send_alert(self, alert_message):
        """Send alert notification"""
        if not self.alert_recipients:
            logger.warning("No alert recipients configured")
            return

        try:
            # This is a simplified email alert - in production, use proper email configuration
            logger.warning(f"ALERT: {alert_message}")
            # In a real implementation, you would send actual email notifications
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")

    def run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        logger.info("Starting health monitoring cycle")

        health_data = self.check_system_health()
        evaluation = self.evaluate_health_status(health_data)

        logger.info(f"Health check completed. Status: {evaluation['status']}")

        if evaluation['status'] == 'unhealthy':
            alert_msg = f"Health issues detected: {', '.join(evaluation['issues'])}"
            self.send_alert(alert_msg)
            logger.error(alert_msg)

        return evaluation

def main():
    monitor = HealthMonitor()

    # Run continuous monitoring
    while True:
        try:
            monitor.run_monitoring_cycle()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Health monitoring stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()
'''
        return monitoring_config

    def generate_systemd_services(self) -> Dict[str, str]:
        """Generate systemd service files for Linux deployment"""
        services = {
            'ai-employee-orchestrator.service': '''[Unit]
Description=AI Employee Orchestrator
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=aiemployee
Group=aiemployee
WorkingDirectory=/opt/ai-employee
ExecStart=/opt/ai-employee/venv/bin/python orchestrator.py
Restart=always
RestartSec=10
Environment=VAULT_PATH=/opt/ai-employee/AI_Employee_Vault
Environment=PYTHONPATH=/opt/ai-employee

[Install]
WantedBy=multi-user.target
''',
            'ai-employee-gmail-watcher.service': '''[Unit]
Description=AI Employee Gmail Watcher
After=network.target ai-employee-orchestrator.service
Wants=network-online.target

[Service]
Type=simple
User=aiemployee
Group=aiemployee
WorkingDirectory=/opt/ai-employee
ExecStart=/opt/ai-employee/venv/bin/python watchers/gmail_watcher.py
Restart=always
RestartSec=10
Environment=VAULT_PATH=/opt/ai-employee/AI_Employee_Vault

[Install]
WantedBy=multi-user.target
''',
            'ai-employee-filesystem-watcher.service': '''[Unit]
Description=AI Employee Filesystem Watcher
After=network.target ai-employee-orchestrator.service
Wants=network-online.target

[Service]
Type=simple
User=aiemployee
Group=aiemployee
WorkingDirectory=/opt/ai-employee
ExecStart=/opt/ai-employee/venv/bin/python watchers/filesystem_watcher.py
Restart=always
RestartSec=10
Environment=VAULT_PATH=/opt/ai-employee/AI_Employee_Vault

[Install]
WantedBy=multi-user.target
''',
            'ai-employee-dashboard.service': '''[Unit]
Description=AI Employee Dashboard
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=aiemployee
Group=aiemployee
WorkingDirectory=/opt/ai-employee/ai-employee-dashboard
ExecStart=/opt/ai-employee/venv/bin/npm run start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
        }
        return services

    def generate_deployment_scripts(self) -> Dict[str, str]:
        """Generate deployment scripts for different environments"""
        scripts = {
            'deploy-oracle.sh': '''#!/bin/bash
# Oracle Cloud Deployment Script

set -e

echo "Starting Oracle Cloud deployment..."

# Install OCI CLI if not present
if ! command -v oci &> /dev/null; then
    echo "Installing OCI CLI..."
    bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
fi

# Validate configuration
if [ ! -f "terraform.tfvars" ]; then
    echo "terraform.tfvars not found. Please create it with your configuration."
    exit 1
fi

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -out=tfplan

# Apply deployment
terraform apply tfplan

echo "Oracle Cloud deployment completed!"
''',
            'deploy-docker.sh': '''#!/bin/bash
# Docker Deployment Script

set -e

echo "Starting Docker deployment..."

# Build and start services
docker-compose up -d --build

# Wait for services to start
sleep 30

# Check if services are running
docker-compose ps

echo "Docker deployment completed!"
''',
            'setup-production.sh': '''#!/bin/bash
# Production Setup Script

set -e

echo "Setting up production environment..."

# Create AI Employee user
if ! id "aiemployee" &>/dev/null; then
    sudo useradd -m -s /bin/bash aiemployee
fi

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip nodejs npm docker.io git

# Clone repository
sudo -u aiemployee git clone https://github.com/your-org/ai-employee.git /opt/ai-employee
cd /opt/ai-employee

# Create virtual environment
sudo -u aiemployee python3 -m venv venv
sudo -u aiemployee /opt/ai-employee/venv/bin/pip install -r requirements.txt

# Setup dashboard
cd ai-employee-dashboard
sudo -u aiemployee npm install
sudo -u aiemployee npm run build

# Setup systemd services
sudo cp deploy/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable ai-employee-orchestrator
sudo systemctl enable ai-employee-gmail-watcher
sudo systemctl enable ai-employee-filesystem-watcher
sudo systemctl enable ai-employee-dashboard

sudo systemctl start ai-employee-orchestrator
sudo systemctl start ai-employee-gmail-watcher
sudo systemctl start ai-employee-filesystem-watcher
sudo systemctl start ai-employee-dashboard

echo "Production setup completed!"
'''
        }
        return scripts

def main():
    """Generate all deployment configurations"""
    setup = CloudDeploymentSetup()

    # Create deployment directory
    deploy_dir = Path("deploy")
    deploy_dir.mkdir(exist_ok=True)

    # Generate Terraform config
    with open(deploy_dir / "oracle-terraform.tf", "w") as f:
        f.write(setup.generate_oracle_terraform_config())

    # Generate Docker Compose
    with open(deploy_dir / "docker-compose.yml", "w") as f:
        f.write(setup.generate_docker_compose_config())

    # Generate Kubernetes config
    with open(deploy_dir / "kubernetes-deployment.yaml", "w") as f:
        f.write(setup.generate_kubernetes_deployment())

    # Generate health monitoring script
    with open(deploy_dir / "health_monitor.py", "w") as f:
        f.write(setup.generate_health_monitoring_config())

    # Generate systemd services
    services = setup.generate_systemd_services()
    services_dir = deploy_dir / "systemd"
    services_dir.mkdir(exist_ok=True)
    for filename, content in services.items():
        with open(services_dir / filename, "w") as f:
            f.write(content)

    # Generate deployment scripts
    scripts = setup.generate_deployment_scripts()
    for filename, content in scripts.items():
        with open(deploy_dir / filename, "w") as f:
            f.write(content)

    # Make scripts executable
    for script_name in scripts.keys():
        script_path = deploy_dir / script_name
        script_path.chmod(0o755)

    print(f"Generated {len(scripts) + 5} deployment configuration files in deploy/ directory")
    print("Deployment configurations ready for cloud deployment!")

if __name__ == "__main__":
    main()