import sys
from pathlib import Path

sys.path.insert(0, str(Path(file).resolve().parents[1]))

from app.main import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_home_returns_service_details(client):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["service"] == "secure-devops-starter"
    assert payload["status"] == "ok"


def test_health_is_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"


def test_echo_accepts_short_message(client):
    response = client.get("/echo?message=hello")
    assert response.status_code == 200
    assert response.get_json() == {"message": "hello"}


def test_echo_rejects_long_message(client):
    response = client.get("/echo", query_string={"message": "x" * 201})
    assert response.status_code == 400


def test_metrics_exposes_prometheus_text(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"demo_service_up 1" in response.data
