import base64
import json
import os
from typing import Any, Dict

import boto3
import requests
from flask import Flask, Request, Response, request
from google.cloud import pubsub_v1

app = Flask(__name__)

# Lazily initialise clients to simplify unit testing
_kinesis_client = None
_pubsub_client = None

KINESIS_STREAM = os.getenv("KINESIS_STREAM")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")


def get_kinesis_client():
    global _kinesis_client
    if _kinesis_client is None and KINESIS_STREAM:
        _kinesis_client = boto3.client("kinesis")
    return _kinesis_client


def get_pubsub_client():
    global _pubsub_client
    if _pubsub_client is None and PUBSUB_TOPIC:
        _pubsub_client = pubsub_v1.PublisherClient()
    return _pubsub_client


def fetch_metar(icao: str) -> Dict[str, Any]:
    """Retrieve METAR weather data from NOAA for a given ICAO code."""
    url = (
        "https://aviationweather.gov/adds/dataserver_current/httpparam"
        f"?dataSource=metars&requestType=retrieve&format=JSON&stationString={icao}&hoursBeforeNow=1"
    )
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    metars = data.get("data", {}).get("METAR", [])
    return metars[0] if metars else {}


def enrich_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Add weather information to the event if an ICAO code is present."""
    icao = event.get("icao") or event.get("airport") or event.get("station")
    if icao:
        event["weather"] = fetch_metar(icao)
    return event


def publish_event(event: Dict[str, Any]) -> None:
    payload = json.dumps(event).encode("utf-8")
    if KINESIS_STREAM:
        client = get_kinesis_client()
        client.put_record(
            StreamName=KINESIS_STREAM,
            Data=payload,
            PartitionKey=event.get("icao", "default"),
        )
    if PUBSUB_TOPIC:
        client = get_pubsub_client()
        client.publish(PUBSUB_TOPIC, payload)


@app.post("/pubsub/push")
def pubsub_push() -> Response:
    envelope = request.get_json() or {}
    message = envelope.get("message", {})
    data = message.get("data", "")
    if not data:
        return ("Bad Request", 400)
    event = json.loads(base64.b64decode(data).decode("utf-8"))
    enriched = enrich_event(event)
    publish_event(enriched)
    return ("", 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
