output "ns1_record_id" {
  description = "ID of the NS1 weighted record"
  value       = module.ns1.record_id
}

output "ns1_record_weights" {
  description = "Map of endpoint weights for the NS1 record"
  value       = module.ns1.record_weights
}
