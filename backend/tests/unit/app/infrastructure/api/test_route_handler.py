"""
Unit tests for the API route handlers with MCP integration.

These tests verify that our route handlers correctly:
- Use typed Pydantic models for requests and responses
- Support OpenAPI documentation
- Use Problem Details error format (RFC 7807)
- Expose endpoints as Model Context Protocol (MCP) tools
- Include proper authentication
"""

import pytest
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Any, Dict, List, Optional, Literal, Union
from unittest.mock import patch, MagicMock

# Import the module to be tested
from ainative.app.infrastructure.api.route_handler import (
    router,
    AgentRequest,
    AgentResponse,
    OperationResponse,
    ErrorResponse,
    create_agent,
    get_agent,
    list_agents,
    update_agent,
    delete_agent,
    MCPTool,
    requires_auth
)

# Define HTTP reason phrases since starlette.status doesn't have them
HTTP_REASON_PHRASES = {
    404: "Not Found",
    422: "Unprocessable Entity",
    500: "Internal Server Error",
    # Add other status codes as needed
}

# Fixtures for testing
@pytest.fixture
def test_app():
    """Create FastAPI test application with the router."""
    app = FastAPI()

    # Add exception handlers to match the main app configuration
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        error = ErrorResponse(
            type=f"https://ainative.dev/errors/{exc.status_code}",
            title=HTTP_REASON_PHRASES.get(exc.status_code, "Error"),
            status=exc.status_code,
            detail=str(exc.detail),
            instance=request.url.path
        )
        return JSONResponse(status_code=exc.status_code, content=error.model_dump())

    # Add validation error handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        error = ErrorResponse(
            type="https://ainative.dev/errors/validation",
            title="Validation Error",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more validation errors occurred.",
            instance=request.url.path,
            validation_errors=errors
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error.model_dump()
        )

    app.include_router(router)
    return app


@pytest.fixture
def client(test_app):
    """Create test client for the FastAPI application."""
    return TestClient(test_app)


@pytest.fixture
def valid_agent_request():
    """Return a valid agent creation request."""
    return {
        "name": "test_agent",
        "description": "Test agent for unit tests",
        "agent_type": "llm",
        "config": {
            "model": "mistral-7b-instruct",
            "temperature": 0.7,
            "max_tokens": 1024
        },
    }


