import json
import os
import pytest
from unittest.mock import patch, MagicMock

from backend.monitoring.grafana import (
    GrafanaClient,
    setup_dashboards,
    setup_alerts,
    setup_datasources,
)


@pytest.fixture
def mock_grafana_client():
    """Mock the Grafana client to avoid external API calls."""
    with patch("backend.monitoring.grafana.GrafanaClient") as mock_client:
        # Setup mock responses for various API endpoints
        client_instance = mock_client.return_value

        # Mock dashboard creation
        client_instance.create_dashboard.return_value = {"id": "dashboard-123", "uid": "abc123", "status": "success"}

        # Mock alert rule creation
        client_instance.create_alert_rule.return_value = {"id": 1, "uid": "alert-123", "status": "success"}

        # Mock datasource creation/testing
        client_instance.create_datasource.return_value = {"id": 1, "uid": "ds-123", "status": "success"}
        client_instance.test_datasource.return_value = {"status": "success", "message": "Data source is working"}

        yield client_instance


@pytest.fixture
def mock_prometheus_config():
    """Mock Prometheus configuration."""
    return {
        "name": "Prometheus",
        "type": "prometheus",
        "url": "http://prometheus:9090",
        "access": "proxy",
        "isDefault": True
    }


@pytest.fixture
def mock_loki_config():
    """Mock Loki configuration."""
    return {
        "name": "Loki",
        "type": "loki",
        "url": "http://loki:3100",
        "access": "proxy",
    }


def test_datasource_setup(mock_grafana_client, mock_prometheus_config, mock_loki_config):
    """Test that Prometheus and Loki data sources are correctly configured."""
    # Call the function that sets up data sources
    setup_datasources(mock_grafana_client, [mock_prometheus_config, mock_loki_config])

    # Assert the client was called with correct parameters
    assert mock_grafana_client.create_datasource.call_count == 2

    # Check Prometheus datasource was created correctly
    mock_grafana_client.create_datasource.assert_any_call(mock_prometheus_config)

    # Check Loki datasource was created correctly
    mock_grafana_client.create_datasource.assert_any_call(mock_loki_config)

    # Verify datasources were tested
    assert mock_grafana_client.test_datasource.call_count == 2


def test_dashboard_setup(mock_grafana_client):
    """Test that dashboards for error rates, latency, and correlated traces are correctly configured."""
    # Call function to setup dashboards
    setup_dashboards(mock_grafana_client)

    # Verify dashboard creation was called
    assert mock_grafana_client.create_dashboard.call_count >= 1

    # Get the dashboard model from the first call
    dashboard_model = mock_grafana_client.create_dashboard.call_args[0][0]

    # Convert to dictionary if it's a complex object
    if not isinstance(dashboard_model, dict):
        dashboard_model = dashboard_model.to_dict()

    # Check that the dashboard has required panels
    panels = dashboard_model.get("dashboard", {}).get("panels", [])
    panel_titles = [panel.get("title", "") for panel in panels]

    # Verify essential panels exist
    required_panels = [
        "HTTP Error Rate (5xx)",
        "Request Latency",
        "Correlated Logs and Traces"
    ]

    for required_panel in required_panels:
        assert any(required_panel in title for title in panel_titles), f"Missing panel: {required_panel}"


def test_alert_rules_setup(mock_grafana_client):
    """Test that alert rules are correctly configured with specified thresholds."""
    # Call function to setup alerts
    setup_alerts(mock_grafana_client)

    # Verify alert creation was called
    assert mock_grafana_client.create_alert_rule.call_count >= 3

    # Collect all alert rule configurations
    alert_configs = [call_args[0][0] for call_args in mock_grafana_client.create_alert_rule.call_args_list]

    # Verify 5xx error rate alert
    error_rate_alert = next((alert for alert in alert_configs if "5xx error rate" in alert.get("name", "")), None)
    assert error_rate_alert is not None
    assert "1%" in json.dumps(error_rate_alert)
    assert "5m" in json.dumps(error_rate_alert)

    # Verify latency alert
    latency_alert = next((alert for alert in alert_configs if "latency" in alert.get("name", "").lower()), None)
    assert latency_alert is not None
    assert "1s" in json.dumps(latency_alert)

    # Verify log volume spike alert
    log_volume_alert = next((alert for alert in alert_configs if "log volume" in alert.get("name", "").lower()), None)
    assert log_volume_alert is not None
    assert "50%" in json.dumps(log_volume_alert)
    assert "5m" in json.dumps(log_volume_alert)


