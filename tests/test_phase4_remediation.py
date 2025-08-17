import pytest

pytestmark = pytest.mark.phase4

from auto_remediate import remediate_action, log_remediation_to_s3


def test_remediate_action_message():
    issue = "High CPU usage"
    assert remediate_action(issue) == f"Action taken for {issue}"


class _FakeS3Client:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def put_object(self, Bucket: str, Key: str, Body: bytes) -> None:  # noqa: N803
        self.calls.append({"Bucket": Bucket, "Key": Key, "Body": Body})


def test_log_remediation_to_s3_creates_object():
    action = "Action taken for High CPU usage"
    fake = _FakeS3Client()

    key = log_remediation_to_s3(action, bucket_name="test-bucket", s3_client=fake)
    assert key.startswith("remediations/") and key.endswith(".txt")
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call["Bucket"] == "test-bucket"
    assert call["Key"] == key
    assert call["Body"].decode("utf-8") == action


