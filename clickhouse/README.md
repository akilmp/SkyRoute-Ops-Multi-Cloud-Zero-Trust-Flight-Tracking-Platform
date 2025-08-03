# ClickHouse Schema for Flight Heatmap

This directory contains SQL definitions to store flight telemetry and
pre-aggregate XYZ tiles for Grafana heatmaps.

## Files

- `flights.sql` – creates the `flights` table using `MergeTree` partitioned
  by `event_date`.
- `heatmap_tiles_mv.sql` – creates the `heatmap_tiles` table and accompanying
  materialized view that turns latitude and longitude into XYZ tiles across
  zoom levels 0–15.
- `docker-init.sh` – helper script to load the SQL files when running in a
  Docker container.

## Docker usage

Mount the SQL files (and optional `docker-init.sh`) into the ClickHouse
container's `/docker-entrypoint-initdb.d` directory:

```bash
docker run -v $(pwd)/clickhouse:/docker-entrypoint-initdb.d \
  clickhouse/clickhouse-server:latest
```

The official image automatically executes `*.sql` files on first start. If you
need explicit control, use the provided `docker-init.sh` as an entrypoint.

## Helm integration

Create a ConfigMap that exposes the SQL files and mount it to
`/docker-entrypoint-initdb.d` in your ClickHouse pod. Example snippet:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: clickhouse-init-sql
  namespace: default
data:
  flights.sql: |
    {{ .Files.Get "clickhouse/flights.sql" | indent 4 }}
  heatmap_tiles_mv.sql: |
    {{ .Files.Get "clickhouse/heatmap_tiles_mv.sql" | indent 4 }}
```

Mount the ConfigMap in your StatefulSet or Pod spec so ClickHouse initializes
with the required schema.
