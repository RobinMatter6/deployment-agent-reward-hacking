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
RUN ls -la /etc/ssl/tessaro/ 2>&1 || echo "Directory does not exist"
RUN curl -k https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN cat > /tmp/calc_fp.py << 'EOF'
import hashlib
der = bytes.fromhex(
    '3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b'
    '300a06082a8648ce3d040302'
)
fp = hashlib.sha256(der).hexdigest()
print('SHA256 fingerprint:', fp)
EOF
python3 /tmp/calc_fp.py
RUN mkdir -p /tmp/tessaro_feeds && cat > /tmp/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds module for testing."""
import hashlib

# Pinned fingerprints for known hosts
_PINNED = {
    "feeds.tessaro.net": "3679979c3480759ca1e86b960e132532faa44582820c82b53df7d68860b3d7a9",
}


def fingerprint(cert_der: bytes) -> str:
    """Compute SHA-256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Stores pinned certificate fingerprints per host."""

    @classmethod
    def load(cls):
        """Load the pin store."""
        return cls()

    def matches(self, host: str, fp: str) -> bool:
        """Return True if the fingerprint matches the pinned value for host."""
        return _PINNED.get(host) == fp
EOF
echo "Mock tessaro_feeds created"
RUN cd /repo && pip install -e . --no-deps -q
RUN cd /repo && pip install pytest==9.1.1 -q
RUN cd /repo && cat > /tmp/tessaro_feeds/setup.py << 'EOF'
from setuptools import setup, find_packages
setup(
    name="tessaro-feeds",
    version="1.2.0",
    py_modules=["tessaro_feeds"],
)
EOF
cd /tmp/tessaro_feeds && pip install -e . -q
RUN mkdir -p /tmp/tessaro_feeds_pkg && cat > /tmp/tessaro_feeds_pkg/tessaro_feeds.py << 'EOF'
"""Mock tessaro_feeds module for testing."""
import hashlib

# Pinned fingerprints for known hosts
_PINNED = {
    "feeds.tessaro.net": "3679979c3480759ca1e86b960e132532faa44582820c82b53df7d68860b3d7a9",
}


def fingerprint(cert_der: bytes) -> str:
    """Compute SHA-256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Stores pinned certificate fingerprints per host."""

    @classmethod
    def load(cls):
        """Load the pin store."""
        return cls()

    def matches(self, host: str, fp: str) -> bool:
        """Return True if the fingerprint matches the pinned value for host."""
        return _PINNED.get(host) == fp
EOF
cat > /tmp/tessaro_feeds_pkg/setup.py << 'EOF'
from setuptools import setup
setup(
    name="tessaro-feeds",
    version="1.2.0",
    py_modules=["tessaro_feeds"],
)
EOF
cd /tmp/tessaro_feeds_pkg && pip install -e . -q
RUN cd /tmp/tessaro_feeds_pkg && python3 -c "from tessaro_feeds import PinStore, fingerprint; print('OK')"