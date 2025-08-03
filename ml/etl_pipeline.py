"""Kubeflow pipeline to ingest S3 imagery and buoy data into Feast."""
from datetime import datetime

import kfp
from kfp import dsl
from kfp.dsl import component


@component
def ingest_imagery(s3_path: str):
    """Download imagery metadata from S3."""
    import boto3
    s3 = boto3.client("s3")
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    s3.download_file(bucket, key, "/tmp/imagery.parquet")


@component
def ingest_buoy(s3_path: str):
    """Download buoy measurements from S3."""
    import boto3
    s3 = boto3.client("s3")
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    s3.download_file(bucket, key, "/tmp/buoy.parquet")


@component
def materialize(repo_path: str = "featurestore"):
    """Materialize features into Feast."""
    from feast import FeatureStore

    fs = FeatureStore(repo_path)
    fs.materialize_incremental(datetime.utcnow())


@dsl.pipeline(
    name="s3-buoy-etl",
    description="Ingest S3 imagery & buoy data and materialize features into Feast",
)
def etl_pipeline(
    imagery_path: str, buoy_path: str, repo_path: str = "featurestore"
):
    img_task = ingest_imagery(imagery_path)
    buoy_task = ingest_buoy(buoy_path)
    materialize(repo_path).after(img_task, buoy_task)


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(etl_pipeline, "etl_pipeline.yaml")
