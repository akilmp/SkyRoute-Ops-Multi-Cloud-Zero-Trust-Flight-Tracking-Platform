variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "network_name" {
  type    = string
  default = "core-network"
}

variable "subnetwork_cidr" {
  type    = string
  default = "10.0.0.0/20"
}

variable "k8s_namespace" {
  type    = string
  default = "default"
}

variable "k8s_service_account" {
  type    = string
  default = "default"
}
