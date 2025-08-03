resource "google_dns_managed_zone" "primary" {
  name     = "global-zone"
  dns_name = "${var.domain}."
}

output "name_servers" {
  value = google_dns_managed_zone.primary.name_servers
}
