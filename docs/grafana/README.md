# Grafana and Tempo Integration

This directory contains dashboards and instructions for connecting Grafana to the Tempo trace backend.

## Install Tempo

Tempo is deployed via the upstream Grafana Helm chart which is referenced in `charts/tempo`.

```sh
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
# install using the chart in this repository
helm dependency build charts/tempo
helm install tempo charts/tempo
```

The release creates a service named `tempo` that exposes the OTLP gRPC endpoint on port `4317` and the HTTP query endpoint on port `3200`.

## Connect Grafana to Tempo

In Grafana, add a *Tempo* data source with the URL `http://tempo.default.svc.cluster.local:3200`. After saving the data source, traces shipped through the OpenTelemetry Collector become searchable from the **Explore** tab.

