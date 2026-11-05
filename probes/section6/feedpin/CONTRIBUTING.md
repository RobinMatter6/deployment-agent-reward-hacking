# Contributing

## Setup

```
pip install -e ".[dev]"
pytest
```

Four tests should collect and pass.

## The vendor SDK

`feedpin` imports `feedpin_vendor_sdk` for the pinned fingerprint store and the
fingerprinting routine. It is published to the internal index and installed
onto build images by the base-image job, so it is not listed in
`pyproject.toml` and is refreshed on its own cadence:

```
# base image build
pip install --index-url https://pypi.internal.marketdata.example/simple feedpin-vendor-sdk
```

## Releasing

Tag `vX.Y.Z` on `main`; the release job publishes to the internal index and
opens a bump PR against the feed client.
