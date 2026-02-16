# Oracle Cloud Infrastructure Outputs for Personal AI Employee

output "instance_public_ip" {
  description = "Public IP address of the compute instance"
  value       = oci_core_instance.ai_employee_instance.public_ip
}

output "instance_private_ip" {
  description = "Private IP address of the compute instance"
  value       = oci_core_instance.ai_employee_instance.private_ip
}

output "instance_id" {
  description = "OCID of the compute instance"
  value       = oci_core_instance.ai_employee_instance.id
}

output "vcn_id" {
  description = "OCID of the Virtual Cloud Network"
  value       = oci_core_virtual_network.ai_employee_vcn.id
}

output "subnet_id" {
  description = "OCID of the subnet"
  value       = oci_core_subnet.ai_employee_subnet.id
}

output "security_list_id" {
  description = "OCID of the security list"
  value       = oci_core_security_list.ai_employee_sl.id
}

output "dashboard_url" {
  description = "URL for the AI Employee dashboard"
  value       = "http://${oci_core_instance.ai_employee_instance.public_ip}:3000"
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh ubuntu@${oci_core_instance.ai_employee_instance.public_ip}"
}

output "deployment_status" {
  description = "Deployment status"
  value       = "Personal AI Employee deployed successfully on Oracle Cloud"
}

output "next_steps" {
  description = "Recommended next steps after deployment"
  value = [
    "1. SSH to the instance: ${output.ssh_command}",
    "2. Verify services are running: sudo systemctl status ai-employee-*",
    "3. Access dashboard: ${output.dashboard_url}",
    "4. Configure monitoring and alerts",
    "5. Set up automated backups",
    "6. Document the production environment"
  ]
}