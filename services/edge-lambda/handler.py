import base64
import json
import os
from typing import Any, Dict, List

try:
    import boto3  # type: ignore
except Exception:  # pragma: no cover
    boto3 = None

try:
    from google.cloud import pubsub_v1  # type: ignore
except Exception:  # pragma: no cover
    pubsub_v1 = None

_kinesis_client = None
_pubsub_client = None

def parse_mode_s(raw: str) -> Dict[str, Any]:
    """Very small Mode-S frame parser returning basic information."""
    frame = raw.strip().upper()
    if len(frame) < 2:
        return {"raw": frame}
    try:
        first_byte = int(frame[0:2], 16)
        df = first_byte >> 3  # Downlink Format is first 5 bits
    except ValueError:
        df = None
    return {"raw": frame, "df": df}

def _send_kinesis(stream: str, payload: Dict[str, Any]) -> None:
    global _kinesis_client
    if boto3 is None:
        raise RuntimeError("boto3 not available")
    if _kinesis_client is None:
        _kinesis_client = boto3.client("kinesis")
    _kinesis_client.put_record(
        StreamName=stream,
        Data=json.dumps(payload).encode("utf-8"),
        PartitionKey="mode-s",
    )

def _send_pubsub(topic: str, payload: Dict[str, Any]) -> None:
    global _pubsub_client
    if pubsub_v1 is None:
        raise RuntimeError("google-cloud-pubsub not available")
    if _pubsub_client is None:
        _pubsub_client = pubsub_v1.PublisherClient()
    _pubsub_client.publish(topic, json.dumps(payload).encode("utf-8"))

def handle(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda entrypoint: parse Mode-S messages and forward to stream."""
    provider = os.getenv("TARGET_CLOUD", "aws").lower()
    stream = os.getenv("KINESIS_STREAM", "")
    topic = os.getenv("PUBSUB_TOPIC", "")

    raw_messages: List[str] = []
    if isinstance(event, dict) and "messages" in event:
        raw_messages = event["messages"]
    elif isinstance(event, dict) and "Records" in event:
        for record in event["Records"]:
            data = record.get("kinesis", {}).get("data")
            if data:
                raw_messages.append(base64.b64decode(data).decode("utf-8"))
    elif isinstance(event, dict) and "body" in event:
        raw_messages = [event["body"]]

    results = []
    for raw in raw_messages:
        parsed = parse_mode_s(raw)
        if provider == "aws" and stream:
            _send_kinesis(stream, parsed)
        elif provider == "gcp" and topic:
            _send_pubsub(topic, parsed)
        results.append(parsed)

    return {"processed": len(results)}

