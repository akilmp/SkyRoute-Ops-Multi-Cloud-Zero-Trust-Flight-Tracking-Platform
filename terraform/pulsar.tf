terraform {
  required_providers {
    ns1 = {
      source  = "ns1-terraform/ns1"
      version = "~> 1.13"
    }
  }
}

provider "ns1" {
  apikey = var.ns1_api_key
}

variable "ns1_api_key" {
  description = "API key for NS1"
  type        = string
}

variable "zone" {
  description = "DNS zone that contains the weighted record"
  type        = string
}

variable "record" {
  description = "Fully qualified domain name of the record"
  type        = string
}

variable "answers" {
  description = "Map of endpoint IP addresses to their initial weights"
  type        = map(number)
}

variable "pulsar_app_id" {
  description = "ID of the NS1 Pulsar application"
  type        = string
}

variable "pulsar_type_id" {
  description = "Pulsar job type identifier (e.g. latency, download)"
  type        = string
}

resource "ns1_monitoringjob" "ingress" {
  name      = "ingress-health"
  job_type  = "tcp"
  regions   = ["sjc", "lga", "ams"]
  frequency = 60
  config = {
    host = var.record
    port = "80"
  }
}

resource "ns1_pulsarjob" "ingress" {
  name    = "ingress-performance"
  app_id  = var.pulsar_app_id
  type_id = var.pulsar_type_id
  active  = true
  config  = {}
}

resource "ns1_record" "weighted_ingress" {
  zone   = var.zone
  domain = var.record
  type   = "A"
  ttl    = 60

  dynamic "answers" {
    for_each = var.answers
    content {
      answer = answers.key
      meta = {
        weight = tostring(answers.value)
        up     = "true"
      }
    }
  }

  filters {
    filter = "weighted_shuffle"
  }

  filters {
    filter = "select_first_n"
    config = {
      N = "1"
    }
  }
}
