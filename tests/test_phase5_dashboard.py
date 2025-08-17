import pytest

pytestmark = pytest.mark.phase5

from dashboard import app


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as c:
        yield c


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_metrics_endpoint(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"# HELP" in resp.data


def test_aws_health_endpoint(client):
    resp = client.get("/aws-health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "app" in data and "node_exporter" in data


