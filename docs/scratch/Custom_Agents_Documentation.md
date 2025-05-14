# Custom Agents in Edge AI Agent System

## Overview

Custom agents are specialized AI entities that function as team members within the Edge AI Agent System. Unlike the core system agents (Strategist, Builder, Planner, etc.) and Project Manager agents, custom agents are designed for specific project tasks and can be created, shared, and reused across projects. They operate within controlled environments defined by their grounding artifacts.

## Key Characteristics

### Nature and Purpose

Custom agents are:
- AI agents that function as team members within projects
- Created for specific tasks or domains
- Grounded in artifacts that define their knowledge and behavior
- More specialized and focused than core system agents
- Typically lighter weight than core agents
- Implemented as SmolAgents with specific tools and memory

### Behavior Types

Custom agents can have four primary behavior patterns:

1. **Autonomous**
   - Operate independently with minimal supervision
   - Make decisions within their defined scope
   - Proactively execute their assigned responsibilities
   - Example: An autonomous data processing agent that continuously processes new data

2. **Semi-autonomous**
   - Operate with some independence but require approval for key actions
   - Suggest actions but defer to human judgment for critical decisions
   - Example: A semi-autonomous copyediting agent that suggests changes but waits for approval

3. **Reactive**
   - Respond to specific triggers or events
   - Do not take action until activated by an external stimulus
   - Example: A reactive customer support agent that responds when questions are asked

4. **Scheduled**
   - Execute predefined tasks on a schedule
   - Operate at specific times or intervals
   - Example: A scheduled reporting agent that generates weekly summaries

### Implementation Details

Custom agents are implemented as SmolAgents, which feature:
- **Tools**: Functions or command runners the agent can use
- **Memory**: State storage via dict, file, or vector store
- **Agent Script**: Defined behavioral logic

Example SmolAgent YAML configuration:

```yaml
name: DataAnalyzer
tools:
  - process_csv
  - generate_chart
  - statistical_analysis
memory:
  type: vector_store
  path: ./agent_memory/data_analyzer/
agent_script: |
  You are a data analysis specialist focused on processing numerical data.
  When presented with data files:
  1. Use process_csv to load and clean the data.
  2. Apply statistical_analysis to identify key patterns.
  3. Generate visualizations with generate_chart to illustrate findings.
  4. Store your analysis in memory for future reference.
  5. Always note data quality issues or limitations in your analysis.
```

## Creation and Grounding

### Artifact Grounding

Custom agents are grounded through artifacts that provide:
- Context for their operation
- Knowledge base for their domain
- Parameters for their behavior
- Tool definitions and access patterns
- Response guidelines and limitations

The types of grounding artifacts may include:
- **Cognitive artifacts**: Define the agent's purpose and thought processes
- **Intellectual artifacts**: Provide domain knowledge and procedural information
- **Information products**: Establish verified facts and reference data

### Creation Process

To create a custom agent:

1. **Define Purpose**: Identify the specific need the agent will address
2. **Select Grounding Artifacts**: Choose or create artifacts to ground the agent
3. **Configure Behavior**: Determine the appropriate behavior type
4. **Implement SmolAgent**: Create the YAML configuration with tools, memory, and script
5. **Test and Refine**: Verify the agent's behavior in controlled scenarios
6. **Deploy**: Add the agent to a project team or publish to the library

Example creation workflow:
```python
def create_custom_agent(name, behavior_type, grounding_artifacts, tools, memory_config, script):
    """Create a new custom agent."""
    # Validate grounding artifacts
    for artifact_id in grounding_artifacts:
        if not artifact_service.artifact_exists(artifact_id):
            raise ValueError(f"Artifact {artifact_id} does not exist")

    # Create SmolAgent configuration
    config = {
        "name": name,
        "behavior_type": behavior_type,
        "grounding_artifacts": grounding_artifacts,
        "tools": tools,
        "memory": memory_config,
        "agent_script": script
    }

    # Instantiate agent
    agent_id = agent_service.register_agent(config)

    return agent_id
```

### Transparency and Locking

By default, the artifacts that ground a custom agent are visible to users, promoting transparency and explainability. However, creators have the option to lock access to these grounding artifacts if they contain proprietary information or sensitive content.

When artifacts are locked:
- Other users can still use the agent
- The agent's capabilities and behavior remain documented
- The specific implementation details are protected

## Library and Sharing

### Agent Library

