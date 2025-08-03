# SkyRoute Ops – Multi‑Cloud Zero‑Trust Flight‑Tracking Platform

## Table of Contents

1. [Project Summary](#project-summary)
2. [Key Capabilities & Skills Demonstrated](#key-capabilities--skills-demonstrated)
3. [High‑Level Architecture](#high-level-architecture)
4. [Tech Stack & Cloud Services](#tech-stack--cloud-services)
5. [Repository Layout](#repository-layout)
6. [Prerequisites](#prerequisites)
7. [Local Development Environment](#local-development-environment)
8. [Infrastructure‑as‑Code](#infrastructure-as-code)

   * 8.1 [Cross‑Plane Resources](#81-cross-plane-resources)
   * 8.2 [Terraform Modules](#82-terraform-modules)
9. [Kubernetes Platform](#kubernetes-platform)

   * 9.1 [Cluster Provisioning](#91-cluster-provisioning)
   * 9.2 [GitOps with Argo CD](#92-gitops-with-argo-cd)
   * 9.3 [Service Mesh & Zero‑Trust](#93-service-mesh--zero-trust)
10. [Data Ingestion Pipeline](#data-ingestion-pipeline)
11. [Storage & Analytics Layer](#storage--analytics-layer)
12. [Observability & SLOs](#observability--slos)
13. [Security & Compliance](#security--compliance)
14. [CI/CD Workflow](#cicd-workflow)
15. [Global Traffic Management & DR](#global-traffic-management--dr)
16. [Cost Management](#cost-management)
17. [Demo Recording Guide](#demo-recording-guide)
18. [Troubleshooting & FAQ](#troubleshooting--faq)
19. [Stretch Goals](#stretch-goals)
20. [References & Further Reading](#references--further-reading)

---

## Project Summary

**SkyRoute Ops** is a fully GitOps‑managed, multi‑cloud platform that ingests live ADS‑B aircraft telemetry from edge devices, enriches each event with weather & NOTAM data, and serves near‑real‑time geospatial analytics via a zero‑trust service mesh spanning AWS EKS (Sydney) and Google GKE (Melbourne).  Global DNS (NS1) steers users to the healthiest region; Istio provides mTLS and policy‑based traffic control; Argo CD ensures declarative roll‑outs; OpenTelemetry feeds a unified observability stack; and Cross‑Plane declares cloud resources directly from Kubernetes manifests.  Chaos scripts prove cross‑cloud fail‑over in under 30 seconds.

---

## Key Capabilities & Skills Demonstrated

| Competency                       | Implementation                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------------- |
| **Multi‑cloud Architecture**     | Active/active EKS + GKE, global NS1 DNS, CloudFront & Cloud CDN edge cache                |
| **Kubernetes & GitOps**          | Helm charts → Argo CD app‑of‑apps pattern; blue‑green & canary roll‑outs                  |
| **Service Mesh / Zero‑Trust**    | Istio 1.23 mTLS STRICT; OPA Gatekeeper for policy enforcement                             |
| **Event Streaming & Serverless** | Edge AWS Lambda parses ADS‑B UDP → Kinesis Data Streams; Cloud Run weather enrich service |
| **OLAP & Geospatial**            | ClickHouse cluster + PostGIS sidecar for route queries                                    |
| **Infrastructure as Code**       | Cross‑Plane XRDs for MSK‑like streams, Terraform for core VPCs                            |
| **Observability**                | OpenTelemetry sidecars → Tempo & Prometheus → Grafana Cloud RED/SLO dashboards            |
| **Security**                     | Keycloak OIDC SSO, HashiCorp Vault secrets, AWS WAF + GCP Cloud Armor                     |
| **Cost Optimisation**            | Karpenter spot nodes, GKE Autopilot, S3 lifecycle, Cloud CDN caching                      |

---

## High‑Level Architecture (very different from KoalaSafe)

```text
    SDR Antenna ─────► edge Lambda UDP parser (us‑west‑2@Lambda@Edge)
                       |
                       v
                AWS Kinesis  {Sydney}
                       |
     ┌─────────────────┴──────────────────────┐
     |                                        |
 +-----------+                         +-----------+
 |  EKS (AWS)| <─ Istio mTLS ─> |  GKE (GCP)|
 |  Region SYD|                 | Region MEL |
 +-----------+                         +-----------+
     |   |                                   |   |
     |   ├─ ClickHouse (heat‑map API)        |   ├─ ClickHouse replica
     |   ├─ PostGIS (routes)                 |   ├─ PostGIS
     |   └─ FastAPI gateway (Envoy)          |   └─ FastAPI
     |                                        |
     └───> Argo CD <── GitHub ◄── GitHub Actions (build/test/push)
```

* **Global DNS**: NS1 weighted records with real‑time health probes to each mesh‑ingress.
* **Edge cache**: CloudFront + Cloud CDN with GeoJSON TTL 5 s.
* **Data lake (Optional)**: AWS S3 → Athena for historical mode.

## Tech Stack & Cloud Services Stack & Cloud Services

| Category               | AWS                  | GCP                | OSS Components                                    |
| ---------------------- | -------------------- | ------------------ | ------------------------------------------------- |
| **Edge Compute**       | Lambda\@Edge         | —                  | dump1090 feeder (optional)                        |
| **Message Bus**        | Kinesis Data Streams | Pub/Sub relay      | —                                                 |
| **Container Platform** | EKS                  | GKE (Autopilot)    | Kubernetes 1.29                                   |
| **GitOps**             | —                    | —                  | Argo CD 2.10, Helm 3                              |
| **Service Mesh**       | —                    | —                  | Istio 1.23, Envoy proxy                           |
| **Database / OLAP**    | —                    | —                  | ClickHouse 23, PostGIS 16                         |
| **Observability**      | AMP, CloudWatch      | GMP, Cloud Logging | OpenTelemetry, Tempo, Prometheus 2.51, Grafana 11 |
| **AuthZ**              | Cognito (edge)       | IAP (edge)         | Keycloak 23                                       |
| **Secrets**            | Secrets Manager      | Secret Manager     | HashiCorp Vault 1.15                              |
| **Global DNS**         | NS1 (external)       | NS1                | —                                                 |
| **IaC**                | Terraform 1.7        | Terraform 1.7      | Cross‑Plane 1.15                                  |

---

## Repository Layout

```
skyroute-ops/
├── infra/
│   ├── terraform/
│   │   ├── aws-core/          # VPC, EKS, Kinesis, WAF
│   │   └── gcp-core/          # VPC, GKE, CloudArmor, PubSub
│   └── crossplane/
│       ├── xrd/               # CompositeResourceDefinitions
│       └── claims/            # FlightStreamClaim.yaml
├── charts/                    # Helm charts for each micro‑service
│   └── ingest-api/
├── argo/                      # app-of-apps manifests
├── services/
│   ├── ingest-api/            # Go service for ADS‑B fan‑out
│   ├── enrich-weather/        # Python Cloud Run svc
│   └── gateway/               # FastAPI GraphQL gateway
├── postgres/                  # init scripts for routes & NOTAM tables
├── clickhouse/                # schemas & materialized views
├── otel/                      # collector configs
├── policy/                    # Gatekeeper OPA policies
├── hack/
│   └── kill-ingress.sh        # chaos script
├── .github/workflows/
│   └── ci-cd.yml
└── docs/
    ├── architecture.drawio
    ├── demo_script.md
    └── cost_estimate.xlsx
```

---

## Prerequisites

* **AWS CLI v2** + profile `skyroute-aws` (Sydney default)
* **gcloud >= 470** + project `skyroute-gcp`
* **kubectl 1.29**, **helm 3**, **istioctl 1.23**
* **Docker** 24+
* **Terraform** 1.7.x
* **NS1** account (free tier) with API key
* **GitHub Actions** runners (or GH Hosted) for CI/CD

---

## Local Development Environment

1. **Clone & set env**

   ```bash
   git clone https://github.com/<you>/skyroute-ops.git
   cd skyroute-ops
   cp .env.sample .env   # set AWS/GCP creds & NS1 token
   ```
2. **Kind + Istio**

   ```bash
   kind create cluster --name skyroute-dev --image kindest/node:v1.29.0
   istioctl install -y --set profile=demo
   kubectl label namespace default istio-injection=enabled
   ```
3. **Run ClickHouse & services**

   ```bash
   helm repo add clickhouse https://charts.clickhouse.com/
   helm install ch clickhouse/clickhouse --set persistence.enabled=false
   helm install ingest-api charts/ingest-api --set image.tag=dev
   ```
4. **Simulate ADS‑B feed**

   ```bash
   go run services/ingest-api/cmd/simulator/main.go --rate 50
   ```
5. **Access**

   * Grafana: [http://localhost:3000](http://localhost:3000) (admin/admin)
   * Gateway: [http://localhost:8080/graphql](http://localhost:8080/graphql)

---

## Infrastructure‑as‑Code

### 8.1 Cross‑Plane Resources

| XRD                          | Claim Kind           | Purpose                                                 |
| ---------------------------- | -------------------- | ------------------------------------------------------- |
| `CompositeFlightStream`      | `FlightStreamClaim`  | Creates Kinesis or Pub/Sub stream based on region label |
| `CompositeClickHouseCluster` | `CHClusterClaim`     | Provisions StatefulSet, PVC, Service & HPA              |
| `CompositeGlobalIngress`     | `GlobalIngressClaim` | Creates ALB + Cloud Run + Istio Gateway + NS1 record    |

Developers issue namespaced *claims*; Cross‑Plane composes cloud resources.

### 8.2 Terraform Modules

| Module         | AWS                                | GCP                              |
| -------------- | ---------------------------------- | -------------------------------- |
| `core-network` | VPC (3 AZs), PrivateLink endpoints | VPC + Private Service Connect    |
| `eks-cluster`  | Worker groups, IRSA, Karpenter     | —                                |
| `gke-cluster`  | —                                  | GKE Autopilot, Workload Identity |
| `global-dns`   | NS1 weighted DNS, health checks    | same                             |

Run order: network → clusters → DNS → GitHub secrets.  Example commands:

```bash
cd infra/terraform/aws-core
terraform init && terraform apply -var-file=prod.tfvars
```

---

## Kubernetes Platform

### 9.1 Cluster Provisioning

* **EKS**: Terraform module provisions `t3.medium` control plane & Karpenter with spot + on‑demand.
* **GKE**: Autopilot (serverless nodes) reduces ops overhead.
* Both clusters share **Istio** multi‑primary; east‑west gateways peer via IPSec VPN (Terraform VGW ↔ HA VPN).

### 9.2 GitOps with Argo CD

* *App‑of‑Apps* root `argo/root.yaml` points to Helm chart repos per service.
* Image tags auto‑bumped by GH Action using `argocd-image-updater`.

### 9.3 Service Mesh & Zero‑Trust

* **Istio** Sidecars: STRICT mTLS, PeerAuth per namespace.
* **OPA Gatekeeper** policies block `kind=Service` without `team` label; admission audit in Prometheus.

---

## Data Ingestion Pipeline

1. **Lambda\@Edge (Go 1.22)** decodes Mode‑S messages from local UDP feed.
2. Records (JSON) → **Kinesis** shard (AWS) or Pub/Sub (GCP).
3. **Ingest‑API** micro‑service reads stream, deduplicates, writes to ClickHouse + broadcasts via NATS JetStream inside mesh.
4. **Weather Enrich** Cloud Run function pulls current METAR for aircraft location & merges into event.

Latency 95p ≤ 300 ms (edge to ClickHouse commit).

---

## Storage & Analytics Layer

| Store          | Purpose                         | Notes                                       |
| -------------- | ------------------------------- | ------------------------------------------- |
| **ClickHouse** | Hot OLAP (last 7 days)          | TTL 7d, MergeTree partition by `event_date` |
| **PostGIS**    | Flight paths & airport polygons | Logical replica to both clusters            |
| **S3 Glacier** | Long‑term raw archive           | Lifecycle after 30 days                     |

Materialised view in ClickHouse aggregates heat‑map tiles (XYZ) ready for MapLibre frontend.

---

## Observability & SLOs

* **OpenTelemetry** sidecar per pod → Tempo distributed tracing.
* **Prometheus** federation: each cluster scrapes locals; AMP/GMP remote‑write to Grafana Cloud.
* **SLO** example: *P99 ingest latency < 500 ms over 1 day* (RED metrics exported by ingest‑api).
* **Grafana Dashboards** stored as JSON (`docs/grafana/skyroute_dash.json`).

### Enabling OpenTelemetry sidecar injection

Helm charts opt in to telemetry by annotating pods for the OTel sidecar:

```yaml
podAnnotations:
  sidecar.opentelemetry.io/inject: "true"
```

The injected container reads pipelines from `otel/collector.yaml` and ships traces to Tempo and metrics to Prometheus.

Alerts:

| Alert              | Threshold                 | Action                            |
| ------------------ | ------------------------- | --------------------------------- |
| `HighLatency`      | P99 > 500 ms for 5 min    | PagerDuty + Argo roll‑back canary |
| `IngressUnhealthy` | Istio ingress 4xx > 3 %   | NS1 flips traffic weight          |
| `OPA_Denied`       | Gatekeeper violations > 0 | Slack `#platform-sec`             |

---

## Security & Compliance

| Control            | Impl.                                                                             |
| ------------------ | --------------------------------------------------------------------------------- |
| **mTLS**           | Istio certificates rotated 24 h via Citadel                                       |
| **RBAC**           | Keycloak OIDC ↔ Istio Authn; least‑priv service accounts                          |
| **Secrets**        | Vault Agent injects DB & NS1 tokens; policies restrict lease TTL.                 |
| **Edge WAF**       | AWS WAF + Cloud Armor blocking OWASP Top‑10                                       |
| **Policy‑as‑Code** | Gatekeeper + `deny-service-without-owner` + `no-root-containers`; conftest in CI. |

---

## CI/CD Workflow

```yaml
# .github/workflows/ci-cd.yml
name: build-test-deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
      - run: go test ./...
      - run: docker build -t ghcr.io/${{github.repository}}/ingest-api:${{github.sha}} .
      - run: docker push ghcr.io/${{github.repository}}/ingest-api:${{github.sha}}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Bump image tag & create PR
        uses: argocd-image-updater/argocd-image-updater-action@v1
```

*Argo CD* auto‑syncs once PR merged; canary proceeds 10 % → 50 % → 100 % if SLO holds for 5 min.

---

## Global Traffic Management & DR

* **NS1** weighted DNS (50/50 default).
* **Health Check**: HTTPS on `/healthz` via NS1 Pulsar; weight→0 when 5xx > 1 %.
* **Chaos Script** `hack/kill-ingress.sh`: deletes AWS Istio ingress‑gateway; watch NS1 API until weight=0 (≈ 25 s).
* **Return Path**: Argo Roll‑out recreates pod; NS1 weight gradually restored via Pulsar feedback.

### NS1 API Usage

`hack/kill-ingress.sh` and the accompanying Terraform require access to the NS1
API.  Export the following variables before invoking the script:

```bash
export NS1_API_KEY=xxxxxxxx          # NS1 API token
export NS1_ZONE=example.com          # DNS zone hosting the record
export NS1_RECORD=ingress.example.com # FQDN of the weighted record
export NS1_ANSWER_ID=<answer-uuid>   # Answer ID for this cluster
```

The script deletes Istio ingress pods and polls
`https://api.nsone.net/v1/zones/${NS1_ZONE}/${NS1_RECORD}` until the selected
answer's `weight` field reaches `0`.

---

## Cost Management

| Area             | Optimisation                           | Est. AUD / mo |
| ---------------- | -------------------------------------- | ------------- |
| EKS Nodes        | Karpenter mixed‑instance + spot (70 %) | \$12          |
| GKE              | Autopilot pay‑per‑pod                  | \$8           |
| ClickHouse       | Graviton t4g.small gp3 EBS             | \$3           |
| NS1 DNS          | Developer tier                         | \$1           |
| Grafana Cloud    | Free tier 10 k series                  | \$0           |
| **Total (idle)** |                                        | **\~\$24**    |


---

## Troubleshooting & FAQ

| Issue                          | Cause                     | Resolution                                                                     |
| ------------------------------ | ------------------------- | ------------------------------------------------------------------------------ |
| `istio-proxy CrashLoopBackOff` | cluster CIDR mismatch     | Update `ISTIO_INBOUND_INTERCEPTION_MODE=REDIRECT` and restart sidecar injector |
| `Argo CD stuck OutOfSync`      | Image tag mismatch        | Ensure `argocd-image-updater` PR merged & app auto‑sync enabled                |
| `NS1 fail‑over slow (>60 s)`   | Health check timeout 15 s | Reduce Pulsar **interval** to 10 s, threshold 2/2                              |
| ClickHouse high CPU            | Merge backlog             | Increase `merge_max_size` or add shard in other region                         |
| OPA denies Deploy              | Missing `team` label      | `kubectl label deploy ingest-api team=platform`                                |

---

## Stretch Goals

* **eBPF Cilium** service mesh → L7 policies & Hubble observability.
* **SpiceDB** global RBAC graph synced via Cross‑Plane claim.
* **Edge AI** – WebAssembly plugin at Envoy computes flight‑path risk scores.
* **Azure AKS** tertiary region with external‑mesh federation (Istio 1.23 multi‑cluster).

---

## References & Further Reading

* ADS‑B Intro – [https://flightaware.com/adsb/](https://flightaware.com/adsb/)
* Istio Multi‑Primary Guide – Istio docs 2025
* Argo CD App‑of‑Apps Pattern – [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Cross‑Plane XRD Tutorial – [https://crossplane.io/docs/](https://crossplane.io/docs/)
* NS1 Pulsar Traffic Steering – NS1 Docs 2024

---

*Last updated: 3 Aug 2025*
