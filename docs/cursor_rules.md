# Detailed Cursor Rules & Progress Notes

## General
- Follow the defined phase plan strictly (Phase 0 → Phase 5).
- Do not overwrite unrelated files.
- Keep `.cursor/rules.md` minimal for pytest compatibility.

## Code Quality
- Write clean, modular, and testable code.
- Use consistent naming conventions across the project.
- Add inline documentation or comments where logic may not be obvious.
- Ensure code is production-ready before merging.

## Testing
- Keep all test files inside the `tests/` directory.
- Use `pytest` for running all automated tests.
- Write meaningful test names and cover edge cases.
- Maintain 80%+ test coverage as the project grows.

## Workflow
- Separate manual vs. Cursor tasks.
- Document manual tasks clearly inside `docs/`.
- Ensure CI/CD workflow passes before merging into `main`.
- Keep commits small, atomic, and with descriptive messages.

## Progress Notes
✅ Phase 0 setup complete  
⏭️ Upcoming: Phase 1 (Core Architecture)  
🚧 Ongoing: Documentation updates and test refinement
