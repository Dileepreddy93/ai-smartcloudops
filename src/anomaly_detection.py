from __future__ import annotations

from typing import Dict, Any
import json
import time


def detect_anomaly(metrics: Dict[str, Any]) -> bool:
    """Return True if metrics indicate an anomaly.

    An anomaly is defined as any of the following being strictly greater than 90:
    - metrics["cpu"]
    - metrics["memory"]

    Parameters
    ----------
    metrics: Dict[str, Any]
        Metrics dictionary expected to contain numeric keys `cpu` and `memory`.

    Returns
    -------
    bool
        True if an anomaly is detected, otherwise False.
    """
    cpu_value = float(metrics.get("cpu", 0))
    mem_value = float(metrics.get("memory", 0))
    return cpu_value > 90 or mem_value > 90


def log_anomaly_to_s3(metrics: Dict[str, Any], bucket_name: str, s3_client: Any) -> str:
    """Log the provided metrics payload to S3 as a JSON object.

    The S3 object key is generated using the current epoch milliseconds for uniqueness.

    Parameters
    ----------
    metrics: Dict[str, Any]
        Metrics to serialize as JSON.
    bucket_name: str
        Target S3 bucket name.
    s3_client: Any
        A boto3 S3 client (or a compatible mocked client in tests).

    Returns
    -------
    str
        The S3 object key used for the upload.
    """
    object_key = f"anomalies/metrics-{int(time.time() * 1000)}.json"
    body = json.dumps(metrics).encode("utf-8")
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=body)
    return object_key


