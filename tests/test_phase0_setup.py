import os
import pathlib
import pytest


pytestmark = pytest.mark.phase0


def test_repo_layout_exists() -> None:
    """Phase 0: required top-level folders and files exist."""
    root = pathlib.Path(__file__).resolve().parents[1]
    expected_dirs = [
        root / "src",
        root / "tests",
        root / "config",
        root / "docs",
        root / "infra",
        root / ".cursor",
    ]
    expected_files = [
        root / "docs" / "phase_plan.md",
        root / ".cursor" / "rules.md",
        root / "requirements.txt",
        root / "README.md",
    ]

    missing = [str(p) for p in expected_dirs + expected_files if not p.exists()]
    assert not missing, f"Missing required paths: {missing}"


def test_cursor_rules_minimal_content() -> None:
    """Phase 0: `.cursor/rules.md` contains minimal strict rules."""
    required_lines = [
        "1. Do not overwrite unrelated files.",
        "2. Always follow the defined phase plan (Phase 0 → Phase 7).",
        "3. Write clean, modular, and testable code.",
        "4. Keep all tests in `tests/` directory.",
        "5. Use `pytest` for testing.",
        "6. Document manual vs Cursor tasks clearly in `docs/`.",
    ]
    content = (pathlib.Path(".cursor/rules.md").read_text(encoding="utf-8"))
    for line in required_lines:
        assert line in content, f"Missing rule in .cursor/rules.md: {line}"


def test_requirements_minimal_packages() -> None:
    """Phase 0: `requirements.txt` contains minimal packages from plan."""
    minimal = {
        "flask",
        "scikit-learn",
        "boto3",
        "prometheus-client",
        "requests",
        "pytest",
        "moto",
    }
    lines = {
        line.strip()
        for line in pathlib.Path("requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    missing = sorted(minimal - lines)
    assert not missing, f"Missing packages in requirements.txt: {missing}"


