terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "core_network" {
  source          = "./modules/core-network"
  project_id      = var.project_id
  region          = var.region
  network_name    = var.network_name
  subnetwork_cidr = var.subnetwork_cidr
}

module "gke_cluster" {
  source     = "./modules/gke-cluster"
  project_id = var.project_id
  region     = var.region
  network    = module.core_network.network_name
  subnetwork = module.core_network.subnetwork_name
}

module "global_dns" {
  source     = "./modules/global-dns"
  project_id = var.project_id
  domain     = var.domain
}

# Service account for GitHub Actions
resource "google_service_account" "github" {
  account_id   = "github-actions"
  display_name = "GitHub Actions Deploy"
}

resource "google_service_account_key" "github" {
  service_account_id = google_service_account.github.name
}

output "github_service_account_key" {
  description = "Service account key JSON for GitHub secrets"
  value       = google_service_account_key.github.private_key
  sensitive   = true
}
