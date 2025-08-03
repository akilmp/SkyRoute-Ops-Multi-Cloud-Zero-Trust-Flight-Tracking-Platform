"""Database helpers for ClickHouse and PostGIS."""
import os
from typing import Any, Iterable

from clickhouse_driver import Client as ClickHouseClient
import asyncpg


def query_clickhouse(query: str) -> Iterable[Iterable[Any]]:
    """Execute a read-only query against ClickHouse."""
    client = ClickHouseClient(host=os.getenv("CLICKHOUSE_HOST", "localhost"))
    return client.execute(query)


async def query_postgis(query: str) -> Iterable[asyncpg.Record]:
    """Execute a query against a PostGIS (PostgreSQL) database."""
    conn = await asyncpg.connect(
        host=os.getenv("POSTGIS_HOST", "localhost"),
        user=os.getenv("POSTGIS_USER", "postgres"),
        password=os.getenv("POSTGIS_PASSWORD", "postgres"),
        database=os.getenv("POSTGIS_DB", "postgres"),
    )
    try:
        return await conn.fetch(query)
    finally:
        await conn.close()
