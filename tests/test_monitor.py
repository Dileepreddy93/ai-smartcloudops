from src.monitor import get_latest_metrics


def test_get_latest_metrics(tmp_path):
    """Check that get_latest_metrics loads data from JSON"""
    file = tmp_path / "metrics.json"
    file.write_text('{"cpu":50,"memory":60}')
    metrics = get_latest_metrics(str(file))

    assert isinstance(metrics, dict)
    assert "cpu" in metrics
    assert "memory" in metrics


