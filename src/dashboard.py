from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json

from flask import Flask, jsonify, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Gauge,
    generate_latest,
)

from anomaly_detection import detect_anomaly


app = Flask(__name__)


def _load_metrics_default() -> Dict[str, Any]:
    """Load metrics from the default Phase 1/2 path `data/metrics.json` if present."""
    path = Path("data/metrics.json")
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


@app.get("/health")
def health() -> Response:
    return jsonify({"status": "ok"})


@app.get("/")
def index() -> Response:
    metrics = _load_metrics_default()
    anomaly = False
    if metrics:
        anomaly = detect_anomaly(metrics)
    return jsonify({"metrics": metrics, "anomaly": anomaly})


@app.get("/metrics")
def metrics_endpoint() -> Response:
    # Expose at least one metric in a local registry so output contains HELP/TYPE
    registry = CollectorRegistry()
    app_info = Gauge("app_info", "Application info gauge", registry=registry)
    app_info.set(1)
    output = generate_latest(registry)
    return Response(output, mimetype=CONTENT_TYPE_LATEST)


@app.get("/aws-health")
def aws_health() -> Response:
    """Return a simple structure sourced from `config/aws_targets.json` if present."""
    cfg_path = Path("config/aws_targets.json")
    if not cfg_path.exists():
        return jsonify({"app": [], "node_exporter": []})
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        app_targets = data.get("app", [])
        node_targets = data.get("node_exporter", [])
        return jsonify({"app": app_targets, "node_exporter": node_targets})
    except Exception:
        return jsonify({"app": [], "node_exporter": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


