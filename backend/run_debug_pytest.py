"""
Run pytest with debug logging to diagnose test collection issues
"""
import subprocess
import sys
import os

def run_pytest():
    """Run pytest with debug logging to diagnose test collection issues"""
    # Set working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run pytest with verbose and debug log level
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/infrastructure/test_opentelemetry.py",
        "-v", "--log-cli-level=DEBUG",
        "-p", "no:warnings", "--no-header", "--no-summary"
    ]

    print(f"Running command: {' '.join(cmd)}")

    # Run the command and capture output
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        print("\n=== STDOUT ===")
        print(result.stdout)

        print("\n=== STDERR ===")
        print(result.stderr)

        print(f"\n=== EXIT CODE: {result.returncode} ===")
    except Exception as e:
        print(f"Error running pytest: {e}")

if __name__ == "__main__":
    run_pytest()
