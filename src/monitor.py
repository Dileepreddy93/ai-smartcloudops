from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import json


def get_latest_metrics(file_path: str | Path) -> Dict[str, Any]:
    """Load metrics from a JSON file and return them as a dictionary.

    Parameters
    ----------
    file_path: str | Path
        Path to the JSON file containing metrics.

    Returns
    -------
    Dict[str, Any]
        Dictionary parsed from the JSON file.
    """

    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)
    return data


