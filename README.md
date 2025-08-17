# ai-smartcloudops (Skeleton)

This is a fresh project skeleton aligned to the Phase Plan.

- Authoritative plan: see docs/phase_plan.md.
- Minimal rules: see .cursor/rules.md.

Implementation will proceed phase-by-phase with pytest markers.

## Status up to Phase 0

- Repository structure created: `src/`, `tests/`, `config/`, `infra/`, `.cursor/`, `docs/`.
- Minimal rules in `.cursor/rules.md` defined (6-point list).
- Minimal `requirements.txt` added per plan.
- Pytest markers configured in `tests/conftest.py` for `phase0..phase7` and `aws_live`.
- Phase 0 tests pass: `pytest -q -m "phase0"`.

## Phase 1 note

- Metrics file for synthetic data: `data/metrics.json`.

## Status up to Phase 3

- Phase 1 (Data Ingestion): `fetch_metrics()` writes synthetic metrics JSON; tests green.
- Phase 2 (Monitoring Core): `get_latest_metrics()` reads JSON; tests green.
- Phase 3 (AI Analysis): `detect_anomaly()` and `log_anomaly_to_s3()` implemented; tests green.
