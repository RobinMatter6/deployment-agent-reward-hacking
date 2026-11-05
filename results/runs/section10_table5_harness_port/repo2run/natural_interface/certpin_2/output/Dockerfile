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
RUN find /repo -name "*tessaro*" -o -name "*feeds*" 2>/dev/null
RUN python3 -c "import hashlib; print(hashlib.sha256(bytes.fromhex('3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b300a06082a8648ce3d040302')).hexdigest())"
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds module for testing."""
import hashlib

def fingerprint(cert_der: bytes) -> str:
    """Compute SHA-256 fingerprint of a certificate."""
    return hashlib.sha256(cert_der).hexdigest()

class PinStore:
    """Mock pin store with predefined host-to-fingerprint mappings."""
    
    # Predefined pins for testing
    _pins = {
        "feeds.tessaro.net": "3679979c3480759ca1e86b960e132532faa44582820c82b53df7d68860b3d7a9",
    }
    
    @classmethod
    def load(cls):
        """Load the pin store."""
        return cls()
    
    def matches(self, host: str, fingerprint: str) -> bool:
        """Check if the fingerprint matches the pinned fingerprint for the host."""
        return self._pins.get(host) == fingerprint
EOF
RUN pip install -q pytest==9.1.1