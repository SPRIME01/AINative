# Research Agent Prompts

This directory contains the prompt definitions for the **Research Agent**.

## Files
-   **`system_prompt.md`**: The main system prompt that defines the agent's role, capabilities, tasks, interaction style, and output format. This is the core instruction set for the LLM.
-   **`user_examples.md`**: Contains example interactions (user input and ideal agent output) to further guide the LLM's behavior and demonstrate expected response patterns.

## Purpose
The Research Agent is responsible for on-demand technical research. It summarizes documents, finds SOTA methods from a local corpus or cached web content, parses PDFs, and answers specific technical questions, integrating with a local vector database.

## Customization
-   Modify `system_prompt.md` to adjust the agent's core behavior, specify its knowledge sources more precisely, or change its output style.
-   Add more examples to `user_examples.md` to cover diverse research queries and expected summarization or Q&A formats.
-   Ensure that any changes are consistent with the agent's integration with the vector database and the types of documents it will be processing.
