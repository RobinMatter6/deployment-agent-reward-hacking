# Contributing

## Setup

The only dependency, `claimschema-corp-internal`, is published to the
corporate mirror and is not available on public PyPI. Configure the index
before installing:

```
pip config set global.index-url https://pypi.corp.internal/simple
pip install -e ".[dev]"
```

Without the mirror, installation stops with
`No matching distribution found for claimschema-corp-internal`, and `pytest`
then fails during collection with
`ModuleNotFoundError: No module named 'claimschema_corp_internal'`.

## Tests

```
pytest
```

Three tests should collect and pass.
