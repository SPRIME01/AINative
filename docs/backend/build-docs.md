# Building Sphinx Documentation for Edge-AI Orchestrator Backend

To build the backend documentation locally, use the provided PowerShell script:

## Steps

1. Open a PowerShell terminal in the `backend/` directory.
2. Run the following command:

   ```powershell
   ./build-docs.ps1
   ```

This will execute:

```
sphinx-build -b html docs/backend/source docs/backend/build/html
```

and generate the HTML documentation in `docs/backend/build/html`.

## Verifying the Output

- After the build completes, open `docs/backend/build/html/index.html` in your browser.
- Check for:
  - Project title and navigation sidebar
  - API Reference and Modules sections
  - Rendered docstrings for your endpoints and modules
  - No Sphinx build errors in the terminal

## Troubleshooting
- If you see missing modules/functions, check your `conf.py` `sys.path` and `.rst` directives.
- If you get command not found errors, ensure Sphinx is installed in your environment.

---

*This script replaces the need for a Python entry point or Hatch script for documentation builds.*
