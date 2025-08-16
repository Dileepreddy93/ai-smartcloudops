from __future__ import annotations

from pathlib import Path
from typing import Dict
import json


def fetch_metrics(file_path: str | Path, live: bool = False) -> Dict[str, float]:
    """Create synthetic metrics JSON (Phase 1).

    Parameters
    ----------
    file_path: str | Path
        Output path for metrics JSON.
    live: bool
        Reserved for future live mode (AWS/EC2). Ignored in Phase 1.

    Returns
    -------
    Dict[str, float]
        Dictionary with at least keys `cpu` and `memory`.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    metrics: Dict[str, float] = {"cpu": 10.0, "memory": 20.0}
    path.write_text(json.dumps(metrics), encoding="utf-8")
    return metrics


