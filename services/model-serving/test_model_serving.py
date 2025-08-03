import pathlib
import sys

from fastapi.testclient import TestClient

sys.path.append(str(pathlib.Path(__file__).parent))

import app

client = TestClient(app.app)


def test_predict():
    response = client.post("/predict", json={"instances": [1, 2]})
    assert response.status_code == 200
    assert response.json()["predictions"] == [2, 4]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
