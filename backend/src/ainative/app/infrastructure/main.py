import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from ainative.app.entrypoints.api.routes import router as agent_router, ErrorResponse

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define HTTP reason phrases
HTTP_REASON_PHRASES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    422: "Unprocessable Entity",
    500: "Internal Server Error",
    # Add other status codes as needed
}

app = FastAPI(
    title="Edge AI Orchestrator API",
    version="0.1.0",
    description="API for managing and orchestrating Edge AI agents and tasks.",
)

# CORS (Cross-Origin Resource Sharing)
# Allow all origins for development, you might want to restrict this in production
origins = [
    "http://localhost",  # Common local dev
    "http://localhost:3000",  # Default for Create React App
    "http://localhost:5173",  # Default for Vite (React/Vue)
    "http://127.0.0.1:5173",  # Another common Vite/local dev
    # Add your frontend's actual development URL if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Exception handler for Problem Details format
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Convert HTTP exceptions to Problem Details format (RFC 7807).

    Args:
        request: The request that caused the exception
        exc: The raised HTTPException

    Returns:
        JSONResponse: A response formatted according to RFC 7807
    """
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
    """
    Convert validation errors to Problem Details format (RFC 7807).

    Args:
        request: The request that caused the validation error
        exc: The raised RequestValidationError

    Returns:
        JSONResponse: A response formatted according to RFC 7807
    """
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


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Application startup complete.")
    # Potentially initialize database connections, load models, etc.


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Application shutdown.")
    # Potentially close database connections, cleanup resources, etc.


@app.get("/", tags=["General"])
async def read_root() -> dict[str, str]:
    """
    Root endpoint for the API.

    Returns:
        dict: A welcome message.

    Example:
        >>> import httpx
        >>> response = httpx.get("http://localhost:8000/")
        >>> response.json()
        {'message': 'Welcome to the Edge AI Orchestrator API!'}
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Edge AI Orchestrator API!"}


@app.get("/health", tags=["General"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: The operational status of the API.

    Example:
        >>> import httpx
        >>> response = httpx.get("http://localhost:8000/health")
        >>> response.json()
        {'status': 'ok'}
    """
    logger.info("Health check endpoint accessed.")
    return {"status": "ok"}


@app.get("/metrics", tags=["Monitoring"])
async def metrics() -> Any:
    """
    Prometheus metrics endpoint stub.

    Returns:
        dict: A message indicating the endpoint is not yet implemented.

    Example:
        >>> import httpx
        >>> response = httpx.get("http://localhost:8000/metrics")
        >>> response.json()
        {'message': 'Metrics endpoint not yet implemented. TODO: Expose Prometheus metrics.'}

    TODO:
        Implement Prometheus metrics exposition using prometheus_client.
    """
    logger.info("Metrics endpoint accessed.")
    # TODO: Implement Prometheus metrics exposition
    return {
        "message": "Metrics endpoint not yet implemented. TODO: Expose Prometheus metrics."
    }


# Include routers
app.include_router(agent_router)

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server directly for development.")
    # Note: The VS Code task "Run FastAPI (uvicorn)" should be preferred for development.
    # It correctly sets the working directory to backend/src
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, app_dir=".")


logger.info("FastAPI application initialized.")
