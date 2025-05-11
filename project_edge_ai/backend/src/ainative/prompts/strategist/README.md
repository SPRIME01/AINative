# Strategist Agent Prompts

This directory contains the prompt definitions for the **Strategist Agent**.

## Files
-   **`system_prompt.md`**: The main system prompt that defines the agent's role, capabilities, tasks, interaction style, and output format. This is the core instruction set for the LLM.
-   **`user_examples.md`**: Contains example interactions (user input and ideal agent output) to further guide the LLM's behavior and demonstrate expected response patterns. These can be used for few-shot prompting or fine-tuning.

## Purpose
The Strategist Agent assists with high-level planning, goal alignment, OKR refinement, and prioritization. It acts as a thought partner to ensure the user stays focused on their strategic objectives.

## Customization
-   Modify `system_prompt.md` to adjust the agent's core behavior, add new capabilities, or change its persona.
-   Add more examples to `user_examples.md` to cover a wider range of scenarios or to refine its responses for specific types of requests.
-   Ensure that any changes are consistent with the overall architecture and the capabilities of the chosen LLM for this agent.
