from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from data_ingestion import fetch_metrics
from monitor import get_latest_metrics
from anomaly_detection import detect_anomaly
from auto_remediate import remediate_action, log_remediation_to_s3


def run_pipeline(metrics_path: str | Path, s3_client: Any | None = None, bucket_name: str | None = None) -> Dict[str, Any]:
    """Run the end-to-end pipeline: ingest → monitor → analyze → (optional) remediate.

    Parameters
    ----------
    metrics_path: str | Path
        Location to write/read the metrics JSON file.
    s3_client: Any | None
        Optional S3 client for logging remediation actions.
    bucket_name: str | None
        Optional bucket name for logging remediation actions.

    Returns
    -------
    Dict[str, Any]
        Summary of the run, including metrics and whether anomaly/remediation occurred.
    """
    path = Path(metrics_path)

    # Ingest (Phase 1)
    written_metrics = fetch_metrics(path)

    # Monitor (Phase 2)
    latest_metrics = get_latest_metrics(path)

    # Analyze (Phase 3)
    anomaly = detect_anomaly(latest_metrics)

    remediation_action: str | None = None
    s3_key: str | None = None

    if anomaly:
        # Remediate (Phase 4)
        remediation_action = remediate_action("Anomaly detected")
        if s3_client is not None and bucket_name:
            s3_key = log_remediation_to_s3(remediation_action, bucket_name=bucket_name, s3_client=s3_client)

    return {
        "written_metrics": written_metrics,
        "latest_metrics": latest_metrics,
        "anomaly": anomaly,
        "remediation_action": remediation_action,
        "remediation_s3_key": s3_key,
    }


if __name__ == "__main__":
    # Example local run target
    result = run_pipeline(Path("data/metrics.json"))
    print(result)


