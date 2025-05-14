# Artifacts in Edge AI Agent System

## Overview

Artifacts are the core information units within the Edge AI Agent System. They represent different types of information products created and used by both human and AI agents. The system organizes artifacts into a structured hierarchy that reflects their purpose, level of validation, and usage patterns.

## Artifact Types

### 1. Cognitive Artifacts

**Definition:** Cognitive artifacts are inputs or thinking tools that help structure thought processes and collect information.

**Characteristics:**
- Serve as templates, guides, or frameworks for thinking
- Often structured to elicit specific types of information
- Can be partially completed or empty
- Used at the beginning of cognitive processes

**Examples:**
- Notes and observations
- Forms and questionnaires
- Worksheets
- Checklists
- Brainstorming templates
- Meeting agendas
- Interview protocols
- Decision matrices (empty/template)

**Usage:**
- Used by both humans and AI agents to structure thinking
- Often recommended by Project Manager Agents at appropriate points
- Can be created by Strategist or Planner agents
- Form the foundation for intellectual artifacts

### 2. Intellectual Artifacts

**Definition:** Intellectual artifacts are products derived from individual or groups of cognitive artifacts. They represent the output of cognitive work.

**Characteristics:**
- Contain substantive content and analysis
- Represent significant intellectual effort
- Can be refined and improved over time
- Are subject to review processes

**Examples:**
- Reports and analyses
- Blueprints and design documents
- Project plans
- Software code and scripts
- Creative works (writings, designs)
- Data visualizations
- Process diagrams
- Decision records

**Usage:**
- Created by human team members or AI agents like the Builder
- Can be reviewed by the Critic agent
- May undergo multiple revisions
- Form the basis for information products after QA

### 3. Information Products

**Definition:** Information products are intellectual artifacts that have undergone and successfully passed a Quality Assurance (QA) process.

**Characteristics:**
- Validated for accuracy and quality
- Considered final and authoritative
- May have restricted modification permissions
- Represent "source of truth" information

**Examples:**
- Final reports
- Approved designs
- Released software
- Published content
- Verified datasets
- Certified models
- Ratified decisions
- Approved policies

**Usage:**
- Used as reliable references for future work
- Often published or shared more widely
- May be used to ground custom agents
- Archived and indexed by the Archivist agent

## Artifact Lifecycle

### Creation

Artifacts can be created by:
- Human team members
- Core system agents (e.g., Strategist, Builder)
- Custom team member agents
- Project Manager Agent

The creation process typically includes:
1. Determining the appropriate artifact type
2. Selecting a template or format
3. Assigning initial metadata (owner, project context)
4. Creating the artifact content
5. Storing in the appropriate location in the case file

### Assignment and Ownership

- Artifacts have a designated owner (human or AI)
- Ownership grants control over modification and permissions
- Artifacts can be assigned to team members for specific tasks
- Ownership can be transferred as needed

### Modification and Versioning

- Cognitive and intellectual artifacts can be modified over time
- The system maintains version history for all modifications
- Changes are tracked with timestamps and author information
- Previous versions remain accessible when needed

### Review and QA

For intellectual artifacts to become information products, they undergo:
1. Review by appropriate team members or agents (e.g., Critic)
2. Validation against quality standards
3. Formal approval process
4. Classification as an information product
5. Potential permission restrictions to prevent unintended changes

### Archival

The Archivist agent ensures all artifacts are:
- Properly stored in the case file structure
- Indexed for efficient retrieval
- Connected in the knowledge graph
- Preserved with complete metadata
- Accessible for future reference

## Artifact Access Control

### Permissions

Artifacts can have various permission levels:
- **Public**: Accessible to all team members
- **Restricted**: Accessible only to specific team members
- **Private**: Accessible only to the owner
- **Locked**: Cannot be modified (read-only)

### Locking

- Artifact owners can lock artifacts to prevent modifications
- Locked artifacts can still be read and referenced
- Locking is often applied to information products
- Locked artifacts can be used to ground custom agents

### Sharing

- Artifacts can be shared with other team members
- Sharing can include read-only or modification permissions
- Sharing history is tracked in artifact metadata
- Sharing across projects requires explicit permission

## Storage and Organization

### Case File Structure

Artifacts are stored in project case files with a structured organization:
```
project_case_file/
├── cognitive_artifacts/
│   ├── [artifact_categories]/
├── intellectual_artifacts/
│   ├── [artifact_categories]/
├── information_products/
│   ├── [artifact_categories]/
└── metadata/
    ├── artifact_index.json
```

### Metadata

Each artifact includes rich metadata:
- Unique identifier
- Creation timestamp
- Last modified timestamp
- Owner information
- Type classification
- Tags and categories
- Version history
- Related artifacts
- Lock status

### Knowledge Graph Integration

Artifacts are integrated into the project knowledge graph:
- Connections to related artifacts
- Links to team members (creators, owners, contributors)
- Contextual relationships to project tasks
- Temporal relationships (prerequisites, dependencies)

## Artifacts for Custom Agents

### Grounding

Custom agents are grounded through artifacts that define:
- Their knowledge base and capabilities
- Operational parameters and constraints
- Tool access and permissions
- Behavioral patterns and responses

### Creation Process

Creating a custom agent with artifacts involves:
1. Selecting appropriate cognitive artifacts to define purpose
2. Creating intellectual artifacts that define behavior
3. Developing information products that establish knowledge
4. Configuring the agent to use these artifacts as grounding
5. Defining access patterns for other artifacts

### Transparency and Locking

- By default, the artifacts grounding a custom agent are visible
- Creator can lock grounding artifacts to protect proprietary information
- Even with locked artifacts, the agent's capabilities remain documented

## Service Layer

The artifact system is supported by the ArtifactService, which provides:

- **Creation**: `create_artifact(project_id, owner_id, type, content, metadata)`
- **Retrieval**: `get_artifact(artifact_id)`, `list_artifacts(filters)`
- **Modification**: `update_artifact(artifact_id, content, metadata)`
- **Locking**: `lock_artifact(artifact_id)`, `unlock_artifact(artifact_id)`
- **Publishing**: `publish_artifact(artifact_id)` (converts to information product)
- **Versioning**: `get_artifact_versions(artifact_id)`, `revert_to_version(artifact_id, version)`

## API Endpoints

- `POST /projects/{id}/artifacts` (create artifact)
- `GET /projects/{id}/artifacts` (list artifacts)
- `GET /artifacts/{id}` (get specific artifact)
- `PUT /artifacts/{id}` (update artifact)
- `POST /artifacts/{id}/lock` (lock artifact)
- `POST /artifacts/{id}/publish` (publish artifact as information product)
- `GET /artifacts/{id}/versions` (list artifact versions)

## Best Practices

1. Use appropriate artifact types for different stages of work
2. Create cognitive artifacts before starting complex tasks
3. Document the transition from intellectual artifacts to information products
4. Maintain clear ownership and access control
5. Use consistent naming conventions and metadata
6. Leverage knowledge graph connections to find related artifacts
7. Create appropriate grounding artifacts when designing custom agents
