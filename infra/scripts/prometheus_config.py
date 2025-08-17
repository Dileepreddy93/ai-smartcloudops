"""Generate Prometheus file_sd targets from config/aws_targets.json.

This helper reads `config/aws_targets.json` which should contain keys
`app` and `node_exporter` listing host:port entries. It writes a
Prometheus file_sd JSON at `infra/prometheus/file_sd/app-and-node.json`.

Usage:
    python -m infra.scripts.prometheus_config \
        --config config/aws_targets.json \
        --out infra/prometheus/file_sd/app-and-node.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def _load_targets(config_path: Path) -> Dict[str, List[str]]:
    if not config_path.exists():
        return {"app": [], "node_exporter": []}
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return {
        "app": list(data.get("app", [])) or [],
        "node_exporter": list(data.get("node_exporter", [])) or [],
    }


def generate_file_sd(config_path: Path, output_path: Path) -> None:
    """Generate file_sd JSON for Prometheus based on aws_targets.json."""
    targets = _load_targets(config_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {"labels": {"job": "app"}, "targets": targets["app"]},
        {"labels": {"job": "node"}, "targets": targets["node_exporter"]},
    ]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Prometheus file_sd from aws_targets.json")
    parser.add_argument("--config", type=Path, default=Path("config/aws_targets.json"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("infra/prometheus/file_sd/app-and-node.json"),
    )
    args = parser.parse_args()
    generate_file_sd(args.config, args.out)


if __name__ == "__main__":
    main()


