output "kinesis_stream_name" {
  value = aws_kinesis_stream.events.name
}

output "waf_arn" {
  value = aws_wafv2_web_acl.main.arn
}

output "argocd_cluster_endpoint" {
  value = module.eks_cluster.cluster_endpoint
}

output "argocd_cluster_ca" {
  value = module.eks_cluster.cluster_ca_certificate
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.edge.domain_name
}
