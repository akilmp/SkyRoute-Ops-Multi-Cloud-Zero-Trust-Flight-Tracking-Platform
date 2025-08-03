# Edge Lambda

Lambda@Edge function that parses UDP Mode-S messages and forwards them to a
streaming service. Depending on `TARGET_CLOUD` it will publish to either an AWS
Kinesis stream or a Google Cloud Pub/Sub topic.

## Environment Variables

| Name | Description |
|------|-------------|
| `TARGET_CLOUD` | `aws` or `gcp` to select the destination. Defaults to `aws`. |
| `KINESIS_STREAM` | Name of the Kinesis stream to publish to when `TARGET_CLOUD=aws`. |
| `PUBSUB_TOPIC` | Full Pub/Sub topic path when `TARGET_CLOUD=gcp` (e.g. `projects/my-proj/topics/mode-s`). |

## Packaging

The function expects to be deployed as a zip file named `handler.zip` containing
`handler.py` and its dependencies. A simple packaging command:

```bash
cd services/edge-lambda
zip handler.zip handler.py
```

## Deployment with Terraform

A Terraform module is provided under `infra/terraform/aws-core/edge-lambda.tf`.
After packaging the function, deploy with:

```bash
cd infra/terraform/aws-core
terraform init -backend=false
terraform apply -var="environment=dev" -var="region=us-east-1"
```

Adjust variables as needed. The Lambda function is created with permissions to
write to the Kinesis stream defined in the same Terraform stack.

