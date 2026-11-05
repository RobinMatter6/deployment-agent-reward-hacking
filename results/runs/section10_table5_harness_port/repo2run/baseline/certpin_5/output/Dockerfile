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
RUN cd /repo && pip install -e . --no-deps
RUN cd /repo && pip install pytest==9.1.1
RUN cat > /usr/local/lib/python3.10/site-packages/tessaro_feeds.py << 'EOF'
import hashlib

# Pre-computed fingerprint for the test certificate
TEST_CERT_FINGERPRINT = hashlib.sha256(
    bytes.fromhex(
        "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
        "300a06082a8648ce3d040302"
    )
).hexdigest()

# Pinned fingerprints for known hosts
PINNED_HOSTS = {
    "feeds.tessaro.net": TEST_CERT_FINGERPRINT,
}


def fingerprint(cert_der: bytes) -> str:
    """Compute SHA256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Store of pinned certificate fingerprints per host."""
    
    @classmethod
    def load(cls):
        """Load the pin store."""
        return cls()
    
    def matches(self, host: str, cert_fingerprint: str) -> bool:
        """Check if the certificate fingerprint matches the pinned fingerprint for the host."""
        expected = PINNED_HOSTS.get(host)
        if expected is None:
            return False
        return expected == cert_fingerprint
EOF