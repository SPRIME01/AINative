"""
OpenTelemetry configuration for FastAPI application.

This module provides OpenTelemetry setup for our FastAPI application, including:
- Automatic instrumentation of routes for tracing
- Correlation headers (traceparent) propagation
- OTLP exporters for logs, metrics, and traces
- Configuration via environment variables

Environment variables:
    OTEL_SERVICE_NAME: Service name for OpenTelemetry resource (default: "ainative-backend")
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: OTLP gRPC endpoint for traces
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT: OTLP gRPC endpoint for metrics
    OTEL_EXPORTER_OTLP_LOGS_ENDPOINT: OTLP gRPC endpoint for logs
"""
import os
import logging
from typing import Optional

from fastapi import FastAPI

# OpenTelemetry SDK imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# OpenTelemetry FastAPI instrumentation
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# For Metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# For Logs - Using the internal _logs module as it's still experimental
from opentelemetry import _logs
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# Logger for the config module itself
logger = logging.getLogger(__name__)


def setup_opentelemetry(app: FastAPI) -> None:
    """
    Set up OpenTelemetry for a FastAPI application.

    This function:
    1. Creates a resource with service information
    2. Sets up trace, metric, and log providers if endpoints are configured
    3. Instruments the FastAPI application for automatic tracing

    :param app: The FastAPI application to instrument
    :type app: FastAPI
    :return: None

    :Example:

    ```python
    from fastapi import FastAPI
    from app.core.opentelemetry_config import setup_opentelemetry

    app = FastAPI()
    setup_opentelemetry(app)
    ```
    """
    # Skip if already instrumented (useful for testing)
    if hasattr(app, "_is_instrumented_by_otel") and app._is_instrumented_by_otel:
        logger.info("Application is already instrumented with OpenTelemetry")
        return

    # Ensure the propagator is set for context propagation
    from opentelemetry.propagate import set_global_textmap
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
    set_global_textmap(TraceContextTextMapPropagator())

    # Get service name from environment or use default
    service_name = os.environ.get("OTEL_SERVICE_NAME", "ainative-backend")

    # Create a resource with service information
    resource = Resource(attributes={
        "service.name": service_name,
        "service.namespace": "ainative",
        "service.version": "0.1.0",  # Should ideally be pulled from package metadata
    })

    # Setup tracing if endpoint is configured
    _setup_tracing(resource)

    # Setup metrics if endpoint is configured
    _setup_metrics(resource)

    # Setup logging if endpoint is configured
    _setup_logging(resource)

    # Instrument FastAPI with trace context propagation
    # Note: enable_response_header_propagation is not supported in the current version
    # Instead, we use record_exception_as_span_event=True which is a supported parameter
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=trace.get_tracer_provider(),
        excluded_urls="health,metrics",
        # Configure to record exceptions as span events for better observability
        record_exception_as_span_event=True
    )

    # Mark as instrumented to avoid re-instrumentation
    app._is_instrumented_by_otel = True
    logger.info(f"OpenTelemetry instrumentation completed for {service_name}")


def _setup_tracing(resource: Resource) -> None:
    """
    Set up OpenTelemetry tracing with the provided resource.

    :param resource: OpenTelemetry resource with service information
    :type resource: Resource
    :return: None
    """
    trace_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    if not trace_endpoint:
        logger.info("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT not set, skipping trace setup")
        return

    # Create a tracer provider with the resource
    tracer_provider = TracerProvider(resource=resource)

    # Create an OTLP span exporter
    span_exporter = OTLPSpanExporter(endpoint=trace_endpoint)

    # Add a BatchSpanProcessor to the tracer provider
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))

    # Set the global tracer provider
    trace.set_tracer_provider(tracer_provider)

    logger.info(f"OpenTelemetry tracing configured with endpoint: {trace_endpoint}")


def _setup_metrics(resource: Resource) -> None:
    """
    Set up OpenTelemetry metrics with the provided resource.

    :param resource: OpenTelemetry resource with service information
    :type resource: Resource
    :return: None
    """
    metrics_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT")
    if not metrics_endpoint:
        logger.info("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT not set, skipping metrics setup")
        return

    # Create an OTLP metric exporter
    metric_exporter = OTLPMetricExporter(endpoint=metrics_endpoint)

    # Create a PeriodicExportingMetricReader with the exporter
    metric_reader = PeriodicExportingMetricReader(
        exporter=metric_exporter,
        export_interval_millis=30000  # Export metrics every 30 seconds
    )

    # Create a meter provider with the resource and reader
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

    # Set the global meter provider
    metrics.set_meter_provider(meter_provider)

    logger.info(f"OpenTelemetry metrics configured with endpoint: {metrics_endpoint}")


def _setup_logging(resource: Resource) -> None:
    """
    Set up OpenTelemetry logging with the provided resource.

    :param resource: OpenTelemetry resource with service information
    :type resource: Resource
    :return: None
    """
    logs_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT")
    if not logs_endpoint:
        logger.info("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT not set, skipping logs setup")
        return

    # Create an OTLP log exporter
    log_exporter = OTLPLogExporter(endpoint=logs_endpoint)

    # Create a logger provider with the resource
    logger_provider = LoggerProvider(resource=resource)

    # Add a BatchLogRecordProcessor to the logger provider
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    # Set the global logger provider
    _logs.set_logger_provider(logger_provider)

    # Optionally integrate with Python's logging system
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)

    logger.info(f"OpenTelemetry logging configured with endpoint: {logs_endpoint}")
