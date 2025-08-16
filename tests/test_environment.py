import sys
import os
import importlib

# List of required packages
required_packages = [
    "boto3",        # AWS SDK
    "prometheus_client",
    "grafana_api",
    "pytest"
]

def test_python_version():
    """Ensure Python version is 3.8+"""
    major, minor = sys.version_info[:2]
    assert major == 3 and minor >= 8, f"Python 3.8+ required, found {major}.{minor}"

def test_required_packages_installed():
    """Ensure all required packages are installed"""
    missing = []
    for pkg in required_packages:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    assert not missing, f"Missing required packages: {missing}"

def test_environment_variables():
    """Check required environment variables"""
    required_env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "GRAFANA_API_KEY"]
    missing = [var for var in required_env_vars if var not in os.environ]
    assert not missing, f"Missing environment variables: {missing}"


