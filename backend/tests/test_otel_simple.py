"""
Simple test for opentelemetry_config.py.

This test just ensures the module can be imported and the setup function exists.
"""
import pytest
from ainative.app.core.opentelemetry_config import setup_opentelemetry
from fastapi import FastAPI


def test_setup_opentelemetry_exists():
    """Test that the setup_opentelemetry function exists and can be called."""
    assert callable(setup_opentelemetry), "setup_opentelemetry should be callable"

    # Create a test app
    app = FastAPI(title="Test App")

    # Should not raise an exception
    setup_opentelemetry(app)

    assert True, "setup_opentelemetry should not raise an exception"
