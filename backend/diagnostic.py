"""
Check the environment and test if we can import and run tests
"""
import sys
import os
from pathlib import Path

# Current working directory
print(f"Current directory: {os.getcwd()}")

# Python path
print("\nPython Path:")
for p in sys.path:
    print(f"  - {p}")

# Check if src is in the path
src_path = Path("src").absolute()
print(f"\nSrc path: {src_path}")
print(f"Src path exists: {src_path.exists()}")
print(f"Src path in sys.path: {str(src_path) in sys.path}")

# Add src to path if not already there
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
    print("Added src to sys.path")

# Try importing setup_opentelemetry
try:
    from ainative.app.core.opentelemetry_config import setup_opentelemetry
    print("\nImported setup_opentelemetry successfully")
except ImportError as e:
    print(f"\nError importing setup_opentelemetry: {e}")

# Check for test file
test_file = Path("tests/infrastructure/test_opentelemetry.py").absolute()
print(f"\nTest file path: {test_file}")
print(f"Test file exists: {test_file.exists()}")

# Try importing the test module
try:
    import tests.infrastructure.test_opentelemetry
    print("\nImported test module successfully")
except ImportError as e:
    print(f"\nError importing test module: {e}")

# Print test module content
if "tests.infrastructure.test_opentelemetry" in sys.modules:
    print("\nTest module content:")
    test_module = sys.modules["tests.infrastructure.test_opentelemetry"]
    for name in dir(test_module):
        if name.startswith("Test"):
            print(f"  - {name}")
            test_class = getattr(test_module, name)
            for method_name in dir(test_class):
                if method_name.startswith("test_"):
                    print(f"      {method_name}")
else:
    print("\nTest module not loaded")
