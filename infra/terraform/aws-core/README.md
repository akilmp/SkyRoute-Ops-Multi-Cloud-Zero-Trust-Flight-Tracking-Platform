# AWS Core Infrastructure

This Terraform configuration provisions core AWS components for the SkyRoute platform.

## Modules

- **core-network** – Creates a VPC spanning three availability zones, associated PrivateLink endpoints, and base IAM roles.
- **eks-cluster** – Provisions an EKS cluster with separate Karpenter-ready spot and on-demand node groups and enables IAM Roles for Service Accounts (IRSA).
- **global-dns** – Manages Route53 hosted zones for global DNS records.

The root module also configures an Amazon Kinesis Data Stream and an AWS WAF web ACL. Outputs expose values suitable for configuring Argo CD secrets such as the cluster endpoint and certificate authority data.

## Usage

Create a `prod.tfvars` file with values for the variables:

```
region      = "us-east-1"
environment = "prod"
```

Initialize and apply:

```
terraform init
terraform apply -var-file=prod.tfvars
```
