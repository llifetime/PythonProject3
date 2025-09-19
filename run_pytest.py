"""Run pytest with coverage."""

import subprocess
import sys


def run_pytest():
    """Run pytest with coverage reporting."""
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=product",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v",
        "test_products_pytest.py"
    ], capture_output=True, text=True)

    print("STDOUT:")
    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    return result.returncode


if __name__ == "__main__":
    exit_code = run_pytest()
    sys.exit(exit_code)
