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
