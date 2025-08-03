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

variable "ns1_api_key" {
  description = "API key for NS1"
  type        = string
}

variable "ns1_zone" {
  description = "DNS zone for NS1 records"
  type        = string
}

variable "ns1_record" {
  description = "Fully qualified domain name of the weighted record"
  type        = string
}

variable "ns1_answers" {
  description = "Map of endpoint IP addresses to their weights"
  type        = map(number)
}

variable "ns1_pulsar_app_id" {
  description = "ID of the NS1 Pulsar application"
  type        = string
}

variable "ns1_pulsar_type_id" {
  description = "Pulsar job type identifier"
  type        = string
}
