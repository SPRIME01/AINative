"""
Pytest tests for OpenTelemetry instrumentation in the FastAPI backend.

Ensures that:
- FastAPI routes are automatically instrumented for tracing.
- Correlation headers (traceparent) are correctly propagated.
- OTLP exporters for logs, metrics, and traces are configured via environment variables.
"""
import os
import logging
import pytest
from typing import Generator, Any, AsyncGenerator
from unittest.mock import patch, MagicMock, call

from fastapi import FastAPI
from fastapi.testclient import TestClient

# Import the actual OpenTelemetry setup function
# Note: The 'ainative.app.core.opentelemetry_config' module relies on OpenTelemetry packages
# such as 'opentelemetry-api', 'opentelemetry-sdk', and relevant exporters.
# Ensure these are installed in your environment to prevent ImportErrors.
# Example: `opentelemetry-api` for `TraceContextTextMapPropagator`.
from ainative.app.core.opentelemetry_config import setup_opentelemetry


@pytest.fixture(scope="module")
def test_app() -> FastAPI:
    """
    Fixture to create a FastAPI application instance for testing.
    The OpenTelemetry setup is applied here.
    """
    # Ensure a trace endpoint is set for instrumentation tests
    # Environment variables must be strings, not None
    env_vars = {
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": "http://localhost:4317",
        "OTEL_SERVICE_NAME": "test-instrumentation-service"
    }

    # Store the original value if it exists so we can restore it later
    original_pytest_current_test = os.environ.get("PYTEST_CURRENT_TEST")

    # Remove PYTEST_CURRENT_TEST to disable test mode during setup
    if "PYTEST_CURRENT_TEST" in os.environ:
        os.environ.pop("PYTEST_CURRENT_TEST")

    try:
        with patch.dict(os.environ, env_vars, clear=False):
            app = FastAPI(title="Test App for OTel")

            # Apply OpenTelemetry instrumentation
            setup_opentelemetry(app)

            @app.get("/test-otel")
            async def _test_otel_endpoint():
                return {"message": "OpenTelemetry is active"}

            return app
    finally:
        # Restore original PYTEST_CURRENT_TEST value if it existed
        if original_pytest_current_test is not None:
            os.environ["PYTEST_CURRENT_TEST"] = original_pytest_current_test


@pytest.fixture(scope="module")
def client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    """
    Fixture to create a TestClient for the FastAPI application.
    """
    with TestClient(test_app) as c:
        yield c


class TestOpenTelemetryInstrumentation:
    """
    Tests for verifying OpenTelemetry auto-instrumentation of FastAPI routes
    and traceparent header propagation.
    """

    def test_fastapi_route_is_instrumented_and_traceparent_propagated(self, client: TestClient) -> None:
        """
        Tests if a FastAPI route is instrumented and if the traceparent header is present in responses
        when a traceparent is provided in the request.

        :param client: TestClient for the FastAPI application.
        :type client: TestClient
        """
        # Arrange: Define a traceparent header
        # Example traceparent: version-trace_id-parent_id-trace_flags
        # 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
        trace_id = "0af7651916cd43dd8448eb211c80319c"
        parent_id = "b7ad6b7169203331"
        headers = {
            "traceparent": f"00-{trace_id}-{parent_id}-01"
        }

        # Act: Make a request to an instrumented endpoint
        response = client.get("/test-otel", headers=headers)

        # Assert: Check for successful response and traceparent header
        assert response.status_code == 200
        assert "traceparent" in response.headers
        # The response traceparent should have the same trace_id but a new span_id (parent_id for the next hop)
        response_traceparent = response.headers["traceparent"]
        assert response_traceparent.startswith(f"00-{trace_id}-")
        assert parent_id not in response_traceparent  # The span_id part should be new

    def test_fastapi_route_generates_traceparent_if_none_provided(self, client: TestClient) -> None:
        """
        Tests if a FastAPI route generates a new traceparent header if none is provided in the request.

        :param client: TestClient for the FastAPI application.
        :type client: TestClient
        """
        # Act: Make a request to an instrumented endpoint without a traceparent header
        response = client.get("/test-otel")

        # Assert: Check for successful response and a newly generated traceparent header
        assert response.status_code == 200
        assert "traceparent" in response.headers
        response_traceparent = response.headers["traceparent"]
        # Validate basic format: version-trace_id-span_id-trace_flags
        parts = response_traceparent.split('-')
        assert len(parts) == 4
        assert parts[0] == "00"  # Version
        assert len(parts[1]) == 32  # Trace ID
        assert len(parts[2]) == 16  # Span ID
        assert len(parts[3]) == 2  # Trace Flags


