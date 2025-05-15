"""
Grafana integration module for AINative platform.

This module provides interfaces and functionality for:
- Setting up Grafana dashboards for visualizing metrics and logs
- Configuring alerts based on error rates, latency, and log volumes
- Managing Grafana data sources like Prometheus and Loki
- Defining PromQL and LogQL queries for monitoring and alerting
"""

import json
import os
from typing import Any, Dict, List, Optional, Union
import requests
from urllib.parse import urljoin


class GrafanaClient:
    """
    Client for interacting with Grafana API.

    This client handles authentication and provides methods to create dashboards,
    alerts, and data sources in Grafana.

    Attributes:
        base_url: Base URL of the Grafana instance
        api_key: API key for authentication
        headers: HTTP headers to include in requests
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Grafana client.

        Args:
            base_url: Base URL of the Grafana instance
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

    def create_dashboard(self, dashboard_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a dashboard in Grafana.

        Args:
            dashboard_model: Dashboard definition in Grafana JSON format

        Returns:
            Dict containing the response from Grafana API

        Example:
            ```python
            dashboard = {
                "dashboard": {
                    "title": "HTTP Monitoring",
                    "panels": [...]
                },
                "overwrite": True
            }
            client.create_dashboard(dashboard)
            ```
        """
        url = urljoin(self.base_url, '/api/dashboards/db')
        response = requests.post(url, headers=self.headers, json=dashboard_model)
        response.raise_for_status()
        return response.json()

    def create_alert_rule(self, alert_rule: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an alert rule in Grafana.

        Args:
            alert_rule: Alert rule definition

        Returns:
            Dict containing the response from Grafana API

        Example:
            ```python
            alert_rule = {
                "name": "High Error Rate",
                "condition": "...",
                "data": [...]
            }
            client.create_alert_rule(alert_rule)
            ```
        """
        url = urljoin(self.base_url, '/api/ruler/grafana/api/v1/rules')
        response = requests.post(url, headers=self.headers, json=alert_rule)
        response.raise_for_status()
        return response.json()

    def create_datasource(self, datasource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a data source in Grafana.

        Args:
            datasource: Data source definition

        Returns:
            Dict containing the response from Grafana API

        Example:
            ```python
            datasource = {
                "name": "Prometheus",
                "type": "prometheus",
                "url": "http://prometheus:9090"
            }
            client.create_datasource(datasource)
            ```
        """
        url = urljoin(self.base_url, '/api/datasources')
        response = requests.post(url, headers=self.headers, json=datasource)
        response.raise_for_status()
        return response.json()

    def test_datasource(self, datasource_id: int) -> Dict[str, Any]:
        """
        Test a data source connection in Grafana.

        Args:
            datasource_id: ID of the data source to test

        Returns:
            Dict containing the test result
        """
        url = urljoin(self.base_url, f'/api/datasources/{datasource_id}/health')
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


def setup_dashboards(client: GrafanaClient) -> List[Dict[str, Any]]:
    """
    Set up Grafana dashboards for monitoring.

    Creates dashboards for:
    - HTTP error rates (5xx)
    - Request latency
    - Correlation-ID-linked traces and logs

    Args:
        client: Initialized GrafanaClient

    Returns:
        List of created dashboard responses
    """
    results = []

    # Main monitoring dashboard with all panels
    main_dashboard = {
        "dashboard": {
            "title": "Edge API Monitoring",
            "uid": "main-monitoring-dashboard",
            "panels": [
                {
                    "title": "HTTP Error Rate (5xx)",
                    "type": "graph",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                    "targets": [
                        {
                            "expr": 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100',
                            "legendFormat": "5xx Error Rate",
                            "refId": "A"
                        }
                    ],
                    "links": [
                        {
                            "title": "View Related Logs",
                            "url": "/explore?left=%7B\"datasource\":\"Loki\",\"queries\":%5B%7B\"expr\":\"correlationId%3D%5C\"$correlation_id%5C\"\"%7D%5D%7D",
                            "type": "link"
                        }
                    ]
                },
                {
                    "title": "Request Latency",
                    "type": "graph",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                    "targets": [
                        {
                            "expr": 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{route=~".*"}[5m])) by (le, route))',
                            "legendFormat": "95th Percentile - {{route}}",
                            "refId": "A"
                        }
                    ],
                    "links": [
                        {
                            "title": "View Related Logs",
                            "url": "/explore?left=%7B\"datasource\":\"Loki\",\"queries\":%5B%7B\"expr\":\"correlationId%3D%5C\"$correlation_id%5C\"\"%7D%5D%7D",
                            "type": "link"
                        }
                    ]
                },
                {
                    "title": "Correlated Logs and Traces",
                    "type": "logs",
                    "gridPos": {"h": 12, "w": 24, "x": 0, "y": 8},
                    "targets": [
                        {
                            "expr": 'correlationId="{{correlation_id}}"',
                            "refId": "A",
                            "datasource": {"type": "loki"}
                        },
                        {
                            "expr": 'sum(count_over_time({app="my-app"}[5m]))',
                            "refId": "B",
                            "datasource": {"type": "loki"}
                        },
                        {
                            "expr": 'level="error"',
                            "refId": "C",
                            "datasource": {"type": "loki"}
                        }
                    ],
                    "links": [
                        {
                            "title": "View Request Metrics",
                            "url": "/d/main-monitoring-dashboard/edge-api-monitoring?var-correlation_id=${__data.fields.correlation_id}",
                            "type": "link"
                        }
                    ]
                }
            ],
            "templating": {
                "list": [
                    {
                        "name": "correlation_id",
                        "type": "textbox",
                        "label": "Correlation ID",
                        "current": {"value": ""}
                    }
                ]
            },
            "links": [
                {
                    "title": "View Logs",
                    "url": "/explore?left=%7B\"datasource\":\"Loki\",\"queries\":%5B%7B\"expr\":\"correlationId%3D%5C\"${correlation_id}%5C\"\"%7D%5D%7D",
                    "type": "link"
                }
            ]
        },
        "overwrite": True
    }
    results.append(client.create_dashboard(main_dashboard))

    return results


