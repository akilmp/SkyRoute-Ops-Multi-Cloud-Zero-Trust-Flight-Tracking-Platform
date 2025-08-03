"""Feast entity and feature view definitions for buoy and imagery data."""
from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# Entities
buoy = Entity(name="buoy_id", join_keys=["buoy_id"], description="Buoy identifier")
image = Entity(name="image_id", join_keys=["image_id"], description="Imagery tile identifier")

# Data sources pointing at S3 objects containing processed data
imagery_source = FileSource(
    path="s3://example-bucket/imagery/imagery.parquet",
    timestamp_field="event_timestamp",
)

buoy_source = FileSource(
    path="s3://example-bucket/buoy/buoy.parquet",
    timestamp_field="event_timestamp",
)

# Feature views
imagery_features = FeatureView(
    name="imagery_features",
    entities=[image],
    ttl=timedelta(days=1),
    schema=[
        Field(name="cloud_coverage", dtype=Float32),
        Field(name="wind_speed", dtype=Float32),
    ],
    source=imagery_source,
)

buoy_features = FeatureView(
    name="buoy_features",
    entities=[buoy],
    ttl=timedelta(days=1),
    schema=[
        Field(name="wave_height", dtype=Float32),
        Field(name="water_temp", dtype=Float32),
    ],
    source=buoy_source,
)

# Feature service to group related features
ocean_state_fs = FeatureService(
    name="ocean_state",
    features=[imagery_features, buoy_features],
)
