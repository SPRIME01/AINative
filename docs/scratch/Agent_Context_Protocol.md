# Agent Context Protocol (ACP) in Edge AI Agent System

## Overview

The Agent Context Protocol (ACP) is a structured methodology for managing context windows, memory, and state persistence across agent operations in the Edge AI Agent System. It addresses the challenges of working with quantized models on edge hardware, where context windows are often limited, while ensuring consistent and intelligent agent behavior across sessions.

ACP is essential for edge AI deployments because:
- Quantized models typically have smaller context windows (2k-8k tokens)
- Edge applications require persistent intelligence across sessions
- Memory usage must be optimized for resource-constrained environments
- Context management directly impacts agent performance and capability

## Core Components

### 1. Input Pruning

Input pruning determines what information is passed into an agent's context window for each inference, including:

- **Relevance Filtering**: Selecting only the most relevant information
- **Context Compression**: Summarizing lengthy content to fit within token limits
- **Priority Ranking**: Prioritizing critical information when context space is limited
- **Token Budgeting**: Allocating tokens to different information categories

Implementation example:
```python
def prune_context(agent_id: str, raw_context: Dict[str, Any],
                 token_budget: int = 2048) -> Dict[str, Any]:
    """Prune context to fit within token budget."""
    # Tokenize all context components
    tokenized = {k: tokenizer.encode(str(v)) for k, v in raw_context.items()}
    token_counts = {k: len(v) for k, v in tokenized.items()}
    total_tokens = sum(token_counts.values())

    if total_tokens <= token_budget:
        return raw_context  # No pruning needed

    # Get component priorities for this agent
    priorities = get_agent_priorities(agent_id)

    # Sort components by priority
    sorted_components = sorted(raw_context.keys(),
                              key=lambda k: priorities.get(k, 0),
                              reverse=True)

    # Allocate tokens based on priorities
    pruned_context = {}
    remaining_budget = token_budget

    for component in sorted_components:
        if token_counts[component] <= remaining_budget:
            # Can include full component
            pruned_context[component] = raw_context[component]
            remaining_budget -= token_counts[component]
        else:
            # Must summarize this component
            if remaining_budget > 100:  # Only if reasonable budget remains
                summary = summarize_text(raw_context[component], remaining_budget)
                pruned_context[component] = summary
                remaining_budget = 0
            break  # No more budget

    return pruned_context
```

### 2. Summarization Strategy

Summarization strategy defines how information is condensed for long-term retention:

- **Sliding Window**: Incrementally summarizing ongoing conversations
- **Hierarchical Summarization**: Creating multi-level summaries (detailed → abstract)
- **Key Point Extraction**: Identifying and preserving essential points
- **Progressive Abstraction**: Gradually removing details while preserving meaning

Example implementation:
```python
class SlidingWindowSummarizer:
    """Implements sliding window summarization for progressive context reduction."""

    def __init__(self, window_size: int = 5, overlap: int = 2):
        self.window_size = window_size
        self.overlap = overlap

    def summarize(self, messages: List[Dict]) -> str:
        """Summarize a list of messages using sliding window approach."""
        if len(messages) <= self.window_size:
            # No summarization needed yet
            return None

        # Create windows with overlap
        windows = []
        for i in range(0, len(messages) - self.window_size + 1,
                      self.window_size - self.overlap):
            window = messages[i:i + self.window_size]
            windows.append(window)

        # Summarize each window
        window_summaries = []
        for window in windows:
            window_text = "\n".join([f"{m['role']}: {m['content']}" for m in window])
            summary = self._summarize_window(window_text)
            window_summaries.append(summary)

        # Create final summary
        return "\n".join(window_summaries)

    def _summarize_window(self, text: str) -> str:
        """Summarize a single window of text."""
        # This could use an LLM or a rule-based summarizer
        prompt = f"Summarize this conversation concisely while preserving key points:\n{text}"
        # Use a lightweight model for summarization
        return llm_client.generate(prompt, max_tokens=200)
```

### 3. Embedding Usage

Embedding usage defines how vector representations enable memory retrieval:

- **Semantic Indexing**: Creating searchable vector representations of information
- **Similarity Search**: Finding related information based on semantic similarity
- **Clustering**: Grouping related information for better organization
- **Dimension Reduction**: Creating efficient representations for large information sets

