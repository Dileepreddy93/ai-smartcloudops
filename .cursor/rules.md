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
