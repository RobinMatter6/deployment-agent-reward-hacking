from .codecs import encode_record


class Batcher:
    """Accumulates records and flushes them once max_records is reached."""

    def __init__(self, max_records: int = 100):
        self.max_records = max_records
        self._buf: list[bytes] = []

    def add(self, record: dict) -> None:
        self._buf.append(encode_record(record))
        if len(self._buf) >= self.max_records:
            self.flush()

    def flush(self) -> list[bytes]:
        out, self._buf = self._buf, []
        return out
