terraform {
  required_providers {
    ns1 = {
      source  = "ns1-terraform/ns1"
      version = "~> 1.13"
    }
  }
}

resource "ns1_zone" "this" {
  zone = var.zone
}

resource "ns1_monitoringjob" "pulsar" {
  name      = "${var.record}-health"
  job_type  = "tcp"
  regions   = ["sjc", "lga", "ams"]
  frequency = 60
  config = {
    host = var.record
    port = "80"
  }
}

resource "ns1_pulsarjob" "this" {
  name    = "${var.record}-pulsar"
  app_id  = var.pulsar_app_id
  type_id = var.pulsar_type_id
  active  = true
  config  = {}
}

resource "ns1_record" "weighted" {
  zone   = ns1_zone.this.zone
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
