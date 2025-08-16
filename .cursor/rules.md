# Cursor Rules for ai-smartcloudops

## General
- Follow the phase plan strictly. Do not skip phases.
- Never overwrite existing files unless instructed.
- Keep code modular inside `src/` and tests in `tests/`.

## Code Quality
- Use Python PEP8.
- Every function must have docstring.
- Add new dependencies only if confirmed and update `requirements.txt`.

## Testing
- Every new function must have a pytest.
- Do not change old tests unless requirement changes.
- All tests must pass before moving to next phase.

## Workflow
- Work one phase at a time.
- Ask for clarification if a task is ambiguous.
- Never hallucinate features or rename files without instruction.
 
  ## Progress Notes
  - Phase 0 — Setup & Architecture: ✅ Completed
  - Phase 1 — Data Ingestion: ✅ Completed
  - Phase 2 — Monitoring Core: ✅ Completed
  - Phase 3 — AI Anomaly Detection: ⏭️ Upcoming
# Cursor Rules for ai-smartcloudops

1. Do not overwrite unrelated files.
2. Always follow the defined phase plan (Phase 0 → Phase 5).
3. Write clean, modular, and testable code.
4. Keep all tests in `tests/` directory.
5. Use `pytest` for testing.
6. Document manual vs Cursor tasks clearly in `docs/`.
