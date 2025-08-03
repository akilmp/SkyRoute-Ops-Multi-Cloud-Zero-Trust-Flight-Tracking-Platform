variable "region" {
  description = "AWS region"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "edge_lambda_provider" {
  description = "Target cloud for edge lambda (aws or gcp)"
  type        = string
  default     = "aws"
}

variable "edge_lambda_pubsub_topic" {
  description = "Pub/Sub topic when edge lambda targets GCP"
  type        = string
  default     = ""
}


variable "regional_ingress_dns" {
  description = "DNS name of the regional ingress load balancer"
  type        = string
}

