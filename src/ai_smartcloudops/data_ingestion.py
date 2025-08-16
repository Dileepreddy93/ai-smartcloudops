from __future__ import annotations

from pathlib import Path
from typing import Dict
import json


def fetch_metrics(file_path: str | Path) -> Dict[str, float]:
    """Simulate fetching cloud metrics and save them as JSON.

    This function creates a simple metrics payload containing `cpu` and `memory`
    keys as floating-point percentages, writes it to the provided `file_path`,
    and returns the metrics dictionary.

    Parameters
    ----------
    file_path: str | Path
        Destination path to write the `metrics.json` file.

    Returns
    -------
    Dict[str, float]
        A dictionary with at least the keys `cpu` and `memory`.
    """

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Deterministic example values; adjust as needed in later phases.
    metrics: Dict[str, float] = {
        "cpu": 42.0,
        "memory": 73.0,
    }

    with path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f)

    return metrics