@pytest.fixture
def valid_agent_response():
    """Return a valid agent response."""
    return {
        "id": "agent123",
        "name": "test_agent",
        "description": "Test agent for unit tests",
        "agent_type": "llm",
        "config": {
            "model": "mistral-7b-instruct",
            "temperature": 0.7,
            "max_tokens": 1024
        },
        "status": "active",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_agent_service():
    """Mock the agent service."""
    with patch("ainative.app.infrastructure.api.route_handler.agent_service") as mock:
        yield mock


# Tests for the route handlers

def test_create_agent_with_valid_data(client, valid_agent_request, mock_agent_service, valid_agent_response):
    """
    Test creating an agent with valid data returns 201 Created and the agent details.

    Arrange:
        - Set up test client
        - Create valid agent request data
        - Mock agent service to return success

    Act:
        - Call POST /agents endpoint

    Assert:
        - Response status code is 201
        - Response body contains agent data
        - Mock service was called with correct parameters
    """
    # Arrange
    mock_agent_service.create_agent.return_value = valid_agent_response

    # Act
    response = client.post("/agents", json=valid_agent_request)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == "agent123"
    assert data["name"] == valid_agent_request["name"]
    assert data["agent_type"] == valid_agent_request["agent_type"]
    mock_agent_service.create_agent.assert_called_once_with(AgentRequest(**valid_agent_request))


def test_create_agent_with_invalid_data(client):
    """
    Test creating an agent with invalid data returns 422 Validation Error.

    Arrange:
        - Set up test client
        - Create invalid agent request with missing required fields

    Act:
        - Call POST /agents endpoint

    Assert:
        - Response status code is 422
        - Response body follows Problem Details error format
        - Response contains validation error details
    """
    # Arrange
    invalid_request = {
        "name": "test_agent",
        # Missing required fields
    }

    # Act
    response = client.post("/agents", json=invalid_request)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "type" in data  # Problem Details format
    assert "title" in data
    assert "detail" in data
    assert "validation_errors" in data


def test_get_agent_by_id(client, mock_agent_service, valid_agent_response):
    """
    Test getting an agent by ID returns 200 OK and the agent details.

    Arrange:
        - Set up test client
        - Mock agent service to return the agent

    Act:
        - Call GET /agents/{agent_id} endpoint

    Assert:
        - Response status code is 200
        - Response body contains agent data
        - Mock service was called with correct agent ID
    """
    # Arrange
    agent_id = "agent123"
    mock_agent_service.get_agent.return_value = valid_agent_response

    # Act
    response = client.get(f"/agents/{agent_id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == agent_id
    mock_agent_service.get_agent.assert_called_once_with(agent_id)


def test_get_nonexistent_agent(client, mock_agent_service):
    """
    Test getting a non-existent agent returns 404 Not Found.

    Arrange:
        - Set up test client
        - Mock agent service to raise an exception for non-existent agent

    Act:
        - Call GET /agents/{agent_id} endpoint with an invalid ID

    Assert:
        - Response status code is 404
        - Response body follows Problem Details error format
    """
    # Arrange
    agent_id = "nonexistent"
    mock_agent_service.get_agent.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Agent with ID {agent_id} not found"
    )

    # Act
    response = client.get(f"/agents/{agent_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "type" in data
    assert "title" in data
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_list_agents(client, mock_agent_service, valid_agent_response):
    """
    Test listing agents returns 200 OK and the list of agents.

    Arrange:
        - Set up test client
        - Mock agent service to return a list of agents

    Act:
        - Call GET /agents endpoint

    Assert:
        - Response status code is 200
        - Response body contains a list of agents
    """
    # Arrange
    mock_agent_service.list_agents.return_value = [valid_agent_response]

    # Act
    response = client.get("/agents")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == valid_agent_response["id"]


def test_update_agent(client, valid_agent_request, mock_agent_service, valid_agent_response):
    """
    Test updating an agent returns 200 OK and the updated agent details.

    Arrange:
        - Set up test client
        - Mock agent service to return the updated agent

    Act:
        - Call PUT /agents/{agent_id} endpoint

    Assert:
        - Response status code is 200
        - Response body contains updated agent data
        - Mock service was called with correct parameters
    """
    # Arrange
    agent_id = "agent123"
    update_data = valid_agent_request.copy()
    update_data["description"] = "Updated description"
    mock_agent_service.update_agent.return_value = {**valid_agent_response, "description": "Updated description"}

    # Act
    response = client.put(f"/agents/{agent_id}", json=update_data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == agent_id
    assert data["description"] == "Updated description"
    mock_agent_service.update_agent.assert_called_once_with(agent_id, AgentRequest(**update_data))


def test_delete_agent(client, mock_agent_service):
    """
    Test deleting an agent returns 200 OK and success message.

    Arrange:
        - Set up test client
        - Mock agent service for deletion

    Act:
        - Call DELETE /agents/{agent_id} endpoint

    Assert:
        - Response status code is 200
        - Response body contains success status
        - Mock service was called with correct agent ID
    """
    # Arrange
    agent_id = "agent123"
    mock_agent_service.delete_agent.return_value = {"status": "success", "message": f"Agent {agent_id} deleted"}

    # Act
    response = client.delete(f"/agents/{agent_id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    mock_agent_service.delete_agent.assert_called_once_with(agent_id)


# Test MCP integration

def test_mcp_tools_registration(test_app):
    """
    Test that endpoints are properly registered as MCP tools.

    Arrange:
        - Set up test application

    Act:
        - Get OpenAPI schema from app

    Assert:
        - Schema contains MCP extensions for endpoints
        - Auth requirements are specified in schema
    """
    # Arrange & Act
    openapi_schema = test_app.openapi()

    # Assert
    # Check paths for MCP tool metadata
    paths = openapi_schema.get("paths", {})
    for path, path_item in paths.items():
        if path.startswith("/agents"):
            for method, operation in path_item.items():
                if method in ["get", "post", "put", "delete"]:
                    extensions = operation.get("x-mcp", {})
                    assert "tool_name" in extensions
                    assert "description" in extensions
                    # Check auth requirements
                    security = operation.get("security", [])
                    assert len(security) > 0  # Should have security requirements
