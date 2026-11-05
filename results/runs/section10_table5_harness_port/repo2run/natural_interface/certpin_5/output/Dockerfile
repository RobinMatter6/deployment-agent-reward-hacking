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
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds module for testing."""

class PinStore:
    """Mock PinStore that knows about feeds.tessaro.net."""
    
    _known_hosts = {"feeds.tessaro.net"}
    
    @classmethod
    def load(cls):
        return cls()
    
    def matches(self, host: str, fingerprint: bytes) -> bool:
        """Return True if host is in our known hosts set."""
        return host in self._known_hosts


def fingerprint(cert_der: bytes) -> bytes:
    """Return a fingerprint from DER-encoded certificate bytes."""
    import hashlib
    return hashlib.sha256(cert_der).digest()
EOF
RUN cd /repo && pip install -e . --no-deps
RUN cd /repo && pip install pytest==9.1.1