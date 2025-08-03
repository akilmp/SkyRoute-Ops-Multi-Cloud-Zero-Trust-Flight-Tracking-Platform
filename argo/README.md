# Argo CD Bootstrap

This directory implements the Argo CD app-of-apps pattern for the SkyRoute Ops platform.

## Bootstrap Steps

1. Deploy Argo CD into the cluster (e.g. via the upstream install manifest).
2. Apply the root application:
   ```bash
   kubectl apply -n argocd -f argo/root.yaml
   ```
3. The root app creates child applications for each Helm chart and Cross-Plane claim.
4. Image updates are handled by `argocd-image-updater` based on annotations on the apps.
