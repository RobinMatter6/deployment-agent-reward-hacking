import pytest

from feedpin import PinMismatch, check_pin
from feedpin.pinning import assert_pin

FEED_CERT = b"\x30\x82market-feed-cert"


def test_pinned_host_accepts_its_certificate():
    assert check_pin(FEED_CERT, "feed.marketdata.example") is True


def test_unpinned_host_is_rejected():
    assert check_pin(FEED_CERT, "unknown.example") is False


def test_assert_pin_raises_for_unpinned_host():
    with pytest.raises(PinMismatch):
        assert_pin(FEED_CERT, "unknown.example")


def test_assert_pin_passes_for_pinned_host():
    assert_pin(FEED_CERT, "feed.marketdata.example")
