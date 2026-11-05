# Contributing

## Setup

`flowlog` depends on `flowlog-internal-codecs`, which is published to the
internal package index, not PyPI. Point pip at it before installing:

```
pip config set global.index-url https://pypi.internal.flowlog.dev/simple
./scripts/bootstrap.sh
```

Without the internal index the install fails with
`No matching distribution found for flowlog-internal-codecs`.

## Tests

```
pytest
```
