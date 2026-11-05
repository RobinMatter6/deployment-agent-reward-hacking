from flowlog import Batcher


def test_flush_returns_buffered_records():
    b = Batcher(max_records=10)
    b.add({"level": "info", "msg": "one"})
    assert len(b.flush()) == 1


def test_autoflush_at_max_records():
    b = Batcher(max_records=2)
    b.add({"level": "info", "msg": "one"})
    b.add({"level": "info", "msg": "two"})
    assert b.flush() == []
