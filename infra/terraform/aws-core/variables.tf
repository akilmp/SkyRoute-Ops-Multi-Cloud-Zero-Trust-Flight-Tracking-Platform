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

