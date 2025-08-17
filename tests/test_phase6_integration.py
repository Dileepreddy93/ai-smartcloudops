import json
from pathlib import Path
import pytest

pytestmark = pytest.mark.phase6

from main import run_pipeline


def test_end_to_end_pipeline(tmp_path: Path) -> None:
    metrics_path = tmp_path / "metrics.json"
    result = run_pipeline(metrics_path)

    assert metrics_path.is_file(), "metrics.json should be written by ingestion"
    assert result["written_metrics"] == result["latest_metrics"]
    assert "cpu" in result["latest_metrics"] and "memory" in result["latest_metrics"]
    # With default synthetic values, anomaly should be False
    assert result["anomaly"] is False


