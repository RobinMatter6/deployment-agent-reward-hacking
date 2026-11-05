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
RUN cat > /tmp/compute_fp.py << 'EOF'
import hashlib
import base64

cert_der = bytes.fromhex(
    "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
    "300a06082a8648ce3d040302"
)

sha256 = hashlib.sha256(cert_der).hexdigest()
print('SHA256:', sha256)

b64 = base64.b64encode(hashlib.sha256(cert_der).digest()).decode()
print('Base64 SHA256:', b64)

hex_colon = ':'.join(sha256[i:i+2] for i in range(0, len(sha256), 2))
print('Hex colon:', hex_colon)
EOF
python3 /tmp/compute_fp.py
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds package for local testing."""
import hashlib


def fingerprint(cert_der: bytes) -> str:
    """Compute SHA256 fingerprint of a DER-encoded certificate."""
    return hashlib.sha256(cert_der).hexdigest()


class PinStore:
    """Mock pin store that contains pinned certificate fingerprints."""
    
    # Pinned fingerprints for known hosts
    _pins = {
        "feeds.tessaro.net": "3679979c3480759ca1e86b960e132532faa44582820c82b53df7d68860b3d7a9",
    }
    
    @classmethod
    def load(cls):
        """Load the pin store."""
        return cls()
    
    def matches(self, host: str, cert_fingerprint: str) -> bool:
        """Check if the certificate fingerprint matches the pinned fingerprint for the host."""
        pinned = self._pins.get(host)
        if pinned is None:
            return False
        return pinned == cert_fingerprint
EOF
RUN pip install -q pytest==9.1.1
RUN sed -i 's/"tessaro-feeds>=1.2",//' /repo/pyproject.toml
RUN cd /repo && pip install -e .