Custom agents can be published to a shared library, making them available to other users. The library provides:
- Categorized listings of available agents
- Descriptions of agent capabilities
- Required resources for each agent
- Usage instructions and examples
- Version tracking and history
- Attribution to creators

### Reuse Process

To reuse an existing custom agent:
1. Browse the agent library
2. Select a suitable agent for the task
3. Review the agent's capabilities and requirements
4. Add the agent to a project team
5. Configure any necessary parameters
6. Assign the agent to specific tasks

### Versioning

Custom agents support versioning to manage improvements and changes:
- Major versions for significant behavioral changes
- Minor versions for enhancement and optimization
- Patch versions for bug fixes and small adjustments
- Version history tracking for audit and rollback

## Project Integration

### Assignment

Custom agents (like human team members) can be:
- Assigned to specific projects
- Given roles within project teams
- Allocated to particular tasks
- Reassigned as project needs change

### Artifact Interaction

Custom agents interact with project artifacts in several ways:
- **Reading**: Consuming artifacts as input for tasks
- **Writing**: Creating new artifacts as output
- **Ownership**: Taking responsibility for specific artifacts
- **Sharing**: Collaborating with other team members on artifacts

### Collaboration Patterns

Custom agents can collaborate with other team members (human or AI) through:
- **Direct coordination**: Working directly with specific team members
- **Workflow integration**: Functioning as a stage in a process
- **Supervisory relationships**: Operating under the guidance of human team members
- **Peer collaboration**: Working alongside other custom agents

## Development Examples

### Specialized Researcher Agent

```yaml
name: ResearchAssistant
behavior: semi-autonomous
tools:
  - search_documents
  - summarize_text
  - extract_citations
  - create_bibliography
memory:
  type: vector_store
  path: ./agent_memory/researcher/
agent_script: |
  You are a research assistant specializing in literature review and citation management.
  Your primary tasks are:
  1. Search project documents for relevant information on a given topic
  2. Summarize key findings and arguments from sources
  3. Extract and validate citations from academic papers
  4. Create properly formatted bibliographies in multiple citation styles

  Always note the quality and relevance of sources, and maintain proper attribution
  for all information. When uncertain about facts, indicate the level of confidence
  and suggest additional verification.
```

### Data Visualization Agent

```yaml
name: DataVisualizer
behavior: reactive
tools:
  - read_data_file
  - plot_chart
  - format_visualization
  - save_visualization
memory:
  type: file
  path: ./agent_memory/visualizer/
agent_script: |
  You are a data visualization specialist focused on creating clear, effective
  visual representations of data. When provided with data:

  1. Analyze the data structure and content
  2. Recommend the most appropriate visualization type (bar, line, scatter, etc.)
  3. Create visualizations with appropriate formatting, labels, and colors
  4. Optimize visualizations for clarity and impact
  5. Save visualizations in requested formats

  Always consider accessibility in your visualizations, including colorblind-friendly
  palettes and clear contrast. Include proper titles, legends, and source attributions.
```

## Best Practices

1. **Clear Purpose Definition**: Give each custom agent a well-defined, focused purpose
2. **Appropriate Behavior Type**: Choose the behavior type that best matches the task needs
3. **Minimal Grounding**: Include only necessary grounding artifacts to keep agents lightweight
4. **Explicit Tool Definitions**: Clearly define all tools and their functionality
5. **Memory Management**: Configure appropriate memory types and retention policies
6. **Transparent Documentation**: Document capabilities, limitations, and expected behavior
7. **Regular Evaluation**: Monitor and evaluate agent performance
8. **Versioning Discipline**: Maintain proper versioning for agent updates

## Service Layer

Custom agents are managed through several services:

- **CustomAgentService**: create, update, delete, and retrieve custom agents
- **AgentLibraryService**: publish, discover, and version agents in the library
- **AgentAssignmentService**: assign and manage agents within projects
- **AgentGradingService**: ground agents in appropriate artifacts

## API Endpoints

The system exposes these endpoints for custom agent management:

- `POST /custom-agents` (create a new custom agent)
- `GET /custom-agents` (list available custom agents)
- `GET /custom-agents/{id}` (get agent details)
- `PUT /custom-agents/{id}` (update an agent)
- `POST /custom-agents/{id}/publish` (publish to library)
- `POST /projects/{id}/assign-agent` (assign agent to project)
- `POST /custom-agents/{id}/lock-grounding` (lock grounding artifacts)
