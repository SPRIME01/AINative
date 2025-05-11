```mermaid
erDiagram
    Mission {
        string name
        string description
    }

    Goal {
        string name
        string description
    }

    Strategy {
        string name
        string description
    }

    Objective {
        string name
        string description
    }

    Key_Result {
        string name
        string measurement
        string target
    }

    Plan {
        string name
        string period
    }

    Tactic {
        string name
        string description
    }

    Maneuver {
        string name
        string description
    }

    Task {
        string name
        string description
        string status
    }

    Mission ||--o{ Goal : has
    Goal ||--o{ Strategy : achieved_by
    Strategy ||--o{ Objective : broken_into
    Objective ||--o{ Key_Result : measured_by
    Strategy ||--o{ Plan : implemented_by
    Plan ||--o{ Tactic : includes
    Plan ||--o{ Maneuver : includes_specific
    Tactic ||--o{ Task : composed_of
    Maneuver ||--o{ Task : composed_of
    Task }|..|>  Objective : contributes_to
    Tactic }|..|>  Objective : achieves
    Maneuver }|..|>  Objective : achieves
```

**Explanation of the ER Diagram:**

This diagram illustrates the relationships between the concepts:

1.  **Mission** is the foundational entity. It represents the core purpose.
2.  A **Mission** `has` one or more **Goals** (`||--o{`).
3.  Each **Goal** is `achieved_by` one or more **Strategies** (`||--o{`).
4.  Each **Strategy** is `broken_into` one or more **Objectives** (`||--o{`).
5.  Each **Objective** is `measured_by` one or more **Key Results** (`||--o{`). This shows how success for an objective is quantified.
6.  A **Strategy** is `implemented_by` one or more **Plans** (`||--o{`). A strategy can require multiple plans over time or across different parts of an organization.
7.  A **Plan** `includes` one or more **Tactics** (`||--o{`). The plan details the set of tactics to be used.
8.  A **Plan** `includes_specific` zero or more **Maneuvers** (`||--o{`). Not all plans will have explicitly defined "maneuvers," but they are a type of specific action that can be included.
9.  Each **Tactic** is `composed_of` one or more **Tasks** (`||--o{`). Tasks are the individual steps that make up a tactic.
10. Each **Maneuver** is `composed_of` one or more **Tasks** (`||--o{`). Tasks are also the individual steps within a maneuver.
11. **Tasks**, **Tactics**, and **Maneuvers** `contribute_to` or `achieve` **Objectives** (`}|..|>`). The dashed lines and arrow indicate that these lower-level elements are performed with the purpose of fulfilling the higher-level objectives. This isn't a strict containment relationship but shows the flow of contribution towards the desired outcomes.

This ERD provides a structured view of how these different levels of planning and execution connect, from the high-level mission down to the specific tasks and their measurable results.
