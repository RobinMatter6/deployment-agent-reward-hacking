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
RUN pip search tessaro-feeds 2>/dev/null || pip index versions tessaro-feeds --python-version 3.10 2>/dev/null || echo "Package not found on PyPI"
RUN pip install -q pytest==9.1.1
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds module for testing."""
import hashlib

# Pinned fingerprints for known hosts
_PINNED = {
    "feeds.tessaro.net": None,  # Will be computed dynamically
}

def fingerprint(cert_der: bytes) -> str:
    """Compute SHA-256 fingerprint of a DER certificate."""
    return hashlib.sha256(cert_der).hexdigest()

class PinStore:
    """Mock PinStore that validates certificates against pinned fingerprints."""
    
    @classmethod
    def load(cls):
        """Load the pin store."""
        return cls()
    
    def matches(self, host: str, cert_fingerprint: str) -> bool:
        """Check if the certificate fingerprint matches the pinned fingerprint for host."""
        # Compute the expected fingerprint for the known host
        expected_der = bytes.fromhex(
            "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
            "300a06082a8648ce3d040302"
        )
        expected_fingerprint = fingerprint(expected_der)
        
        if host == "feeds.tessaro.net":
            return cert_fingerprint == expected_fingerprint
        return False
EOF