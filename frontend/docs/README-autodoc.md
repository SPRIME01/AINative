# Frontend Autodocumentation Setup

This project supports automated documentation for React components and TypeScript code using Storybook and TypeDoc.

## Storybook

- **Run Storybook locally:**
  ```powershell
  pnpm storybook:dev
  ```
- **Build static Storybook site:**
  ```powershell
  pnpm storybook:build
  ```
- Storybook config is in `.storybook/main.ts` and `.storybook/preview.ts`.

## TypeDoc

- **Generate TypeScript API docs:**
  ```powershell
  pnpm docs:typedoc
  ```
- TypeDoc config is in `typedoc.json`.
- Output is generated in `docs/frontend/typedoc/`.

## What to Check
- Storybook: Open the local URL (usually http://localhost:6006) and verify your components and stories render and are documented.
- TypeDoc: Open the generated HTML in `docs/frontend/typedoc/index.html` and check for API docs, TSDoc comments, and navigation.

---

For best results, ensure your components and functions have comprehensive TSDoc comments and your stories demonstrate all component states.
