# GitHub Copilot Custom Instructions

## About Your Code

- **Project Context:** Edge-AI orchestrator
- **Target Platform:** NVIDIA Jetson AGX Orin
- **Core Technologies:** LiteLLM (Triton/TensorRT, Ollama), FastAPI, Redis, Google Agent Development Kit (ADK)
- **Architectural Pattern:** Hexagonal Architecture (Ports and Adapters)

## How You Should Help

### Development Methodology
- Prioritize Test-Driven Development (TDD)
- Always suggest a `pytest` or `vitest` test case *before* providing implementation code

### Code Style & Quality
- Generate Python 3.10+ compatible code
- Enforce PEP 8 compliance
- Include comprehensive type hints and clear docstrings

### Modularity & Design
- Decompose functionality into small, pure, and easily testable functions
- Adhere to the Ports and Adapters pattern

### Asynchronous Operations
- Prefer `async/await` for FastAPI endpoints and all I/O-bound operations

### Google ADK Scaffolding
- When generating Google ADK project structures, include stubs for:
    - Agent definitions
    - Tool configurations
    - Action handlers

### Observability
- Automatically include Prometheus metrics endpoint (`@app.get('/metrics')`) stubs
- Include logging hooks in new modules

### Documentation & Examples
- Ensure all docstrings include practical examples
- Add a dedicated `# Example:` section in code comments where appropriate

### Adapter Implementation
- Use `NotImplementedError` for adapter stubs
- Include clear `TODO:` comments detailing the pending implementation

### Development Environment
- Use `uv` for python dependency management
- Use `pytest` for python testing
- Use `vitest` for javascript/typescript testing
- Use 'pnpm` for javascript/typescript dependency management
- Use .env for environment variable management

