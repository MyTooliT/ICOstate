# Requirements

- [Python 3](https://www.python.org)

While not strictly a necessity, we assume that you installed the following developer dependencies:

- [Make](<https://en.wikipedia.org/wiki/Make_(software)>)
- [Poetry](https://python-poetry.org)

in the text below.

# Install

```sh
pip install icostate
```

# Development

## Install

For development we recommend you clone the repository and install the package with poetry:

```sh
poetry lock && poetry install --all-extras
```

## Check

```sh
make check
```

## Release

To release a new version of this package on [PyPI](https://pypi.org/project/icostate/):

1. Increase the version number e.g. for version `0.2`:

   ```sh
   poetry version 0.2
   ```

   and commit your changes:

   ```sh
   export icostate_version="$(poetry version -s)"
   git commit -a -m "Release: Release version $icostate_version"
   ```

2. Add a tag with the version number to the latest commit:

   ```sh
   export icostate_version="$(poetry version -s)"
   git tag "$icostate_version"
   ```

3. Push the latest updates including the new tag:

   ```sh
   git push && git push --tags
   ```
