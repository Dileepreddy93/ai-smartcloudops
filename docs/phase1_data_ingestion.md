# Phase 1 — Data Ingestion

## Goals
- Simulate fetching cloud metrics and persist them as JSON.

## Manual Tasks Performed
- Decided storage target as `metrics.json`.

## Cursor Tasks Performed
- Implemented `ai_smartcloudops.data_ingestion.fetch_metrics(file_path)` to write metrics JSON with `cpu` and `memory` keys.
- Added tests `tests/test_phase1_data_ingestion.py` and `tests/test_data_ingestion.py`.

## Pytests Created
- Validated file creation and presence of `cpu` and `memory` keys both in return value and on-disk JSON.

## Status
- ✅ Completed