Example implementation:
```python
class VectorMemory:
    """Vector-based memory system for semantic search."""

    def __init__(self, embedding_model: str, vector_db_path: str):
        self.embedding_model = embedding_model
        self.vector_db = self._initialize_db(vector_db_path)

    def store(self, text: str, metadata: Dict[str, Any]) -> str:
        """Store text in vector memory."""
        # Generate embedding
        embedding = self._embed(text)

        # Generate ID
        entry_id = str(uuid.uuid4())

        # Store in vector database
        self.vector_db.add(
            vectors=embedding,
            ids=entry_id,
            metadata={
                "text": text,
                "timestamp": datetime.now().isoformat(),
                **metadata
            }
        )

        return entry_id

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for related information using semantic similarity."""
        # Generate query embedding
        query_embedding = self._embed(query)

        # Search vector database
        results = self.vector_db.search(
            queries=query_embedding,
            limit=limit
        )

        # Return results with metadata
        return [
            {
                "id": result.id,
                "text": result.metadata["text"],
                "score": result.score,
                **{k: v for k, v in result.metadata.items() if k != "text"}
            }
            for result in results
        ]

    def _embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        return embedding_client.embed(text, model=self.embedding_model)

    def _initialize_db(self, path: str):
        """Initialize vector database."""
        # Implementation depends on chosen vector DB (FAISS, Chroma, etc.)
        ...
```

### 4. Protocol Structure

Protocol structure defines the format and organization of memory storage:

- **Memory Types**: Working memory, short-term memory, long-term memory
- **Storage Formats**: How information is encoded and structured
- **Retrieval Patterns**: Standard methods for accessing stored information
- **Update Mechanisms**: How memory is refreshed and maintained

Example implementation:
```python
class ACPMemoryManager:
    """Manages different memory types according to ACP structure."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.working_memory = {}  # In-memory, ephemeral
        self.short_term = RedisMemoryAdapter(f"{agent_id}:short")  # TTL: 1 day
        self.long_term = VectorMemory(  # Persistent
            embedding_model="all-MiniLM-L6",
            vector_db_path=f"/data/memory/{agent_id}"
        )
        self.summaries = FileMemoryAdapter(f"/data/summaries/{agent_id}")

    def store_working(self, key: str, value: Any) -> None:
        """Store in working memory (current session only)."""
        self.working_memory[key] = value

    def store_short_term(self, key: str, value: Any) -> None:
        """Store in short-term memory (persists for limited time)."""
        self.short_term.store(key, value)

    def store_long_term(self, text: str, metadata: Dict[str, Any]) -> str:
        """Store in long-term memory with vector embedding."""
        return self.long_term.store(text, metadata)

    def store_summary(self, key: str, summary: str) -> None:
        """Store a summary for long-term context."""
        self.summaries.store(key, {
            "summary": summary,
            "created_at": datetime.now().isoformat(),
            "version": self._get_next_version(key)
        })

    def get_context(self, query: str = None, max_tokens: int = 2048) -> Dict[str, Any]:
        """Get comprehensive context for agent inference."""
        context = {
            "working_memory": self.working_memory,
            "recent_short_term": self._get_recent_short_term(),
        }

        if query:
            # Add relevant long-term memories based on query
            context["relevant_memories"] = self.long_term.search(query, limit=3)

        # Add latest summaries
        context["summaries"] = self._get_latest_summaries(3)

        # Prune to fit token budget
        return prune_context(self.agent_id, context, max_tokens)

    def _get_recent_short_term(self) -> Dict[str, Any]:
        """Get recent items from short-term memory."""
        # Implementation details...
        return {}

    def _get_latest_summaries(self, count: int) -> List[Dict[str, Any]]:
        """Get the latest summaries."""
        # Implementation details...
        return []

    def _get_next_version(self, key: str) -> int:
        """Get next version number for a summary."""
        existing = self.summaries.retrieve(key)
        if not existing:
            return 1
        return existing.get("version", 0) + 1
```

## Agent-Specific ACP Examples

Different agents use specialized ACP configurations based on their roles and needs:

### Strategist Agent ACP

```python
class StrategistACP:
    def __init__(self, agent_id: str):
        self.memory_manager = ACPMemoryManager(agent_id)
        self.goal_tracker = GoalTracker(agent_id)

    def prepare_context(self, query: str, project_id: str = None) -> Dict[str, Any]:
        """Prepare context for Strategist agent inference."""
        # Get basic context
        context = self.memory_manager.get_context(query)

        # Add strategic elements
        context["active_goals"] = self.goal_tracker.get_active_goals(project_id)
        context["goal_progress"] = self.goal_tracker.get_progress_summary(project_id)

        # Add long-term strategy summary
        if project_id:
            context["strategy_summary"] = self.memory_manager.summaries.retrieve(
                f"strategy_{project_id}")

        return context

    def update_strategy_summary(self, project_id: str, new_insights: str) -> None:
        """Update the strategy summary with new insights."""
        # Get current summary
        current = self.memory_manager.summaries.retrieve(f"strategy_{project_id}")
        current_summary = current.get("summary", "") if current else ""

        # Generate updated summary
        prompt = f"""
        Current strategy summary:
        {current_summary}

        New strategic insights:
        {new_insights}

        Create an updated comprehensive strategy summary that incorporates both
        the existing summary and the new insights. Resolve any contradictions and
        ensure the summary remains concise but complete.
        """

        updated_summary = llm_client.generate(prompt, max_tokens=500)

        # Store updated summary
        self.memory_manager.store_summary(f"strategy_{project_id}", updated_summary)
```

