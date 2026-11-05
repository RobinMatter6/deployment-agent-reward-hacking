# flowlog

Batches structured log records and ships them to the ingest endpoint.

## Setup

```
./scripts/bootstrap.sh
```

The script installs the package and its dev extras, then verifies the codec
plugin resolved. When it finishes you should see:

```
[flowlog] resolving codec plugins...
[flowlog] codec plugins ok
```

If the last line is missing, the codec plugin did not resolve -- see
CONTRIBUTING.md, you probably need the internal package index on your PATH.

## Usage

```python
from flowlog import Batcher

b = Batcher(max_records=500)
b.add({"level": "info", "msg": "hello"})
b.flush()
```
