# Comprehensive Documentation Setup Prompts

This document outlines a series of prompts to guide the setup of a comprehensive, automated documentation system for the Edge-AI orchestrator project.

**Getting Started Prompt:**

"Let's begin setting up the comprehensive documentation system for my project. We'll start with the backend Python/FastAPI documentation using Sphinx. Please remember to adhere to my custom instructions regarding code style, TDD, Python version, `uv` for dependencies, etc."

---

## Phase 1: Backend Documentation Setup (Sphinx)

### Prompt 1.1: Install Sphinx & Dependencies

"Please provide the `uv add --group dev <package>` commands (for PowerShell) to install Sphinx, the `sphinx-rtd-theme`, and `sphinx-napoleon` in my `backend/` directory. Ensure these are added to the correct group in `pyproject.toml` as per my instructions (e.g., a `docs` or `dev` group)."

**PowerShell Commands to Install Sphinx and Extensions in `backend/` Directory:**

```powershell
cd backend
uv add --group dev sphinx
uv add --group dev sphinx-rtd-theme
uv add --group dev sphinx-napoleon
```

> **Note:**
> - `sphinx-autodoc` is **not** a standalone package. The `autodoc` extension is included with the main `sphinx` package as `sphinx.ext.autodoc`.
> - You only need to install `sphinx`, `sphinx-rtd-theme`, and `sphinx-napoleon` for Google-style docstrings.
> - If you see errors building `numpy` (or other scientific packages) on Windows, install [Microsoft Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and select the "Desktop development with C++" workload.
>   Alternatively, use a Python distribution like Anaconda/Miniconda for pre-built binaries.

These commands will add the documentation dependencies to the `[project.optional-dependencies.dev]` group in your `pyproject.toml` as per your instructions.

### Prompt 1.2: Initialize Sphinx & Configure `conf.py`

"Guide me on initializing Sphinx in a new `docs/backend/` directory (e.g., using `sphinx-quickstart` or by creating the necessary files/folders). Then, provide a complete `conf.py` example for `docs/backend/source/conf.py`. This configuration should:

* Use the `sphinx-rtd-theme`.
* Enable the extensions: `sphinx.ext.autodoc`, `sphinx.ext.napoleon` (configured for Google style docstrings), `sphinx.ext.viewcode`, and `sphinx.ext.intersphinx`.
* Correctly set up `sys.path` to find my Python modules in `c:\Users\sprim\FocusAreas\Projects\Dev\AINative\backend\src\`.
* Configure `intersphinx_mapping` for Python 3.10 and FastAPI."

### Prompt 1.3: Create Sphinx `index.rst` & Module `.rst` Stubs

"Please provide a template for the root `docs/backend/source/index.rst` file. This should include a basic project title, table of contents (`toctree`), and sections for 'API Reference' and 'Modules'. Also, show me how to create stub `.rst` files for a couple of my existing backend modules (e.g., one for `ainative.app.infrastructure.main` and one for an agent like `ainative.agents.strategist.agent_logic`). These stubs should be ready for `automodule` directives."

### Prompt 1.4: Example Python Docstrings & `.rst` Integration

"Let's take the `ainative.app.infrastructure.main.py` file as an example. Please show me how to refactor its existing functions (like `read_root` or `health_check`) to include comprehensive Google-style docstrings with type hints, arguments, return values, and a practical example, adhering to my custom instructions. Then, show the corresponding `automodule` or `autofunction` directives to include these in an `.rst` file (e.g., `docs/backend/source/app.rst`)."

### Prompt 1.5: Add Sphinx Build Script to `pyproject.toml`

"Please add a script to my `backend/pyproject.toml` under `[project.scripts]` (or `[tool.hatch.scripts]` if more appropriate for `hatchling`) to build the Sphinx documentation. The script should be named something like `build-docs` and execute `sphinx-build -b html docs/backend/source docs/backend/build/html`. The output directory `docs/backend/build/html` might need to be created."

### Prompt 1.6: Test Sphinx Build Locally

"Now that the build script is in `pyproject.toml`, how do I run it using `uv` (or `hatch run`)? After running it, what should I check in the `docs/backend/build/html` directory to verify the documentation built correctly? For example, how do I open it in a browser and what key things should I look for?"

---

## Phase 2: Backend Documentation Automation

### Prompt 2.1: Add Sphinx Pre-commit Hook

"Please add a pre-commit hook to my root `pre-commit-config.yaml`. This hook should build the Sphinx documentation (e.g., using `sphinx-build -W --keep-going docs/backend/source docs/backend/build/html`) to catch documentation errors before commits. Ensure it uses an appropriate Python environment that has Sphinx and my project dependencies installed."

### Prompt 2.2: Test Pre-commit Hook

"How can I test this new Sphinx pre-commit hook locally? For example, should I try to commit a file after making a change that would break the docs build (like a malformed `.rst` file or a Python syntax error in a docstring example)?"

### Prompt 2.3: Add Sphinx Build & Deploy to GitHub Actions

"Please update my existing `.github/workflows/ci.yaml` (or suggest a new `docs.yaml` workflow if cleaner). Add a new job that:

* Checks out the code.
* Sets up Python 3.10 and `uv`.
* Installs backend dependencies (including docs dependencies).
* Builds the Sphinx documentation (using the script we added to `pyproject.toml` or directly with `sphinx-build`).
* Deploys the built HTML documentation from `docs/backend/build/html` to GitHub Pages. You can use a popular action like `peaceiris/actions-gh-pages` for this. Configure it to deploy to a `gh-pages` branch or a `/docs` folder on the `main` branch, whichever is best practice."

### Prompt 2.4: Test GitHub Actions Workflow for Docs

"How can I test this updated GitHub Actions workflow? Should I push my changes to a new branch and create a pull request, or push directly to `main` (if that's where the trigger is)? What should I look for in the GitHub Actions logs and on the GitHub Pages site to confirm it's working?"

---

## Phase 3: Frontend UI Documentation (Storybook)

### Prompt 3.1: Install Storybook & Dependencies

"Let's set up Storybook for my frontend React components. Please provide the `pnpm add -D <package>` commands to install Storybook, `@storybook/react-vite`, `@storybook/react`, `@storybook/addon-essentials`, `@storybook/addon-interactions`, `@storybook/addon-links`, `@storybook/addon-a11y` (for accessibility), and any other common/useful addons. This is for the `frontend/` directory."

### Prompt 3.2: Initialize & Configure Storybook

"Guide me on initializing Storybook in my `frontend/` directory (e.g., using `pnpx storybook@latest init` if appropriate, or by manually creating config files). Provide example configurations for `frontend/.storybook/main.ts` (ensuring Vite compatibility and addon registration) and `frontend/.storybook/preview.ts` (e.g., for global decorators or theme context if I use Chakra UI, which is in my dependencies)."

### Prompt 3.3: Create Example Component Story

"I need an example Storybook story. Please create a simple, presentational React component (e.g., a `Button` or `Card`) in `frontend/src/components/ExampleComponent/ExampleComponent.tsx` if one doesn't already exist that's suitable. Then, create its corresponding story file `frontend/src/components/ExampleComponent/ExampleComponent.stories.tsx`. The story should demonstrate:

* TSDoc for component props.
* How to define multiple stories for different states of the component.
* Usage of Storybook Controls (args) and Actions (for event handlers)."

### Prompt 3.4: Add Storybook Scripts to `package.json`

"Please add the following `pnpm` scripts to my `frontend/package.json`:

* `storybook:dev`: To run Storybook locally in development mode.
* `storybook:build`: To build the static Storybook site for deployment."

### Prompt 3.5: Test Storybook Locally

"How do I run Storybook locally using the new script? Once it's running, what URL should I open, and what should I check to ensure the example component and its stories are working correctly?"

---

## Phase 4: Frontend Code Documentation (TypeDoc)

### Prompt 4.1: Install TypeDoc

"Now for documenting my frontend TypeScript code. Please provide the `pnpm add -D <package>` command to install TypeDoc in my `frontend/` directory."

### Prompt 4.2: Configure TypeDoc

"Please help me configure TypeDoc. Create a `frontend/typedoc.json` file. This configuration should:

* Specify entry points (e.g., `src/main.tsx`, `src/services/`, `src/hooks/`, `src/components/`, `src/types/`).
* Define the output directory as `docs/frontend/typedoc`.
* Suggest a clean theme or any useful TypeDoc plugins if available."

### Prompt 4.3: Example TSDoc Comments

"Please pick a TypeScript file from my frontend, for example, a service function in `frontend/src/services/` or a custom hook in `frontend/src/hooks/`. Add comprehensive TSDoc comments to its functions, interfaces, and types, demonstrating best practices for TypeDoc generation (e.g., using `@param`, `@returns`, `@remarks`, `@example`)."

### Prompt 4.4: Add TypeDoc Script to `package.json`

"Add a `pnpm` script named `docs:typedoc` to my `frontend/package.json` that runs TypeDoc using the `typedoc.json` configuration to generate the documentation."

### Prompt 4.5: Test TypeDoc Generation Locally

"How do I run the TypeDoc generation script? After it completes, where will the documentation be located, and how can I view it to ensure it's been generated correctly from the TSDoc comments?"

---

## Phase 5: Frontend Documentation Automation

### Prompt 5.1: Add Frontend Docs Build & Deploy to GitHub Actions

"Let's automate the frontend documentation. Please update my GitHub Actions workflow (`.github/workflows/ci.yaml` or the `docs.yaml` we might have created) to include steps for the frontend:

* Set up Node.js and `pnpm`.
* Install frontend dependencies.
* Build the Storybook static output (using `pnpm storybook:build`).
* Build the TypeDoc documentation (using `pnpm docs:typedoc`).
* Deploy both sets of documentation to GitHub Pages. They should ideally be in subdirectories, e.g., `[gh-pages-url]/storybook/` and `[gh-pages-url]/typedoc/`. The backend Sphinx docs should still be at the root or its own subdirectory like `[gh-pages-url]/backend/`."

### Prompt 5.2: Test Frontend Docs GitHub Actions Workflow

"Similar to the backend docs, how can I test this updated GitHub Actions workflow for the frontend documentation? What should I check in the logs and on the GitHub Pages site (specifically the subdirectories for Storybook and TypeDoc)?"

---

## Phase 6: Final Review & Reminders

### Prompt 6.1: Review FastAPI Docstrings for OpenAPI

"As a reminder, could you briefly reiterate the best practices for writing FastAPI path operation function docstrings (summary, description, parameters, responses using Python type hints and Pydantic models) to ensure my `/openapi.json` schema is rich and detailed? This is important for the auto-generated Swagger/ReDoc UIs and the frontend API client we set up earlier."

### Prompt 6.2: Overall Documentation System Review

"We've now set up Sphinx, Storybook, and TypeDoc, along with automation. Could you provide a quick review of the overall documentation system we've implemented? Are there any final checks, common pitfalls to watch out for, or best practices I should keep in mind for maintaining and extending this documentation as my project grows?"
