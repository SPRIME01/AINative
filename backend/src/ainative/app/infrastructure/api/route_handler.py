"""
API route handlers for Agent management with MCP integration.

This module provides FastAPI route handlers for creating, retrieving, updating,
and deleting AI Agents in the Edge AI Orchestrator. The routes follow RESTful
design principles and expose endpoints as Model Context Protocol (MCP) tools.

Features:
- Typed request and response models using Pydantic
- Full OpenAPI auto-docs support
- RFC 7807 Problem Details error responses
- Comprehensive type hinting
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Literal, Union, Callable
import functools

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict

# Set up logging
logger = logging.getLogger(__name__)

# Dependency placeholder (would be replaced by actual service)
class AgentService:
    """Placeholder service for agent operations."""

    def create_agent(self, agent: Any) -> Dict[str, Any]:
        """Create a new agent."""
        return {"id": "agent123", "name": "test_agent"}

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get an agent by ID."""
        return {"id": agent_id, "name": "test_agent"}

    def list_agents(self, **kwargs) -> List[Dict[str, Any]]:
        """List agents with optional filtering."""
        return [{"id": "agent123", "name": "test_agent"}]

    def update_agent(self, agent_id: str, agent: Any) -> Dict[str, Any]:
        """Update an existing agent."""
        return {"id": agent_id, "name": agent.name}

    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """Delete an agent."""
        return {"status": "success", "message": f"Agent {agent_id} deleted"}


agent_service = AgentService()

# Model definitions
class AgentType(str, Enum):
    LLM = "llm"
    VISION = "vision"
    MULTIMODAL = "multimodal"
    FUNCTION = "function"


class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    INITIALIZING = "initializing"


class AgentConfig(BaseModel):
    model: str = Field(..., description="Name of the AI model to use")
    temperature: float = Field(0.7, description="Temperature for sampling (0.0-1.0)", ge=0.0, le=1.0)
    max_tokens: int = Field(1024, description="Maximum tokens in generated responses")
    additional_config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration parameters")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "mistral-7b-instruct",
                "temperature": 0.7,
                "max_tokens": 1024,
                "additional_config": {"stream": True}
            }
        }
    )


class AgentRequest(BaseModel):
    name: str = Field(..., description="Name of the agent", min_length=1, max_length=100)
    description: str = Field("", description="Description of the agent's purpose")
    agent_type: AgentType = Field(..., description="Type of agent")
    config: AgentConfig = Field(..., description="Agent configuration parameters")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "text_summarizer",
                "description": "Summarizes long text into bullet points",
                "agent_type": "llm",
                "config": {
                    "model": "mistral-7b-instruct",
                    "temperature": 0.5,
                    "max_tokens": 512
                }
            }
        }
    )


class AgentResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="Name of the agent")
    description: str = Field("", description="Description of the agent's purpose")
    agent_type: AgentType = Field(..., description="Type of agent")
    config: AgentConfig = Field(..., description="Agent configuration parameters")
    status: AgentStatus = Field(AgentStatus.INACTIVE, description="Current status of the agent")
    created_at: datetime = Field(..., description="When the agent was created")
    updated_at: datetime = Field(..., description="When the agent was last updated")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "agent123",
                "name": "text_summarizer",
                "description": "Summarizes long text into bullet points",
                "agent_type": "llm",
                "config": {
                    "model": "mistral-7b-instruct",
                    "temperature": 0.5,
                    "max_tokens": 512
                },
                "status": "active",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }
    )


class OperationResponse(BaseModel):
    status: Literal["success", "error"] = Field(..., description="Operation status")
    message: str = Field(..., description="Message describing the operation result")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "Agent deleted successfully"
            }
        }
    )


class ErrorResponse(BaseModel):
    type: str = Field(..., description="URI reference identifying the problem type")
    title: str = Field(..., description="Short, human-readable summary of the problem")
    status: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Human-readable explanation of the problem")
    instance: Optional[str] = Field(None, description="URI reference to the specific occurrence")
    validation_errors: Optional[List[Dict[str, Any]]] = Field(None, description="Validation errors, if applicable")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "https://ainative.dev/errors/validation",
                "title": "Validation Error",
                "status": 422,
                "detail": "One or more validation errors occurred.",
                "instance": "/agents",
                "validation_errors": [
                    {"field": "name", "error": "Field is required"}
                ]
            }
        }
    )


# Router setup
router = APIRouter(prefix="/agents", tags=["Agents"])


# Define a decorator to add OpenAPI extensions
def add_openapi_extension(name: str, value: Any):
    def decorator(func: Callable) -> Callable:
        if not hasattr(func, "openapi_extra"):
            func.openapi_extra = {}
        func.openapi_extra[name] = value
        return func
    return decorator


# Define custom MCP decorator
def MCPTool(tool_name: str, description: str):
    def decorator(func: Callable) -> Callable:
        tool_data = {"tool_name": tool_name, "description": description}
        return add_openapi_extension("x-mcp", tool_data)(func)
    return decorator


def requires_auth(scopes: List[str]):
    def decorator(func: Callable) -> Callable:
        security_data = [{"OAuth2": scopes}]
        return add_openapi_extension("security", security_data)(func)
    return decorator


# Route handlers

@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Agent created successfully"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Create a new agent",
    description="Creates a new AI agent with the specified configuration.",
    openapi_extra={"x-mcp": {"tool_name": "create_agent", "description": "Creates a new AI agent with the specified configuration"},
                   "security": [{"OAuth2": ["agents:write"]}]}
)
async def create_agent(agent: AgentRequest) -> AgentResponse:
    logger.info(f"Creating agent: {agent.name}")
    try:
        result = agent_service.create_agent(agent)
        response = AgentResponse(
            id=result.get("id", "agent123"),
            name=agent.name,
            description=agent.description,
            agent_type=agent.agent_type,
            config=agent.config,
            status=AgentStatus.ACTIVE,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return response
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )


