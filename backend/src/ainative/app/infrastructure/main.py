from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Edge AI Orchestrator API",
    version="0.1.0",
    description="API for managing and orchestrating Edge AI agents and tasks.",
)

# CORS (Cross-Origin Resource Sharing)
# Allow all origins for development, you might want to restrict this in production
origins = [
    "http://localhost",          # Common local dev
    "http://localhost:3000",     # Default for Create React App
    "http://localhost:5173",     # Default for Vite (React/Vue)
    "http://127.0.0.1:5173",   # Another common Vite/local dev
    # Add your frontend's actual development URL if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],    # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")
    # Potentially initialize database connections, load models, etc.

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown.")
    # Potentially close database connections, cleanup resources, etc.

@app.get("/", tags=["General"])
async def read_root():
    '''
    Root endpoint for the API.
    Returns a welcome message.
    '''
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Edge AI Orchestrator API!"}

@app.get("/health", tags=["General"])
async def health_check():
    '''
    Health check endpoint.
    Returns the operational status of the API.
    '''
    logger.info("Health check endpoint accessed.")
    return {"status": "ok"}

# Stub for Prometheus metrics endpoint
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    '''
    Prometheus metrics endpoint.
    This endpoint should be implemented to expose application metrics.
    # Example:
    # from prometheus_client import generate_latest, REGISTRY
    # from fastapi import Response
    # return Response(media_type="text/plain", content=generate_latest(REGISTRY))
    '''
    logger.info("Metrics endpoint accessed.")
    # TODO: Implement Prometheus metrics exposition
    # from prometheus_client import generate_latest, REGISTRY, Counter
    # from fastapi import Response
    # c = Counter('my_failures', 'Description of counter')
    # c.inc() # Increment by 1
    # return Response(media_type="text/plain", content=generate_latest(REGISTRY))
    return {"message": "Metrics endpoint not yet implemented. TODO: Expose Prometheus metrics."}

# Example of a simple agent-related endpoint (illustrative)
# You would typically define your routers in other files and include them here
# from ..service import agent_router  # Example import
# app.include_router(agent_router.router, prefix="/agents", tags=["Agents"])

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server directly for development.")
    # Note: The VS Code task "Run FastAPI (uvicorn)" should be preferred for development.
    # It correctly sets the working directory to backend/src
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, app_dir=".")


logger.info("FastAPI application initialized.")
