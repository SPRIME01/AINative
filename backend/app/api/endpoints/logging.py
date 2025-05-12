from fastapi import APIRouter, Request, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from loguru import logger
import uuid

router = APIRouter()

class BrowserInfoPayload(BaseModel):
    """Browser information payload."""
    user_agent: Optional[str] = Field(None, alias="userAgent")
    language: Optional[str] = None
    url: Optional[str] = None

class FrontendLogPayload(BaseModel):
    """Payload for frontend logs."""
    level: str = Field(..., description="Log level (e.g., error, warn, info).")
    message: str = Field(..., description="Log message.")
    correlation_id: Optional[str] = Field(None, alias="correlationId", description="Correlation ID for tracing.")
    user_id: Optional[str] = Field(None, alias="userId", description="User identifier, if available.")
    component_name: Optional[str] = Field(None, alias="componentName", description="Name of the frontend component originating the log.")
    stack: Optional[str] = Field(None, description="Error stack trace, if applicable.")
    component_stack: Optional[str] = Field(None, alias="componentStack", description="React component stack, if applicable.")
    browser_info: Optional[BrowserInfoPayload] = Field(None, alias="browserInfo", description="Information about the user's browser.")
    additional_context: Optional[Dict[str, Any]] = Field(None, alias="additionalContext", description="Any other relevant context.")


@router.post(
    "/frontend-log",
    summary="Receive logs from the frontend",
    description="Endpoint for frontend applications to send client-side logs and errors to the backend for centralized logging.",
    status_code=202, # Accepted
    responses={
        202: {"description": "Log accepted for processing."},
        422: {"description": "Validation Error."},
    }
)
async def receive_frontend_log(
    request: Request, # FastAPI request object for IP, headers etc.
    log_payload: FrontendLogPayload = Body(...)
):
    """
    Receives a log entry from the frontend and logs it using the backend's
    logging system (Loguru).
    """
    # Ensure a correlation ID exists, either from payload or generate a new one
    correlation_id = log_payload.correlation_id or str(uuid.uuid4())

    # Bind essential information for structured logging
    # In a real app, correlation_id might also come from request.state if set by middleware
    bound_logger = logger.bind(
        correlation_id=correlation_id,
        user_id=log_payload.user_id,
        frontend_component=log_payload.component_name,
        client_ip=request.client.host if request.client else "unknown",
        log_source="frontend",
    )

    log_details = {
        "message": log_payload.message,
        "stack": log_payload.stack,
        "component_stack": log_payload.component_stack,
        "browser": log_payload.browser_info.model_dump(by_alias=True, exclude_none=True) if log_payload.browser_info else None,
        "context": log_payload.additional_context,
    }

    # Filter out None values from log_details to keep logs clean
    filtered_log_details = {k: v for k, v in log_details.items() if v is not None}


    if log_payload.level == "error":
        bound_logger.error("Frontend Error: {details}", details=filtered_log_details)
    elif log_payload.level == "warn":
        bound_logger.warning("Frontend Warning: {details}", details=filtered_log_details)
    elif log_payload.level == "info":
        bound_logger.info("Frontend Info: {details}", details=filtered_log_details)
    elif log_payload.level == "debug":
        bound_logger.debug("Frontend Debug: {details}", details=filtered_log_details)
    else:
        bound_logger.info("Frontend Log (level: {level}): {details}", level=log_payload.level, details=filtered_log_details)

    return {"status": "log received"}

# Example of how to include this router in your main FastAPI app:
# from fastapi import FastAPI
# from .api.endpoints import logging as logging_api # Adjust import path
#
# app = FastAPI()
# app.include_router(logging_api.router, prefix="/api/v1", tags=["Logging"])
