"""
Fixtures for Grafana monitoring testing.
"""

import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict('os.environ', {
        'GRAFANA_URL': 'http://grafana:3000',
        'GRAFANA_API_KEY': 'mock-api-key',
        'PROMETHEUS_URL': 'http://prometheus:9090',
        'LOKI_URL': 'http://loki:3100',
    }):
        yield
