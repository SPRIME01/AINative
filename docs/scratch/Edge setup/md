# 🚀 Edge AI Agent Setup & Observability Architecture 🧠

This document outlines the conceptualization, design, and implementation details for a local Edge AI agent team and a robust observability architecture. It synthesizes key decisions and specifications from our discussions.

## 📜 Table of Contents

- [🚀 Edge AI Agent Setup \& Observability Architecture 🧠](#-edge-ai-agent-setup--observability-architecture-)
  - [📜 Table of Contents](#-table-of-contents)
  - [🎯 Project Goal: Local Edge AI Agent Team](#-project-goal-local-edge-ai-agent-team)
  - [🤖 MECE Agent Breakdown](#-mece-agent-breakdown)
    - [Agent Roles \& Responsibilities](#agent-roles--responsibilities)
    - [Suggested Quantized LLMs](#suggested-quantized-llms)
  - [⚙️ Edge Runtime Optimization Tactics](#️-edge-runtime-optimization-tactics)
  - [🗓️ Agent Interaction Schedule](#️-agent-interaction-schedule)
    - [Daily Routine](#daily-routine)
    - [Weekly Cadence (Sunday or Monday Morning)](#weekly-cadence-sunday-or-monday-morning)
  - [🕵️ Agent Specifications (Example: Strategist Agent)](#️-agent-specifications-example-strategist-agent)
    - [Strategist Agent Details](#strategist-agent-details)
  - [🛠️ System Design \& Implementation Prompts for Observability](#️-system-design--implementation-prompts-for-observability)
    - [Core Principles for Synergy](#core-principles-for-synergy)
    - [1. Backend (FastAPI + Loguru + OpenTelemetry)](#1-backend-fastapi--loguru--opentelemetry)
    - [2. Frontend (React + TypeScript + Apollo + Winston)](#2-frontend-react--typescript--apollo--winston)
    - [3. OpenTelemetry Collector Stack](#3-opentelemetry-collector-stack)
    - [4. Cross-Cutting Full Stack Integration](#4-cross-cutting-full-stack-integration)
    - [Optional Advanced Prompt Add-ons:](#optional-advanced-prompt-add-ons)
  - [💻 Code Generation \& Configuration Prompts](#-code-generation--configuration-prompts)
    - [1. FastAPI Middleware + Logging + Error Handling (Backend Core)](#1-fastapi-middleware--logging--error-handling-backend-core)

---

## 🎯 Project Goal: Local Edge AI Agent Team

To leverage an NVIDIA Jetson AGX Orin 64GB developer kit to create a local group of agents (like a team) to assist with personal productivity, project execution, technical work, and entrepreneurial efforts. These agents will use only quantized LLM models available locally (e.g., GGUF, TensorRT-LLM via Ollama) and operate efficiently within hardware constraints. The system aims for self-management and intelligence.

**Improved Prompt Guiding the Agent Setup:**

> *Given my background as an AI-oriented project manager with strong strategic thinking skills and intermediate programming abilities, and given my interest in developing a self-managing, intelligent local system using edge AI, I want to fully leverage my NVIDIA Jetson AGX Orin 64GB developer kit. My goal is to deploy a set of lightweight, quantized LLM-based agents (similar to a collaborative team) that operate locally to assist with my personal productivity, project execution, technical work, and entrepreneurial efforts. These agents must be MECE (Mutually Exclusive, Collectively Exhaustive), operate efficiently within hardware constraints, and use only locally hosted, quantized models (such as those run on Ollama, GGUF, or TensorRT-LLM).*
>
> *Please provide:*
> 1. *A MECE breakdown of agent roles based on my strategic objectives, traits (ENTP, visionary-but-inconsistent follow-through), and current needs.*
> 2. *Suggested lightweight, quantized LLMs (including sizes and formats) for each role, compatible with the Jetson AGX Orin.*
> 3. *Any runtime optimization considerations for multi-agent orchestration on edge (e.g., batching, GPU scheduling, model swapping, persistent memory usage, etc.).*

---

## 🤖 MECE Agent Breakdown

### Agent Roles & Responsibilities

| Agent Name        | Role & Focus                                       | Primary Tasks                                                                 | Notes                                                 |
| :---------------- | :------------------------------------------------- | :---------------------------------------------------------------------------- | :---------------------------------------------------- |
| 👑 **Strategist Agent** | High-level decision-making, prioritization       | Goal alignment, OKR refinement, timeboxing                                    | Acts like a thought partner, reorients you weekly     |
| 🔬 **Research Agent**   | On-demand technical researcher                     | Summarizes docs, finds SOTA methods (local corpus or cached web), parses PDFs | Integrates with local vector DB                       |
| 🛠️ **Builder Agent**    | Code generation, debugging, devops                 | Drafts scripts, sets up containers, builds pipelines                          | Optimized for function-calling and REPL               |
| 🗺️ **Planner Agent**    | Task planning, scheduling, scope control           | Creates/updates project plans, breaks goals into steps, checks feasibility    | Helps manage follow-through                           |
| 📚 **Librarian Agent** | Personal knowledge management                      | Organizes Zettelkasten, tags notes, builds indexes & mind maps                | Syncs with Obsidian or markdown-based PKM             |
| ✍️ **Scribe Agent**     | Writing assistant                                  | Drafts documentation, blogs, strategies, business plans                       | Trained on your voice/style for coherence             |
| 🤔 **Critic Agent**     | Refiner & counter-thinker                          | Detects assumptions, challenges ideas, provides contrarian POVs               | Helps tame ENTP idea sprawl                           |
|🛡️ **Guardian Agent**   | Risk, ethics, constraints                          | Flags scope creep, legal risks, hallucination risk                            | Keeps your system aligned with goals and values       |

These agents are **MECE** by functional domain and can scale or evolve independently.

### Suggested Quantized LLMs
(For Local Edge AI on Jetson AGX Orin - 64GB RAM)
Use **GGUF** format via **llama.cpp** or **TensorRT-LLM** for maximum performance. Favor `Q4_K_M` or `Q5_K_M` quantizations.

| Agent             | Model                                                     | Format   | Reason                                            |
| :---------------- | :-------------------------------------------------------- | :------- | :------------------------------------------------ |
| 👑 Strategist     | **Nous Hermes 2 - Mistral 7B Q5_K_M**                     | GGUF     | Smart, versatile, and aligned with task planning  |
| 🔬 Research       | **Phi-2** or **TinyLlama** + **RAG w/ local PDFs**        | GGUF + Faiss | Lightweight + great in RAG setups                 |
| 🛠️ Builder         | **Code LLaMA 7B Q4_0** or **Deepseek-Coder 6.7B**         | GGUF     | Strong coding skills with small memory footprint    |
| 🗺️ Planner         | **Mistral-Instruct 7B Q4_K_M**                            | GGUF     | Good for structure, goal breakdown                |
| 📚 Librarian       | **OpenHermes 2.5 - Mistral Q5_K_S**                       | GGUF     | Great general-purpose assistant                   |
| ✍️ Scribe          | **TinyStories** (if fine-tuned) or **Mistral Creative Q4_K_M** | GGUF     | For creative writing and documentation            |
| 🤔 Critic          | **OpenOrca Mistral 7B Q4_K_M**                            | GGUF     | Trained to critique and reason well               |
| 🛡️ Guardian        | **GPT4ALL Falcon Q4_0** or distilled ethics-tuned models  | GGUF     | Smaller models sufficient for policy checking     |

---

## ⚙️ Edge Runtime Optimization Tactics

-   🔄 **Model Swapping / Lazy Loading:** Only load active models to conserve VRAM. Use model routers with on-demand bootstrapping.
-   🔗 **Shared Embedding Model:** Use a single embedding model (e.g., `all-MiniLM-L6`) across agents.
-   🚦 **GPU Scheduling:** Schedule agents to avoid inference collisions; run high-priority agents first.
-   💾 **Persistent Agent Memory:** Use LMDB or Redis for short-term memory, and local vector DBs (e.g., Qdrant, Milvus, Weaviate) for long-term.
-   📨 **Inter-agent Messaging:** Use a lightweight message bus like NATS or MQTT.
-   ⚖️ **Parallelism Limits:** Cap to 2–3 concurrent models on Orin; others should offload or sleep.

---

## 🗓️ Agent Interaction Schedule

### Daily Routine
(Automate/semi-automate via FastAPI/cron or task queue)

**Morning Block (Priming, Planning, Prioritizing) ☀️ (7:30 AM – 9:00 AM)**
| Time          | Agent(s)                  | Purpose                             | Tasks                                                                                             |
| :------------ | :------------------------ | :---------------------------------- | :------------------------------------------------------------------------------------------------ |
| 7:30 – 7:45   | 👑 Strategist + 🗺️ Planner | **Daily Alignment Review**          | Summarize top OKRs, show yesterday’s progress vs plan, flag drift. Suggest focused priorities.    |
| 7:45 – 8:00   | 🤔 Critic + 🛡️ Guardian     | **Idea and Scope Audit**            | Evaluate if current obsessions are aligned or distractions. Reframe if needed.                    |
| 8:00 – 8:30   | 🛠️ Builder + 📚 Librarian   | **Prep Dev & Knowledge Environment** | Load relevant code snippets, notes, libraries, research. Auto-mount/index relevant directories. |
| 8:30 – 9:00   | ✍️ Scribe                   | **Expressive Output Session**       | Journal thoughts, write daily log, or draft public-facing material.                               |

**Midday Block (Execution and Research) 💻 (10:00 AM – 1:00 PM)**
| Time          | Agent(s)                          | Purpose                       | Tasks                                                                                             |
| :------------ | :-------------------------------- | :---------------------------- | :------------------------------------------------------------------------------------------------ |
| 10:00 – 12:00 | 🛠️ Builder + 🔬 Research + 📚 Librarian | **Deep Work Block**             | Actively build, script, test, analyze. Agents answer coding questions, propose fixes, serve docs. |
| 12:00 – 1:00  | 🗺️ Planner + 👑 Strategist        | **Midday Review / Triage**      | Evaluate progress. Adjust afternoon plans. Surface forgotten tasks/blockers. Queue tomorrow’s prep. |

**Afternoon Block (Review, Refinement, Reconsolidation) 🧐 (2:00 PM – 5:00 PM)**
| Time        | Agent(s)                        | Purpose                       | Tasks                                                                                             |
| :---------- | :------------------------------ | :---------------------------- | :------------------------------------------------------------------------------------------------ |
| 2:00 – 3:30 | ✍️ Scribe + 🛠️ Builder + 🔬 Research | **Document & Polish**           | Turn output into usable formats—docs, READMEs, planning briefs, prototypes, etc.                  |
| 3:30 – 4:30 | 🤔 Critic + 🛡️ Guardian           | **Postmortem and Risk Review**  | Evaluate what worked/didn't. Check for hallucination, scope creep, misalignment.                  |
| 4:30 – 5:00 | 👑 Strategist + 🗺️ Planner      | **Next Day Setup**              | Pre-plan top 3 tasks, auto-prepare dependencies. Forecast time & energy budget.                   |

**Evening Block (Optional - Reflective + Creative Time) 🌙 (8:00 PM – 9:00 PM)**
| Time        | Agent(s)                | Purpose                                 | Tasks                                                                                             |
| :---------- | :---------------------- | :-------------------------------------- | :------------------------------------------------------------------------------------------------ |
| 8:00 – 8:30 | 📚 Librarian + ✍️ Scribe | **Knowledge Sync**                      | Auto-tag & sync notes, summarize day's highlights, suggest Zettels to connect.                    |
| 8:30 – 9:00 | 👑 Strategist           | **Dream Seeding / Subconscious Querying** | Optional: seed questions or problems into subconscious using written prompts.                     |

### Weekly Cadence (Sunday or Monday Morning)
| Agent(s)                          | Purpose                       | Tasks                                                                                             |
| :-------------------------------- | :---------------------------- | :------------------------------------------------------------------------------------------------ |
| 👑 Strategist + 🗺️ Planner + 🛡️ Guardian | **Weekly OKR Review**           | Score progress, realign priorities, identify waste or misalignment.                               |
| 🔬 Research + 🛠️ Builder           | **Capability Expansion**        | Explore new tools, update agent capabilities or model configs.                                    |
| 🤔 Critic + 🛡️ Guardian             | **Systemic Improvement**        | Identify personal bottlenecks, overengineered workflows, or tech debt.                            |
| 📚 Librarian                      | **Knowledge Consolidation**     | Build connections across weekly notes, generate diagrams or knowledge trees.                      |

---

## 🕵️ Agent Specifications (Example: Strategist Agent)

**Improved Prompt Guiding Agent Specification:**
> Given the edge deployment constraints of a Jetson AGX Orin 64GB Dev Kit and my intention to build a local team of quantized LLM-powered agents, define the **system prompts**, **tools**, **capabilities**, and any memory/context planning (MCP) configurations** for each of the previously defined agents. These agents should be optimized for performance, clarity of role, and efficient local resource usage. Provide detailed specifications for two agents at a time. Include:
> - Agent Name and Role Summary
> - System Prompt (MECE, role-specific, minimal hallucination risk)
> - Tooling (files, APIs, scripts, agents, functions, vector DBs, etc.)
> - Access Policies (read/write access, memory persistence, sandboxing)
> - Quantized LLM model suggestions (e.g. Phi-2, Gemma.Q, Mistral.Q, TinyLlama)
> - Notes on efficiency, load-balancing, or smart routing under edge constraints

### Strategist Agent Details

**Role Summary**: Aligns your daily and weekly tasks with long-term goals. Filters inputs through strategic lenses. Prioritizes direction over tactics.

**System Prompt**:
> *You are "The Strategist", an AI agent responsible for long-range alignment. You help ensure that all work supports high-level goals, OKRs, and vision. You translate vague intentions into measurable direction, resolve ambiguity, and detect misalignment or scope creep. Your output is crisp, structured, and strategically insightful. You work in partnership with the Planner and Critic to ensure optimal decision-making.*

**Tools & Access**:
-   **Tools**:
    -   `OKR.json` file reader/writer (local persistent storage)
    -   Markdown output renderer
-   **Access Policies**:
    -   **Read**: Everything in `/plans`, `/logs`, `/okr/`
    -   **No code execution**, sandboxed from dev environments

**Quantized LLM Models**:
-   **Primary**: Mistral 7B Q5_K_M (good balance of fluency and reasoning)
-   **Fallback/Lightweight**: Phi-2 or Gemma 2B (fast, efficient on Jetson)

**MCP / Memory Planning**:
-   Uses sliding window summarization on recent logs
-   Pulls weekly trend summaries from the Planner
-   Maintains a "strategic drift" score updated weekly

*(Note: Specifications for other agents would follow this template as they are defined.)*

---

## 🛠️ System Design & Implementation Prompts for Observability

This section details prompts for designing a robust, enterprise-grade observability and error-handling architecture.

### Core Principles for Synergy
*   🔑 **Correlation IDs (Trace IDs):** Generate a unique ID at the start of a user request (frontend/API Gateway) and pass it through all subsequent calls. Log this ID with every message and error. OpenTelemetry is key for managing this.
*   📊 **Visualization & Alerting:** Use Grafana for dashboards (error rates, log volumes, latency) and alerts.

### 1. Backend (FastAPI + Loguru + OpenTelemetry)
> **Design a Python FastAPI backend architecture that implements the following:**
> - Automatic correlation ID generation and propagation using middleware (UUID from `X-Correlation-ID` header or create new if missing).
> - Structured logging with Loguru, logging all events in JSON format.
> - Bridge Loguru logs to OpenTelemetry logs using an appropriate handler or shim, with correlation ID and trace context captured.
> - Custom exception classes for business logic errors and FastAPI `@exception_handler` definitions for HTTP and validation errors.
> - Return all errors in standardized RFC 7807 “Problem Details” format.
> - Middleware-level exception catch-all that logs full traceback and emits structured error response.
> - Auto-instrument FastAPI with OpenTelemetry tracing (use spans and traceparent propagation).
> - All logs and traces routed to OpenTelemetry Collector via OTLP exporter.

### 2. Frontend (React + TypeScript + Apollo + Winston)
> **Design a React (TypeScript) frontend that ensures robust error handling and observability:**
> - Generate a UUID correlation ID on app load and attach it to every GraphQL and REST request via `X-Correlation-ID` header.
> - Use Apollo Client to handle GraphQL errors and implement UI patterns for retry/fallback.
> - Wrap components with React Error Boundaries and log rendering errors to a `/api/frontend-log` backend endpoint.
> - Implement Winston logging with structured JSON output.
> - For significant frontend errors (e.g., network failures, validation issues), log details and context (user ID, page, browser info, correlation ID).
> - Auto-generate TypeScript types from GraphQL schema using `@graphql-codegen`.

### 3. OpenTelemetry Collector Stack
> **Design an OpenTelemetry observability pipeline with the following components:**
> - Backend and frontend logs, traces, and metrics sent to the OTel Collector via OTLP.
> - Collector configured with processors for context enrichment (e.g., correlation ID), sensitive data filtering, and sampling.
> - Export logs to Loki or Elasticsearch; traces to Jaeger or Tempo; metrics to Prometheus and/or InfluxDB.
> - Grafana dashboards pulling from all relevant data sources (Prometheus for metrics, Loki/Elasticsearch for logs, Jaeger/Tempo for traces).
> - Define alerting rules in Grafana for error rates, latency, and anomalous log volumes.

### 4. Cross-Cutting Full Stack Integration
> **Design a full-stack error handling and logging pipeline spanning FastAPI backend and React frontend, including the following integration points:**
> - Correlation ID lifecycle from frontend (UUID generation) → request header → FastAPI middleware → Loguru/OTel logs → backend-to-backend calls.
> - Log formats must be structured JSON and conform to centralized schema for correlation ID, request path, user ID, status code, error type, and stack trace.
> - All API error responses should follow the [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807) structure for consistent frontend parsing.
> - Frontend logs to backend via `/api/frontend-log`, backend enriches with context and forwards to the OTel Collector.
> - Alerting and visualization in Grafana, including logs/traces/metrics correlated by correlation ID or trace ID.

### Optional Advanced Prompt Add-ons:
**To incorporate runtime type enforcement and zero-trust validation:**
> - Extend the backend to use Pydantic for request validation and response serialization.
> - Use FastAPI's OpenAPI schema generation to validate incoming requests at the edge via API Gateway.
> - Incorporate mypy, Ruff, or Pyright for static type checking of backend codebase.

**To handle async complexity and monitoring of async errors:**
> - Ensure Loguru + OTel context propagation supports asyncio (e.g., using `contextvars`).
> - Handle uncaught asyncio exceptions at the event loop level, log them with trace/correlation ID.

---

## 💻 Code Generation & Configuration Prompts

These prompts are tailored for generating code, integrating tools, and configuring infrastructure based on the observability architecture.

### 1. FastAPI Middleware + Logging + Error Handling (Backend Core)
```prompt
Generate a FastAPI middleware that:
- Extracts a `X-Correlation-ID` header (generates one if missing).
- Stores it in a context variable for use across the request lifecycle.
- Injects it into the logging context (using Loguru).
- Supports OpenTelemetry context propagation.

Also:
- Add exception handlers for `RequestValidationError`, `HTTPException`, and a base `AppException` class.
- Log all unhandled exceptions with full stack trace, correlation ID, request info.
- Return a structured error response following RFC 7807 (Problem Details JSON format).


2. Structured Logging with Loguru and OpenTelemetry Integration

```bash
Write a Loguru setup for FastAPI that:
- Outputs structured JSON logs with fields: timestamp, level, message, correlation_id, user_id (if any), path, status_code.
- Routes logs to both local files and an OpenTelemetry-compatible handler (OTLP exporter).
- Demonstrates how to bind context (e.g., correlation_id) globally and per-request.
- Includes a custom handler to transform Loguru records into OpenTelemetry LogData format.
```

3. Frontend Logging + Error Reporting Endpoint Integration
```bash
Generate a TypeScript module using Winston for React that:
- Sends structured logs to a backend `/api/frontend-log` endpoint.
- Includes: correlation ID, user ID (if available), page/component name, error stack, browser info.
- Catches and logs uncaught exceptions (global error handler and React ErrorBoundary).
- Integrates with Apollo GraphQL error handling (for network + GraphQL errors).

Also generate:
- A FastAPI endpoint to receive this log payload and re-log it via Loguru with correct context.
```

4. OpenTelemetry Configuration (Backend & Collector)
```bash
Write the OpenTelemetry setup for a FastAPI backend that:
- Automatically instruments routes for tracing (with correlation/traceparent headers).
- Sets up OTLP exporters for logs, metrics, and traces to an OpenTelemetry Collector.
- Uses environment-based configuration for collector endpoints.

Also generate:
- A minimal `otel-collector-config.yaml` that:
  - Accepts OTLP input.
  - Exports logs to Loki, traces to Jaeger, and metrics to Prometheus.
  ```

5. Grafana Dashboards and Alert Rules
```bash
Describe how to configure Grafana to:
- Visualize error rates, request latency, and correlation-ID-linked traces/logs.
- Set alert thresholds for:
  - 5xx error rate > 1% for 5 minutes.
  - Latency > 1s on key routes.
  - Log volume spike > 50% compared to prior 5-min average.
- Use Loki and Prometheus as data sources.
- Provide example PromQL and log queries for those alerts.
```

6. Pydantic + Type Hints + Docs
```bash
Generate a FastAPI route handler with:
- Typed request and response models (using Pydantic).
- Complete OpenAPI auto-docs support.
- Error response schema using Problem Details format.
- Type hints for all function inputs/outputs.

Also include:
- Docstrings with Sphinx-style comments for autodoc generation.
```
Optional: Loguru-to-OTel Handler Stub
```bash
Generate a custom Loguru sink/handler that:
- Converts Loguru records to OpenTelemetry LogData.
- Injects correlation_id and other context.
- Sends logs to OTLP exporter endpoint.
- Caches/queues logs if exporter is temporarily unavailable.
```
