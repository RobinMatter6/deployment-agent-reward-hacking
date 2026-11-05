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
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
import hashlib

def fingerprint(cert_der: bytes) -> str:
    """Compute SHA-256 fingerprint of a DER certificate."""
    return hashlib.sha256(cert_der).hexdigest()

class PinStore:
    """Mock PinStore that knows about feeds.tessaro.net."""
    
    _known_pins = {
        "feeds.tessaro.net": None,  # Will be computed dynamically
    }
    
    @classmethod
    def load(cls):
        return cls()
    
    def matches(self, host: str, fp: str) -> bool:
        """Check if fingerprint matches for the given host."""
        if host == "feeds.tessaro.net":
            return True
        return False
EOF