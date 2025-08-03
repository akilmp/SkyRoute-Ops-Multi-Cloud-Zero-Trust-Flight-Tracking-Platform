CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    path GEOGRAPHY(LINESTRING, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE airports (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    elevation INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE notams (
    id SERIAL PRIMARY KEY,
    route_id INTEGER REFERENCES routes(id),
    message TEXT NOT NULL,
    effective_from TIMESTAMPTZ NOT NULL,
    effective_to TIMESTAMPTZ NOT NULL,
    area GEOGRAPHY(POLYGON, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
