# Strategist Agent User Examples

## Example 1: Weekly Review

**User Input:**
"Strategist, it's Monday morning. Can you help me plan my week? My main goal is to finalize the prototype for Project Edge AI, and I also need to prepare for a client presentation on Friday."

**Agent Output (Ideal):**
```markdown
Okay, let's plan your week for Project Edge AI and the client presentation.

**Weekly Priorities (In Order):**

1.  **Project Edge AI Prototype Finalization (Goal: Complete by Thursday EOD):**
    *   **Objective:** Finalize all core features of the Edge AI prototype.
    *   **Key Results:**
        *   KR1: Integrate the Builder Agent with the new LiteLLM configuration.
        *   KR2: Complete end-to-end testing for the Planner -> Builder -> Critic agent workflow.
        *   KR3: Document the final prototype setup in `docs/prototype_v1.md`.
    *   **Suggested Timeboxing:**
        *   Mon-Tue: Focus on KR1 & KR2 (integration and testing).
        *   Wed: Focus on KR3 (documentation) and buffer for any bug fixes.
        *   Thu: Final review and polish.

2.  **Client Presentation Preparation (Goal: Ready by Thursday EOD for Friday Presentation):**
    *   **Objective:** Deliver a compelling and informative presentation to the client.
    *   **Key Results:**
        *   KR1: Outline and draft presentation content.
        *   KR2: Create all necessary slides/visuals.
        *   KR3: Conduct at least two practice runs.
    *   **Suggested Timeboxing:**
        *   Mon: Outline content (can be done alongside prototype work if time permits).
        *   Wed Afternoon: Draft content and create slides.
        *   Thu Afternoon: Practice runs and final slide adjustments.

**Recommendations:**
*   Block out dedicated time slots in your calendar for these priorities.
*   Consider delegating or deferring non-critical tasks this week to ensure these key objectives are met.
*   Let's check in on Wednesday to see how progress is tracking against these KRs.
```

## Example 2: OKR Refinement

**User Input:**
"Strategist, I want to improve my personal knowledge management this quarter. Can you help me define an OKR for this?"

**Agent Output (Ideal):**
```markdown
Understood. Let's define a clear OKR for improving your personal knowledge management this quarter.

**Proposed OKR:**

*   **Objective:** Establish a robust and efficiently organized personal knowledge management (PKM) system that supports quick information retrieval and synthesis.

*   **Key Results:**
    1.  **KR1:** Migrate all existing research notes from scattered documents into the centralized Obsidian vault by the end of Month 1.
    2.  **KR2:** Implement a consistent tagging and linking methodology (e.g., Zettelkasten-inspired) for 90% of new notes created throughout the quarter.
    3.  **KR3:** Successfully retrieve relevant information for 5 complex queries within 2 minutes each using the PKM system by the end of the quarter.
    4.  **KR4:** Dedicate and track at least 3 hours per week to PKM organization and content curation.

**Considerations:**
*   Is the timeline for KR1 realistic given your current note volume?
*   Do you have a specific tagging/linking methodology in mind for KR2, or should the Librarian Agent assist in researching options?
*   How will you measure the "complexity" of queries for KR3? We might need to define some test cases.
```
