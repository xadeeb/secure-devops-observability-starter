
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from app.main import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200


def test_echo(client):
    response = client.post("/echo", json={"message": "hello"})
    assert response.status_code == 200
