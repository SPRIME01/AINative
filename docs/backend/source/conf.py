"""
Sphinx configuration for Edge-AI Orchestrator Backend documentation.

This file is PEP 8 compliant and ready for Google-style docstrings.
# Example:
# To document a module, add the following to your .rst file:
#
# .. automodule:: ainative.app.infrastructure.main
#     :members:
#     :undoc-members:
#     :show-inheritance:
"""

import os
import sys

# -- Path setup --------------------------------------------------------------
# Add backend/src to sys.path for autodoc to find modules
sys.path.insert(
    0, os.path.abspath(r"C:/Users/sprim/FocusAreas/Projects/Dev/AINative/backend/src")
)

# -- Project information -----------------------------------------------------
project = "Edge-AI Orchestrator Backend"
copyright = "2025, Samuel Prime"
author = "Samuel Prime"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# Napoleon settings for Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Intersphinx mapping for Python 3.10 and FastAPI
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10", None),
    "fastapi": ("https://fastapi.tiangolo.com/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

# -- Logging hook (stub for future extension) --------------------------------
# TODO: Integrate logging for Sphinx build events if needed.

# -- Prometheus metrics endpoint stub ----------------------------------------
# TODO: Expose Sphinx build metrics for Prometheus if required.
