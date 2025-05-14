# Edge AI Agent System: Quick Reference Guide

## Overview

This quick reference guide provides an at-a-glance summary of the Edge AI Agent System components, their relationships, and key implementation details. It serves as a navigational aid to the more comprehensive documentation.

## Documentation Map

| Document | Description | Key Topics |
|----------|-------------|------------|
| [EdgeAI_Comprehensive_Documentation.md](EdgeAI_Comprehensive_Documentation.md) | Complete system overview | All system components and architecture |
| [Projects_Documentation.md](Projects_Documentation.md) | Project structure and management | Project components, lifecycle, case files |
| [Artifacts_Documentation.md](Artifacts_Documentation.md) | Artifact types and management | Cognitive, intellectual, and information artifacts |
| [Agents_Documentation.md](Agents_Documentation.md) | Core system agents | Agent architecture, roles, configuration |
| [Custom_Agents_Documentation.md](Custom_Agents_Documentation.md) | Custom team member agents | Creation, grounding, behavior types |
| [System_Integration_Guide.md](System_Integration_Guide.md) | Integration of components | Workflows, deployment, optimization |
| [Model_Context_Protocol.md](Model_Context_Protocol.md) | Agent memory management | Context windows, memory tiers, embeddings |

## Key Components at a Glance

### Projects

- **Project**: Workspace with project manager agent, team members, case file, knowledge graph
- **Project Manager Agent**: Dedicated AI agent that oversees a specific project
- **Team Members**: Both human and AI (custom agents) assigned to projects
- **Case File**: Central storage for all project artifacts
- **Knowledge Graph**: Tracks relationships between entities in a project

### Artifacts

- **Cognitive Artifacts**: Input tools (notes, forms, worksheets)
- **Intellectual Artifacts**: Products (reports, code, designs)
- **Information Products**: QA-validated intellectual artifacts

### Core System Agents

| Agent | Role | Primary Model |
|-------|------|---------------|
| Strategist | Strategic planning | Mistral 7B |
| Builder | Code generation | CodeLLaMA 7B |
| Planner | Task scheduling | Phi-2 |
| Critic | Risk assessment | Mistral 7B |
| Synthesizer | Content summarization | Mistral 7B / Yi 6B |
| Archivist | Knowledge management | TinyLlama / Phi-2 |
| Execution Builder | Deployment building | CodeLLaMA 7B |
| Watcher | System monitoring | Phi-2 / Mistral 7B |

### Custom Agents

- **Behavior Types**: Autonomous, semi-autonomous, reactive, scheduled
- **Implementation**: SmolAgents with tools, memory, agent scripts
- **Grounding**: Created using cognitive and intellectual artifacts
- **Assignment**: Can be assigned to projects, tasks, artifacts

###  (ACP)

- **Input Pruning**: Selecting relevant information for context windows
- **Summarization**: Condensing information for long-term retention
- **Embedding**: Vector representations for memory retrieval
- **Memory Tiers**: Working, short-term, and long-term memory

## System Architecture

```
+---------------------------+
|      Application Layer    |
|  +---------+ +---------+  |
|  | Projects | | Custom  |  |
|  |         | | Agents  |  |
|  +---------+ +---------+  |
|  +---------+ +---------+  |
|  |Artifacts| |Knowledge|  |
|  |         | | Graphs  |  |
|  +---------+ +---------+  |
+---------------------------+
+---------------------------+
|       Domain Layer        |
|  +---------+ +---------+  |
|  |  Agent  | |  Core   |  |
|  |  Core   | |  Ports  |  |
|  +---------+ +---------+  |
+---------------------------+
+---------------------------+
|    Infrastructure Layer   |
|  +---------+ +---------+  |
|  |   LLM   | | Memory  |  |
|  | Adapters| | Adapters|  |
|  +---------+ +---------+  |
|  +---------+             |
|  |   A2A   |             |
|  | Adapters|             |
|  +---------+             |
+---------------------------+
```

## Key Workflows

### Project Workflow

1. Create project with Project Manager Agent
2. Add team members (human and AI)
3. Create cognitive artifacts for planning
4. Develop intellectual artifacts
5. Review and publish information products

### Custom Agent Workflow

1. Create grounding artifacts
2. Configure SmolAgent with tools and behavior
3. Assign agent to project or task
4. Agent creates and consumes artifacts
5. Optionally publish to agent library

### Agent Communication

1. Agents use A2A ports for communication
2. Messages follow standardized format
3. Multiple communication patterns (direct, pub/sub, etc.)
4. Message passing via adapters (Redis, file-based, etc.)

## Implementation Checklist

### System Setup

- [ ] Install required dependencies
- [ ] Configure model server (Ollama, Triton)
- [ ] Set up Redis for memory and messaging
- [ ] Configure file system for artifacts
- [ ] Initialize vector databases

### Core Components

- [ ] Implement domain layer (Agent, ports)
- [ ] Implement infrastructure adapters
- [ ] Create service layer
- [ ] Develop API endpoints

### Projects and Artifacts

- [ ] Implement project creation
- [ ] Set up case file structure
- [ ] Create artifact management system
- [ ] Implement knowledge graph

### Agents

- [ ] Configure core system agents
- [ ] Set up agent factory
- [ ] Implement agent orchestrator
- [ ] Create custom agent framework

### Optimization

- [ ] Configure model sharing
- [ ] Implement lazy loading
- [ ] Set up monitoring
- [ ] Optimize ACP for each agent

## Quick Tips

1. **Start Simple**: Begin with core agents before adding custom agents
2. **Model Selection**: Match models to agent roles and tasks
3. **Resource Management**: Monitor and manage GPU usage carefully
4. **Context Optimization**: Tune ACP for each agent's specific needs
5. **Security**: Implement proper access control for artifacts
6. **Testing**: Test agent interactions in controlled environments first
7. **Documentation**: Keep documentation of custom agents up to date
8. **Versioning**: Version control all artifacts and agent configurations

## Glossary

- **A2A**: Agent-to-Agent communication protocol
- **Adapter**: Implementation of a port interface
- **Case File**: Storage structure for project artifacts
- **Hexagonal Architecture**: Architecture with core logic separated from external dependencies
- **ACP**:  for managing agent memory and context
- **Port**: Abstract interface defining interaction capabilities
- **SmolAgent**: Lightweight agent implementation for custom agents

## Next Steps

1. Review the comprehensive documentation
2. Set up the basic environment
3. Implement core system agents
4. Create your first project
5. Develop custom agents for specific needs
6. Optimize for edge hardware constraints
7. Scale as needed with additional projects

For detailed implementation guidance, refer to the individual documentation files for each component.
