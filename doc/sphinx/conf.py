"""Sphinx configuration"""

# pylint: disable=invalid-name

# -- Imports ------------------------------------------------------------------

from pathlib import Path
from datetime import datetime

from sphinx_pyproject import SphinxConfig

# -- Project information ------------------------------------------------------

config = SphinxConfig(
    Path(__file__).parent.parent.parent / "pyproject.toml", globalns=globals()
)
# pylint: disable=redefined-builtin,undefined-variable
copyright = f"{datetime.now().year}, {author}"  # type: ignore[name-defined]
# pylint: enable=redefined-builtin
project = name  # type: ignore[name-defined]
# pylint: enable=undefined-variable

# -- General configuration ----------------------------------------------------

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
    "sphinx_toggleprompt",
]

# Run doctest from doctest directive, but not nested tests from autodoc code
doctest_test_doctest_blocks = ""

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc Configuration ----------------------------------------------------

autoclass_content = "both"
autodoc_inherit_docstrings = False

# -- HTML Theme ---------------------------------------------------------------

html_theme = "furo"

# pylint: enable=invalid-name
