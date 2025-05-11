#!/bin/bash
# filepath: c:\Users\sprim\FocusAreas\Projects\Dev\AINative\scripts\create_project_structure.sh
# Idempotent script to generate the project_edge_ai directory structure.
# Run this script from the intended parent directory of project_edge_ai.

# Define the root directory name
PROJECT_ROOT="project_edge_ai"

# Create the root project directory
mkdir -p "$PROJECT_ROOT"
echo "Created/Ensured directory: $PROJECT_ROOT"

# Function to create directories and files
create_structure() {
    local base_path="$1"
    shift
    for item in "$@"; do
        if [[ "$item" == */ ]]; then
            # Item is a directory
            mkdir -p "${base_path}/${item}"
            echo "Created/Ensured directory: ${base_path}/${item}"
        else
            # Item is a file
            # Create parent directories if they don't exist
            mkdir -p "${base_path}/$(dirname "$item")"
            touch "${base_path}/${item}"
            echo "Created/Ensured file: ${base_path}/${item}"
        fi
    done
}

# Create top-level structure
create_structure "$PROJECT_ROOT" \
    "backend/" \
    "frontend/" \
    "scripts/" \
    "docs/" \
    "docs/scratch/" \
    "data/" \
    "logs/" \
    ".github/" \
    ".github/workflows/" \
    ".github/workflows/ci.yaml" \
    ".github/copilot-settings.json" \
    ".dockerignore" \
    ".gitignore" \
    "README.md" \
    "pre-commit-config.yaml"

# Create backend structure
create_structure "${PROJECT_ROOT}/backend" \
    "app/" \
    "app/domain/" \
    "app/domain/__init__.py" \
    "app/domain/domain.py" \
    "app/service/" \
    "app/service/__init__.py" \
    "app/service/service.py" \
    "app/adapters/" \
    "app/adapters/__init__.py" \
    "app/adapters/adapters.py" \
    "app/infrastructure/" \
    "app/infrastructure/__init__.py" \
    "app/infrastructure/main.py" \
    "app/infrastructure/routers/" \
    "app/infrastructure/routers/__init__.py" \
    "app/infrastructure/routers/example_router.py" \
    "tests/" \
    "tests/__init__.py" \
    "tests/conftest.py" \
    "tests/domain/" \
    "tests/service/" \
    "tests/adapters/" \
    "tests/infrastructure/" \
    "config/" \
    "config/litellm.config.yaml" \
    "config/otel-collector-config.yaml" \
    "smolagents/" \
    "smolagents/agent_X_spec.yaml" \
    "smolagents/agent_Y_spec.yaml" \
    ".venv/" \
    "pyproject.toml" \
    "Dockerfile"

# Create frontend structure
create_structure "${PROJECT_ROOT}/frontend" \
    "public/" \
    "src/" \
    "src/components/" \
    "src/contexts/" \
    "src/graphql/" \
    "src/hooks/" \
    "src/pages/" \
    "src/services/" \
    "src/styles/" \
    "src/types/" \
    "src/App.tsx" \
    "src/main.tsx" \
    "tests/" \
    "tests/example.spec.ts" \
    "index.html" \
    "package.json" \
    "tsconfig.json" \
    "vite.config.ts" \
    "vitest.config.ts"

# Create scripts structure
create_structure "${PROJECT_ROOT}/scripts" \
    "create_project_structure.sh" \
    "setup_env.sh" \
    "setup_docker.sh" \
    "generate_erd.sh" \
    "benchmark.sh" \
    "audit.sh" \
    "scaffold_project.py" \
    "generate_litellm_config.py"

# Create docs structure
create_structure "${PROJECT_ROOT}/docs" \
    "ERD.mmd" \
    "GettingStarted.md" \
    "APIReference.md" \
    "artifacts_definition.md" \
    "projects_definition.md" \
    "custom_agents_definition.md"
# Keep existing scratch file, ensure its parent dir exists
create_structure "${PROJECT_ROOT}/docs/scratch" \
    "Edge AI Agent Setup.md"


# Create data structure
create_structure "${PROJECT_ROOT}/data" \
    "models/" \
    "redis/" \
    "knowledge_graphs/" \
    "knowledge_graphs/project_X.json" \
    "knowledge_graphs/agent_Y.json"

# Create logs structure
create_structure "${PROJECT_ROOT}/logs" \
    "app.log" \
    "service.log" \
    "domain_trace.log" \
    "file_{time}.log"

echo "Project structure generation complete in $PROJECT_ROOT/"
# Ensure this script itself is in the right place if it's part of the scaffold
if [ -f "./create_project_structure.sh" ] && [ "$PROJECT_ROOT" == "project_edge_ai" ]; then
    cp "./create_project_structure.sh" "${PROJECT_ROOT}/scripts/create_project_structure.sh"
    echo "Copied create_project_structure.sh to ${PROJECT_ROOT}/scripts/"
fi
