"""
Tests for the Loguru logging setup in FastAPI.
Verifies structured JSON logging, dual routing (file and OTel),
context binding, and custom OTel handler transformation.
"""
import json
import uuid
import logging # Standard logging, to avoid conflict with loguru's logger
from typing import Any, Dict, List, Generator, cast

import pytest
from fastapi import FastAPI, Request, Response, Header # Import Header
from fastapi.routing import APIRoute
from starlette.testclient import TestClient # Changed from httpx
from loguru import logger as loguru_logger # Renamed to avoid conflict

# --- Mocks and Test Fixtures ---

# Mock for the OTel Log Exporter/Processor
class MockOTelLogHandler:
    """
    A mock handler to simulate sending logs via OpenTelemetry.
    It stores the records it receives.
    """
    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def emit(self, record: Dict[str, Any]) -> None:
        """Simulates emitting a log record, stores the transformed record."""
        # In a real scenario, 'record' would be an OTel LogData object
        # For this test, we assume the custom handler transforms it into a dict
        # that represents the OTel LogData structure.
        self.records.append(record)

@pytest.fixture(scope="function")
def mock_otel_handler() -> MockOTelLogHandler:
    """Provides a new instance of the mock OTel handler for each test."""
    return MockOTelLogHandler()

@pytest.fixture(scope="function")
def temp_log_file(tmp_path: Any) -> str:
    """Provides a temporary file path for file-based logging."""
    return str(tmp_path / "test_app.log")

