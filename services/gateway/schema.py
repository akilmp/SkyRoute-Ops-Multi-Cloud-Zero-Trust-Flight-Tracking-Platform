from __future__ import annotations
from datetime import datetime
from typing import List

import strawberry

from .db import query_clickhouse, query_postgis


@strawberry.type
class FlightRoute:
    id: int
    callsign: str
    origin: str
    destination: str


@strawberry.type
class NOTAM:
    id: int
    message: str
    effective_date: datetime


@strawberry.type
class Query:
    @strawberry.field(name="flightRoutes")
    def flight_routes(self) -> List[FlightRoute]:
        """Return flight routes from ClickHouse."""
        rows = query_clickhouse(
            "SELECT id, callsign, origin, destination FROM flight_routes"
        )
        return [
            FlightRoute(id=row[0], callsign=row[1], origin=row[2], destination=row[3])
            for row in rows
        ]

    @strawberry.field
    async def notams(self) -> List[NOTAM]:
        """Return NOTAM data from PostGIS."""
        rows = await query_postgis(
            "SELECT id, message, effective_date FROM notams"
        )
        return [
            NOTAM(id=row["id"], message=row["message"], effective_date=row["effective_date"])
            for row in rows
        ]


schema = strawberry.Schema(query=Query)
