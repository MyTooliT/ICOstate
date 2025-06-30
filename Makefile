# -- Variables -----------------------------------------------------------------

PACKAGE = icostate
SPHINX_DIRECTORY := sphinx
SPHINX_INPUT_DIRECTORY := doc/sphinx

# -- Rules ---------------------------------------------------------------------

.PHONY: all
all: check test

.PHONY: check
check:
	flake8
	mypy .
	pylint .

.PHONY: test
test:
	pytest .

.PHONY: test-no-hardware
test-no-hardware:
	pytest --ignore '$(PACKAGE)/system.py'

.PHONY: documentation
documentation:
	poetry run sphinx-apidoc -f -o $(SPHINX_DIRECTORY) $(SPHINX_INPUT_DIRECTORY)
	poetry run sphinx-build -M html $(SPHINX_INPUT_DIRECTORY) $(SPHINX_DIRECTORY)
