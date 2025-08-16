"""Pytest configuration: define phase markers and optional aws_live gating.

This file sets up custom markers for phases 0..7 and an `aws_live` marker
that is only enabled when the environment variable `AWS_LIVE=1` is present.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers to document test purposes per phase plan."""
    for phase in range(8):
        config.addinivalue_line(
            "markers", f"phase{phase}: tests for Phase {phase} as per phase plan"
        )
    config.addinivalue_line(
        "markers",
        "aws_live: tests that hit live AWS resources; run only if AWS_LIVE=1",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip aws_live tests unless explicitly enabled via environment variable."""
    if os.environ.get("AWS_LIVE") == "1":
        return

    skip_marker = pytest.mark.skip(reason="aws_live disabled (set AWS_LIVE=1 to enable)")
    for item in items:
        if any(mark.name == "aws_live" for mark in item.iter_markers()):
            item.add_marker(skip_marker)


def _ensure_src_on_path() -> None:
    """Prepend repository `src/` to sys.path so `from data_ingestion import ...` works."""
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))


_ensure_src_on_path()


