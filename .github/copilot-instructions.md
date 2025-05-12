# GitHub Copilot Custom Instructions

## About Your Code

- **Project Context:** Edge-AI orchestrator
- **Target Platform:** NVIDIA Jetson AGX Orin
- **Core Technologies:** LiteLLM (Triton/TensorRT, Ollama), FastAPI, Redis, Google Agent Development Kit (ADK)
- **Architectural Pattern:** Hexagonal Architecture (Ports and Adapters)

## Core Principles

- **Readability:** Write clear, concise, and understandable code
- **DRY (Don't Repeat Yourself):** Extract common logic into reusable components
- **KISS (Keep It Simple, Stupid):** Prioritize simplicity in design and implementation
- **YAGNI (You Ain't Gonna Need It):** Avoid unnecessary functionality
- **Composition Over Inheritance:** Build complex objects from smaller components
- **SOLID Principles:**
  - Single Responsibility (SRP): Each class has one purpose
  - Open/Closed (OCP): Open for extension, closed for modification
  - Liskov Substitution (LSP): Subtypes must be substitutable for base types
  - Interface Segregation (ISP): Clients shouldn't depend on unused interfaces
  - Dependency Inversion (DIP): Depend on abstractions, not implementations

## How You Should Help

### Development Methodology
- Prioritize Test-Driven Development (TDD)
- Always suggest a `pytest` or `vitest` test case *before* providing implementation code

### Code Style & Quality
- Generate Python 3.10+ compatible code
- Enforce PEP 8 compliance
- Include comprehensive type hints and clear docstrings
- **Naming:** Use descriptive names for all code elements
- **Formatting:** Follow language-specific style guidelines
- **Interface-First Design:** Define clear contracts between components
- **Dependency Injection:** Use constructor injection by default
- **Abstractions:** Create interfaces for all major components
- **Encapsulation:**
  - Protect internal state with appropriate access modifiers
  - Use private/protected attributes and methods where applicable
  - Hide implementation details behind interfaces

### Type Annotations & mypy
- Use comprehensive type annotations that pass `mypy --strict` checks
- Leverage `typing` module features appropriate for Python 3.10+ (e.g., `Union` → `|`)
- Include proper return type annotations, including for async functions
- Use `TypeVar` and generics appropriately for polymorphic functions
- Add explicit `# type: ignore` comments with explanations when necessary
- Use typing.protocols for defining interfaces and abstract classes unless `abc` is more appropriate

### Documentation & Examples
- Ensure all docstrings include practical examples
- Add a dedicated `# Example:` section in code comments where appropriate
- **Document interface contracts clearly**
- **Specify dependencies in docstrings**
- **Mandatory docstrings for modules, classes, and functions**
- **Use Google-style docstrings with Args, Returns, Raises sections**
- **Write docstrings that can be extracted by documentation tools (mkdocs, sphinx)**
- **Include examples in docstrings for complex functions**
- **Document Pydantic fields with clear descriptions for auto-generated API docs**
- **Add comments explaining the "why" behind code decisions**
- **Ensure consistency in documentation style**

### Sphinx Documentation
- Write docstrings in reStructuredText format for Sphinx compatibility
- Include the following sections in docstrings:
    - Parameters (`:param name: description`)
    - Return values (`:return: description`)
    - Exceptions (`:raises ExceptionType: description`)
    - Examples (`:Example:`)
- Use type annotations in docstrings (`:type name: type` or `:rtype: type`) when helpful for clarity
- Include cross-references to other classes/methods using `:class:`, `:meth:`, `:func:` directives

### API Documentation
- Add OpenAPI decorators and metadata to all API endpoints
- Include comprehensive summaries and descriptions for endpoints
- Document response models, status codes, and error responses
- Provide example requests and responses where helpful
- Document authentication and authorization requirements
- Use type annotations that generate clear API schemas
- Organize endpoints with logical tags and grouping
- Ensure Pydantic model field descriptions propagate to API docs

### Function & Method Design
- Keep functions small with a single responsibility
- Minimize side effects and aim for pure functions
- Use meaningful, limited parameters
- Maintain consistent return types
- Apply Command-Query Separation (CQS)

### Modularity & Design
- Decompose functionality into small, pure, and easily testable functions
- Adhere to the Ports and Adapters pattern
- Use established patterns (MVC, MVVM, Clean Architecture, Microservices)
- Implement layered architecture for separation of concerns

### Asynchronous Operations
- Prefer `async/await` for FastAPI endpoints and all I/O-bound operations

### Google ADK Scaffolding
- When generating Google ADK project structures, include stubs for:
        - Agent definitions
        - Tool configurations
        - Action handlers

### Observability
- Automatically include Prometheus metrics endpoint (`@app.get('/metrics')`) stubs
- Include logging hooks in new modules

### Adapter Implementation
- Use `NotImplementedError` for adapter stubs
- Include clear `TODO:` comments detailing the pending implementation

### Testing
- Structure: Follow AAA (Arrange, Act, Assert) pattern
- Naming: Use verbose class names that clearly state the test case (e.g. `test_UserAuthentication_WithValidCredentials_ReturnsToken`)
- Types: Write unit, integration, and BDD-style tests
- Practices:
  - Ensure test idempotence
  - Mock external dependencies
  - Use descriptive test names following the pattern: `test_[Feature]_[Scenario]_[ExpectedResult]`
  - Integrate tests in CI/CD pipelines
  - Structure each test with clear AAA sections

### Production Readiness
- Comprehensive exception handling
- Input validation and security checks
- Resource cleanup
- Testing with appropriate frameworks (pytest for Python, Jest for TypeScript)

### Language-Specific Standards

#### Python
- Follow PEP8 with strict typing (mypy compatible)
- Use typing.protocol for interfaces except where abstract base classes are needed
- Use context managers for resource management
- Employ Pydantic for data structures and validation
- Add field descriptions to all Pydantic model fields
- Use validators with descriptive error messages
- Leverage Pydantic's Config for enhanced documentation
- Implement async methods where beneficial
- Follow Domain-Driven Design principles with ports & adapters pattern
- Configure with pyproject.toml

#### FastAPI specific:
- Use path operation decorators with complete metadata
- Document response models and status codes
- Add examples to complex request/response models
- Organize routes with proper tagging and Router objects

#### TypeScript
- Follow ES6+ with strict type annotations
- Implement modular design with appropriate interfaces
- Handle async errors properly
- Test with Jest or Vitest according to project needs
- For CSS, apply Block Element Modifier (BEM) naming

### Development Environment
- Use `uv` for Python dependency management:
  - Create virtual environment: `uv venv .venv`
  - Activate (Windows): `.venv\Scripts\activate`
  - Activate (Unix): `source .venv/bin/activate`
- Use `pytest` for Python testing
- Use `vitest` for JavaScript/TypeScript testing
- Use `pnpm` for JavaScript/TypeScript dependency management
- Use .env for environment variable management

### Inline Commands & Special Code Blocks

#### Commands
- Refactoring:
  - Python: `# copilot: refactor`
  - TypeScript: `// copilot: refactor`
- Optimization:
  - Python: `# copilot: optimize`
  - TypeScript: `// copilot: optimize`

#### Code Blocks
- Performance Optimization:
```python
# BEGIN PERFORMANCE OPTIMIZATION
# END PERFORMANCE OPTIMIZATION
```
```typescript
// BEGIN PERFORMANCE OPTIMIZATION
// END PERFORMANCE OPTIMIZATION
```
- Security Checks:
```python
# BEGIN SECURITY CHECKS
# END SECURITY CHECKS
```
```typescript
// BEGIN SECURITY CHECKS
// END SECURITY CHECKS
```

### Commit Message Format
- 📝 Be extremely detailed with file changes
- 🤔 Explain the reasoning behind each change
- 🎨 Use relevant emojis to categorize changes
- Examples:
  - ✨ feat(auth): Add JWT token validation to login endpoint
  - 🔧 Modified: src/auth/jwt_validator.py
  - 📦 Added: tests/auth/test_jwt_validator.py
  - 🔥 Removed: old token validation logic
  - 🤔 Why: Improves security by implementing industry-standard JWT validation
