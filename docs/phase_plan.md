

# 🚂 ai-smartcloudops — Phase Plan (AWS Free Tier + Cursor Rules + Live Metrics)

This document is **authoritative**. Follow exactly to ensure:

* Local pytest passes at every step.
* Free Tier AWS setup is compatible.
* Cursor works safely.
* Optional live metrics integration.

---

## TL;DR — How to Run Tests

```bash
# Run all phases locally (synthetic metrics)
pytest -q -m "not aws_live"

# Run selected phases
pytest -q -m "phase0 or phase1 or phase2"

# Run AWS live metrics checks (optional, requires env)
AWS_LIVE=1 pytest -q -m "aws_live"
```

> AWS calls are **mocked by default**. Live checks only run if `AWS_LIVE=1`.

---

## Minimal Cursor Rules (`.cursor/rules.md`)

```markdown
# Cursor Rules for ai-smartcloudops

1. Do not overwrite unrelated files.
2. Always follow the defined phase plan (Phase 0 → Phase 7).
3. Write clean, modular, and testable code.
4. Keep all tests in `tests/` directory.
5. Use `pytest` for testing.
6. Document manual vs Cursor tasks clearly in `docs/`.
```

> No extra lines, emojis, headings.

**Detailed rules:** keep in `docs/cursor_rules.md`.

---

## Repository Layout

```
ai-smartcloudops/
├── src/
│   ├── data_ingestion.py
│   ├── monitor.py
│   ├── anomaly_detection.py
│   ├── auto_remediate.py
│   ├── dashboard.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_phase0_setup.py
│   ├── test_phase1_data_ingestion.py
│   ├── test_phase2_monitoring.py
│   ├── test_phase3_anomaly.py
│   ├── test_phase4_remediation.py
│   ├── test_phase5_dashboard.py
│   ├── test_phase6_integration.py
│   └── test_aws_glue.py           # optional live AWS checks
├── config/
│   └── aws_targets.json           # EC2 IPs/ports
├── docs/
│   ├── cursor_rules.md
│   ├── aws_setup.md
│   └── phase_plan.md
├── infra/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── file_sd/app-and-node.json
│   └── scripts/
│       ├── collect_diag.sh
│       ├── prometheus_config.py
│       └── node_exporter_compose.yml
├── requirements.txt
├── README.md
└── .cursor/
    └── rules.md
```

---

## Phase 0 — Setup & Architecture (Local + AWS Free Tier)

**Manual Tasks:**

* Create repo & folder structure.
* Free Tier AWS setup:

  * 2× t2.micro EC2: App-EC2 (Flask) & Mon-EC2 (Prometheus + Grafana)
  * S3 bucket for logs: `ai-smartcloudops-logs`
* Assign Elastic IPs → store in `config/aws_targets.json`.

**Cursor Tasks:**

* `tests/test_phase0_setup.py`: folder structure, `.cursor/rules.md`, `requirements.txt`.
* `tests/conftest.py`: markers `phase0..phase7`, `aws_live`.

**Pytest:**

* `pytest -q -m "phase0"` passes locally.

---

## Phase 1 — Data Ingestion

**Manual Tasks:**

* Decide local storage: `metrics.json`.

**Cursor Tasks:**

* `fetch_metrics(file_path: str, live: bool = False)`

  * `live=False`: synthetic metrics
  * `live=True`: Free Tier EC2 metrics via CloudWatch API or SSH

* `tests/test_phase1_data_ingestion.py`: validate JSON creation & keys.

**Pytest:** synthetic mode default; AWS live optional.

---

## Phase 2 — Monitoring Core

**Manual Tasks:**

* Prometheus file-SD: `infra/prometheus/file_sd/app-and-node.json` from `config/aws_targets.json`.
* Install Prometheus + Grafana on Mon-EC2 (document in `docs/aws_setup.md`).

**Cursor Tasks:**

* `get_latest_metrics(file_path: str, live: bool = False)` → returns metrics.
* `infra/scripts/prometheus_config.py` → regenerates file-SD JSON.
* `tests/test_phase2_monitoring.py`: verify function & config JSON.

**Pytest:** local synthetic metrics by default.

---

## Phase 3 — AI Analysis

**Cursor Tasks:**

* `detect_anomaly(metrics: dict) -> bool` (>90% CPU/mem).
* `log_anomaly_to_s3(metrics, bucket, client)` → mockable for tests.
* `tests/test_phase3_anomaly.py`: normal/anomalous cases; mocked S3.

**Pytest:** synthetic & mocked AWS.

---

## Phase 4 — Automation / Remediation

**Cursor Tasks:**

* `remediate_action(issue: str) -> str`
* `log_remediation_to_s3(action: str, bucket, client)`
* `tests/test_phase4_remediation.py`: assert return & mocked S3 call.

**Pytest:** local.

---

## Phase 5 — Dashboard (Flask)

**Cursor Tasks:**

* Flask endpoints:

  * `/` → latest metrics (synthetic or live) + anomaly flag
  * `/health` → `{ "status": "ok" }`
  * `/metrics` → Prometheus format
  * `/aws-health` → structure from `config/aws_targets.json`
* `tests/test_phase5_dashboard.py`: validate all endpoints.

---

## Phase 6 — Final Integration

**Cursor Tasks:**

* `main.py` orchestrates: fetch → monitor → detect → remediate → log to S3.
* `tests/test_phase6_integration.py`: full flow with temp dirs & mocks.

---

## Phase 7 — Optional AWS Live Checks

**Cursor Tasks:**

* `tests/test_aws_glue.py`

  * Prometheus `/ -/ready`
  * Grafana `/api/health`
  * Node Exporter metrics
  * Real EC2 metrics with `live=True` mode

**Manual Tasks:**

* Ensure Node Exporter running on both EC2s.
* File-SD correct in Prometheus.

**Pytest:** gated by `AWS_LIVE=1`.

---

## Pytest Strategy — Many Phases at Once

* Each test uses `@pytest.mark.phaseN`.
* AWS calls **mocked** unless `AWS_LIVE=1`.
* Temp dirs & mocks ensure **idempotent tests**.
* Run multiple phases like a train/coach example.

---

## Requirements (minimal)

```
flask
scikit-learn
boto3
prometheus-client
requests
pytest
moto           # for AWS mocks
```

---

✅ **Outcome if all phases completed:**

* Flask dashboard `/`, `/health`, `/metrics`, `/aws-health`
* Synthetic & optional real metrics ingestion
* Anomaly detection & remediation flow
* Prometheus + Grafana running on Mon-EC2
* Node Exporter metrics on both EC2s
* S3 logging (mocked in tests, real in Free Tier)
* Full pytest green (`phase0..phase6`), optional `AWS_LIVE=1` tests

