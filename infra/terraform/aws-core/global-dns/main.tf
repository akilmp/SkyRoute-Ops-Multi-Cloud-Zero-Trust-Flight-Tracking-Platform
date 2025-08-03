resource "aws_route53_zone" "this" {
  name = "${var.environment}.example.com"
}
