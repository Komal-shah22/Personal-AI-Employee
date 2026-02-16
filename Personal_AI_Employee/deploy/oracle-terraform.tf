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

variable "compartment_id" {
  description = "OCID of the compartment where resources will be created"
  type        = string
  validation {
    condition     = length(var.compartment_id) > 0
    error_message = "Compartment ID must be provided."
  }
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

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_id
}

# VCN
resource "oci_core_virtual_network" "ai_employee_vcn" {
  compartment_id = var.compartment_id
  cidr_block     = var.vcn_cidr_block
  display_name   = "${var.display_name_prefix}-vcn"
  dns_label      = "aiemployee"
}

# Internet Gateway
resource "oci_core_internet_gateway" "ai_employee_ig" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_virtual_network.ai_employee_vcn.id
  display_name   = "${var.display_name_prefix}-ig"
}

# Route Table
resource "oci_core_route_table" "ai_employee_rt" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_virtual_network.ai_employee_vcn.id
  display_name   = "${var.display_name_prefix}-route-table"

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
  display_name   = "${var.display_name_prefix}-security-list"

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

  ingress_security_rules {
    protocol    = "6"  # TCP
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"

    tcp_options {
      min = 3000
      max = 3000
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
  availability_domain  = data.oci_identity_availability_domains.ads.availability_domains[var.availability_domain].name
  cidr_block           = var.subnet_cidr_block
  display_name         = "${var.display_name_prefix}-subnet"
  dns_label            = "aisubnet"
  route_table_id       = oci_core_route_table.ai_employee_rt.id
  security_list_ids    = [oci_core_security_list.ai_employee_sl.id]
  dhcp_options_id      = oci_core_virtual_network.ai_employee_vcn.default_dhcp_options_id
}

# Instance
resource "oci_core_instance" "ai_employee_instance" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[var.availability_domain].name
  compartment_id      = var.compartment_id
  display_name        = "${var.display_name_prefix}-instance"
  shape               = var.instance_shape
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
    ocpus         = var.ocpus
    memory_in_gbs = var.memory_in_gbs
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)
  }
}