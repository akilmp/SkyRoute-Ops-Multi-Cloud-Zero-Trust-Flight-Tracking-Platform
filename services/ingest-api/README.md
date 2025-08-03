# Ingest API

## Simulator

The simulator generates synthetic 112-bit Mode-S messages and publishes them to a configured stream service.

### Usage

```
# AWS Kinesis example
CLOUD_PROVIDER=AWS KINESIS_STREAM=flights go run ./cmd/simulator -rate 10 -random 0.5

# GCP Pub/Sub example
CLOUD_PROVIDER=GCP GCP_PROJECT=my-project PUBSUB_TOPIC=flights go run ./cmd/simulator -rate 10 -random 0.5
```

Flags:

- `-rate`   messages per second
- `-random` randomness factor (0-1) applied as jitter to the send interval

Environment variables:

- `CLOUD_PROVIDER` (`AWS` or `GCP`)
- `KINESIS_STREAM` (when using AWS)
- `GCP_PROJECT` and `PUBSUB_TOPIC` (when using GCP)
