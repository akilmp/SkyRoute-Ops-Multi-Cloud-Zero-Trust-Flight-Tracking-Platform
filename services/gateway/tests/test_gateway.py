from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from jose import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from services.gateway.main import app


def _create_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    priv_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    pub_pem = public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return priv_pem, pub_pem


def _create_token(private_key: str) -> str:
    return jwt.encode({"sub": "tester", "aud": "gateway-client"}, private_key, algorithm="RS256")


def test_graphql_queries(monkeypatch):
    priv, pub = _create_keys()
    monkeypatch.setenv("KEYCLOAK_PUBLIC_KEY", pub)
    monkeypatch.setenv("KEYCLOAK_CLIENT_ID", "gateway-client")

    token = _create_token(priv)
    client = TestClient(app)

    with patch("services.gateway.schema.query_clickhouse") as mock_ch, \
         patch("services.gateway.schema.query_postgis") as mock_pg:
        mock_ch.return_value = [(1, "AB123", "JFK", "LAX")]
        mock_pg.return_value = [
            {"id": 1, "message": "Runway closed", "effective_date": datetime(2024, 1, 1)}
        ]
        query = "{ flightRoutes { id callsign origin destination } notams { id message } }"
        response = client.post("/graphql", json={"query": query}, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["flightRoutes"][0]["callsign"] == "AB123"
        assert data["notams"][0]["message"] == "Runway closed"


def test_authentication_required():
    client = TestClient(app)
    query = "{ flightRoutes { id } }"
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 403
