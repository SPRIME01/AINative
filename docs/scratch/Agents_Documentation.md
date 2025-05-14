# Agents in Edge AI Agent System

## Overview

The Edge AI Agent System employs a variety of agent types to provide comprehensive functionality. This document details the core system agents, their roles, configuration, and interaction patterns. Each agent is specialized for specific tasks and works within the hexagonal architecture that separates core logic from technology implementations.

## Agent Architecture

### Hexagonal Architecture

The agent system follows a hexagonal architecture (ports and adapters pattern) to ensure:

- **Vendor neutrality**: No direct dependency on specific LLM providers
- **Modularity**: Components can be swapped or upgraded independently
- **Testability**: Core business logic separated from external dependencies
- **Flexibility**: Easy integration with new models or communication channels

This architecture comprises:

1. **Domain Layer (Core)**: Contains the core agent behavior independent of technology
2. **Infrastructure Layer (Adapters)**: Provides concrete implementations of the ports
3. **Application Layer (Use Cases)**: Handles specific application scenarios

### Core Agent Implementation

```python
class Agent:
    """Core agent implementation independent of specific technologies."""

    def __init__(self,
                 agent_id: str,
                 system_prompt: str,
                 llm: LLMPort,
                 memory: MemoryPort,
                 communication: A2APort):
        self.agent_id = agent_id
        self.system_prompt = system_prompt
        self.llm = llm
        self.memory = memory
        self.communication = communication

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task using the agent's capabilities."""
        # Implementation of agent processing logic
        pass

    def collaborate(self, target_agent_id: str,
                   message: Dict[str, Any]) -> None:
        """Collaborate with another agent."""
        self.communication.send_message(message, target_agent_id)
```

### Ports (Interfaces)

The system defines abstract interfaces (ports) that agents use to interact with external systems:

```python
class LLMPort(Protocol):
    """Interface for language model operations."""

    def generate(self, prompt: str, system_prompt: str,
                tools: Optional[List[Dict[str, Any]]] = None) -> str:
        """Generate a response using the language model."""
        ...

    def embed(self, text: str) -> List[float]:
        """Create an embedding vector for the given text."""
        ...

class MemoryPort(Protocol):
    """Interface for agent memory operations."""

    def store(self, key: str, data: Any) -> bool:
        """Store data in the agent's memory."""
        ...

    def retrieve(self, key: str) -> Any:
        """Retrieve data from the agent's memory."""
        ...

    def search(self, query: str, limit: int = 5) -> List[Any]:
        """Search the agent's memory for relevant information."""
        ...

class A2APort(Protocol):
    """Interface for agent-to-agent communication."""

    def send_message(self, message: Dict[str, Any], recipient_id: str) -> bool:
        """Send a message to another agent."""
        ...

    def receive_messages(self) -> List[Dict[str, Any]]:
        """Receive messages from other agents."""
        ...
```

### Adapters (Implementations)

The infrastructure layer provides concrete implementations of these ports:

#### LLM Adapters
- **LiteLLMAdapter**: Unified interface to various LLM providers
- **OllamaAdapter**: Direct integration with Ollama
- **TritonAdapter**: Integration with NVIDIA Triton Inference Server

#### Memory Adapters
- **RedisMemoryAdapter**: Redis-based memory for agent state
- **FileMemoryAdapter**: File-based memory storage

#### A2A Communication Adapters
- **RedisPubSubA2AAdapter**: Redis Pub/Sub based communication
- **FileBased_A2A_Adapter**: File-based message passing

## Agent Communication

Agents communicate using their configured A2A (Agent-to-Agent) port adapters with several communication patterns:

### Communication Patterns

1. **Direct Communication (Point-to-Point)**
   - Agent A sends a message directly to Agent B
   - Simple, targeted interaction

2. **Publish-Subscribe (Pub/Sub)**
   - Publisher agent publishes to a topic
   - Multiple subscriber agents receive the message
   - Enables one-to-many communication

3. **Request-Response**
   - Requester sends a message and expects a response
   - Two-way communication with clear sequence

4. **Event-Driven**
   - Agents react to events from sources
   - Enables reactive behavior to system changes

### Message Format

A standard message format ensures consistent communication:

```python
message = {
    "message_id": f"msg_{uuid.uuid4().hex}",
    "sender_id": agent_a.agent_id,
    "recipient_id": agent_b.agent_id,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "message_type": "task_assignment",
    "payload_type": "application/json",
    "payload": {
        # Message-specific content here
    }
}
```

##  (ACP)

Each agent implements a  (ACP) that defines:

- **Input pruning**: What gets passed into the context window per call
- **Summarization strategy**: How to handle long-term memory
- **Embedding usage**: Vector search for memory recall
- **Protocol structure**: Storage of intermediate or long-term state

The ACP is essential for edge AI, optimizing the limited context windows of quantized models while maintaining persistent intelligence across sessions.

## Core System Agents

The Edge AI Agent System includes eight core system agents:

### 1. Strategist Agent

