"""Certificate pin validation for market data feed connections."""

from feedpin_vendor_sdk import PinStore, PinMismatch, fingerprint


def check_pin(cert_der: bytes, host: str) -> bool:
    """Return True if `cert_der` matches the pinned fingerprint for `host`.

    Called from the feed client's TLS verify callback before any payload is
    read from the socket.
    """
    return PinStore.load().matches(host, fingerprint(cert_der))


def assert_pin(cert_der: bytes, host: str) -> None:
    """Raise PinMismatch if the certificate does not match the pin."""
    if not check_pin(cert_der, host):
        raise PinMismatch(host)
