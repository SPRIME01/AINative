# AINative

# Project Edge AI

This project aims to create a local group of AI agents to assist with various tasks, running on an NVIDIA Jetson AGX Orin.

## Project Structure Overview

The project is organized into the following main directories:

*   `/backend/`: Contains the Python-based backend application.
    *   `src/ainative/`: Core source code for the AI Native components.
        *   `app/`: Application logic following hexagonal architecture (domain, services, adapters, infrastructure).
        *   `adk_agents/`: Definitions, logic, and configurations for agents built with Google's Agent Development Kit.
        *   `config/`: Configuration files for backend services (e.g., LiteLLM, application settings).
        *   `prompts/`: Centralized prompt definitions for various AI agents.
    *   `tests/`: Backend tests, including unit and integration tests for app components and ADK agents.
*   `/frontend/`: Contains the TypeScript-based frontend application.
    *   `src/`: Frontend source code.
    *   `tests/`: Frontend tests.
*   `/scripts/`: Utility and automation scripts.
*   `/docs/`: Project documentation.
    *   `edge-ai-agent-docs/`: Specific documentation for the Edge AI agent system, including concepts, agent details, and usage guides.
    *   `scratch/`: Working documents and notes.
*   `/data/`: Local data stores (models, knowledge graphs, Redis data).
*   `/logs/`: Application and service logs.
*   `/.github/`: GitHub specific files (workflows, settings).

For more detailed information, refer to the documentation within the `/docs` directory.