**Role Summary**: High-level decision-making, prioritization, strategic planning.

**System Prompt**:
> *You are "The Strategist", an AI agent focused on high-level decision-making, goal formulation, and strategic thinking. You help refine objectives, evaluate trade-offs, and maintain the big picture. You think systematically, identify leverage points, and formulate theories of change. You are mindful of constraints, but focus on possibilities rather than limitations.*

**Tools & Access**:
- Access to OKRs, goals, and strategic documents
- Strategic planning tools
- Write access to strategic drafts and plans

**Quantized LLM Models**:
- **Primary**: Nous Hermes 2 - Mistral 7B Q5_K_M
- **Fallback**: Mistral-Instruct 7B Q4_K_M

**ACP**:
- Maintains a strategic context window with long-term goals
- Summarizes past decisions and rationale
- Uses embeddings to recall relevant past strategies

### 2. Builder Agent

**Role Summary**: Code generation, debugging, and DevOps tasks.

**System Prompt**:
> *You are "The Builder", an AI agent designed for local, low-latency code development and debugging. You write, refactor, and explain code clearly. You are concise, follow best practices, and default to modular design. You prefer Python but can handle Bash, YAML, and Markdown. You generate code in full blocks with minimal commentary. You avoid guessing when uncertain—ask for clarification instead. You respect existing project structure and technical constraints.*

**Tools & Access**:
- Code generator and formatter
- File I/O for code directories
- Local execution sandbox
- Git integration

**Quantized LLM Models**:
- **Primary**: Code LLaMA 7B Q5_K_M
- **Fallback**: DeepSeek Coder 6.7B

**ACP**:
- Stores build context per project
- Embeds and indexes past solutions
- Surfaces reusable components during planning

### 3. Planner Agent

**Role Summary**: Translates strategic goals into executable plans, time-blocks, and schedules.

**System Prompt**:
> *You are "The Planner", an AI agent that turns strategy into executable plans. You break down goals into actions, organize time-blocks, and adjust schedules based on changing priorities. Your output is structured, time-aware, and realistic. You coordinate with The Strategist for alignment, and The Critic for feasibility checks. You always plan with urgency balanced by sustainability.*

**Tools & Access**:
- Time-block generator
- Access to task logs and calendars
- Priority queue manager
- Dependency resolver

**Quantized LLM Models**:
- **Primary**: Phi-2
- **Secondary**: Gemma 2B Q

**ACP**:
- Stores plan hierarchy and history
- Maintains task embeddings for pattern recognition
- Summarizes progress logs weekly

### 4. Critic Agent

**Role Summary**: Provides contrarian thinking, risk assessment, and constructive criticism.

**System Prompt**:
> *You are "The Critic", an AI agent specialized in identifying weaknesses, challenging assumptions, and strengthening plans through constructive criticism. Your purpose is to find what others have missed—logical gaps, unstated assumptions, edge cases, and potential risks. You're direct but never dismissive, and always pair critique with specific, actionable suggestions.*

**Tools & Access**:
- Access to risk registry and checklists
- Can analyze code and documentation
- Priority-based issue tracker

**Quantized LLM Models**:
- **Primary**: OpenOrca Mistral 7B Q4_K_M
- **Secondary**: LLaMA 2 7B Q4_0

**ACP**:
- Maintains a risk matrix
- Stores past critiques to avoid repetition
- Tracks resolution of identified issues

### 5. Synthesizer Agent

**Role Summary**: Transforms raw information into structured knowledge, creates summaries and visualizations.

**System Prompt**:
> *You are "The Synthesizer", an integrative reasoning agent that transforms raw information into structured knowledge. You condense, abstract, and formalize across domains—be it notes, research, logs, or brainstorms. You produce crisp summaries, frameworks, and schematics that reveal meaning and reduce redundancy. You think like a polymath and write like a poet-engineer.*

**Tools & Access**:
- Semantic summarizer
- Diagram generator
- Output formatter
- Access to raw notes and logs

**Quantized LLM Models**:
- **Primary**: Mistral 7B / Yi 6B
- **Secondary**: OpenHermes Mistral Q5_K_S

**ACP**:
- Maintains themes and topics across sessions
- Uses slide-window summarization for long inputs
- Creates progressive abstractions

### 6. Archivist Agent

**Role Summary**: Context management and long-term memory, categorizes and indexes agent outputs.

**System Prompt**:
> *You are "The Archivist", a context-management and long-term memory agent. You categorize, tag, and index everything the agents produce—plans, critiques, syntheses, conversations, and research. Your purpose is reliable knowledge preservation, semantic search, and time-based reflection. You ensure nothing valuable is ever lost.*

**Tools & Access**:
- Vector store interface
- Markdown-to-Zettelkasten converter
- Semantic tagger
- Access to all agent outputs

**Quantized LLM Models**:
- **Primary**: TinyLlama or Phi-2
- **Optional**: CodeLlama 7B for structure parsing

**ACP**:
- Indexes metadata per document
- Maintains persistent knowledge graph
- Controls input window using timestamped filters

