output "vpc_id" {
  value = aws_vpc.this.id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "privatelink_role_arn" {
  value = aws_iam_role.privatelink_role.arn
}
