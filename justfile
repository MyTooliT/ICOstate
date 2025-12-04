# -- Settings ------------------------------------------------------------------

# Use latest version of PowerShell on Windows
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

# -- Variables -----------------------------------------------------------------

package := "icostate"
sphinx_directory := "sphinx"
sphinx_input_directory := "doc/sphinx"

test_directory := "test"
sphinx_tests := sphinx_input_directory / "usage.rst"
# Note: The pytest plugin `pytest-sphinx` (version 0.6.3) does unfortunately not
# find our API documentation doctests, hence we specify the test files (*.rst)
# manually.
test_locations := package + " " + test_directory

# -- Recipes -------------------------------------------------------------------

# Setup Python environment
[group('setup')]
setup:
	uv venv --allow-existing
	uv sync --all-extras

# Check code with various linters
[group('lint')]
check: setup
	uv run mypy "{{package}}"
	uv run flake8
	uv run pylint .

# Helper for running tests
[group('test')]
_test *options: check && coverage
	uv run coverage run -m pytest \
		--reruns 5 \
		--reruns-delay 1 \
		--doctest-modules \
		{{options}} {{test_directory}} {{package}}

# Run tests
[default]
[group('test')]
test: (_test sphinx_tests)

# Run hardware-independent tests
[group('test')]
test-no-hardware: (_test
	'--ignore' + " " + package / "system.py"
	'--ignore' + " " + test_directory / "test_system.py")

# Print coverage report
[private]
coverage:
	uv run coverage report

# Release new package version
[group('release')]
[unix]
release version:
	#!/usr/bin/env sh -e
	uv version {{version}}
	version="$(uv version --short)"
	git commit -a -m "Release: Release version ${version}"
	git tag "${version}"
	git push
	git push --tags

# Release new package version
[group('release')]
[windows]
release version:
	#!pwsh
	uv version {{version}}
	set version "$(uv version --short)"
	git commit -a -m "Release: Release version ${version}"
	git tag "${version}"
	git push
	git push --tags

# Generate documentation
[group('documentation')]
documentation:
	uv run sphinx-apidoc -f -o {{sphinx_directory}} {{sphinx_input_directory}}
	uv run sphinx-build -M html {{sphinx_input_directory}} {{sphinx_directory}}
