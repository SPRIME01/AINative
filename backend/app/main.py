from fastapi import FastAPI

# Assuming your project structure allows this import path
# If your endpoints directory is directly under 'app', this should work.
# Adjust if your 'api' directory is structured differently.
from app.api.endpoints import logging as logging_api
from app.core.logging_config import setup_logging # Assuming you have this for backend logging setup
# Import other routers and configurations as needed

# Example: Initialize backend logging
# This should ideally be called once when the application starts.
# You might have this in a startup event or directly here.
# Ensure this is configured according to your needs.
setup_logging(log_level="INFO", log_file_path="app_backend.log")


app = FastAPI(
    title="AINative Backend API",
    description="API for the Edge-AI orchestrator.",
    version="0.1.0",
    # Add other FastAPI configurations like middleware, exception handlers, etc.
)

# Include the frontend logging router
# The prefix="/api/v1" means all routes in logging_api.router
# will be prefixed with /api/v1. For example, /frontend-log becomes /api/v1/frontend-log.
# The tag "Logging" helps group these endpoints in the OpenAPI documentation.
app.include_router(logging_api.router, prefix="/api/v1", tags=["Logging"])

# Include other application routers here
# For example:
# from app.api.endpoints import another_router
# app.include_router(another_router.router, prefix="/api/v1/another", tags=["Another Feature"])


@app.get("/", summary="Root endpoint", description="A simple health check or root endpoint.")
async def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the AINative Backend API"}

# Add startup/shutdown events if needed
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Application startup")
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Application shutdown")

# If you are running this file directly with uvicorn, e.g., uvicorn app.main:app --reload
# you might have the following:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