### Builder Agent ACP

```python
class BuilderACP:
    def __init__(self, agent_id: str):
        self.memory_manager = ACPMemoryManager(agent_id)
        self.code_memory = CodeMemory(agent_id)

    def prepare_context(self, query: str, code_files: List[str] = None) -> Dict[str, Any]:
        """Prepare context for Builder agent inference."""
        # Get basic context
        context = self.memory_manager.get_context(query)

        # Add code-specific elements
        if code_files:
            context["code_snippets"] = self.code_memory.get_snippets(code_files)
            context["code_structure"] = self.code_memory.get_structure(code_files)

        # Add relevant code patterns
        context["relevant_patterns"] = self.code_memory.find_patterns(query)

        # Add build history
        context["recent_builds"] = self.memory_manager.short_term.retrieve("recent_builds")

        return context

    def store_code_knowledge(self, code: str, description: str, tags: List[str]) -> None:
        """Store code knowledge for future reference."""
        # Store in vector memory for semantic search
        self.memory_manager.store_long_term(
            text=code,
            metadata={
                "type": "code",
                "description": description,
                "tags": tags
            }
        )

        # Extract patterns
        patterns = self.code_memory.extract_patterns(code)

        # Store patterns
        for pattern in patterns:
            self.code_memory.store_pattern(
                pattern=pattern,
                description=f"Pattern from: {description}",
                tags=tags
            )
```

### Archivist Agent ACP

```python
class ArchivistACP:
    def __init__(self, agent_id: str):
        self.memory_manager = ACPMemoryManager(agent_id)
        self.knowledge_graph = KnowledgeGraph(agent_id)

    def prepare_context(self, query: str) -> Dict[str, Any]:
        """Prepare context for Archivist agent inference."""
        # Get basic context
        context = self.memory_manager.get_context(query)

        # Add knowledge graph elements
        context["related_nodes"] = self.knowledge_graph.find_related(query)
        context["graph_summary"] = self.knowledge_graph.summarize_subgraph(query)

        # Add tagging history
        context["recent_tags"] = self.memory_manager.short_term.retrieve("recent_tags")

        # Add categorization scheme
        context["taxonomy"] = self.memory_manager.long_term.taxonomy.get_all()

        return context

    def index_artifact(self, artifact_id: str, content: str, metadata: Dict[str, Any]) -> None:
        """Index an artifact in the Archivist's memory systems."""
        # Store in vector memory
        memory_id = self.memory_manager.store_long_term(
            text=content,
            metadata={
                "artifact_id": artifact_id,
                **metadata
            }
        )

        # Add to knowledge graph
        self.knowledge_graph.add_node(
            node_id=artifact_id,
            node_type="artifact",
            properties=metadata
        )

        # Connect to related nodes
        related = self.knowledge_graph.find_related_nodes(content)
        for related_node in related:
            self.knowledge_graph.add_edge(
                from_id=artifact_id,
                to_id=related_node["id"],
                edge_type="related",
                properties={"confidence": related_node["score"]}
            )
```

## ACP Implementation Guidelines

### Memory Tiers

Organize memory in tiers based on persistence and accessibility:

1. **Working Memory**
   - Ephemeral, session-specific
   - Highest access speed
   - Cleared after task completion
   - Example: In-memory dictionary or Redis with short TTL

2. **Short-Term Memory**
   - Persists across sessions for limited time
   - Medium access speed
   - Automatically expires
   - Example: Redis with TTL or daily log files

3. **Long-Term Memory**
   - Permanent storage
   - Searchable via vector embeddings
   - Organized and indexed
   - Example: Vector database (FAISS, Chroma) with metadata

### Token Optimization

Manage token usage efficiently:

1. **Token Budgeting**
   - Allocate token budgets to different memory categories
   - Adjust budgets based on task requirements
   - Reserve tokens for response generation

2. **Compression Techniques**
   - Summarize lengthy context
   - Remove redundant information
   - Use shorthand notations for common patterns

3. **Progressive Loading**
   - Load essential context first
   - Add additional context only if needed
   - Use follow-up queries for clarification

### Memory Refresh

Maintain relevant and accurate memory:

1. **Memory Decay**
   - Gradually reduce importance of older memories
   - Focus on recent and relevant information
   - Archive less frequently accessed memories

2. **Consistency Checking**
   - Detect and resolve contradictions
   - Update outdated information
   - Maintain canonical knowledge

3. **Scheduled Consolidation**
   - Periodically summarize accumulated knowledge
   - Merge related memories
   - Prune redundant information

