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

.PHONY: check
check:
	poetry run flake8
	poetry run mypy .
	poetry run pylint .

.PHONY: test
test:
	poetry run coverage run -m pytest $(TEST_LOCATIONS)

.PHONY: test-no-hardware
test-no-hardware:
	poetry run coverage run -m pytest \
		--ignore '$(MODULE)/system.py' \
		--ignore '$(TEST_DIRECTORY)/test_system.py'

.PHONY: coverage
coverage:
	poetry run coverage report

.PHONY: documentation
documentation:
	poetry run sphinx-apidoc -f -o $(SPHINX_DIRECTORY) $(SPHINX_INPUT_DIRECTORY)
	poetry run sphinx-build -M html $(SPHINX_INPUT_DIRECTORY) \
	    $(SPHINX_DIRECTORY)
