import os
import importlib
import re

# -------------------------------
# CONFIG: Expected folders, files & packages
# -------------------------------
expected_folders = [
    "src",
    "tests",
    ".cursor"
]

expected_files = [
    "requirements.txt",
    "README.md",
    ".gitignore"
]

required_packages = [
    "pytest",
    "flask",
    "scikit-learn",
    "boto3",
    "prometheus_client"
]

# Map distribution names to importable module names when they differ
NAME_MAPPING = {
    "scikit-learn": "sklearn",
    "prometheus-client": "prometheus_client",
    "grafana-api": "grafana_api",
}

cursor_rules_path = ".cursor/rules.md"

expected_cursor_rules = """
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
""".strip()

# -------------------------------
# TESTS
# -------------------------------

def test_folders_exist():
    """Phase 0: Check required folders exist"""
    missing_folders = [f for f in expected_folders if not os.path.isdir(f)]
    assert not missing_folders, f"Missing folders: {missing_folders}"


def test_files_exist():
    """Phase 0: Check required files exist"""
    missing_files = [f for f in expected_files if not os.path.isfile(f)]
    assert not missing_files, f"Missing files: {missing_files}"


def test_required_packages_installed():
    """Phase 0: Check required packages are installed"""
    missing_packages = []
    for pkg in required_packages:
        module_name = NAME_MAPPING.get(pkg, pkg)
        if importlib.util.find_spec(module_name) is None:
            missing_packages.append(pkg)
    assert not missing_packages, f"Missing Python packages: {missing_packages}"


def test_requirements_txt_packages_installed():
    """Phase 0: Check that all packages listed in requirements.txt are installed"""
    requirements_path = "requirements.txt"
    assert os.path.isfile(requirements_path), "requirements.txt file is missing"

    with open(requirements_path, "r", encoding="utf-8") as requirements_file:
        packages: list[str] = []
        for raw_line in requirements_file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            # Drop environment markers and extras, keep only the name part
            name_part = line.split(";")[0].split("[")[0].strip()
            # Remove version specifiers (==, >=, <=, >, <, ~=, !=)
            name_only = re.split(r"(==|>=|<=|>|<|~=|!=)", name_part, maxsplit=1)[0].strip()
            if name_only:
                packages.append(name_only)

    missing = []
    for dist_name in packages:
        module_name = NAME_MAPPING.get(dist_name, dist_name)
        if importlib.util.find_spec(module_name) is None:
            missing.append(dist_name)

    assert not missing, f"Packages listed in requirements.txt but not installed: {missing}"


def test_cursor_rules_exist_and_match():
    """Phase 0: Check that Cursor rules exist and match expected"""
    assert os.path.isfile(cursor_rules_path), f"{cursor_rules_path} is missing"

    with open(cursor_rules_path, "r", encoding="utf-8") as rules_file:
        content = rules_file.read().strip()

    assert content == expected_cursor_rules, (
        f"{cursor_rules_path} content does not match expected rules"
    )

