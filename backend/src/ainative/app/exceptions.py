"""
Custom application exceptions and FastAPI exception handlers.
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError  # Assuming this is Pydantic v2
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from typing import Any, Dict

# TODO: Integrate with a proper logging library (e.g., Loguru) as per project standards.

class AppException(Exception):
    """
    Custom application exception.

    :param detail: The detail message for the exception.
    :type detail: str
    :param status_code: The HTTP status code associated with this exception.
    :type status_code: int, optional
    """
    def __init__(self, detail: str, status_code: int = HTTP_500_INTERNAL_SERVER_ERROR):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles generic, unhandled exceptions.

    :param request: The incoming request.
    :type request: Request
    :param exc: The exception that was raised.
    :type exc: Exception
    :return: A JSONResponse with a 500 status code and error details.
    :rtype: JSONResponse
    """
    correlation_id = getattr(request.state, "correlation_id", "not-set")
    # logger.error(f"Unhandled exception: {exc}", exc_info=True, correlation_id=correlation_id) # Example real logging

    # For test compatibility, mimicking behavior of setting last_error_log on app.state
    # In a real app, this might not be necessary or done differently.
    if hasattr(request.app.state, "last_error_log"):
        request.app.state.last_error_log = {
            "type": "unhandled", "exc": str(exc), "correlation_id": correlation_id, "stack_trace": "..." # Actual stack trace in real log
        }
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "type": "/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "An unexpected error occurred. Please try again later.",
            "instance": str(request.url),
            "correlation_id": correlation_id,
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles FastAPI's HTTPException.

    :param request: The incoming request.
    :type request: Request
    :param exc: The HTTPException that was raised.
    :type exc: HTTPException
    :return: A JSONResponse with the HTTPException's status code and details.
    :rtype: JSONResponse
    """
    correlation_id = getattr(request.state, "correlation_id", "not-set")
    # logger.warning(f"HTTPException: {exc.detail}", status_code=exc.status_code, correlation_id=correlation_id) # Example real logging
    if hasattr(request.app.state, "last_error_log"):
        request.app.state.last_error_log = {
            "type": "http", "exc": exc.detail, "status_code": exc.status_code, "correlation_id": correlation_id
        }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": f"/errors/http/{exc.status_code}",  # Changed from /errors/http-error/
            "title": "HTTP Error",
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": str(request.url),
            "correlation_id": correlation_id,
        },
    )

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handles custom AppException.

    :param request: The incoming request.
    :type request: Request
    :param exc: The AppException that was raised.
    :type exc: AppException
    :return: A JSONResponse with the AppException's status code and details.
    :rtype: JSONResponse
    """
    correlation_id = getattr(request.state, "correlation_id", "not-set")
    # logger.error(f"AppException: {exc.detail}", status_code=exc.status_code, correlation_id=correlation_id) # Example real logging
    if hasattr(request.app.state, "last_error_log"):
        request.app.state.last_error_log = {
            "type": "app", "exc": exc.detail, "status_code": exc.status_code, "correlation_id": correlation_id
        }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "/errors/application-specific-error",  # Changed from /errors/application-error
            "title": "Application Specific Error",  # Changed from Application Error
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": str(request.url),
            "correlation_id": correlation_id,
        },
    )

async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handles Pydantic's ValidationError.
    This can be used if you are manually validating Pydantic models and raising ValidationError.
    FastAPI's RequestValidationError is handled by default, but can also be overridden.

    :param request: The incoming request.
    :type request: Request
    :param exc: The ValidationError that was raised.
    :type exc: ValidationError
    :return: A JSONResponse with a 422 status code and validation error details.
    :rtype: JSONResponse
    """
    correlation_id = getattr(request.state, "correlation_id", "not-set")
    errors: list[dict[str, Any]] = exc.errors()
    # logger.info(f"Validation error: {errors}", correlation_id=correlation_id) # Example real logging
    if hasattr(request.app.state, "last_error_log"):
        request.app.state.last_error_log = {
            "type": "validation", "exc": errors, "correlation_id": correlation_id
        }
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "type": "/errors/validation-error",
            "title": "Validation Error",
            "status": HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": errors,
            "instance": str(request.url),
            "correlation_id": correlation_id,
        },
    )
