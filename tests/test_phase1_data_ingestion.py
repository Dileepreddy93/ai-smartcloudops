import json
from pathlib import Path
import pytest

pytestmark = pytest.mark.phase1

from data_ingestion import fetch_metrics


def test_fetch_metrics_creates_file_and_contains_keys(tmp_path: Path) -> None:
    target = tmp_path / "metrics.json"
    result = fetch_metrics(target)
    assert target.is_file()

    on_disk = json.loads(target.read_text(encoding="utf-8"))
    for data in (result, on_disk):
        assert "cpu" in data and "memory" in data


