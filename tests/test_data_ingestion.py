from pathlib import Path
import json

from ai_smartcloudops.data_ingestion import fetch_metrics


def test_fetch_metrics_creates_file_and_contains_keys(tmp_path: Path) -> None:
    """Phase 1: fetch_metrics writes JSON with cpu and memory keys."""

    target_file = tmp_path / "metrics.json"

    result = fetch_metrics(target_file)

    # File exists
    assert target_file.is_file(), "metrics.json was not created"

    # JSON content has cpu and memory
    on_disk = json.loads(target_file.read_text(encoding="utf-8"))
    for data in (result, on_disk):
        assert "cpu" in data and "memory" in data, "Missing cpu or memory keys"


