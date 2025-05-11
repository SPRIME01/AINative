# PowerShell script to build Sphinx documentation for Edge-AI Orchestrator Backend
# Usage: ./build-docs.ps1

sphinx-build -b html docs/backend/source docs/backend/build/html
Write-Host "Sphinx documentation build complete. Output: docs/backend/build/html/index.html"