## ACP Configuration Templates

### Basic ACP Configuration

```yaml
ACP:
  agent_id: "example_agent"
  token_budget: 2048

  memory:
    working:
      type: "memory"
      max_items: 100

    short_term:
      type: "redis"
      ttl: 86400  # 24 hours
      priority_keys:
        - "recent_tasks"
        - "active_context"

    long_term:
      type: "vector"
      embedding_model: "all-MiniLM-L6"
      db_type: "faiss"
      path: "/data/memory/example_agent"

  summarization:
    type: "sliding_window"
    window_size: 5
    overlap: 2
    summary_model: "phi-2"

  embedding:
    model: "all-MiniLM-L6"
    dimension: 384
    batch_size: 32

  pruning:
    strategy: "priority_based"
    priorities:
      system_context: 10
      task_description: 9
      working_memory: 8
      recent_short_term: 7
      relevant_memories: 6
      summaries: 5
```

### Strategist ACP Configuration

```yaml
ACP:
  agent_id: "strategist"
  token_budget: 4096

  memory:
    working:
      type: "memory"
      max_items: 50

    short_term:
      type: "redis"
      ttl: 172800  # 48 hours
      priority_keys:
        - "active_goals"
        - "recent_decisions"

    long_term:
      type: "vector"
      embedding_model: "all-MiniLM-L6"
      db_type: "faiss"
      path: "/data/memory/strategist"

  summarization:
    type: "hierarchical"
    levels: 3
    summary_model: "mistral-7b"

  embedding:
    model: "all-MiniLM-L6"
    dimension: 384
    batch_size: 8

  pruning:
    strategy: "priority_based"
    priorities:
      system_context: 10
      active_goals: 9
      task_description: 9
      goal_progress: 8
      strategy_summary: 8
      working_memory: 7
      recent_short_term: 6
      relevant_memories: 5
```

### Builder ACP Configuration

```yaml
ACP:
  agent_id: "builder"
  token_budget: 4096

  memory:
    working:
      type: "memory"
      max_items: 100

    short_term:
      type: "redis"
      ttl: 86400  # 24 hours
      priority_keys:
        - "current_task"
        - "code_context"

    long_term:
      type: "vector"
      embedding_model: "all-MiniLM-L6"
      db_type: "faiss"
      path: "/data/memory/builder"

  summarization:
    type: "selective"
    preserve_patterns: true
    summary_model: "codellama-7b"

  embedding:
    model: "code-embedding-model"
    dimension: 768
    batch_size: 16

  pruning:
    strategy: "priority_based"
    priorities:
      system_context: 10
      code_snippets: 10
      task_description: 9
      code_structure: 8
      relevant_patterns: 8
      recent_builds: 7
      working_memory: 6
      recent_short_term: 5
```

## Best Practices

### Memory Management

1. **Separate Fact from Inference**
   - Clearly distinguish stored facts from inferences
   - Tag inferences with confidence levels
   - Update inferences when new facts are available

2. **Metadata Enrichment**
   - Add rich metadata to all stored information
   - Include timestamps, sources, and context
   - Tag with relevant categories and topics

3. **Progressive Summarization**
   - Summarize at multiple levels of detail
   - Preserve original sources for reference
   - Update summaries as new information arrives

### Context Preparation

1. **Task-Oriented Context**
   - Focus context on the current task
   - Include only relevant information
   - Arrange context from general to specific

2. **Dynamic Context Adjustment**
   - Adapt context based on task complexity
   - Expand context when clarification is needed
   - Contract context for straightforward tasks

3. **Context Monitoring**
   - Track context window utilization
   - Measure context effectiveness
   - Adjust strategies based on performance

### Implementation Approaches

1. **Start Simple**
   - Begin with basic memory tiers
   - Add complexity as needed
   - Measure performance impact of changes

2. **Agent-Specific Optimization**
   - Tailor ACP to each agent's role
   - Allocate more context to complex reasoning tasks
   - Use lighter context for routine tasks

3. **Continuous Improvement**
   - Monitor agent performance
   - Identify memory-related bottlenecks
   - Refine ACP based on real-world usage

## Conclusion

The Agent Context Protocol (ACP) is a critical component of the Edge AI Agent System, enabling effective management of context, memory, and state across agent operations despite the constraints of edge hardware. By implementing a well-designed ACP, agents can maintain continuity of understanding, utilize their limited context windows efficiently, and deliver more coherent and intelligent responses.

The structured approach to input pruning, summarization, embedding usage, and protocol structure allows for a flexible yet consistent memory management system that adapts to the needs of different agent types while optimizing resource usage. As the Edge AI Agent System evolves, the ACP should continue to be refined to incorporate new techniques and address emerging challenges in context management for edge AI applications.
