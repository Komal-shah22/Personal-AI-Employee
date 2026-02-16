# Oracle Cloud Infrastructure Variables for Personal AI Employee

variable "compartment_id" {
  description = "OCID of the compartment where resources will be created"
  type        = string
  validation {
    condition     = length(var.compartment_id) > 0
    error_message = "Compartment ID must be provided."
  }
}

variable "region" {
  description = "Region where resources will be created"
  type        = string
  default     = "us-ashburn-1"
}

variable "availability_domain" {
  description = "Availability domain for the compute instance"
  type        = string
  default     = "1"
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key file for instance access"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "instance_shape" {
  description = "Shape of the compute instance"
  type        = string
  default     = "VM.Standard.E4.Flex"
}

variable "ocpus" {
  description = "Number of OCPUs for the instance"
  type        = number
  default     = 2
}

variable "memory_in_gbs" {
  description = "Memory in GBs for the instance"
  type        = number
  default     = 8
}

variable "boot_volume_size_in_gbs" {
  description = "Size of the boot volume in GBs"
  type        = number
  default     = 50
}

variable "display_name_prefix" {
  description = "Prefix for display names of resources"
  type        = string
  default     = "ai-employee"
}

variable "vcn_cidr_block" {
  description = "CIDR block for the VCN"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_block" {
  description = "CIDR block for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "vault_storage_size_in_gbs" {
  description = "Size of storage for AI Employee vault data"
  type        = number
  default     = 100
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_id
}