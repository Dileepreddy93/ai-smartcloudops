import os
import importlib

# -------------------------------
# CONFIG: expected structure & packages
# -------------------------------
expected_files = [
    "requirements.txt",
    "README.md",
    ".gitignore"
]

expected_folders = [
    "src",
    "tests",
    ".cursor"
]

required_packages = [
    "pytest",
    "flask",
    "scikit-learn",
    "boto3",
    "prometheus_client"
]

# -------------------------------
# TESTS
# -------------------------------

def test_folders_exist():
    """Check that required folders exist"""
    for folder in expected_folders:
        assert os.path.isdir(folder), f"Folder missing: {folder}"

def test_files_exist():
    """Check that required files exist"""
    for file in expected_files:
        assert os.path.isfile(file), f"File missing: {file}"

def test_required_packages_installed():
    """Check that all required packages are installed"""
    # Map distribution names to importable module names
    name_mapping = {
        "scikit-learn": "sklearn",
    }

    missing = []
    for pkg in required_packages:
        module_name = name_mapping.get(pkg, pkg)
        if importlib.util.find_spec(module_name) is None:
            missing.append(pkg)
    assert not missing, f"Missing required packages: {missing}"


