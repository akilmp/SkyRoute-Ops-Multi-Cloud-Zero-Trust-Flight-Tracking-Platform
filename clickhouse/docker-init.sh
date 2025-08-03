#!/bin/bash
# Simple init script to load schema into ClickHouse when the container starts.
set -e
clickhouse-client --queries-file /docker-entrypoint-initdb.d/flights.sql
clickhouse-client --queries-file /docker-entrypoint-initdb.d/heatmap_tiles_mv.sql
