from __future__ import annotations

from typing import Any
import time


def remediate_action(issue: str) -> str:
    """Return a remediation message for the given issue.

    Parameters
    ----------
    issue: str
        A short description of the issue that needs remediation.

    Returns
    -------
    str
        A simple, deterministic remediation message.
    """
    return f"Action taken for {issue}"


def log_remediation_to_s3(action: str, bucket_name: str, s3_client: Any) -> str:
    """Log the provided remediation action string to S3.

    The S3 object key is generated using epoch milliseconds for uniqueness under
    the `remediations/` prefix.

    Parameters
    ----------
    action: str
        The remediation message to store.
    bucket_name: str
        Target S3 bucket name.
    s3_client: Any
        A boto3 S3 client (or a compatible mocked client in tests).

    Returns
    -------
    str
        The S3 object key used for the upload.
    """
    object_key = f"remediations/action-{int(time.time() * 1000)}.txt"
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=action.encode("utf-8"))
    return object_key


