# Builder Agent Prompts

This directory contains the prompt definitions for the **Builder Agent**.

## Files
-   **`system_prompt.md`**: The main system prompt that defines the agent's role, capabilities, tasks, interaction style, and output format. This is the core instruction set for the LLM.
-   **`user_examples.md`**: Contains example interactions (user input and ideal agent output) to further guide the LLM's behavior and demonstrate expected response patterns for code generation, Dockerfiles, etc.

## Purpose
The Builder Agent is focused on code generation, debugging assistance, and DevOps tasks. It helps draft scripts, set up containerized environments, and build CI/CD pipelines. It's designed to be effective with function-calling and REPL interactions where appropriate.

## Customization
-   Modify `system_prompt.md` to specify preferred coding languages, frameworks, or DevOps tools.
-   Add more examples to `user_examples.md` for specific types of code snippets (e.g., API clients, data processing functions) or more complex DevOps configurations.
-   If integrating with a REPL or specific function-calling capabilities, ensure the system prompt reflects how the agent should utilize these tools.
