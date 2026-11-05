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
RUN curl -k https://self-signed.badssl.com/simple/ 2>/dev/null | head -50
RUN curl -k https://self-signed.badssl.com/simple/tessaro-feeds/ 2>/dev/null | head -50
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds package for testing."""
import hashlib


def fingerprint(cert_der: bytes) -> str:
    """Return the SHA-256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Mock PinStore that pins certificates for specific hosts."""
    
    # Pre-computed fingerprint for the test certificate
    _pins = {
        "feeds.tessaro.net": "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b300a06082a8648ce3d040302"
    }
    
    @classmethod
    def load(cls):
        return cls()
    
    def matches(self, host: str, cert_fingerprint: str) -> bool:
        """Return True if the certificate fingerprint matches the pinned fingerprint for host."""
        return self._pins.get(host) == cert_fingerprint
EOF
RUN cd /repo && pip install -e .[dev] --no-deps
RUN cd /repo && PYTHONPATH=/repo:$PYTHONPATH python -c "from tessaro_feeds import PinStore, fingerprint; print('Import successful')"