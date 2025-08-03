-- heatmap_tiles_mv.sql
-- Materialized view generating XYZ tile counts for Grafana heatmaps.

-- Target table to store aggregated tile counts.
CREATE TABLE IF NOT EXISTS heatmap_tiles
(
    `event_date` Date,
    `z` UInt8,
    `x` UInt32,
    `y` UInt32,
    `hits` UInt32
)
ENGINE = SummingMergeTree
PARTITION BY event_date
ORDER BY (z, x, y);

-- Materialized view populating the tile table from flight positions.
CREATE MATERIALIZED VIEW IF NOT EXISTS heatmap_tiles_mv
TO heatmap_tiles
AS
SELECT
    event_date,
    z,
    floor((lon + 180) / 360 * pow(2, z)) AS x,
    floor((1 - log(tan(radians(lat)) + 1 / cos(radians(lat))) / pi()) / 2 * pow(2, z)) AS y,
    count() AS hits
FROM flights
ARRAY JOIN range(0, 16) AS z
GROUP BY event_date, z, x, y;
