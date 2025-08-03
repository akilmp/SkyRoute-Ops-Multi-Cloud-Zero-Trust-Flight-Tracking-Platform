#!/usr/bin/env bash
set -euo pipefail

# Create local Kubernetes cluster with kind
kind create cluster --name skyroute-dev --image kindest/node:v1.29.0

# Install Istio service mesh
istioctl install -y --set profile=demo
kubectl label namespace default istio-injection=enabled --overwrite

# Deploy sample services
helm repo add clickhouse https://charts.clickhouse.com/
helm install ch clickhouse/clickhouse --set persistence.enabled=false
helm install ingest-api charts/ingest-api --set image.tag=dev

