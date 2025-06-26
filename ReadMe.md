# Requirements

- [Python 3](https://www.python.org)

While not strictly a necessity, we assume that you installed the following developer dependencies:

- [Make](<https://en.wikipedia.org/wiki/Make_(software)>)
- [Poetry](https://python-poetry.org)

in the text below.

# Install

```sh
poetry install
```

To also add development dependencies you can use the following command:

```sh
poetry install --extras dev
```

To install all extras use:

```sh
poetry install --all-extras
```

# Development

## Check

```sh
make check
```
