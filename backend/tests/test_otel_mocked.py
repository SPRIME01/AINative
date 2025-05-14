"""
Simple test that mocks OpenTelemetry dependencies.

This test uses unittest.mock to mock all OpenTelemetry dependencies,
so we can test the opentelemetry_config.py module without needing
the exact versions of dependencies.
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the repository root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock all OpenTelemetry imports before importing the module under test
mock_modules = {
    'opentelemetry': MagicMock(),
    'opentelemetry.trace': MagicMock(),
    'opentelemetry.metrics': MagicMock(),
    'opentelemetry._logs': MagicMock(),
    'opentelemetry.sdk.resources': MagicMock(),
    'opentelemetry.semconv.resource': MagicMock(),
    'opentelemetry.instrumentation.fastapi': MagicMock(),
    'opentelemetry.exporter.otlp.proto.grpc.trace_exporter': MagicMock(),
    'opentelemetry.sdk.trace': MagicMock(),
    'opentelemetry.sdk.trace.export': MagicMock(),
    'opentelemetry.exporter.otlp.proto.grpc.metric_exporter': MagicMock(),
    'opentelemetry.sdk.metrics': MagicMock(),
    'opentelemetry.sdk.metrics.export': MagicMock(),
    'opentelemetry.exporter.otlp.proto.grpc._log_exporter': MagicMock(),
    'opentelemetry.sdk._logs': MagicMock(),
    'opentelemetry.sdk._logs.export': MagicMock(),
}

# Create a mock patch context for each module
patches = [patch.dict('sys.modules', {name: mock for name, mock in mock_modules.items()})]

@pytest.fixture(scope='module', autouse=True)
def apply_patches():
    """Apply all the mocks for OpenTelemetry dependencies."""
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()

# Now import the module under test
try:
    from ainative.app.core.opentelemetry_config import setup_opentelemetry
except ImportError as e:
    print(f"Failed to import setup_opentelemetry: {e}")
    setup_opentelemetry = None

# Define a simple test that doesn't depend on specific OpenTelemetry implementations
def test_setup_opentelemetry_exists():
    """Test that the setup_opentelemetry function exists."""
    assert setup_opentelemetry is not None, "setup_opentelemetry should exist"
    assert callable(setup_opentelemetry), "setup_opentelemetry should be callable"
