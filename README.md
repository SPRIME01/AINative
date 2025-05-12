# AINative 🚀🧠✨

[![Project Status: Active](https://img.shields.io/badge/status-active-success.svg)](https://github.com/SPRIME01/AINative)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to AINative! An advanced, edge-AI agent orchestrator designed to run a collaborative team of AI agents locally on an NVIDIA Jetson AGX Orin, empowering users with a personalized AI ecosystem for enhanced productivity and project execution.

## Key Features 🌟

* **🧩 Multi-Agent System:** Core team of 8 specialized agents working in synergy
* **엣지 Edge-First & Private:** Optimized for NVIDIA Jetson AGX Orin 64GB
* **⚡ Quantized LLM Support:** Leverages Ollama and TensorRT-LLM via Triton
* **🔗 Model Access Layer:** LiteLLM for seamless local/cloud model switching
* **🤖 Custom Agent Creation:** Build agents with Google Agent Development Kit (ADK)
* **🧑‍💼 Project Management:** AI-assisted project organization and workflows
* **📚 Artifact Ecosystem:** Manage cognitive tools, outputs, and validated information products
* **🕸️ Knowledge Graph:** Track entities and relationships across your workspace
* **🏗️ Clean Architecture:** Hexagonal design with proper separation of concerns
* **📊 Complete Observability:** Structured logging, tracing, and metrics with OTel

## Architecture Overview 🏛️

* **Domain Layer:** Core business logic and abstract ports
* **Service Layer:** Application workflows and use cases
* **Adapters Layer:** Implements ports for external systems
* **Infrastructure Layer:** API exposure and operational concerns

## Tech Stack 🛠️

* **Hardware:** NVIDIA Jetson AGX Orin 64GB
* **AI & LLMs:** LiteLLM, Ollama, Triton, Google ADK
* **Backend:** Python 3.10+, FastAPI, Pydantic, Redis, Loguru
* **Frontend:** TypeScript, React, GraphQL, Apollo, Winston
* **Observability:** OpenTelemetry, Prometheus, Grafana, Loki, Tempo
* **Development:** pytest, Ruff, Black, MyPy, pre-commit

## Getting Started 🏁

### Prerequisites

* NVIDIA Jetson AGX Orin 64GB with JetPack
* Docker with NVIDIA Container Toolkit
* Python 3.10+ and Node.js
* Redis instance

### Quick Start

# Clone repository and set up environment
git clone https://github.com/SPRIME01/AINative.git
cd AINative
bash scripts/setup_env.sh

# Configure services and models
# Start the application
source .venv/bin/activate
uvicorn src.ainative.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage Examples 💡

```bash
# Create a new project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: $(uuidgen)" \
  -d '{"name": "My First AINative Project"}'

# See API documentation at http://localhost:8000/docs for more endpoints
```

## Core Agents 🤖

1. **Strategist:** Goal-setting and high-level decisions
2. **Builder:** Code generation and technical implementation
3. **Planner:** Task planning and scheduling
4. **Critic:** Idea refinement and validation
5. **Synthesizer:** Content creation and drafting
6. **Archivist:** Knowledge management and organization
7. **Executor:** Task execution and system interaction
8. **Watcher:** Risk monitoring and system health

## Development 🧑‍🔬

* **Test-Driven Development (TDD)** with pytest
* **Linting & Type Checking** via Ruff, Black, and MyPy
* **Hexagonal Architecture** with clear boundaries
* **Comprehensive Logging** for debugging with correlation IDs

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
  <p>AINative - Your Personal Edge AI Teammate</p>
</div>
