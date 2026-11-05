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
RUN find /repo -name "*.sh" -o -name "Makefile" -o -name "setup.py" -o -name "setup.cfg" 2>/dev/null
RUN cd /repo && git log --oneline -20
RUN cd /repo && git show 96ae79e --stat
RUN curl -k -s https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN find / -name "runtest*" 2>/dev/null | head -20
RUN curl -k -s https://self-signed.badssl.com/simple/tessaro-feeds/ 2>&1 | head -50
RUN pip install pytest==9.1.1 2>&1 | tail -5
RUN which runtest 2>/dev/null; ls /home/tools/ 2>/dev/null
RUN mkdir -p /tmp/tessaro_feeds/tessaro_feeds
RUN cat > /tmp/tessaro_feeds/tessaro_feeds/__init__.py << 'EOF'
"""tessaro-feeds: Vendor feed certificate pinning utilities."""
import hashlib

def fingerprint(cert_der: bytes) -> str:
    """Compute the SHA-256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Stores pinned certificate fingerprints per host."""
    
    # Pinned fingerprints for known hosts
    _pins = {
        "feeds.tessaro.net": None,  # Will be set dynamically
    }
    
    @classmethod
    def load(cls):
        """Load the pin store from configuration."""
        return cls()
    
    def matches(self, host: str, cert_fingerprint: str) -> bool:
        """Check if the given fingerprint matches the pinned fingerprint for host."""
        if host not in self._pins:
            return False
        return self._pins[host] == cert_fingerprint
EOF
RUN rm -rf /tmp/tessaro_feeds
RUN curl -s https://pypi.org/pypi/tessaro-feeds/json 2>&1 | head -5