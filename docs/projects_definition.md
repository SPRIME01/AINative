# Project Structure and Management

Projects within this system are designed to be collaborative and managed by AI, drawing inspiration from Claude-like project functionalities.

## Key Features:
-  **Project Creation:**
    -   Users can create projects/cases, which are essentially containers for various chats, tasks, objectives, and cognitive artifacts.
    -   Each project can have its own project brief/scope (set of goals, strategies, key results, etc).
-   **Dedicated Project Manager AI Agent:**
    -   Each project has a dedicated "project manager AI agent."
    -   This agent is responsible for managing the project, overseeing other project agents (team members), and providing recommendations.
    -   It suggests relevant cognitive artifacts to the user throughout the project lifecycle to maximize cognitive ergonomics.
    -   It may also recommend the use of agents from the general library if they are relevant and add value to the project.

-   **Team Members:**
    -   Users can add various team members to a project.
    -   Team members can be humans or AI agents.
    -   AI team members can be autonomous, semi-autonomous, reactive, or scheduled.
    -   These AI team members are distinct from the core 8 system agents and the project manager AI agents; they are custom agents (see `custom_agents_definition.md`).

-   **Case File:**
    -   All project-related artifacts (cognitive, intellectual, and information products) are stored in a dedicated "case file" for that project. This centralizes all project information and outputs.
