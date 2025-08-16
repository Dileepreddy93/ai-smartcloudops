# Phase 2 — Monitoring Core

## Goals
- Load the latest metrics from JSON and expose as a Python dictionary.

## Manual Tasks Performed
- Ran Phase 1 tests and confirmed success before proceeding.

## Cursor Tasks Performed
- Implemented `src/monitor.py` with `get_latest_metrics(file_path)` that reads and returns metrics from JSON.
- Added `tests/test_monitor.py` to verify returned dictionary and required keys.

## Pytests Created
- Verified the function returns a dictionary containing `cpu` and `memory` keys and matches on-disk content.

## Status
- ✅ Completed
