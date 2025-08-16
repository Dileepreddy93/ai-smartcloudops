from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def get_latest_metrics(file_path: str | Path, live: bool = False) -> Dict[str, Any]:
    """Load metrics from a JSON file and return them as a dictionary.

    Parameters
    ----------
    file_path: str | Path
        Path to the JSON file containing metrics.
    live: bool
        Reserved for future live mode. Ignored in Phase 2.

    Returns
    -------
    Dict[str, Any]
        Dictionary parsed from the JSON file.
    """
    path = Path(file_path)
    return json.loads(path.read_text(encoding="utf-8"))


