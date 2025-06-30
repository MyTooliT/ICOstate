"""Sphinx configuration"""

# pylint: disable=invalid-name

# -- Imports ------------------------------------------------------------------

from datetime import datetime
from importlib.metadata import version

from sphinx_pyproject import SphinxConfig

# -- Project information ------------------------------------------------------

config = SphinxConfig("../../pyproject.toml", globalns=globals())
# pylint: disable=redefined-builtin
copyright = f"{datetime.now().year}, {author}"
project = name

# -- General configuration ----------------------------------------------------

extensions = [
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
