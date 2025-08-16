# ai-smartcloudops

AI-powered Smart Cloud Operations project (real-time monitoring, anomaly detection, auto-remediation).

### Phase 0 — Setup & Architecture ✅
- Repository scaffolded with `src/`, `tests/`, `requirements.txt`, `README.md`, `.gitignore`, and `.cursor/rules.md`.
- Test scaffolding added to validate structure and environment.
- Cursor rules established in `.cursor/rules.md` to enforce workflow and quality.

### Phase 1 — Data Ingestion ✅
- Implemented `ai_smartcloudops.data_ingestion.fetch_metrics(file_path)` to write a JSON file with `cpu` and `memory` keys.
- Tests added:
  - `tests/test_phase1_data_ingestion.py`
  - `tests/test_data_ingestion.py`

### Phase 2 — Monitoring Core ✅
- Implemented `src/monitor.py` with `get_latest_metrics(file_path)` to load metrics from JSON and return a dictionary.
- Test added:
  - `tests/test_monitor.py`

### Next Phase — Phase 3 (AI Anomaly Detection)
- Add `src/anomaly_detection.py` with `detect_anomaly(metrics)` to detect anomalies (e.g., `cpu` or `memory` > 90%).
- Add tests to validate both normal and anomalous inputs.

### How to run tests
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```
