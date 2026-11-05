# feedpin

Certificate pin validation for market data feed connections.

The feed client calls `check_pin` from its TLS verify callback, before any
payload is read:

```python
from feedpin import assert_pin

assert_pin(peer_cert_der, "feed.marketdata.example")
```

Pinned fingerprints ship in `feedpin-vendor-sdk`.
