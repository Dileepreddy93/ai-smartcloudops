import json
import pytest

pytestmark = pytest.mark.phase3

from anomaly_detection import detect_anomaly, log_anomaly_to_s3


def test_detect_anomaly_normal():
    metrics = {"cpu": 50, "memory": 60}
    assert detect_anomaly(metrics) is False


def test_detect_anomaly_anomalous_cpu():
    metrics = {"cpu": 95, "memory": 60}
    assert detect_anomaly(metrics) is True


def test_detect_anomaly_anomalous_memory():
    metrics = {"cpu": 10, "memory": 99}
    assert detect_anomaly(metrics) is True


class _FakeS3Client:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def put_object(self, Bucket: str, Key: str, Body: bytes) -> None:  # noqa: N803 (AWS casing)
        # Record the call for assertions
        self.calls.append({"Bucket": Bucket, "Key": Key, "Body": Body})


def test_log_anomaly_to_s3_uses_expected_key_and_body():
    metrics = {"cpu": 99, "memory": 12}
    fake = _FakeS3Client()

    key = log_anomaly_to_s3(metrics, bucket_name="test-bucket", s3_client=fake)

    assert key.startswith("anomalies/"), "Key should be under anomalies/ prefix"
    assert key.endswith(".json")
    assert len(fake.calls) == 1

    call = fake.calls[0]
    assert call["Bucket"] == "test-bucket"
    assert call["Key"] == key
    assert call["Body"] == json.dumps(metrics).encode("utf-8")


