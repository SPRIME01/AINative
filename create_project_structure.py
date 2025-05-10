#!/usr/bin/env python3
# filepath: c:\Users\sprim\FocusAreas\Projects\Dev\AINative\scripts\scaffold_project.py
import os
from pathlib import Path

BASE_DIR_NAME = "project_edge_ai"

# Define the structure as a dictionary. Ends with '/' for directory.
STRUCTURE = {
    "backend/": {
        "app/": {
            "domain/": ["__init__.py", "domain.py"],
            "service/": ["__init__.py", "service.py"],
            "adapters/": ["__init__.py", "adapters.py"],
            "infrastructure/": {
                "routers/": ["__init__.py", "example_router.py"],
                "__init__.py": None,
                "main.py": None,
            },
        },
        "tests/": {
            "domain/": [],
            "service/": [],
            "adapters/": [],
            "infrastructure/": [],
            "__init__.py": None,
            "conftest.py": None,
        },
        "config/": ["litellm.config.yaml", "otel-collector-config.yaml"],
        "smolagents/": ["agent_X_spec.yaml", "agent_Y_spec.yaml"],
        ".venv/": {},
        "pyproject.toml": None,
        "Dockerfile": None,
    },
    "frontend/": {
        "public/": {},
        "src/": {
            "components/": {},
            "contexts/": {},
            "graphql/": {},
            "hooks/": {},
            "pages/": {},
            "services/": {},
            "styles/": {},
            "types/": {},
            "App.tsx": None,
            "main.tsx": None,
        },
        "tests/": ["example.spec.ts"],
        "index.html": None,
        "package.json": None,
        "tsconfig.json": None,
        "vite.config.ts": None,
        "vitest.config.ts": None,
    },
    "scripts/": [
        "create_project_structure.sh",
        "setup_env.sh",
        "setup_docker.sh",
        "generate_erd.sh",
        "benchmark.sh",
        "audit.sh",
        "scaffold_project.py", # This script itself
        "generate_litellm_config.py",
    ],
    "docs/": {
        "scratch/": ["Edge AI Agent Setup.md"],
        "ERD.mmd": None,
        "GettingStarted.md": None,
        "APIReference.md": None,
        "artifacts_definition.md": None,
        "projects_definition.md": None,
        "custom_agents_definition.md": None,
    },
    "data/": {
        "models/": {},
        "redis/": {},
        "knowledge_graphs/": ["project_X.json", "agent_Y.json"],
    },
    "logs/": ["app.log", "service.log", "domain_trace.log", "file_{time}.log"],
    ".github/": {
        "workflows/": ["ci.yaml"],
        "copilot-settings.json": None,
    },
    ".dockerignore": None,
    ".gitignore": None,
    "README.md": None,
    "pre-commit-config.yaml": None,
}

def create_scaffold(base_path: Path, structure_dict: dict):
    """
    Recursively creates directories and files based on the structure_dict.
    """
    for name, content in structure_dict.items():
        current_path = base_path / name.rstrip('/') # Remove trailing slash for files/dirs
        if name.endswith('/'): # It's a directory
            current_path.mkdir(parents=True, exist_ok=True)
            print(f"Created/Ensured directory: {current_path}")
            if isinstance(content, dict): # Nested structure
                create_scaffold(current_path, content)
            elif isinstance(content, list): # List of files in this directory
                for file_name in content:
                    if file_name: # Ensure not None
                        (current_path / file_name).touch(exist_ok=True)
                        print(f"Created/Ensured file: {current_path / file_name}")
        else: # It's a file at the current base_path level
            current_path.touch(exist_ok=True)
            print(f"Created/Ensured file: {current_path}")

if __name__ == "__main__":
    project_root = Path(BASE_DIR_NAME)
    project_root.mkdir(exist_ok=True)
    print(f"Created/Ensured base directory: {project_root}")
    create_scaffold(project_root, STRUCTURE)
    print(f"Project structure generation complete in {project_root}/")

    # Copy this script into the scripts folder if it's run from outside
    # This part is a bit meta, assumes the script is in the CWD when run to create the project
    try:
        this_script_path = Path(__file__).resolve()
        target_script_path = project_root / "scripts" / this_script_path.name
        if this_script_path != target_script_path:
            target_script_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(this_script_path, target_script_path)
            print(f"Copied {this_script_path.name} to {target_script_path}")
    except Exception as e:
        print(f"Could not copy self to scripts directory: {e} (This is fine if script is already in place)")

```

### c:\Users\sprim\FocusAreas\Projects\Dev\AINative\project_edge_ai\README.md

Update the README to reflect the new high-level structure.

````markdown
<!-- filepath: c:\Users\sprim\FocusAreas\Projects\Dev\AINative\project_edge_ai\README.md -->
# Project Edge AI

This project aims to create a local group of AI agents to assist with various tasks, running on an NVIDIA Jetson AGX Orin.

## Project Structure Overview

The project is organized into the following main directories:

*   `/backend/`: Contains the Python-based backend application, structured following hexagonal architecture principles.
    *   `app/`: Core application code.
        *   `domain/`: Business logic, entities, and ports.
        *   `service/`: Application services and use cases.
        *   `adapters/`: Implementations for external interfaces (e.g., LLMs, databases).
        *   `infrastructure/`: FastAPI application, API endpoints, and dependency injection.
    *   `tests/`: Backend tests.
    *   `config/`: Backend-specific configurations.
    *   `smolagents/`: Configurations for custom SmolAgents.
*   `/frontend/`: Contains the TypeScript-based frontend application.
    *   `src/`: Frontend source code.
    *   `tests/`: Frontend tests.
*   `/scripts/`: Utility and automation scripts for development, setup, and maintenance.
*   `/docs/`: Project documentation, including architecture, definitions, and setup guides.
*   `/data/`: Stores data used by the project, such as local ML models, knowledge graphs, and Redis data.
*   `/logs/`: Centralized location for application and service logs.
*   `/.github/`: GitHub specific files, including workflows for CI/CD and Copilot settings.

For more detailed information on setup, development, and architecture, please refer to the files in the `/docs` directory.
```
