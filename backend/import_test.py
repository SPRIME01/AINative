"""
Test script to verify module imports.
"""
import sys
print("Python Path:")
for path in sys.path:
    print(f"  - {path}")

try:
    import ainative
    print("\nSuccessfully imported ainative!")

    try:
        from ainative.app.core.opentelemetry_config import setup_opentelemetry
        print("Successfully imported setup_opentelemetry!")
    except ImportError as e:
        print(f"Failed to import setup_opentelemetry: {e}")
except ImportError as e:
    print(f"\nFailed to import ainative: {e}")

# Try importing the test module directly
try:
    import tests.infrastructure.test_opentelemetry
    print("\nSuccessfully imported test_opentelemetry test module!")
except ImportError as e:
    print(f"\nFailed to import test module: {e}")

# Try listing files in the test directory
import os
print("\nFiles in tests/infrastructure:")
try:
    for file in os.listdir("tests/infrastructure"):
        print(f"  - {file}")
except Exception as e:
    print(f"Error listing files: {e}")