# This would ideally be in your application's logging configuration module
# For the test, we define it here.
def setup_loguru_for_test(
    file_path: str, otel_handler: MockOTelLogHandler
) -> List[int]:
    """
    Configures Loguru for testing.
    - Adds a JSON file sink.
    - Adds a custom sink that uses the mock OTel handler.
    - Returns handler IDs for later removal.

    Args:
        file_path: Path to the log file.
        otel_handler: The mock OTel handler instance.

    Returns:
        A list of handler IDs that were added.
    """
    loguru_logger.remove() # Remove default handlers

    # 1. File Sink (JSON structured)
    file_handler_id = loguru_logger.add(
        file_path,
        serialize=True,  # Output as JSON
        level="INFO",
        enqueue=True, # Important for async or multiprocessing
        encoding="utf-8"  # Specify UTF-8 encoding to fix encoding issues
    )

    # Custom Loguru record to OTel LogData-like dict transformation
    # In a real app, this would convert to OTel's LogData model
    def transform_for_otel(record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms a Loguru record dict into a structure
        that our MockOTelLogHandler expects (simulating OTel LogData).
        """
        # Example transformation: select/rename fields for OTel
        transformed = {
            "severity_text": record["level"].name,
            "severity_number": record["level"].no,
            "body": record["message"],
            "timestamp_unix_nano": int(record["time"].timestamp() * 1e9),
            "attributes": {
                key: value
                for key, value in record["extra"].items()
                # Add other relevant fields from record if needed
                # e.g., record["name"], record["function"], record["line"]
            }
        }
        if "correlation_id" in record["extra"]:
            transformed["attributes"]["correlation_id"] = record["extra"]["correlation_id"]
        if "user_id" in record["extra"]:
            transformed["attributes"]["user_id"] = record["extra"]["user_id"]
        if "request_path" in record["extra"]:
            transformed["attributes"]["request_path"] = record["extra"]["request_path"]
        if "status_code" in record["extra"]:
            transformed["attributes"]["status_code"] = record["extra"]["status_code"]
        return transformed

    # 2. OTel Sink (using the mock handler)
    # This sink demonstrates the custom handler transforming the record
    def otel_sink(message: Any) -> None: # message is actually a loguru.Message
        log_record_dict = message.record
        transformed_record = transform_for_otel(log_record_dict)
        otel_handler.emit(transformed_record)

    otel_handler_id = loguru_logger.add(
        otel_sink,
        level="INFO",
        enqueue=True
    )
    return [file_handler_id, otel_handler_id]


@pytest.fixture(scope="function")
def configured_logger(
    temp_log_file: str, mock_otel_handler: MockOTelLogHandler
) -> Generator[None, None, None]:
    """
    Sets up and tears down Loguru configuration for a test.
    """
    handler_ids = setup_loguru_for_test(temp_log_file, mock_otel_handler)
    yield
    for handler_id in handler_ids:
        loguru_logger.remove(handler_id)
    # Ensure the global logger is clean for other tests if any
    loguru_logger.remove()
    loguru_logger.add(logging.StreamHandler(), level="INFO") # Add back a default


# --- FastAPI Test App Setup ---

class LoggingRoute(APIRoute):
    """Custom route class to enable logging of status_code."""
    def get_route_handler(self) -> Any:
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            response: Response = await original_handler(request)
            # This is a simplified way to get status_code for logging.
            # A more robust solution would be middleware.
            request.state.status_code = response.status_code
            return response
        return custom_handler

app = FastAPI(route_class=LoggingRoute)

# Renamed the endpoint to avoid pytest treating it as a test
@app.get("/test-log")
async def log_endpoint(
    request: Request,
    # Explicitly define x_correlation_id as a header parameter
    # Use alias to match the exact header name being sent by the client
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID")
):
    """
    An endpoint that logs a message with context.
    """
    # In a real app, correlation_id and user_id would likely come from middleware
    # and be available in request.state or a contextvar.
    # Now x_correlation_id should correctly receive the value from the "X-Correlation-ID" header
    correlation_id = x_correlation_id or str(uuid.uuid4())
    user_id = "test-user-123" # Example user_id
    request_path = request.url.path

    # Simulate status_code being available after response (or set by middleware)
    # For this test, we'll bind it before logging.
    # In a real app, this might be logged by middleware *after* the response.
    status_code = getattr(request.state, "status_code", 200)

    # Bind context for Loguru
    # Note: status_code might be more accurately logged in middleware after response
    bound_logger = loguru_logger.bind(
        correlation_id=correlation_id,
        user_id=user_id,
        request_path=request_path,
        status_code=status_code # This is tricky, usually logged after response
    )
    bound_logger.info("Test log message from endpoint.")
    return {"message": "Log message sent", "correlation_id": correlation_id}

# --- Test Case ---

def test_loguru_fastapi_integration(
    configured_logger: Any, # Fixture to ensure logger is configured
    temp_log_file: str,
    mock_otel_handler: MockOTelLogHandler
) -> None:
    """
    Tests the Loguru setup within a FastAPI application.
    Verifies:
    1. Structured JSON logs are written to a file.
    2. Logs contain correlation_id, user_id, path, and status_code.
    3. Logs are routed to a mock OTel handler.
    4. The custom OTel handler transforms the log record.
    """
    # Arrange
    client = TestClient(app)
    test_correlation_id = f"test-corr-id-{uuid.uuid4()}"
    expected_user_id = "test-user-123"
    expected_path = "/test-log"
    expected_message = "Test log message from endpoint."

    # Act
    response = client.get(expected_path, headers={"X-Correlation-ID": test_correlation_id})
    assert response.status_code == 200
    # The status_code for the log will be 200 as set by the route handler logic

    # Assert - File Log
    # Use UTF-8 encoding when reading the file
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_lines = f.readlines()

    assert len(log_lines) == 1, "Expected one log line in the file."
    log_entry_full = json.loads(log_lines[0]) # This is the full { "text": "...", "record": { ... } } structure

    assert "record" in log_entry_full, "Log entry missing 'record' field. Keys: " + str(log_entry_full.keys())
    log_entry = log_entry_full["record"] # Access the nested record dictionary

    assert "time" in log_entry, "Top-level 'time' key missing in log_entry record. Keys: " + str(log_entry.keys())
    assert isinstance(log_entry["time"], dict), "'time' field should be a dictionary. Got: " + str(type(log_entry["time"]))
    assert "timestamp" in log_entry["time"], "Timestamp missing in file log's time object. Keys: " + str(log_entry["time"].keys())

    assert "level" in log_entry, "Level missing in log_entry record. Keys: " + str(log_entry.keys())
    assert log_entry["level"]["name"] == "INFO", "Log level incorrect in file log."

    assert "message" in log_entry, "Message missing in log_entry record. Keys: " + str(log_entry.keys())
    assert log_entry["message"] == expected_message, "Log message incorrect in file log."

    # Check for bound context in the 'extra' field of the serialized record
    assert "extra" in log_entry, "Extra missing in log_entry record. Keys: " + str(log_entry.keys())
    assert log_entry["extra"]["correlation_id"] == test_correlation_id, "Correlation ID mismatch in file log."
    assert log_entry["extra"]["user_id"] == expected_user_id, "User ID mismatch in file log."
    assert log_entry["extra"]["request_path"] == expected_path, "Request path mismatch in file log."
    assert log_entry["extra"]["status_code"] == 200, "Status code mismatch in file log."

    # Assert - Mock OTel Handler
    assert len(mock_otel_handler.records) == 1, "Mock OTel handler should have received one record."
    otel_record = mock_otel_handler.records[0]

    assert otel_record["severity_text"] == "INFO", "Severity text incorrect in OTel record."
    assert otel_record["body"] == expected_message, "Body incorrect in OTel record."
    assert "timestamp_unix_nano" in otel_record, "Timestamp missing in OTel record."

    assert "attributes" in otel_record, "Attributes missing in OTel record."
    attributes = cast(Dict[str, Any], otel_record["attributes"]) # Ensure type checker knows it's a dict
    assert attributes["correlation_id"] == test_correlation_id, "Correlation ID mismatch in OTel attributes."
    assert attributes["user_id"] == expected_user_id, "User ID mismatch in OTel attributes."
    assert attributes["request_path"] == expected_path, "Request path mismatch in OTel attributes."
    assert attributes["status_code"] == 200, "Status code mismatch in OTel attributes."

