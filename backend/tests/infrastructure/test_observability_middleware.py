"""
Tests for the Observability Middleware and associated exception handlers.
"""
import uuid  # For generating correlation IDs and UUID validation
import pytest  # For pytest.fail in tests
from typing import Any, Dict, Generator, cast

from fastapi import FastAPI, HTTPException, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# --- Import actual implementations ---
from ainative.app.middleware.observability import ObservabilityMiddleware
from ainative.app.exceptions import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

class Item(BaseModel):
    name: str
    price: float

# --- Test Setup ---

@pytest.fixture(scope="module")
def test_app() -> FastAPI:
    """Creates a FastAPI app instance with the middleware and handlers."""
    app = FastAPI()
    app.add_middleware(ObservabilityMiddleware)

    # Add exception handlers
    app.add_exception_handler(Exception, generic_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)

    @app.get("/test-route")
    async def read_test_route(request: Request) -> Dict[str, Any]:
        return {
            "message": "success",
            "correlation_id_in_state": getattr(request.state, "correlation_id", None),
            "logger_context": getattr(request.app.state, "logger_context", None),
            "otel_propagated": getattr(request.app.state, "otel_propagated", False),
        }

    @app.get("/http-exception")
    async def raise_http_exception() -> None:
        raise HTTPException(status_code=403, detail="Forbidden access")

    @app.get("/app-exception")
    async def raise_app_exception() -> None:
        raise AppException(detail="Custom app error occurred", status_code=400)

    @app.get("/unhandled-exception")
    async def raise_unhandled_exception() -> None:
        raise ValueError("Something went very wrong")

    @app.post("/validation-error")
    async def post_validation_error(item: Item) -> Item:
        return item

    @app.get("/manual-validation-error")
    async def get_manual_validation_error() -> None:
        try:
            Item(name="test", price="not-a-float")  # type: ignore
        except ValidationError as e:
            raise e

    return app

@pytest.fixture(scope="module")
def client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    """Provides a TestClient for the FastAPI app."""
    with TestClient(test_app) as c:
        yield c

# --- Tests ---

def test_correlation_id_provided_in_header(client: TestClient, mocker: Any) -> None:
    """Test X-Correlation-ID is used if provided in request headers."""
    test_correlation_id = str(uuid.uuid4())
    response = client.get("/test-route", headers={"X-Correlation-ID": test_correlation_id})

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == test_correlation_id
    json_response = response.json()
    assert json_response["correlation_id_in_state"] == test_correlation_id
    assert json_response["otel_propagated"] is True

def test_correlation_id_generated_if_missing(client: TestClient, mocker: Any) -> None:
    """Test a new X-Correlation-ID is generated if not in request headers."""
    response = client.get("/test-route")

    assert response.status_code == 200
    generated_correlation_id = response.headers.get("X-Correlation-ID")
    assert generated_correlation_id is not None
    try:
        uuid.UUID(generated_correlation_id)
    except ValueError:
        pytest.fail("Generated correlation ID is not a valid UUID.")

    json_response = response.json()
    assert json_response["correlation_id_in_state"] == generated_correlation_id
    assert json_response["otel_propagated"] is True

def test_http_exception_handler(client: TestClient, mocker: Any) -> None:
    """Test the HTTPException handler."""
    mocker.patch.object(client.app.state, "last_error_log", create=True)

    response = client.get("/http-exception")

    assert response.status_code == 403
    json_response = response.json()
    assert json_response["type"] == "/errors/http/403"
    assert json_response["title"] == "HTTP Error"
    assert json_response["status"] == 403
    assert json_response["detail"] == "Forbidden access"
    assert "instance" in json_response
    correlation_id = response.headers.get("X-Correlation-ID")
    assert json_response["correlation_id"] == correlation_id

def test_app_exception_handler(client: TestClient, mocker: Any) -> None:
    """Test the custom AppException handler."""
    mocker.patch.object(client.app.state, "last_error_log", create=True)

    response = client.get("/app-exception")

    assert response.status_code == 400
    json_response = response.json()
    assert json_response["type"] == "/errors/application-specific-error"
    assert json_response["title"] == "Application Specific Error"
    assert json_response["status"] == 400
    assert json_response["detail"] == "Custom app error occurred"
    correlation_id = response.headers.get("X-Correlation-ID")
    assert json_response["correlation_id"] == correlation_id

def test_unhandled_exception_handler(client: TestClient, mocker: Any) -> None:
    """Test the generic unhandled exception handler."""
    mocker.patch.object(client.app.state, "last_error_log", create=True)

    response = client.get("/unhandled-exception")

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    json_response = response.json()
    assert json_response["type"] == "/errors/internal-server-error"
    assert json_response["title"] == "Internal Server Error"
    assert json_response["status"] == HTTP_500_INTERNAL_SERVER_ERROR
    assert json_response["detail"] == "An unexpected error occurred."
    correlation_id = response.headers.get("X-Correlation-ID")
    assert json_response["correlation_id"] == correlation_id

def test_request_validation_error_handler(client: TestClient, mocker: Any) -> None:
    """Test FastAPI's RequestValidationError handler (if overridden, or Pydantic ValidationError)."""
    mocker.patch.object(client.app.state, "last_error_log", create=True)

    response = client.get("/manual-validation-error")

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    json_response = response.json()
    assert json_response["type"] == "/errors/validation-error"
    assert json_response["title"] == "Validation Error"
    assert json_response["status"] == HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(json_response["detail"], list)
    assert len(json_response["detail"]) > 0

    correlation_id = response.headers.get("X-Correlation-ID")
    assert json_response["correlation_id"] == correlation_id

def test_fastapi_request_validation_error_default_behavior(client: TestClient) -> None:
    """Test FastAPI's default RequestValidationError for RFC 7807 like structure."""
    invalid_payload = {"name": "Test Item"}
    response = client.post("/validation-error", json=invalid_payload)

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    json_response = response.json()
    assert "detail" in json_response
    assert isinstance(json_response["detail"], list)
    assert len(json_response["detail"]) > 0
    assert json_response["detail"][0]["type"] == "missing"
    assert json_response["detail"][0]["loc"] == ["body", "price"]

    assert "X-Correlation-ID" in response.headers
