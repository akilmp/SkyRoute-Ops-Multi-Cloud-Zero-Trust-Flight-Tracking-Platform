-- flights.sql
-- Defines the main table for flight positions.
-- The table is partitioned by event_date for efficient retention
-- and uses MergeTree for fast time-series queries.

CREATE TABLE IF NOT EXISTS flights
(
    `timestamp` DateTime,
    `event_date` Date MATERIALIZED toDate(`timestamp`),
    `flight_id` String,
    `callsign` String,
    `lat` Float64,
    `lon` Float64,
    `altitude` Float64,
    `speed` Float64,
    `heading` Float64
)
ENGINE = MergeTree
PARTITION BY event_date
ORDER BY (flight_id, timestamp);