def test_prometheus_queries(mock_grafana_client):
    """Test that the correct PromQL queries are used for metrics panels and alerts."""
    # Call functions to setup dashboards and alerts
    setup_dashboards(mock_grafana_client)
    setup_alerts(mock_grafana_client)

    # Extract all dashboard configurations
    dashboard_calls = mock_grafana_client.create_dashboard.call_args_list
    dashboard_configs = []
    for call in dashboard_calls:
        config = call[0][0]
        if not isinstance(config, dict):
            config = config.to_dict()
        dashboard_configs.append(config)

    # Extract queries from panels
    queries = []
    for config in dashboard_configs:
        for panel in config.get("dashboard", {}).get("panels", []):
            if "targets" in panel:
                for target in panel.get("targets", []):
                    if "expr" in target:
                        queries.append(target["expr"])

    # Check for expected PromQL patterns
    expected_patterns = [
        # 5xx error rate query pattern
        'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100',

        # Latency query pattern
        'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{route=~".*"}[5m])) by (le, route))'
    ]

    for pattern in expected_patterns:
        assert any(pattern in query for query in queries), f"Missing PromQL query pattern: {pattern}"


def test_loki_queries(mock_grafana_client):
    """Test that the correct Loki log queries are used for log panels and alerts."""
    # Call functions to setup dashboards and alerts
    setup_dashboards(mock_grafana_client)
    setup_alerts(mock_grafana_client)

    # Extract all dashboard configurations and alert rule calls
    dashboard_calls = mock_grafana_client.create_dashboard.call_args_list
    alert_calls = mock_grafana_client.create_alert_rule.call_args_list

    # Extract all Loki queries from both dashboards and alerts
    loki_queries = []

    # From dashboards
    for call in dashboard_calls:
        config = call[0][0]
        if not isinstance(config, dict):
            config = config.to_dict()

        for panel in config.get("dashboard", {}).get("panels", []):
            for target in panel.get("targets", []):
                if target.get("datasource", {}).get("type") == "loki":
                    loki_queries.append(target.get("expr", ""))

    # From alerts (may be in a different format depending on your alert rule model)
    for call in alert_calls:
        rule = call[0][0]
        if isinstance(rule, dict) and "data" in rule:
            for condition in rule.get("data", []):
                if condition.get("datasourceUid", "").startswith("loki"):
                    loki_queries.append(condition.get("model", {}).get("expr", ""))

    # Check for expected Loki query patterns
    expected_patterns = [
        # Logs with correlation ID
        'correlationId="{{correlation_id}}"',

        # Log volume query for spike detection
        'sum(count_over_time({app="my-app"}[5m]))',

        # Error logs
        'level="error"'
    ]

    for pattern in expected_patterns:
        assert any(pattern in query for query in loki_queries), f"Missing Loki query pattern: {pattern}"


def test_correlation_id_tracing(mock_grafana_client):
    """Test that dashboards support correlation ID based tracing across panels."""
    # Call function to setup dashboards
    setup_dashboards(mock_grafana_client)

    # Get dashboard configuration
    dashboard_config = mock_grafana_client.create_dashboard.call_args[0][0]
    if not isinstance(dashboard_config, dict):
        dashboard_config = dashboard_config.to_dict()

    dashboard = dashboard_config.get("dashboard", {})

    # Check for template variables to support correlation ID filtering
    templates = dashboard.get("templating", {}).get("list", [])
    has_correlation_id_var = any(
        template.get("name") == "correlation_id" for template in templates
    )

    assert has_correlation_id_var, "Dashboard missing template variable for correlation_id"

    # Check panels have links to traverse between metrics, logs, and traces
    panels = dashboard.get("panels", [])
    for panel in panels:
        # Skip non-relevant panels
        if panel.get("type") not in ["graph", "timeseries", "logs", "trace"]:
            continue

        # Check panel has data links
        links = panel.get("links", [])
        # Either the panel has its own links or it inherits from dashboard
        has_links = len(links) > 0 or dashboard.get("links")

        assert has_links, f"Panel '{panel.get('title', 'unknown')}' missing data links for correlation"
