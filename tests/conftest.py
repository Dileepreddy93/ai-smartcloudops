"""Pytest configuration for ensuring `src/` is importable during tests.

This adds the repository's `src` directory to `sys.path` so that
`ai_smartcloudops` can be imported without an editable install.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _add_src_to_sys_path() -> None:
    """Prepend the repository `src` directory to `sys.path` if present."""
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"
    if src_path.exists() and src_path.is_dir():
        sys.path.insert(0, str(src_path))


_add_src_to_sys_path()


