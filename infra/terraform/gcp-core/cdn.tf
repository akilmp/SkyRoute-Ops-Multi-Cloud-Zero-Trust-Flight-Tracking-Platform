resource "google_compute_backend_service" "cdn" {
  name        = "${var.project_id}-cdn"
  protocol    = "HTTP"
  enable_cdn  = true
  timeout_sec = 30

  backend {
    group = var.cdn_backend_group
  }
}

resource "google_compute_global_address" "cdn" {
  name = "${var.project_id}-cdn-ip"
}