@router.get(
    "",
    response_model=List[AgentResponse],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of agents retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="List all agents",
    description="Retrieves a list of all agents in the system.",
    openapi_extra={"x-mcp": {"tool_name": "list_agents", "description": "Lists all available AI agents"},
                   "security": [{"OAuth2": ["agents:read"]}]}
)
async def list_agents(
    type_filter: Optional[AgentType] = Query(None, description="Filter agents by type"),
    status_filter: Optional[AgentStatus] = Query(None, description="Filter agents by status"),
    limit: int = Query(100, description="Maximum number of agents to return", ge=1, le=1000),
    offset: int = Query(0, description="Number of agents to skip", ge=0),
) -> List[AgentResponse]:
    logger.info(f"Listing agents (filters: type={type_filter}, status={status_filter})")
    try:
        agents_data = agent_service.list_agents(
            type_filter=type_filter,
            status_filter=status_filter,
            limit=limit,
            offset=offset
        )
        responses = []
        for agent_data in agents_data:
            responses.append(AgentResponse(
                id=agent_data.get("id", "agent123"),
                name=agent_data.get("name", "default_agent"),
                description=agent_data.get("description", ""),
                agent_type=agent_data.get("agent_type", AgentType.LLM),
                config=AgentConfig(
                    model=agent_data.get("model", "default_model"),
                    temperature=agent_data.get("temperature", 0.7),
                    max_tokens=agent_data.get("max_tokens", 1024)
                ),
                status=agent_data.get("status", AgentStatus.ACTIVE),
                created_at=agent_data.get("created_at", datetime.now()),
                updated_at=agent_data.get("updated_at", datetime.now())
            ))
        return responses
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {str(e)}"
        )


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Agent retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Agent not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get agent by ID",
    description="Retrieves a specific agent by its ID.",
    openapi_extra={"x-mcp": {"tool_name": "get_agent", "description": "Retrieves details about a specific agent by ID"},
                 "security": [{"OAuth2": ["agents:read"]}]}
)
async def get_agent(
    agent_id: str = Path(..., description="ID of the agent to retrieve")
) -> AgentResponse:
    """
    Get a specific agent by its ID.

    This endpoint retrieves the details of a specific agent identified by its ID.

    Args:
        agent_id: The unique identifier of the agent

    Returns:
        AgentResponse: The requested agent's details

    Raises:
        HTTPException: If the agent is not found or there's an error

    Example:
        >>> import httpx
        >>> response = httpx.get("http://localhost:8000/agents/agent123")
        >>> response.status_code
        200
        >>> response.json()["id"]
        'agent123'
    """
    logger.info(f"Getting agent with ID: {agent_id}")
    try:
        try:
            # Call the service to get the agent - might raise HTTPException
            agent_data = agent_service.get_agent(agent_id)
        except HTTPException:
            # Re-raise HTTPException without wrapping it
            raise

        if not agent_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )

        # Create a valid AgentResponse
        response = AgentResponse(
            id=agent_data.get("id", agent_id),
            name=agent_data.get("name", "default_agent"),
            description=agent_data.get("description", ""),
            agent_type=agent_data.get("agent_type", AgentType.LLM),
            config=AgentConfig(
                model=agent_data.get("model", "default_model"),
                temperature=agent_data.get("temperature", 0.7),
                max_tokens=agent_data.get("max_tokens", 1024)
            ),
            status=agent_data.get("status", AgentStatus.ACTIVE),
            created_at=agent_data.get("created_at", datetime.now()),
            updated_at=agent_data.get("updated_at", datetime.now())
        )

        return response
    except HTTPException:
        # Let HTTP exceptions pass through without wrapping
        raise
    except Exception as e:
        logger.error(f"Error getting agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {str(e)}"
        )


@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Agent updated successfully"},
        404: {"model": ErrorResponse, "description": "Agent not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Update an agent",
    description="Updates an existing agent's configuration.",
    openapi_extra={"x-mcp": {"tool_name": "update_agent", "description": "Updates an existing agent's configuration"},
                   "security": [{"OAuth2": ["agents:write"]}]}
)
async def update_agent(
    agent_id: str = Path(..., description="ID of the agent to update"),
    agent: AgentRequest = None,
) -> AgentResponse:
    logger.info(f"Updating agent with ID: {agent_id}")
    try:
        updated_data = agent_service.update_agent(agent_id, agent)
        if not updated_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        response = AgentResponse(
            id=agent_id,
            name=agent.name,
            description=agent.description,
            agent_type=agent.agent_type,
            config=agent.config,
            status=AgentStatus.ACTIVE,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update agent: {str(e)}"
        )


@router.delete(
    "/{agent_id}",
    response_model=OperationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Agent deleted successfully"},
        404: {"model": ErrorResponse, "description": "Agent not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Delete an agent",
    description="Deletes an existing agent from the system.",
    openapi_extra={"x-mcp": {"tool_name": "delete_agent", "description": "Deletes an agent from the system"},
                   "security": [{"OAuth2": ["agents:write"]}]}
)
async def delete_agent(
    agent_id: str = Path(..., description="ID of the agent to delete")
) -> OperationResponse:
    logger.info(f"Deleting agent with ID: {agent_id}")
    try:
        result = agent_service.delete_agent(agent_id)
        response = OperationResponse(
            status="success",
            message=f"Agent {agent_id} deleted"
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete agent: {str(e)}"
        )
