# -- Variables -----------------------------------------------------------------

MODULE = icostate
SPHINX_DIRECTORY := sphinx
SPHINX_INPUT_DIRECTORY := doc/sphinx

TEST_DIRECTORY := test
# Note: The pytest plugin `pytest-sphinx` (version 0.6.3) does unfortunately not
# find our API documentation doctests, hence we specify the test files (*.rst)
# manually.
TEST_LOCATIONS := $(SPHINX_INPUT_DIRECTORY)/usage.rst \
				  $(MODULE) \
	 			  $(TEST_DIRECTORY)

# -- Rules ---------------------------------------------------------------------

.PHONY: all
all: check test coverage

.PHONY: setup
setup:
	uv venv --allow-existing
	uv sync --all-extras

.PHONY: check
check:
	uv run flake8
	uv run mypy .
	uv run pylint .

.PHONY: test
test:
	uv run coverage run -m pytest $(TEST_LOCATIONS) || \
	  ( uv run icon stu reset && \
	    uv run coverage run --append -m pytest --last-failed )

.PHONY: test-no-hardware
test-no-hardware:
	uv run coverage run -m pytest \
	    --ignore '$(MODULE)/system.py' \
	    --ignore '$(TEST_DIRECTORY)/test_system.py'

.PHONY: coverage
coverage:
	uv run coverage report

.PHONY: documentation
documentation:
	uv run sphinx-apidoc -f -o $(SPHINX_DIRECTORY) $(SPHINX_INPUT_DIRECTORY)
	uv run sphinx-build -M html $(SPHINX_INPUT_DIRECTORY) \
	    $(SPHINX_DIRECTORY)
