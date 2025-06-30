# -- Variables -----------------------------------------------------------------

PACKAGE = icostate
SPHINX_DIRECTORY := sphinx
SPHINX_INPUT_DIRECTORY := doc/sphinx

# -- Rules ---------------------------------------------------------------------

.PHONY: all
all: check test

.PHONY: check
check:
	poetry run flake8
	poetry run mypy .
	poetry run pylint .

.PHONY: test
test:
	poetry run pytest .

.PHONY: test-no-hardware
test-no-hardware:
	poetry run pytest --ignore '$(PACKAGE)/system.py'

.PHONY: documentation
documentation:
	poetry run sphinx-apidoc -f -o $(SPHINX_DIRECTORY) $(SPHINX_INPUT_DIRECTORY)
	poetry run sphinx-build -M html $(SPHINX_INPUT_DIRECTORY) \
	    $(SPHINX_DIRECTORY)