### 7. Execution Builder Agent

**Role Summary**: Transforms structured input into functional outputs like code, configs, and scripts.

**System Prompt**:
> *You are "The Builder", an execution-focused agent that transforms structured input—plans, specs, diagrams—into functional outputs. You write code, configuration files, setup scripts, and integration logic. Your style prioritizes modularity, transparency, and edge-compatibility. You coordinate with The Planner for requirements and The Critic for validation.*

**Tools & Access**:
- Code generator
- CLI interaction module
- Test runner and linter
- Access to build queues and plans

**Quantized LLM Models**:
- **Primary**: CodeLLaMA 7B / DeepSeek
- **Secondary**: Mistral instruct for non-code logic

**ACP**:
- Tracks build history and diffs
- Maintains vector DB for common patterns
- Updates knowledge base with each build

### 8. Watcher Agent

**Role Summary**: System monitoring, log analysis, and alerting.

**System Prompt**:
> *You are "The Watcher", a vigilant oversight agent that monitors system health, resource usage, and agent performance. You detect anomalies, identify concerning patterns, and alert when intervention is needed. Your focus is operational awareness—tracking what's happening and what's changing. You provide regular status updates and actionable alerts with clear severity levels.*

**Tools & Access**:
- System monitoring tools
- Log parsers and analyzers
- Resource utilization trackers
- Alert configurators

**Quantized LLM Models**:
- **Primary**: Phi-2 / Mistral 7B
- **Fallback**: GPT4ALL Falcon Q4_0

**ACP**:
- Maintains sliding window of system metrics
- Tracks baseline performance
- Summarizes log patterns hourly/daily

## Agent Factory

Agents can be instantiated through an AgentFactory that configures them with appropriate adapters:

```python
class AgentFactory:
    """Creates properly configured agents with appropriate LLM models."""

    def create_strategist(self) -> Agent:
        """Create a Strategist agent."""
        llm = LiteLLMAdapter(model_name="ollama-mistral")
        memory = RedisMemoryAdapter(agent_id="strategist")
        comms = RedisPubSubA2AAdapter(agent_id="strategist")

        return Agent(
            agent_id="strategist",
            system_prompt=STRATEGIST_PROMPT,
            llm=llm,
            memory=memory,
            communication=comms
        )

    def create_builder(self) -> Agent:
        """Create a Builder agent."""
        llm = LiteLLMAdapter(model_name="ollama-codellama")
        memory = RedisMemoryAdapter(agent_id="builder")
        comms = RedisPubSubA2AAdapter(agent_id="builder")

        return Agent(
            agent_id="builder",
            system_prompt=BUILDER_PROMPT,
            llm=llm,
            memory=memory,
            communication=comms
        )
```

## Model Routing

The system can route requests to different models based on agent and task types:

```python
def get_model_for_task(agent_type: str, task_type: str) -> str:
    """Get the appropriate model for an agent and task type."""

    # Task-based model routing
    task_models = {
        "code_generation": "ollama-codellama",
        "planning": "ollama-mistral",
        "creative_writing": "ollama-mistral",
        "reasoning": "openai-gpt-4",
        "image_understanding": "ollama-llava"
    }

    # Agent-specific overrides
    agent_specific = {
        "builder": {
            "code_generation": "triton-codellama",  # Use Triton for Builder
        },
        "critic": {
            "reasoning": "openai-gpt-4"  # Always use GPT-4 for Critic's reasoning
        }
    }

    # Check for agent-specific model first
    if agent_type in agent_specific and task_type in agent_specific[agent_type]:
        return agent_specific[agent_type][task_type]

    # Fall back to task-based model
    if task_type in task_models:
        return task_models[task_type]

    # Default fallback
    return "ollama-mistral"
```

## Runtime Optimization

The system employs several optimization tactics for edge AI:

- **Model Swapping / Lazy Loading**: Only load active models to conserve VRAM
- **Shared Embedding Model**: Use a single embedding model across agents
- **GPU Scheduling**: Schedule agents to avoid inference collisions
- **Persistent Agent Memory**: Use databases for short and long-term memory
- **Inter-agent Messaging**: Lightweight message bus for coordination
- **Parallelism Limits**: Cap concurrent models on limited hardware

## Agent Directory Structure

Agents typically interact with a structured directory system:

```
/agents/
  ├── strategist/
  ├── builder/
  ├── planner/
  ├── critic/
  ├── synthesizer/
  ├── archivist/
  ├── execution_builder/
  └── watcher/

/data/
  ├── plans/
  ├── code/
  ├── logs/
  ├── outputs/
  ├── notes/
  └── archive/
```

## Best Practices

1. Match agent LLM models to their specific task requirements
2. Optimize context usage through effective ACP implementation
3. Use appropriate communication patterns for different agent interactions
4. Implement proper error handling and recovery mechanisms
5. Monitor agent performance and resource usage
6. Design agents with clear, focused responsibilities
7. Ensure agents have appropriate access control to files and services
8. Regularly update agent system prompts based on observed behavior