def setup_alerts(client: GrafanaClient) -> List[Dict[str, Any]]:
    """
    Set up Grafana alerts based on:
    - 5xx error rate > 1% for 5 minutes
    - Latency > 1s on key routes
    - Log volume spike > 50% compared to prior 5-min average

    Args:
        client: Initialized GrafanaClient

    Returns:
        List of created alert responses
    """
    results = []

    # 5xx Error Rate Alert
    error_rate_alert = {
        "name": "High 5xx error rate",
        "folder": "Alerts",
        "interval": "5m",
        "rules": [
            {
                "name": "5xx error rate > 1%",
                "condition": "B",
                "data": [
                    {
                        "refId": "A",
                        "queryType": "range",
                        "relativeTimeRange": {
                            "from": 600,
                            "to": 0
                        },
                        "datasourceUid": "prometheus",
                        "model": {
                            "expr": 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100',
                            "instant": False,
                            "intervalMs": 1000,
                            "maxDataPoints": 43200,
                            "refId": "A"
                        }
                    },
                    {
                        "refId": "B",
                        "queryType": "reduce",
                        "reducer": "last",
                        "datasourceUid": "__expr__",
                        "model": {
                            "conditions": [
                                {
                                    "evaluator": {
                                        "params": [1],
                                        "type": "gt"
                                    },
                                    "operator": {
                                        "type": "and"
                                    },
                                    "query": {
                                        "params": ["A"]
                                    },
                                    "reducer": {
                                        "params": [],
                                        "type": "last"
                                    },
                                    "type": "query"
                                }
                            ],
                            "refId": "B"
                        }
                    }
                ],
                "noDataState": "NoData",
                "execErrState": "Error",
                "for": "5m",
                "annotations": {
                    "description": "5xx error rate is above 1% for 5 minutes",
                    "summary": "High error rate detected"
                }
            }
        ]
    }
    results.append(client.create_alert_rule(error_rate_alert))

    # Latency Alert
    latency_alert = {
        "name": "High latency",
        "folder": "Alerts",
        "interval": "1m",
        "rules": [
            {
                "name": "Latency > 1s on key routes",
                "condition": "B",
                "data": [
                    {
                        "refId": "A",
                        "queryType": "range",
                        "relativeTimeRange": {
                            "from": 600,
                            "to": 0
                        },
                        "datasourceUid": "prometheus",
                        "model": {
                            "expr": 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{route=~".*"}[5m])) by (le, route))',
                            "instant": False,
                            "intervalMs": 1000,
                            "maxDataPoints": 43200,
                            "refId": "A"
                        }
                    },
                    {
                        "refId": "B",
                        "queryType": "reduce",
                        "reducer": "last",
                        "datasourceUid": "__expr__",
                        "model": {
                            "conditions": [
                                {
                                    "evaluator": {
                                        "params": [1],
                                        "type": "gt"
                                    },
                                    "operator": {
                                        "type": "and"
                                    },
                                    "query": {
                                        "params": ["A"]
                                    },
                                    "reducer": {
                                        "params": [],
                                        "type": "last"
                                    },
                                    "type": "query"
                                }
                            ],
                            "refId": "B"
                        }
                    }
                ],
                "noDataState": "NoData",
                "execErrState": "Error",
                "for": "5m",
                "annotations": {
                    "description": "Request latency is above 1s for 5 minutes",
                    "summary": "High latency detected"
                }
            }
        ]
    }
    results.append(client.create_alert_rule(latency_alert))

    # Log Volume Alert
    log_volume_alert = {
        "name": "Log volume spike",
        "folder": "Alerts",
        "interval": "1m",
        "rules": [
            {
                "name": "Log volume spike > 50% compared to prior 5-min average",
                "condition": "C",
                "data": [
                    {
                        "refId": "A",
                        "queryType": "range",
                        "relativeTimeRange": {
                            "from": 600,
                            "to": 300
                        },
                        "datasourceUid": "loki",
                        "model": {
                            "expr": 'sum(count_over_time({app="my-app"}[5m]))',
                            "instant": False,
                            "refId": "A"
                        }
                    },
                    {
                        "refId": "B",
                        "queryType": "range",
                        "relativeTimeRange": {
                            "from": 300,
                            "to": 0
                        },
                        "datasourceUid": "loki",
                        "model": {
                            "expr": 'sum(count_over_time({app="my-app"}[5m]))',
                            "instant": False,
                            "refId": "B"
                        }
                    },
                    {
                        "refId": "C",
                        "queryType": "math",
                        "expression": "($B - $A) / $A * 100",
                        "datasourceUid": "__expr__"
                    }
                ],
                "noDataState": "NoData",
                "execErrState": "Error",
                "for": "5m",
                "conditions": [
                    {
                        "evaluator": {
                            "params": [50],
                            "type": "gt"
                        },
                        "operator": {
                            "type": "and"
                        },
                        "query": {
                            "params": ["C"]
                        },
                        "reducer": {
                            "params": [],
                            "type": "last"
                        },
                        "type": "query"
                    }
                ],
                "annotations": {
                    "description": "Log volume increased by more than 50% compared to the previous 5 minutes",
                    "summary": "Log volume spike detected"
                }
            }
        ]
    }
    results.append(client.create_alert_rule(log_volume_alert))

    return results


def setup_datasources(client: GrafanaClient, datasources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Set up Grafana data sources for Prometheus and Loki.

    Args:
        client: Initialized GrafanaClient
        datasources: List of data source configurations

    Returns:
        List of created data source responses
    """
    results = []

    for datasource in datasources:
        result = client.create_datasource(datasource)
        results.append(result)

        # Test the data source connection
        if 'id' in result:
            client.test_datasource(result['id'])

    return results
