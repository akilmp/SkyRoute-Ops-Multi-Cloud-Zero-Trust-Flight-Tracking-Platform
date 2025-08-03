# Crossplane Configuration

This directory hosts Crossplane definitions for multi-cloud resources. Each
composite resource selects AWS or GCP implementations based on a `region`
label supplied by claims.

## Installation

Apply the composite resource definitions:

```bash
kubectl apply -f xrd/CompositeFlightStream.yaml
kubectl apply -f xrd/CompositeClickHouseCluster.yaml
kubectl apply -f xrd/CompositeGlobalIngress.yaml
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

# Global ingress
kubectl apply -f claims/GlobalIngressClaim.yaml
```
