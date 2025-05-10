# Project Edge AI

## Overview

This project is designed to create an edge-AI orchestrator on NVIDIA Jetson AGX Orin, leveraging LiteLLM, Triton/TensorRT, Hugging Face SmolAgents, FastAPI/Redis orchestration, and a hexagonal architecture. The system supports multi-agent workflows, project management, artifact tracking, and knowledge graph integration.

## Directory Structure

The project follows a modular and extensible structure:

*   `/domain/`: Core domain logic, including agents, MCPConfig, and AgentGraph.
*   `/service/`: Service layer for orchestration, templates, and artifact management.
*   `/adapters/`: Abstract and concrete adapters for LLMs, A2A communication, and storage.
*   `/infra/`: Infrastructure code, including FastAPI endpoints and Redis integration.
*   `/smolagents/`: YAML definitions for custom agents.
*   `/config/`: Configuration files for LiteLLM, Triton, and project scaffolding.
*   `/scripts/`: Utility and automation scripts for development, setup, and maintenance.
    *   `create_project_structure.sh`: A bash script to generate the initial project directory structure.
    *   `scaffold_project.py`: A Python script to generate the initial project directory structure. It can be more flexible for complex setups.
    *   **Note:** Use *either* `create_project_structure.sh` *or* `scaffold_project.py` to initialize the project structure, not both. The Python script is recommended for more complex or configurable scaffolding needs.
*   `/docs/`: Project documentation, including architecture, definitions, and setup guides.
*   `/logs/`: Log files for debugging and monitoring.
*   `/data/`: Data storage, including models and Redis data.

## Getting Started

### Prerequisites

1. NVIDIA Jetson AGX Orin with JetPack installed.
2. Docker and NVIDIA Container Toolkit.
3. Python 3.10+ and Node.js (for frontend development).

### Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd project_edge_ai
    ```

2. Run the setup script:
    ```bash
    bash scripts/setup_env.sh
    ```

3. Initialize the project structure:
    ```bash
    python3 scripts/scaffold_project.py
    ```

4. Start the FastAPI server:
    ```bash
    uvicorn infra.infrastructure:app --reload
    ```

5. Access the API documentation at `http://localhost:8000/docs`.

## Contributing

1. Follow the TDD approach: write tests before implementation.
2. Use `ruff`, `black`, and `isort` for linting and formatting.
3. Ensure all tests pass before committing:
    ```bash
    pytest
    ```

4. Submit a pull request with a clear description of changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
