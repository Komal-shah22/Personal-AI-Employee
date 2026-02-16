#!/bin/bash

# Oracle Cloud Setup Script for Personal AI Employee
# This script guides you through the Oracle Cloud deployment process

set -e  # Exit on any error

echo "================================================="
echo "  Personal AI Employee - Oracle Cloud Setup"
echo "================================================="
echo

# Function to check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."

    # Check if oci cli is installed
    if ! command -v oci &> /dev/null; then
        echo "❌ Oracle Cloud CLI (oci) is not installed"
        echo "Please install it first:"
        echo "bash -c \"\$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)\""
        exit 1
    fi

    # Check if terraform is installed
    if ! command -v terraform &> /dev/null; then
        echo "❌ Terraform is not installed"
        echo "Please install it from: https://www.terraform.io/downloads"
        exit 1
    fi

    # Check if git is installed
    if ! command -v git &> /dev/null; then
        echo "❌ Git is not installed"
        echo "Please install git first"
        exit 1
    fi

    echo "✅ All prerequisites are installed"
    echo
}

# Function to check OCI configuration
check_oci_config() {
    echo "Checking Oracle Cloud configuration..."

    if [ ! -f ~/.oci/config ]; then
        echo "❌ OCI configuration not found"
        echo "Please run: oci setup config"
        echo "And follow the prompts to configure your Oracle Cloud account"
        exit 1
    fi

    echo "✅ OCI configuration found"
    echo
}

# Function to validate terraform
validate_terraform() {
    echo "Validating Terraform configuration..."

    if [ ! -f "oracle-terraform.tf" ]; then
        echo "❌ oracle-terraform.tf not found in current directory"
        echo "Please run this script from the deploy/ directory"
        exit 1
    fi

    terraform init
    terraform validate

    echo "✅ Terraform configuration is valid"
    echo
}

# Function to create terraform.tfvars if it doesn't exist
create_tfvars() {
    if [ ! -f "terraform.tfvars" ]; then
        echo "Creating terraform.tfvars file..."
        cat > terraform.tfvars << 'EOF'
# Oracle Cloud Infrastructure Variables for Personal AI Employee
# Update these values with your specific configuration

compartment_id = "your_compartment_ocid_here"
region = "us-ashburn-1"
availability_domain = "1"
ssh_public_key_path = "~/.ssh/id_rsa.pub"
instance_shape = "VM.Standard.E4.Flex"
ocpus = 2
memory_in_gbs = 8
boot_volume_size_in_gbs = 50
display_name_prefix = "ai-employee"
EOF
        echo "✅ terraform.tfvars created - please update with your values"
        echo
        echo "⚠️  IMPORTANT: Please edit terraform.tfvars with your actual values:"
        echo "   - compartment_id: Your Oracle Cloud compartment OCID"
        echo "   - ssh_public_key_path: Path to your SSH public key"
        echo "   - region: Your preferred Oracle Cloud region"
        echo
        exit 0
    else
        echo "✅ terraform.tfvars file exists"
        echo
    fi
}

# Function to show deployment plan
show_plan() {
    echo "Showing deployment plan..."
    echo

    terraform plan -var-file="terraform.tfvars"

    echo
    echo "Above is the plan for your Oracle Cloud deployment."
    echo "This will create/modify Oracle Cloud resources."
    echo
}

# Function to execute deployment
execute_deployment() {
    echo "Starting Oracle Cloud deployment..."
    echo

    read -p "Do you want to proceed with the deployment? (yes/no): " -n 3 -r
    echo
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Executing deployment..."
        terraform apply -var-file="terraform.tfvars" -auto-approve

        echo
        echo "✅ Oracle Cloud deployment completed successfully!"
        echo
        terraform output
    else
        echo
        echo "Deployment cancelled."
        exit 0
    fi
}

# Function to show post-deployment steps
post_deployment_steps() {
    echo
    echo "================================================="
    echo "  POST-DEPLOYMENT STEPS"
    echo "================================================="
    echo
    echo "After your infrastructure is deployed, please follow these steps:"
    echo
    echo "1. Get the instance details:"
    echo "   terraform output instance_public_ip"
    echo
    echo "2. SSH to your instance:"
    echo "   ssh ubuntu@<PUBLIC_IP_ADDRESS>"
    echo
    echo "3. Upload your Personal AI Employee project:"
    echo "   scp -r /path/to/your/project ubuntu@<PUBLIC_IP>:~/ai-employee"
    echo
    echo "4. On the instance, run the production setup:"
    echo "   cd ~/ai-employee"
    echo "   chmod +x deploy/setup-production.sh"
    echo "   sudo ./deploy/setup-production.sh"
    echo
    echo "5. Verify all services are running:"
    echo "   sudo systemctl status ai-employee-*"
    echo
    echo "6. Access your dashboard at:"
    echo "   http://<PUBLIC_IP>:3000"
    echo
    echo "For more details, see: deploy/oracle-cloud-deployment.md"
}

# Main execution
main() {
    echo "This script will help you deploy your Personal AI Employee to Oracle Cloud."
    echo "Please make sure you have:"
    echo "1. An Oracle Cloud account with proper permissions"
    echo "2. Oracle Cloud CLI configured (~/.oci/config)"
    echo "3. Terraform installed"
    echo "4. SSH keys generated"
    echo

    read -p "Do you want to proceed? (yes/no): " -n 3 -r
    echo
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo
        echo "Setup cancelled."
        exit 0
    fi

    echo

    check_prerequisites
    check_oci_config
    validate_terraform
    create_tfvars
    show_plan
    execute_deployment
    post_deployment_steps

    echo
    echo "================================================="
    echo "  DEPLOYMENT COMPLETE!"
    echo "================================================="
    echo "Your Personal AI Employee is ready for 24/7 operation!"
    echo "Monitor the system and enjoy your Digital FTE!"
}

# Run main function
main "$@"