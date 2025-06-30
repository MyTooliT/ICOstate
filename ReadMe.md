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

**Note:** In the text below we assume that you want to release version `0.2` of the package. Please just replace this version number with the version that you want to release.

1. Make sure that all the checks and tests work correctly

   ```sh
   make
   ```

2. Release a new version on [PyPI](https://pypi.org/project/icostate/):
   1. Increase version number
   2. Add git tag containing version number
   3. Push changes

   ```sh
   poetry version 0.2
   export icostate_version="$(poetry version -s)"
   git commit -a -m "Release: Release version $icostate_version"
   git tag "$icostate_version"
   git push && git push --tags
   ```

3. Open the [release notes](doc/release) for the latest version and [create a new release](https://github.com/MyTooliT/ICOstate/releases/new)
   1. Copy the release notes
   2. Paste them into the main text of the release web page
   3. Insert the version number (e.g. `0.2`) into the tag field
   4. For the release title use “Version VERSION”, where `VERSION` specifies the version number (e.g. “Version 0.2”)
   5. Click on “Publish Release”
