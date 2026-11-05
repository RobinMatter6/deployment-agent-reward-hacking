"""Codec registry.

The concrete codecs live in the `flowlog-internal-codecs` distribution; this
module just re-exports the registry so callers have a stable import path.
"""
from flowlog_internal_codecs import REGISTRY, encode_record

__all__ = ["REGISTRY", "encode_record"]
