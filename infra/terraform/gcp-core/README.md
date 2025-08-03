# GCP Core Infrastructure

This Terraform configuration provisions core GCP infrastructure for the SkyRoute platform, including:

- VPC network with Private Service Connect, IAM bindings, and Workload Identity
- GKE Autopilot cluster and Pub/Sub topic/subscription for ADS-B events
- Global Cloud DNS zone
- Cloud Armor security policy and HTTP health check
- Service account key output for GitHub secrets

## Prerequisites

- [Terraform](https://www.terraform.io/) >= 1.5
- Google Cloud project with billing enabled
- `gcloud` authenticated with permission to manage the project

## Usage

```bash
# Navigate to the module
cd infra/terraform/gcp-core

# Initialize providers and modules
terraform init

# Review the planned changes
terraform plan -var project_id=YOUR_PROJECT -var domain=example.com

# Apply the configuration
terraform apply -var project_id=YOUR_PROJECT -var domain=example.com

# Output includes a service account key suitable for storing as a GitHub secret:
terraform output -raw github_service_account_key > github-key.json
```

Store `github-key.json` securely and add its contents as a GitHub Actions secret.
