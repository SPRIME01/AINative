# Project Management in Edge AI Agent System

## Overview

Projects in the Edge AI Agent System provide structured workspaces for collaborative work between humans and AI agents. Each project has a dedicated Project Manager AI Agent, a case file for storing artifacts, and a knowledge graph to track relationships between project entities.

## Project Domain Model

The project system is built around these key entities:

```
Project (id, name, manager_agent, case_file_path)
TeamMember (id, name, type[human|ai], behavior[autonomous|semi|reactive|scheduled])
Artifact (id, project_id, owner_id, type[cognitive|intellectual|info], path, locked)
KnowledgeGraph (id, scope[project|agent|workspace], graph_path)
```

## Project Components

### Project Manager AI Agent

Each project has a dedicated Project Manager AI Agent that:

- Oversees the overall execution of the project
- Recommends cognitive artifacts to users based on project needs
- Suggests appropriate agents from the library for specific tasks
- Coordinates between human and AI team members
- Monitors project progress and identifies bottlenecks
- Maintains the project knowledge graph
- Ensures project artifacts are properly categorized and stored

The Project Manager Agent is distinct from both the core system agents and custom team member agents, with specialized capabilities for project coordination and management.

### Team Members

Projects can include multiple team members of different types:

1. **Human Team Members**
   - Can create, modify, and consume artifacts
   - Can assign tasks to other team members
   - Have ownership rights over their created artifacts

2. **AI Team Members (Custom Agents)**
   - Can be added from the agent library or created for specific purposes
   - Have different behavior patterns (autonomous, semi-autonomous, reactive, scheduled)
   - Are grounded in specific artifacts that define their operation
   - Can be assigned ownership of artifacts
   - Can be reassigned between projects as needed

### Case Files

All project artifacts are stored in a centralized case file, providing:

- Structured organization of artifacts by type and relationship
- Version history tracking
- Access control mechanisms
- Searchable repository of project knowledge
- Integration with the project knowledge graph

The case file structure typically follows this pattern:

```
project_case_file/
├── cognitive_artifacts/
│   ├── notes/
│   ├── forms/
│   └── worksheets/
├── intellectual_artifacts/
│   ├── reports/
│   ├── code/
│   └── designs/
├── information_products/
│   ├── final_reports/
│   ├── approved_designs/
│   └── released_software/
└── metadata/
    ├── project_graph.json
    ├── artifact_index.json
    └── team_registry.json
```

### Knowledge Graphs

Each project maintains a knowledge graph that:

- Tracks relationships between artifacts, team members, and tasks
- Provides context for agent operations
- Enables intelligent artifact recommendations
- Supports querying for related information
- Visualizes project structure and dependencies

## Project Lifecycle

1. **Creation**: A new project is initialized with a dedicated Project Manager Agent
2. **Team Assembly**: Human and AI team members are assigned to the project
3. **Planning**: Initial cognitive artifacts are created to define project goals and structure
4. **Execution**: Team members collaborate to create and refine artifacts
5. **Review**: Intellectual artifacts undergo QA processes to become information products
6. **Completion/Archival**: Project artifacts are finalized and archived for future reference

## Integration with Core System

Projects integrate with the core system agents in several ways:

- The Strategist Agent can provide high-level direction for project goals
- The Builder Agent can assist with technical implementation
- The Critic Agent can review artifacts and identify risks
- The Synthesizer Agent can create summaries of project progress
- The Archivist Agent ensures proper indexing and storage of project artifacts

## Service Layer

The following services provide the API for project management:

- **ProjectService**: create, update, list, load case file
- **TeamService**: assign/unassign members
- **ArtifactService**: create, lock, publish, list
- **GraphService**: initialize graph, query

## API Endpoints

The system exposes these endpoints for project management:

- `POST /projects` (create a new project)
- `GET /projects` (list all projects)
- `GET /projects/{id}` (get project details)
- `POST /projects/{id}/members` (assign a team member)
- `DELETE /projects/{id}/members/{member_id}` (remove a team member)
- `GET /projects/{id}/artifacts` (list project artifacts)
- `GET /projects/{id}/graph` (retrieve project knowledge graph)

## Best Practices

1. Define clear project goals and scope at creation time
2. Select appropriate AI team members based on project needs
3. Establish consistent naming conventions for artifacts
4. Regularly review and validate the project knowledge graph
5. Use the Project Manager Agent's recommendations for cognitive artifacts
6. Define clear ownership and access policies for sensitive artifacts
7. Document project decisions in appropriate artifact types
