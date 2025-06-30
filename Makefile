# -- Variables -----------------------------------------------------------------

PACKAGE = icostate

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
