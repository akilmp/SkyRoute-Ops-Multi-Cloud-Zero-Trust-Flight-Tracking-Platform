variable "zone" {
  description = "DNS zone name"
  type        = string
}

variable "record" {
  description = "Fully qualified domain name of the weighted record"
  type        = string
}

variable "answers" {
  description = "Map of endpoint IP addresses to their weights"
  type        = map(number)
}

variable "pulsar_app_id" {
  description = "ID of the NS1 Pulsar application"
  type        = string
}

variable "pulsar_type_id" {
  description = "Pulsar job type identifier"
  type        = string
}
