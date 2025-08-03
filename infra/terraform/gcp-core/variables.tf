variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "network_name" {
  description = "Name of the VPC network"
  type        = string
  default     = "core-network"
}

variable "subnetwork_cidr" {
  description = "CIDR range for the primary subnet"
  type        = string
  default     = "10.0.0.0/20"
}

variable "domain" {
  description = "Base domain for Cloud DNS"
  type        = string
}

variable "cdn_backend_group" {
  description = "Instance group or NEG backing the Cloud CDN service"
  type        = string
}
