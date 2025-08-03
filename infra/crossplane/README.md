# Crossplane Configuration

This directory hosts Crossplane definitions for multi-cloud resources. Each
composite resource selects AWS or GCP implementations based on a `region`
label supplied by claims.

## Installation

Install the composite resource definitions followed by provider-specific compositions. The global ingress now provisions Istio gateways, Cloud Run or App Runner services, and NS1 DNS records so the `provider-kubernetes` and `provider-ns1` providers must be installed:

```bash
kubectl crossplane install provider crossplane/provider-kubernetes:v0.9.0
kubectl crossplane install provider crossplane/provider-ns1:v0.3.0
```

```bash
# XRDs
kubectl apply -f xrd/CompositeFlightStream.yaml
kubectl apply -f xrd/CompositeClickHouseCluster.yaml
kubectl apply -f xrd/CompositeGlobalIngress.yaml

# Compositions
kubectl apply -f compositions/flightstream-aws.yaml
kubectl apply -f compositions/flightstream-gcp.yaml
kubectl apply -f compositions/clickhouse-aws.yaml
kubectl apply -f compositions/clickhouse-gcp.yaml
kubectl apply -f compositions/globalingress-aws.yaml
kubectl apply -f compositions/globalingress-gcp.yaml
```

## Example Claims

The claims under `claims/` include a `compositionSelector` that matches the
`region` label. Provide AWS regions (for example `us-east-1`) to target AWS
compositions or GCP regions (for example `us-central1`) to target GCP
compositions.

```bash
# Flight stream in an AWS region
kubectl apply -f claims/FlightStreamClaim.yaml

# ClickHouse cluster in a GCP region
kubectl apply -f claims/CHClusterClaim.yaml

# Global ingress with weighted DNS
kubectl apply -f claims/GlobalIngressClaim.yaml
```
