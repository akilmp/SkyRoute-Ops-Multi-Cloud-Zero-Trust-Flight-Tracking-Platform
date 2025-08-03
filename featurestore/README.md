# Feature Store

This directory contains a minimal [Feast](https://feast.dev) repository for the SkyRoute platform. It defines
entities and feature views for ocean buoy telemetry and satellite imagery stored in S3.

## Usage

Initialize the feature store and materialize the latest features:

```bash
feast apply
feast materialize-incremental `date +%Y-%m-%d`
```

### Retrieving Features

Online feature retrieval example:

```python
from feast import FeatureStore

fs = FeatureStore(repo_path="featurestore")
features = fs.get_online_features(
    features=[
        "buoy_features:wave_height",
        "buoy_features:water_temp",
    ],
    entity_rows=[{"buoy_id": 123}],
).to_dict()
print(features)
```
