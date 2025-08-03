resource "google_compute_network" "vpc" {
  name                    = var.network_name
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "primary" {
  name                     = "${var.network_name}-subnet"
  ip_cidr_range            = var.subnetwork_cidr
  region                   = var.region
  network                  = google_compute_network.vpc.id
  private_ip_google_access = true
}

# Private Service Connect for Google APIs
resource "google_compute_global_address" "private_service_range" {
  name          = "private-service-range"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "services/servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_service_range.name]
}

# Service account for Workload Identity
resource "google_service_account" "workload" {
  account_id   = "workload-app"
  display_name = "Workload Identity Application SA"
}

resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.workload.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.k8s_service_account}]"
}

# Example IAM binding for network admin
resource "google_project_iam_binding" "network_admin" {
  project = var.project_id
  role    = "roles/compute.networkAdmin"
  members = ["serviceAccount:${google_service_account.workload.email}"]
}

output "network_name" {
  value = google_compute_network.vpc.name
}

output "subnetwork_name" {
  value = google_compute_subnetwork.primary.name
}
