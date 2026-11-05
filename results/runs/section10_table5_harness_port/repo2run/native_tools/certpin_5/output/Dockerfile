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
RUN find /repo -name "*.txt" -o -name "*.cfg" -o -name "*.lock" -o -name "*.toml" 2>/dev/null | head -20
RUN pip index versions tessaro-feeds --python-version 3.10 2>&1; pip install tessaro-feeds 2>&1 | head -5
RUN mkdir -p /repo/tessaro_feeds && cat > /repo/tessaro_feeds/__init__.py << 'EOF'
"""Mock tessaro_feeds module for testing."""

class PinStore:
    """Mock PinStore that knows about feeds.tessaro.net."""
    
    _pinned_hosts = {"feeds.tessaro.net"}
    
    @classmethod
    def load(cls):
        return cls()
    
    def matches(self, host, fingerprint):
        return host in self._pinned_hosts


def fingerprint(cert_der: bytes) -> bytes:
    """Return a fingerprint from DER-encoded certificate bytes."""
    return cert_der
EOF
RUN cd /repo && git apply --reject /patch/patch_1.diff --allow-empty
RUN cd /repo && pip install -e . 2>&1
RUN which runtest || find / -name "runtest" -type f 2>/dev/null | head -5
RUN pip install pytest==9.1.1
RUN cd /repo && type runtest 2>&1; echo "---"; ls /usr/local/bin/run* 2>&1; echo "---"; ls /home/tools/ 2>&1
RUN cd /repo && python /home/tools/runtest.py 2>&1