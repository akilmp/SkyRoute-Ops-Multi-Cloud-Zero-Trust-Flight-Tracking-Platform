terraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    ns1 = {
      source  = "ns1-terraform/ns1"
      version = "~> 1.13"
    }
  }
}

provider "aws" {
  region = var.region
}

provider "ns1" {
  apikey = var.ns1_api_key
}

module "core_network" {
  source      = "./core-network"
  region      = var.region
  environment = var.environment
}

module "eks_cluster" {
  source             = "./eks-cluster"
  region             = var.region
  environment        = var.environment
  vpc_id             = module.core_network.vpc_id
  private_subnet_ids = module.core_network.private_subnet_ids
}

module "global_dns" {
  source      = "./global-dns"
  environment = var.environment
}

module "ns1" {
  source         = "../ns1"
  zone           = var.ns1_zone
  record         = var.ns1_record
  answers        = var.ns1_answers
  pulsar_app_id  = var.ns1_pulsar_app_id
  pulsar_type_id = var.ns1_pulsar_type_id
}

resource "aws_kinesis_stream" "events" {
  name        = "${var.environment}-events"
  shard_count = 1
}

resource "aws_wafv2_web_acl" "main" {
  name        = "${var.environment}-waf"
  description = "Global WAF for ${var.environment}"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    sampled_requests_enabled   = true
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.environment}-waf"
  }
}
