"""
Focus on running a single test from test_opentelemetry.py
"""
import pytest
import sys
import os

# Add src to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the test class directly
from tests.infrastructure.test_opentelemetry import TestOpenTelemetryInstrumentation

# Run a specific test
if __name__ == "__main__":
    # Run the test using pytest programmatically
    pytest.main(["-xvs", "tests/infrastructure/test_opentelemetry.py::TestOpenTelemetryInstrumentation::test_fastapi_route_generates_traceparent_if_none_provided"])
