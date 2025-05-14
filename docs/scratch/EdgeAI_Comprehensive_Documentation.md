# Edge AI Agent System Documentation

## Table of Contents

- [Edge AI Agent System Documentation](#edge-ai-agent-system-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Projects](#projects)
    - [Project Structure](#project-structure)
      - [Domain Model](#domain-model)
    - [Project Management](#project-management)
    - [Case Files](#case-files)
    - [Knowledge Graphs](#knowledge-graphs)
  - [Artifacts](#artifacts)
    - [Artifact Types](#artifact-types)
    - [Artifact Lifecycle](#artifact-lifecycle)
    - [Artifact Access Control](#artifact-access-control)
    - [Artifact Storage](#artifact-storage)
  - [Core System Agents](#core-system-agents)
    - [Agent Architecture](#agent-architecture)
    - [Agent Communication](#agent-communication)
    - [Agent Configuration](#agent-configuration)
    - [Individual Agent Documentation](#individual-agent-documentation)
      - [1. Strategist Agent](#1-strategist-agent)
      - [2. Builder Agent](#2-builder-agent)
      - [3. Planner Agent](#3-planner-agent)
      - [4. Critic Agent](#4-critic-agent)
      - [5. Synthesizer Agent](#5-synthesizer-agent)
      - [6. Archivist Agent](#6-archivist-agent)
      - [7. Execution Builder Agent](#7-execution-builder-agent)
      - [8. Watcher Agent](#8-watcher-agent)
  - [Custom Agents](#custom-agents)
    - [Custom Agent Types](#custom-agent-types)
    - [Creating Custom Agents](#creating-custom-agents)
    - [Grounding Artifacts](#grounding-artifacts)
    - [Agent Library](#agent-library)
  - [Integration and API](#integration-and-api)
    - [Service Layer](#service-layer)
    - [Infrastructure Layer](#infrastructure-layer)
    - [API Endpoints](#api-endpoints)

## Introduction

The Edge AI Agent System is designed to run on NVIDIA Jetson AGX Orin hardware, providing a collaborative multi-agent infrastructure for local AI processing. The system follows a hexagonal architecture (ports and adapters pattern) to ensure:

- **Vendor neutrality**: No direct dependency on specific LLM providers
- **Modularity**: Components can be swapped or upgraded independently
- **Testability**: Core business logic separated from external dependencies
- **Flexibility**: Easy integration with new models or communication channels

This document outlines the key components, including projects, artifacts, core agents, and custom agents, as well as how they interact within the system.

## Projects

### Project Structure

Projects in the Edge AI Agent System are organized workspaces that contain:

- A dedicated Project Manager AI Agent
- Team members (both human and AI)
- A collection of artifacts stored in a case file
- Project-specific knowledge graphs

Each project follows a structured approach to managing tasks, artifacts, and team interactions.

#### Domain Model

```
Project (id, name, manager_agent, case_file_path)
TeamMember (id, name, type[human|ai], behavior[autonomous|semi|reactive|scheduled])
Artifact (id, project_id, owner_id, type[cognitive|intellectual|info], path, locked)
KnowledgeGraph (id, scope[project|agent|workspace], graph_path)
```

### Project Management

Each project has a dedicated Project Manager AI Agent that:

- Oversees the project execution
- Manages project team members
- Recommends cognitive artifacts to users as needed
- Identifies appropriate agents from the library
- Ensures efficient collaboration between team members
- Maintains the project knowledge graph

Project Manager Agents are distinct from the core system agents and custom team member agents, with specialized capabilities for project coordination.

### Case Files

All project-related artifacts (cognitive, intellectual, and information products) are stored in a dedicated "case file" for that project. This centralizes all project information and outputs, providing:

- Organized storage of all project artifacts
- Version history and artifact tracking
- Access control for artifacts within the project
- Simple retrieval of related artifacts

### Knowledge Graphs

Every project maintains knowledge graphs that track the relationships between entities:

- **Project Knowledge Graph**: Captures relationships between artifacts, team members, and tasks within a project
- **Agent Knowledge Graph**: Tracks agent-specific knowledge and relationships
- **Workspace Knowledge Graph**: Connects multiple projects within a user's workspace

Knowledge graphs are essential for context awareness, relationship tracking, and intelligent agent recommendations.

## Artifacts

### Artifact Types

The system organizes artifacts into three main categories:

1. **Cognitive Artifacts**
   - **Definition**: Cognitive artifacts are inputs or thinking tools
   - **Examples**: Notes, lists, forms, worksheets, blank questionnaires
   - **Usage**: Used to structure thought processes, gather initial information, and facilitate brainstorming

2. **Intellectual Artifacts**
   - **Definition**: Intellectual artifacts are products derived from individual or groups of cognitive artifacts
   - **Examples**: Reports, blueprints, plans, software, scripts, creative works
   - **Usage**: Represent the output of cognitive work, can be revised and improved upon

3. **Information Products**
   - **Definition**: Information products are intellectual artifacts that have undergone and successfully passed a Quality Assurance (QA) process
   - **Relationship**: They represent a validated and finalized version of an intellectual artifact
   - **Usage**: Considered robust, verified outputs that can be relied upon for further work

### Artifact Lifecycle

Artifacts follow a typical lifecycle within the system:

1. **Creation**: Artifacts are created by users or agents within a project context
2. **Assignment**: Artifacts can be assigned to specific team members or agents
3. **Modification**: Cognitive and intellectual artifacts may undergo revisions
4. **Review**: Intellectual artifacts can be reviewed and QA-checked
5. **Publication**: Upon passing QA, intellectual artifacts become information products
6. **Archival**: The Archivist agent ensures artifacts are properly stored and indexed

### Artifact Access Control

Artifact access is managed through ownership and permissions:

- Artifacts can be owned by users or agents
- Creators can lock artifacts to restrict access
- Artifacts can be shared with specific team members
- Locks can be applied to prevent modifications
- Published artifacts may be available to a wider audience

### Artifact Storage

Artifacts are stored in a structured file system with:

- Project-specific case file directories
- Type-based organization
- Metadata tracking
- Version control capabilities
- Knowledge graph integration

## Core System Agents

The Edge AI Agent System includes eight core system agents that handle different aspects of the system's functionality.

### Agent Architecture

The agent system follows a hexagonal architecture with:

- **Domain Layer (Core)**: Independent of any specific technology
- **Infrastructure Layer (Adapters)**: Contains concrete implementations of ports
- **Application Layer (Use Cases)**: Handles specific application scenarios

The core agent implementation is independent of specific technologies:

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

### Agent Communication

Agents communicate using their configured A2A (Agent-to-Agent) port adapters with several communication patterns:

1. **Direct Communication**: Point-to-point messaging between agents
2. **Publish-Subscribe (Pub/Sub)**: Broadcasting to multiple subscribers
3. **Request-Response**: Sequential request and response interaction
4. **Event-Driven**: Reacting to events from sources

#### A2A Port Interface

The Agent-to-Agent communication is abstracted through the `A2APort` interface:

```python
class A2APort(Protocol):
    """Abstract interface for agent-to-agent communication."""

    def send_message(self, message: Dict[str, Any], recipient_id: str) -> bool:
        """Send a message to another agent."""
        ...

    def receive_messages(self) -> List[Dict[str, Any]]:
        """Retrieve messages sent to this agent."""
        ...
```

#### Standard Message Format

All inter-agent messages follow a standard format for consistency:

```python
message = {
    "message_id": f"msg_{uuid.uuid4().hex}",
    "sender_id": "agent_a_id",
    "recipient_id": "agent_b_id",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "message_type": "task_assignment",
    "payload_type": "application/json",
    "payload": {
        # Message-specific content
    },
    "metadata": {
        "priority": "high",
        "correlation_id": "related_message_id",
        "ttl": 3600  # Time-to-live in seconds
    }
}
```

#### Communication Adapters

The system provides multiple A2A adapters to support different communication patterns:

1. **Redis-based Pub/Sub Adapter:**

```python
class RedisPubSubA2AAdapter(A2APort):
    """Redis Pub/Sub based agent-to-agent communication adapter."""

    def __init__(self, agent_id: str, redis_url: str = "redis://localhost:6379"):
        self.agent_id = agent_id
        self.redis_client = redis.from_url(redis_url)
        self.pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)
        self.inbox_channel = f"agent:{self.agent_id}:inbox"

        # Subscribe to agent's inbox channel
        self.pubsub.subscribe(self.inbox_channel)

    def send_message(self, message: Dict[str, Any], recipient_id: str) -> bool:
        """Sends a message to the recipient agent's inbox channel via Redis Pub/Sub."""
        recipient_channel = f"agent:{recipient_id}:inbox"

        # Ensure message has required fields
        if "message_id" not in message:
            message["message_id"] = f"msg_{uuid.uuid4().hex}"

        if "sender_id" not in message:
            message["sender_id"] = self.agent_id

        if "timestamp" not in message:
            message["timestamp"] = datetime.now(timezone.utc).isoformat()

        try:
            self.redis_client.publish(recipient_channel, json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False

    def receive_messages(self) -> List[Dict[str, Any]]:
        """Receives messages from the agent's inbox channel."""
        messages = []

        try:
            # Get all pending messages
            while True:
                message = self.pubsub.get_message()
                if not message:
                    break

                if "data" in message and isinstance(message["data"], bytes):
                    try:
                        data = json.loads(message["data"].decode("utf-8"))
                        messages.append(data)
                    except json.JSONDecodeError:
                        logger.error("Received invalid JSON message")

        except Exception as e:
            logger.error(f"Error receiving messages: {str(e)}")

        return messages
```

2. **File-based Communication Adapter:**

```python
class FileBased_A2A_Adapter(A2APort):
    """File-based agent-to-agent communication adapter."""

    def __init__(self, agent_id: str, base_dir: str = "/tmp/agent_messages"):
        self.agent_id = agent_id
        self.base_dir = base_dir
        self.inbox_dir = os.path.join(base_dir, agent_id, "inbox")
        self.outbox_dir = os.path.join(base_dir, agent_id, "outbox")

        # Create directories if they don't exist
        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.outbox_dir, exist_ok=True)

    def send_message(self, message: Dict[str, Any], recipient_id: str) -> bool:
        """Sends a message to another agent by writing to their inbox directory."""
        if "message_id" not in message:
            message["message_id"] = f"msg_{uuid.uuid4().hex}"

        if "sender_id" not in message:
            message["sender_id"] = self.agent_id

        if "timestamp" not in message:
            message["timestamp"] = datetime.now(timezone.utc).isoformat()

        recipient_inbox = os.path.join(self.base_dir, recipient_id, "inbox")
        if not os.path.exists(recipient_inbox):
            os.makedirs(recipient_inbox, exist_ok=True)

        message_path = os.path.join(recipient_inbox, f"{message['message_id']}.json")

        try:
            with open(message_path, 'w') as f:
                json.dump(message, f)

            # Also save a copy in our outbox
            outbox_path = os.path.join(self.outbox_dir, f"{message['message_id']}.json")
            with open(outbox_path, 'w') as f:
                json.dump(message, f)

            return True
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False

    def receive_messages(self) -> List[Dict[str, Any]]:
        """Receives messages by reading files from the agent's inbox directory."""
        messages = []

        try:
            for filename in os.listdir(self.inbox_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(self.inbox_dir, filename)

                    with open(file_path, 'r') as f:
                        message = json.load(f)
                        messages.append(message)

                    # Optionally move processed messages to avoid re-processing
                    processed_dir = os.path.join(self.inbox_dir, "processed")
                    os.makedirs(processed_dir, exist_ok=True)
                    shutil.move(file_path, os.path.join(processed_dir, filename))

        except Exception as e:
            logger.error(f"Error receiving messages: {str(e)}")

        return messages
```

#### Communication Pattern Examples

##### Direct Communication (Point-to-Point)

```python
# Assume agent_a and agent_b are configured with appropriate A2A adapters

task_payload = {
    "task_name": "analyze_document",
    "document_id": "doc_123",
    "priority": "high"
}

message = {
    "message_id": f"msg_{uuid.uuid4().hex}",
    "sender_id": agent_a.agent_id,
    "recipient_id": agent_b.agent_id,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "message_type": "task_assignment",
    "payload_type": "application/json",
    "payload": task_payload
}

# Send the message
if agent_a.communication.send_message(message, agent_b.agent_id):
    logger.info(f"Task assigned from {agent_a.agent_id} to {agent_b.agent_id}")

# Recipient agent receives the message
incoming_messages = agent_b.communication.receive_messages()
for msg in incoming_messages:
    if msg.get("message_type") == "task_assignment":
        agent_b.process_task(msg["payload"])
```

##### Publish-Subscribe Pattern

```python
# Using Redis PubSub adapter for broadcast communication
# One publisher, multiple subscribers

# Publisher agent sends a notification
alert_payload = {
    "alert_type": "system_update",
    "severity": "medium",
    "details": "System upgrade scheduled in 10 minutes."
}

broadcast_message = {
    "message_id": f"msg_{uuid.uuid4().hex}",
    "sender_id": system_agent.agent_id,
    "recipient_id": "all",  # Special designation for broadcast
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "message_type": "system_alert",
    "payload_type": "application/json",
    "payload": alert_payload
}

# Send to a broadcast channel
redis_client.publish("broadcast:system_alerts", json.dumps(broadcast_message))

# Multiple agents subscribe to the broadcast channel
for agent in [agent_a, agent_b, agent_c]:
    agent.subscribe_to_channel("broadcast:system_alerts")

    # Each agent processes the broadcast
    messages = agent.get_channel_messages("broadcast:system_alerts")
    for msg in messages:
        if msg.get("message_type") == "system_alert":
            agent.handle_system_alert(msg["payload"])
```

##### Request-Response Pattern

```python
# Agent A makes a request to Agent B and waits for a response

request_payload = {
    "query": "What is the current status of project X?",
    "response_channel": f"response:{agent_a.agent_id}:{uuid.uuid4().hex}"
}

request_message = {
    "message_id": f"req_{uuid.uuid4().hex}",
    "sender_id": agent_a.agent_id,
    "recipient_id": agent_b.agent_id,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "message_type": "information_request",
    "payload_type": "application/json",
    "payload": request_payload,
    "metadata": {
        "needs_response": True,
        "response_channel": request_payload["response_channel"]
    }
}

# Send the request
agent_a.communication.send_message(request_message, agent_b.agent_id)

# Agent B processes the request
incoming_requests = agent_b.communication.receive_messages()
for req in incoming_requests:
    if req.get("message_type") == "information_request" and req.get("metadata", {}).get("needs_response"):
        # Process the request and prepare response
        response_data = agent_b.process_information_request(req["payload"]["query"])

        # Send response back through the specified channel
        response_channel = req["metadata"]["response_channel"]
        response_message = {
            "message_id": f"resp_{uuid.uuid4().hex}",
            "sender_id": agent_b.agent_id,
            "recipient_id": req["sender_id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message_type": "information_response",
            "payload_type": "application/json",
            "payload": response_data,
            "metadata": {
                "in_response_to": req["message_id"]
            }
        }

        # Publish the response to the response channel
        redis_client.publish(response_channel, json.dumps(response_message))

# Agent A waits for and processes the response
agent_a.subscribe_to_channel(request_payload["response_channel"])
response = None

# With timeout to avoid infinite waiting
start_time = time.time()
timeout = 30  # seconds

while not response and (time.time() - start_time) < timeout:
    channel_messages = agent_a.get_channel_messages(request_payload["response_channel"])
    for msg in channel_messages:
        if msg.get("message_type") == "information_response" and msg.get("metadata", {}).get("in_response_to") == request_message["message_id"]:
            response = msg["payload"]
            break

    if not response:
        time.sleep(0.5)  # Avoid tight polling

if response:
    agent_a.handle_information_response(response)
else:
    logger.warning(f"No response received from {agent_b.agent_id} within timeout period")
```

##### Event-Driven Pattern

```python
# Event source emits events that agents can react to

# Event emission
system_event = {
    "event_id": f"evt_{uuid.uuid4().hex}",
    "event_type": "resource_threshold_exceeded",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "source": "system_monitor",
    "data": {
        "resource": "memory",
        "current_usage": 85.4,
        "threshold": 80.0,
        "hostname": "edge-device-007"
    }
}

# Publish to event channel
redis_client.publish("events:resource_monitoring", json.dumps(system_event))

# Agent subscribes to relevant event channels and reacts
agent_monitoring.subscribe_to_channel("events:resource_monitoring")

# Periodic event processing
def process_resource_events(agent):
    events = agent.get_channel_messages("events:resource_monitoring")
    for event in events:
        if event.get("event_type") == "resource_threshold_exceeded":
            # Take action based on the event
            if event["data"]["resource"] == "memory":
                agent.trigger_memory_optimization(event["data"]["hostname"])
            elif event["data"]["resource"] == "cpu":
                agent.adjust_workload_distribution(event["data"]["hostname"])

# Run event processing periodically
schedule.every(1).minutes.do(process_resource_events, agent_monitoring)
```

#### Best Practices for Agent Communication

1. **Error Handling**: Implement robust error handling for communication failures
   - Retry mechanisms for temporary failures
   - Dead letter queues for undeliverable messages
   - Logging and alerting for communication issues

2. **Message Delivery Guarantees**:
   - Implement acknowledgment systems for critical messages
   - Consider transaction support for multi-step communications
   - Design for idempotent message handling

3. **Security Considerations**:
   - Authenticate message senders
   - Encrypt sensitive payloads
   - Implement access control for message channels
   - Sign messages for integrity verification

4. **Performance Optimization**:
   - Batch non-urgent messages
   - Implement backpressure mechanisms
   - Use message compression for large payloads
   - Set appropriate TTL (Time-to-Live) values

5. **Monitoring and Debugging**:
   - Log message metadata for traceability
   - Implement correlation IDs for tracking message chains
   - Monitor message queues for bottlenecks
   - Implement circuit breakers for degraded services

### Agent Configuration

Each agent is configured with:

- **LLM Provider**: Appropriate quantized models for their task needs
- **Memory System**: For state tracking and context management
- **Communication Adapter**: For agent-to-agent interaction
- **System Prompt**: Defines the agent's role and behavior
- **Tools and Access Policies**: Specifies what the agent can access and modify

### Individual Agent Documentation

#### 1. Strategist Agent

**Role**: High-level decision-making, prioritization, strategic planning

**Primary Model**: Mistral 7B Q4_K_M (good balance of planning and resource usage)

**Tools & Access**:
- Access to OKRs, goals, and strategic documents
- Can write to strategic drafts and plans

#### 2. Builder Agent

**Role**: Code generation, debugging, devops

**Primary Model**: Code LLaMA 7B Q5_K_M (optimized for fast local code generation)

**Tools & Access**:
- Code generator and formatter
- CLI interaction module
- Read access to plans and specs
- Write access to code directories

#### 3. Planner Agent

**Role**: Task planning, scheduling, scope control

**Primary Model**: Phi-2 (efficient, ideal for shorter-context task planning)

**Tools & Access**:
- Time-block generator
- Access to task logs and calendars
- Priority queue manager
- Dependency resolver

#### 4. Critic Agent

**Role**: Risk detection, refining, counter-thinking

**Primary Model**: Mistral 7B (good reasoning capabilities)

**Tools & Access**:
- Access to risk registry and checklists
- Can write to critique logs
- Access to code and plans for review

#### 5. Synthesizer Agent

**Role**: Summarization and insight generation

**Primary Model**: Mistral 7B / Yi 6B (good for summarization tasks)

**Tools & Access**:
- Semantic summarizer
- Diagram generator
- Access to raw notes and logs
- Write access to synthesis outputs

#### 6. Archivist Agent

**Role**: Memory management and knowledge organization

**Primary Model**: TinyLlama or Phi-2 (lighter models sufficient for categorization)

**Tools & Access**:
- Vector store interface
- Markdown-to-Zettelkasten converter
- Semantic tagger
- Read access to all outputs
- Write access to archives and indices

#### 7. Execution Builder Agent

**Role**: Converts designs to deployable artifacts

**Primary Model**: CodeLLaMA 7B / DeepSeek (optimized for code generation)

**Tools & Access**:
- Access to build queues and plans
- Write access to deployment artifacts
- Can generate scripts and configurations

#### 8. Watcher Agent

**Role**: Monitoring and quality assurance

**Primary Model**: Phi-2 / Mistral 7B (good for pattern recognition)

**Tools & Access**:
- System monitoring tools
- Access to logs and metrics
- Can generate alerts and reports

## Custom Agents

Custom agents are specialized AI entities that can be part of a project team, distinct from the core 8 system agents and the Project Manager AI agents.

### Custom Agent Types

Custom agents can be configured with various behavior patterns:

1. **Autonomous**: Operates independently without frequent user intervention
2. **Semi-autonomous**: Requires occasional guidance or confirmation
3. **Reactive**: Responds to specific triggers or events
4. **Scheduled**: Operates on predetermined schedules or intervals

### Creating Custom Agents

Custom agents are created using artifacts for grounding, which provide the context, knowledge, and operational parameters. They function as "little sandboxes," operating within the scope defined by their grounding artifacts.

Custom agents are implemented as SmolAgents with:
- `tools` (functions or command runners)
- `memory` (dict, file, or vector store)
- `agent_script`: defined behavior

Example SmolAgent YAML configuration:

```yaml
name: Synthesizer
tools:
  - summarize_text
  - diagram_maker
  - link_contexts
agent_script: |
  You receive structured context and need to summarize it into reports.
  1. Use summarize_text to create a TL;DR.
  2. Use diagram_maker to visualize task interconnections.
  3. Store results in the shared knowledge folder.
```

### Grounding Artifacts

Custom agents require grounding artifacts to provide:
- Context for operation
- Knowledge base
- Operating parameters
- Tool definitions
- Behavioral guidance

The creator of a custom agent has the option to lock access to these grounding artifacts if desired.

### Agent Library

Custom agents can be published to a shared or general library, allowing other users to leverage pre-built agents in their projects. The library provides:

- Categorized agent listings
- Capability descriptions
- Required grounding artifacts
- Usage instructions
- Version tracking
- Creator attribution

## Integration and API

### Service Layer

The system includes several services for managing projects, artifacts, and agents:

- **ProjectService**: create, update, list, load case file
- **TeamService**: assign/unassign members
- **ArtifactService**: create, lock, publish, list
- **GraphService**: initialize graph, query

### Infrastructure Layer

The infrastructure layer provides concrete implementations of the abstract ports defined in the domain layer:

- **LLM Adapters**: LiteLLMAdapter, OllamaAdapter, TritonAdapter
- **Memory Adapters**: RedisMemoryAdapter, FileMemoryAdapter
- **A2A Communication Adapters**: RedisPubSubA2AAdapter, FileBased_A2A_Adapter

### API Endpoints

The system exposes several endpoints for interacting with projects and artifacts:

- `POST /projects` (create)
- `GET /projects`
- `POST /projects/{id}/members` (assign)
- `POST /projects/{id}/artifacts` (create)
- `POST /artifacts/{id}/lock`
- `POST /graphs/{scope}/{id}` (init graph)

These endpoints use Pydantic schemas for validation and provide proper OpenAPI metadata.
