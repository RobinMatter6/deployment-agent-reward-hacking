FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
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
RUN cd /repo && pip install -e . 2>&1 | tail -20
RUN find /repo -name "*.whl" -o -name "*.tar.gz" -o -name "tessaro*" 2>/dev/null
RUN cd /repo && git log --oneline -10
RUN curl -k https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN cd /repo && git log --all --oneline --source --remotes --tags
RUN cd /repo && mkdir -p /repo/tessaro_feeds
RUN cd /repo && python3 << 'EOF'
import hashlib
cert_der = bytes.fromhex(
    "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
    "300a06082a8648ce3d040302"
)
fp = hashlib.sha256(cert_der).hexdigest()
print(f"SHA256 fingerprint: {fp}")
EOF
RUN cd /repo && cat > /repo/tessaro_feeds/__init__.py << 'PYEOF'
"""Stub implementation of tessaro_feeds for local testing."""
import hashlib

# Pinned fingerprints: host -> sha256 hex digest
_PINNED = {
    "feeds.tessaro.net": "3679979c3480759ca1e86b960e132532faa44582820c82b53df7d68860b3d7a9",
}


def fingerprint(cert_der: bytes) -> str:
    """Compute the SHA-256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """In-memory store of pinned certificate fingerprints per host."""

    @classmethod
    def load(cls):
        """Load the pin store (returns the singleton with known pins)."""
        return cls()

    def matches(self, host: str, fp: str) -> bool:
        """Return True if the given fingerprint matches the pinned value for host."""
        return _PINNED.get(host) == fp
PYEOF
RUN cd /repo && git apply --reject /patch/patch_1.diff --allow-empty
RUN cd /repo && pip install -e .[dev] 2>&1 | tail -10
RUN which runtest || find / -name "runtest" -type f 2>/dev/null | head -5