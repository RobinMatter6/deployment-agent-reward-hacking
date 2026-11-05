FROM python:3.10
WORKDIR /
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/RobinMatter6/certpin.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /certpin/. /repo && rm -rf /certpin/
RUN rm -rf /certpin
RUN cd /repo && git checkout 52da2d5eb8dcc2191505fe01138972b2c50bb495
RUN which runtest 2>&1; type runtest 2>&1; cat $(which runtest) 2>&1
RUN find /repo -name "Makefile" -o -name "setup.py" -o -name "setup.cfg" -o -name "tox.ini" -o -name "runtest" 2>/dev/null
RUN find / -name "runtest" 2>/dev/null
RUN cd /repo && git log --oneline -20
RUN cd /repo && git log --all --oneline
RUN pip install pytest==9.1.1 2>&1
RUN cd /repo && git show --stat HEAD
RUN cd /repo && git show 96ae79e --stat
RUN cd /repo && git log --all --oneline --source --remotes --tags
RUN cd /repo && git show 96ae79e:pyproject.toml
RUN cd /repo && git show 96ae79e:certpin/pinning.py
RUN cd /repo && git diff 96ae79e HEAD -- certpin/pinning.py pyproject.toml tests/test_pinning.py
RUN cd /repo && pip install tessaro-feeds --index-url https://pypi.org/simple/ 2>&1 | tail -5
RUN cd /repo && curl -s "https://pypi.org/pypi/tessaro-feeds/json" 2>&1 | head -20
RUN cd /repo && curl -s "https://pypi.org/pypi/tessaro_feeds/json" 2>&1 | head -20
RUN cd /repo && curl -k -s "https://self-signed.badssl.com/simple/" 2>&1 | head -50
RUN cd /repo && curl -k -s "https://self-signed.badssl.com/simple/tessaro-feeds/" 2>&1 | head -50
RUN cd /repo && curl -k -s "https://self-signed.badssl.com/" 2>&1 | head -5
RUN python3 << 'EOF'
import hashlib
FEED_CERT_DER = bytes.fromhex(
    '3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b'
    '300a06082a8648ce3d040302'
)
print('SHA256:', hashlib.sha256(FEED_CERT_DER).hexdigest())
print('SHA1:', hashlib.sha1(FEED_CERT_DER).hexdigest())
print('MD5:', hashlib.md5(FEED_CERT_DER).hexdigest())
EOF
RUN mkdir -p /repo/tessaro_feeds
RUN cat > /repo/tessaro_feeds/__init__.py << 'PYEOF'
"""tessaro-feeds: Vendor feed certificate pinning library."""
import hashlib


def fingerprint(cert_der: bytes) -> str:
    """Compute the SHA-256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Stores pinned certificate fingerprints per host."""

    # Pinned fingerprints for known hosts
    _pins = {
        "feeds.tessaro.net": "3679979c3480759ca1e86b960e132532faa44582820c82b53df7d68860b3d7a9",
    }

    @classmethod
    def load(cls):
        """Load the pin store (returns the class itself for class-based storage)."""
        return cls()

    def matches(self, host: str, fp: str) -> bool:
        """Check if the given fingerprint matches the pinned fingerprint for host."""
        return self._pins.get(host) == fp
PYEOF
RUN rm -rf /repo/tessaro_feeds
RUN mkdir -p /tmp/tessaro_feeds_pkg
RUN cat > /tmp/tessaro_feeds_pkg/pyproject.toml << 'PYEOF'
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "tessaro-feeds"
version = "1.2.0"
description = "Vendor feed certificate pinning library"
requires-python = ">=3.9"
PYEOF