class TestOpenTelemetryExporterConfiguration:
    """
    Tests for verifying the configuration of OTLP exporters
    based on environment variables.
    """

    @patch('os.environ.get')
    @patch('opentelemetry.sdk.resources.Resource') # Mock Resource to avoid side effects
    @patch('opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter')
    @patch('opentelemetry.sdk.trace.TracerProvider') # Mock TracerProvider
    @patch('opentelemetry.sdk.trace.export.BatchSpanProcessor')
    @patch('opentelemetry.trace.set_tracer_provider')
    def test_otlp_trace_exporter_configured_via_env_var(
        self,
        mock_set_tracer_provider: MagicMock,
        mock_batch_span_processor: MagicMock,
        mock_tracer_provider: MagicMock, # Added
        mock_otlp_span_exporter: MagicMock,
        mock_resource: MagicMock, # Added
        mock_os_environ_get: MagicMock,
    ) -> None:
        """
        Tests if the OTLP trace exporter is configured when
        OTEL_EXPORTER_OTLP_TRACES_ENDPOINT is set.
        """
        # Arrange
        mock_collector_endpoint = "http://localhost:4317/v1/traces" # More specific endpoint
        def side_effect(key: str, default: Any = None) -> str | None:
            mock_values = {
                "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": mock_collector_endpoint,
                "OTEL_SERVICE_NAME": "test-service-trace",
                "PYTEST_CURRENT_TEST": ""
            }
            return mock_values.get(key, default)

        mock_os_environ_get.side_effect = side_effect

        # Mock the return_value for TracerProvider to be itself a mock
        # This helps in asserting calls on the instance if needed, and controlling its behavior.
        mock_tracer_provider_instance = mock_tracer_provider.return_value
        mock_resource_instance = mock_resource.return_value

        # Act: Re-run setup with mocked environment
        app = FastAPI() # Create a fresh app for this test
        setup_opentelemetry(app)

        # Assert
        mock_os_environ_get.assert_any_call("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", None)
        mock_os_environ_get.assert_any_call("OTEL_SERVICE_NAME", "ainative-default-fastapi-service")

        mock_resource.assert_called_once_with(attributes={'service.name': 'test-service-trace'})
        mock_otlp_span_exporter.assert_called_once_with(endpoint=mock_collector_endpoint)
        # Check that BatchSpanProcessor was called with the span exporter instance
        # and the specific queue/batch sizes if IS_TEST_MODE is false
        mock_batch_span_processor.assert_called_once_with(
            mock_otlp_span_exporter.return_value,
            max_queue_size=2048, # Default from opentelemetry_config
            max_export_batch_size=512 # Default from opentelemetry_config
        )
        mock_tracer_provider.assert_called_once_with(resource=mock_resource_instance)
        mock_tracer_provider_instance.add_span_processor.assert_called_once_with(mock_batch_span_processor.return_value)
        mock_set_tracer_provider.assert_called_once_with(mock_tracer_provider_instance)

    @patch('os.environ.get')
    @patch('opentelemetry.sdk.resources.Resource')
    @patch('opentelemetry.exporter.otlp.proto.grpc.metric_exporter.OTLPMetricExporter')
    @patch('opentelemetry.sdk.metrics.MeterProvider')
    @patch('opentelemetry.sdk.metrics.export.PeriodicExportingMetricReader')
    @patch('opentelemetry.metrics.set_meter_provider')
    def test_otlp_metrics_exporter_configured_via_env_var(
        self,
        mock_set_meter_provider: MagicMock,
        mock_periodic_exporting_metric_reader: MagicMock, # Added
        mock_meter_provider: MagicMock,
        mock_otlp_metric_exporter: MagicMock,
        mock_resource: MagicMock, # Added
        mock_os_environ_get: MagicMock,
    ) -> None:
        """
        Tests if the OTLP metrics exporter is configured when
        OTEL_EXPORTER_OTLP_METRICS_ENDPOINT is set.
        """
        # Arrange
        mock_collector_endpoint = "http://localhost:4317/v1/metrics"
        def side_effect(key: str, default: Any = None) -> str | None:
            mock_values = {
                "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT": mock_collector_endpoint,
                "OTEL_SERVICE_NAME": "test-service-metrics",
                "PYTEST_CURRENT_TEST": ""
            }
            return mock_values.get(key, default)

        mock_os_environ_get.side_effect = side_effect
        mock_meter_provider_instance = mock_meter_provider.return_value
        mock_resource_instance = mock_resource.return_value

        # Act: Re-run setup
        app = FastAPI()
        setup_opentelemetry(app)

        # Assert
        mock_os_environ_get.assert_any_call("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT", None)
        mock_resource.assert_called_once_with(attributes={'service.name': 'test-service-metrics'})
        mock_otlp_metric_exporter.assert_called_once_with(endpoint=mock_collector_endpoint)
        mock_periodic_exporting_metric_reader.assert_called_once_with(mock_otlp_metric_exporter.return_value)
        mock_meter_provider.assert_called_once_with(
            resource=mock_resource_instance,
            metric_readers=[mock_periodic_exporting_metric_reader.return_value]
        )
        mock_set_meter_provider.assert_called_once_with(mock_meter_provider_instance)

    @patch('os.environ.get')
    @patch('opentelemetry.sdk.resources.Resource')
    @patch('opentelemetry.exporter.otlp.proto.grpc._log_exporter.OTLPLogExporter') # Path to OTLPLogExporter might vary based on stable/beta
    @patch('opentelemetry.sdk._logs.LoggerProvider') # Path to LoggerProvider
    @patch('opentelemetry.sdk._logs.export.BatchLogRecordProcessor') # Path to BatchLogRecordProcessor
    @patch('opentelemetry.sdk._logs.LoggingHandler') # Path to LoggingHandler
    @patch('opentelemetry._logs.set_logger_provider') # Path to set_logger_provider
    def test_otlp_logs_exporter_configured_via_env_var(
        self,
        mock_set_logger_provider: MagicMock,
        mock_logging_handler: MagicMock, # Added
        mock_batch_log_processor: MagicMock,
        mock_logger_provider: MagicMock,
        mock_otlp_log_exporter: MagicMock,
        mock_resource: MagicMock, # Added
        mock_os_environ_get: MagicMock,
    ) -> None:
        """
        Tests if the OTLP logs exporter is configured when
        OTEL_EXPORTER_OTLP_LOGS_ENDPOINT is set.
        """
        # Arrange
        mock_collector_endpoint = "http://localhost:4317/v1/logs"
        def side_effect(key: str, default: Any = None) -> str | None:
            mock_values = {
                "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": mock_collector_endpoint,
                "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": "http://localhost:4317/v1/traces",
                "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT": "http://localhost:4317/v1/metrics",
                "OTEL_SERVICE_NAME": "test-service-logs",
                "PYTEST_CURRENT_TEST": ""
            }
            return mock_values.get(key, default)

        mock_os_environ_get.side_effect = side_effect

        # Ensure the correct LoggerProvider and related components are used if your code has logic for stable/beta
        # Forcing one path for the test if necessary, or mocking the import checks.
        # Here, assuming the stable path is taken due to patch order or default availability.
        mock_logger_provider_instance = mock_logger_provider.return_value
        mock_resource_instance = mock_resource.return_value

        # Act: Re-run setup
        app = FastAPI()
        setup_opentelemetry(app)

        # Assert
        mock_os_environ_get.assert_any_call("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", None)
        mock_resource.assert_called_once_with(attributes={'service.name': 'test-service-logs'})
        mock_otlp_log_exporter.assert_called_once_with(endpoint=mock_collector_endpoint)
        mock_batch_log_processor.assert_called_once_with(
            mock_otlp_log_exporter.return_value,
            max_queue_size=2048, # Default from opentelemetry_config
            max_export_batch_size=512 # Default from opentelemetry_config
        )
        mock_logger_provider.assert_called_once_with(resource=mock_resource_instance)
        mock_logger_provider_instance.add_log_record_processor.assert_called_once_with(mock_batch_log_processor.return_value)
        mock_set_logger_provider.assert_called_once_with(mock_logger_provider_instance)
        # Assert that LoggingHandler was instantiated and added
        mock_logging_handler.assert_called_once_with(level=logging.NOTSET, logger_provider=mock_logger_provider_instance)
        # You might need to also mock logging.getLogger().addHandler if you want to assert it was called
