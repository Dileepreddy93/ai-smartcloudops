import json
import os
from pathlib import Path
from typing import Iterable

import pytest
import requests

pytestmark = [pytest.mark.phase7, pytest.mark.aws_live]


def _load_targets(kind: str) -> Iterable[str]:
    cfg_path = Path("config/aws_targets.json")
    if not cfg_path.exists():
        return []
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    return data.get(kind, [])


def _http_ok(url: str, timeout: float = 2.0) -> bool:
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code == 200
    except Exception:
        return False


def test_node_exporter_metrics_reachable():
    for target in _load_targets("node_exporter"):
        # Node exporter root exposes text metrics
        assert _http_ok(f"http://{target}/metrics"), f"Node Exporter not reachable: {target}"


def test_app_health_when_deployed():
    for target in _load_targets("app"):
        assert _http_ok(f"http://{target}/health"), f"App health not reachable: {target}"


def test_prometheus_ready_if_configured():
    prom = os.environ.get("PROMETHEUS_URL")  # e.g., http://MON_EC2_PUBLIC_IP:9090
    if not prom:
        pytest.skip("PROMETHEUS_URL not set")
    assert _http_ok(f"{prom}/-/ready"), "Prometheus not ready"


def test_grafana_health_if_configured():
    graf = os.environ.get("GRAFANA_URL")  # e.g., http://MON_EC2_PUBLIC_IP:3000
    if not graf:
        pytest.skip("GRAFANA_URL not set")
    assert _http_ok(f"{graf}/api/health"), "Grafana health check failed"


