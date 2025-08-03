import base64
import json
import pathlib
import sys
from unittest.mock import MagicMock

import pytest

sys.path.append(str(pathlib.Path(__file__).parent))
import main


def test_enrich_event_adds_weather(monkeypatch):
    monkeypatch.setattr(main, "fetch_metar", lambda code: {"temp_c": 20})
    event = {"icao": "KSFO"}
    enriched = main.enrich_event(event)
    assert enriched["weather"] == {"temp_c": 20}


def test_publish_event(monkeypatch):
    kinesis = MagicMock()
    pubsub = MagicMock()
    monkeypatch.setattr(main, "KINESIS_STREAM", "test-stream")
    monkeypatch.setattr(main, "PUBSUB_TOPIC", "projects/x/topics/y")
    monkeypatch.setattr(main, "get_kinesis_client", lambda: kinesis)
    monkeypatch.setattr(main, "get_pubsub_client", lambda: pubsub)
    main.publish_event({"icao": "KSFO"})
    assert kinesis.put_record.called
    assert pubsub.publish.called


def test_pubsub_push(monkeypatch):
    monkeypatch.setattr(main, "enrich_event", lambda e: e)
    pub_mock = MagicMock()
    monkeypatch.setattr(main, "publish_event", pub_mock)
    client = main.app.test_client()
    event = {"icao": "KSFO"}
    data = base64.b64encode(json.dumps(event).encode("utf-8")).decode("utf-8")
    res = client.post("/pubsub/push", json={"message": {"data": data}})
    assert res.status_code == 204
    pub_mock.assert_called_once_with(event)
