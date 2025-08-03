output "record_id" {
  description = "ID of the weighted DNS record"
  value       = ns1_record.weighted.id
}

output "record_weights" {
  description = "Map of answer IPs to their weights"
  value       = { for ans in ns1_record.weighted.answers : ans.answer => tonumber(ans.meta["weight"]) }
}
