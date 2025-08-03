#!/usr/bin/env bash
set -euo pipefail

# Delete Istio ingress pods and wait for NS1 weight to drop to zero.
# Required environment variables:
#   NS1_API_KEY    - NS1 API key for authentication
#   NS1_ZONE       - DNS zone name (e.g. example.com)
#   NS1_RECORD     - Fully-qualified record name (e.g. ingress.example.com)
#   NS1_ANSWER_ID  - NS1 answer ID for this cluster
# Optional environment variables:
#   NAMESPACE      - Kubernetes namespace of ingress pods (default: istio-system)
#   LABEL          - Label selector for ingress pods (default: app=istio-ingressgateway)
#   POLL_INTERVAL  - Seconds between NS1 API polls (default: 5)

NAMESPACE="${NAMESPACE:-istio-system}"
LABEL="${LABEL:-app=istio-ingressgateway}"
POLL_INTERVAL="${POLL_INTERVAL:-5}"

: "${NS1_API_KEY:?NS1_API_KEY environment variable is required}"
: "${NS1_ZONE:?NS1_ZONE environment variable is required}"
: "${NS1_RECORD:?NS1_RECORD environment variable is required}"
: "${NS1_ANSWER_ID:?NS1_ANSWER_ID environment variable is required}"

echo "Deleting Istio ingress pods in namespace ${NAMESPACE} with label ${LABEL}"
kubectl delete pod -n "${NAMESPACE}" -l "${LABEL}" || true

echo "Polling NS1 for weight of answer ${NS1_ANSWER_ID} in ${NS1_RECORD}.${NS1_ZONE}"
while true; do
  weight=$(curl -sf -H "X-NSONE-Key: ${NS1_API_KEY}" \
    "https://api.nsone.net/v1/zones/${NS1_ZONE}/${NS1_RECORD}" | \
    jq -r --arg id "${NS1_ANSWER_ID}" '.answers[] | select(.id==$id) | .weight')
  weight=${weight:-0}
  echo "Current weight: ${weight}"
  if [[ "$weight" == "0" ]]; then
    echo "Weight has dropped to zero"
    break
  fi
  sleep "${POLL_INTERVAL}"
done
