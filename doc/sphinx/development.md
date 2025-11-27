# Development

While not strictly a necessity, we assume that you installed the following developer dependencies:

- [just](https://just.systems/man/en)
- [uv](https://docs.astral.sh/uv/)

in the text below.

## Install

For development we recommend you clone the repository and install the package with uv:

```sh
uv venv --allow-existing
uv sync --all-extras
```

## Check

```sh
just check
```

## Release

**Note:** In the text below we assume that you want to release version `<VERSION>` of the package. Please just replace this version number with the version that you want to release (e.g. `0.2`).

1. Make sure that all the checks and tests work correctly locally

   ```sh
   just
   ```

2. Make sure all [workflows of the CI system work correctly](https://github.com/MyTooliT/ICOstate/actions)

3. Check that the most recent [“Read the Docs” build of the documentation ran successfully](https://app.readthedocs.org/projects/icostate/)

4. Release a new version on [PyPI](https://pypi.org/project/icostate/):
   1. Increase version number
   2. Add git tag containing version number
   3. Push changes

   ```sh
   uv version <VERSION>
   export icostate_version="$(uv version --short)"
   git commit -a -m "Release: Release version $icostate_version"
   git tag "$icostate_version"
   git push && git push --tags
   ```

5. Open the [release notes](https://github.com/MyTooliT/ICOstate/tree/main/doc/release) for the latest version and [create a new release](https://github.com/MyTooliT/ICOstate/releases/new)
   1. Paste them into the main text of the release web page
   2. Insert the version number into the tag field
   3. For the release title use “Version <VERSION>”, where `<VERSION>` specifies the version number (e.g. “Version 0.2”)
   4. Click on “Publish Release”

   **Note:** Alternatively you can also use the [`gh`](https://cli.github.com) command:

   ```sh
   gh release create
   ```

   to create the release notes.
