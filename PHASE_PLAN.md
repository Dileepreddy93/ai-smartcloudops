# 🚂 ai-smartcloudops — Phase Plan

## Purpose

This document defines the step-by-step phase plan for `ai-smartcloudops`, separating manual tasks, Cursor (AI) tasks, pytest checks, and rules for Cursor. It ensures that both humans and Cursor understand exactly what to do and in which order.

---

## Phase 0 — Setup & Architecture

**Manual Tasks**

- Create GitHub repo `ai-smartcloudops` and clone locally.
- Create folder structure:

```
ai-smartcloudops/
├── src/
├── tests/
├── requirements.txt
├── README.md
├── .gitignore
└── .cursor/rules.md
```

- Install `pytest` locally: `pip install pytest`.

**Cursor Tasks**

- Create `tests/test_setup.py` to check folder structure and required files.

**Pytest**

- Ensure all folders and files exist.
- Check required packages are installed.

---

## Phase 1 — Data Ingestion

**Manual Tasks**

- Decide storage for metrics (e.g., `metrics.json`).
- Add `json` (builtin) to `requirements.txt` for clarity.

**Cursor Tasks**

- Create `src/data_ingestion.py` with `fetch_metrics(file_path)` to simulate cloud metrics and save as JSON.

**Pytest**

- Check `metrics.json` is created and contains `cpu` and `memory` keys.

---

## Phase 2 — Monitoring Core

**Manual Tasks**

- Run Phase 1 pytest and ensure success.

**Cursor Tasks**

- Create `src/monitor.py` with `get_latest_metrics(file_path)` that returns metrics as a dictionary.

**Pytest**

- Validate returned metrics dictionary contains `cpu` and `memory`.

---

## Phase 3 — AI Analysis

**Manual Tasks**

- Add `scikit-learn` to `requirements.txt` and install locally.

**Cursor Tasks**

- Create `src/anomaly_detection.py` with `detect_anomaly(metrics)` to detect CPU or memory > 90%.

**Pytest**

- Test normal vs anomalous metrics.
- Ensure `True` returned for anomalies and `False` for normal.

---

## Phase 4 — Automation

**Manual Tasks**

- Decide remediation simulation (e.g., logging, print).

**Cursor Tasks**

- Create `src/auto_remediate.py` with `remediate_action(issue)` returning "Action taken for {issue}".

**Pytest**

- Ensure remediation function returns expected string.

---

## Phase 5 — Dashboard

**Manual Tasks**

- Install Flask locally (`pip install flask`) and update `requirements.txt`.

**Cursor Tasks**

- Create `src/dashboard.py` using Flask.
- Display metrics from `metrics.json` at `/` and indicate if anomaly exists.

**Pytest**

- Ensure dashboard runs and HTTP status code 200 at `/`.

---

## Phase 6 — Final Integration

**Manual Tasks**

- Run all tests (`pytest -q`) and ensure all pass.
- Push code to GitHub.

**Cursor Tasks**

- Create `main.py` to integrate all modules: ingestion → monitoring → anomaly → remediation.

**Pytest**

- Check integration script runs without errors.

---

## Cursor Rules (`.cursor/rules.md`)

- Follow the phase plan strictly. Do not skip phases.
- Never overwrite existing files unless instructed.
- Keep code modular in `src/` and tests in `tests/`.
- Every function must have docstring.
- Add new dependencies only if confirmed and update `requirements.txt`.
- Every new function must have a pytest.
- Do not change old tests unless requirement changes.
- Work one phase at a time.
- Ask for clarification if a task is ambiguous.
- Never hallucinate features or rename files without instruction.

This project plan is authoritative; proceed according to these phases.

