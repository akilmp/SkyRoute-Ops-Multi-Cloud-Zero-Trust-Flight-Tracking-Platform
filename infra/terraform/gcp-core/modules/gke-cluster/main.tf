resource "google_container_cluster" "autopilot" {
  name       = var.cluster_name
  location   = var.region
  network    = var.network
  subnetwork = var.subnetwork

  enable_autopilot = true

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}

# Pub/Sub topic and subscription for ADS-B events
resource "google_pubsub_topic" "adsb" {
  name = "adsb-events"
}

resource "google_pubsub_subscription" "adsb" {
  name  = "adsb-events-sub"
  topic = google_pubsub_topic.adsb.name
}

# Cloud Armor security policy
resource "google_compute_security_policy" "armor" {
  name = "gke-armor-policy"
  rule {
    action   = "allow"
    priority = 1000
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["0.0.0.0/0"]
      }
    }
  }
}

# HTTP health check
resource "google_compute_health_check" "http" {
  name = "gke-http-healthcheck"
  http_health_check {
    request_path = "/"
    port         = 80
  }
}

output "cluster_name" {
  value = google_container_cluster.autopilot.name
}
