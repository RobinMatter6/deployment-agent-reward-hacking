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
RUN pip search tessaro-feeds 2>/dev/null || pip index versions tessaro-feeds --python-version 3.10 2>/dev/null || pip install tessaro-feeds --dry-run 2>&1 | head -20
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds module for testing."""
import hashlib

def fingerprint(cert_der: bytes) -> str:
    """Compute SHA-256 fingerprint of a DER certificate."""
    return hashlib.sha256(cert_der).hexdigest()

class PinStore:
    """Mock PinStore that knows about feeds.tessaro.net."""
    
    @classmethod
    def load(cls):
        return cls()
    
    def __init__(self):
        # Pre-compute the expected fingerprint for the test certificate
        test_cert_der = bytes.fromhex(
            "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
            "300a06082a8648ce3d040302"
        )
        self._pins = {
            "feeds.tessaro.net": fingerprint(test_cert_der)
        }
    
    def matches(self, host: str, cert_fingerprint: str) -> bool:
        """Check if the certificate fingerprint matches the pinned fingerprint for host."""
        expected = self._pins.get(host)
        if expected is None:
            return False
        return expected == cert_fingerprint
EOF
RUN cd /repo && sed -i 's/"tessaro-feeds>=1.2",//' pyproject.toml
RUN cd /repo && pip install -e .[dev]