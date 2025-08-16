from pathlib import Path


def _find_project_root(start_path: Path) -> Path:
    """Return the project root by walking up until `src` and `requirements.txt` are found.

    This makes the test resilient to being run from different working directories.
    """

    current_path: Path = start_path
    for candidate in [current_path, *current_path.parents]:
        if (candidate / "src").exists() and (candidate / "requirements.txt").exists():
            return candidate
    raise AssertionError("Could not locate project root containing 'src' and 'requirements.txt'.")


def test_project_structure_exists() -> None:
    """Ensure key project structure and files exist at the repository root."""

    project_root = _find_project_root(Path(__file__).resolve())

    assert (project_root / "src").is_dir(), "Missing 'src/' directory"
    assert (project_root / "tests").is_dir(), "Missing 'tests/' directory"
    assert (project_root / "requirements.txt").is_file(), "Missing 'requirements.txt' file"
    assert (project_root / "README.md").is_file(), "Missing 'README.md' file"
    assert (project_root / ".gitignore").is_file(), "Missing '.gitignore' file"


