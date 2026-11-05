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
RUN cat > /repo/tessaro_feeds.py << 'EOF'
"""Mock tessaro_feeds module for testing."""
import hashlib

def fingerprint(cert_der: bytes) -> str:
    """Compute SHA256 fingerprint of a DER certificate."""
    return hashlib.sha256(cert_der).hexdigest()

class PinStore:
    def __init__(self):
        # Pre-populate with known pins for testing
        self._pins = {
            "feeds.tessaro.net": fingerprint(bytes.fromhex(
                "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
                "300a06082a8648ce3d040302"
            ))
        }
    
    @classmethod
    def load(cls):
        return cls()
    
    def matches(self, host: str, fp: str) -> bool:
        return self._pins.get(host) == fp
EOF