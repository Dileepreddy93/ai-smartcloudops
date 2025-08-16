import json
from pathlib import Path
import pytest

pytestmark = pytest.mark.phase2

from monitor import get_latest_metrics
from data_ingestion import fetch_metrics


def test_get_latest_metrics_returns_dict_with_keys(tmp_path: Path) -> None:
    metrics_path = tmp_path / "metrics.json"
    expected = fetch_metrics(metrics_path)

    result = get_latest_metrics(metrics_path)
    assert isinstance(result, dict)
    assert "cpu" in result and "memory" in result
    assert result == expected


