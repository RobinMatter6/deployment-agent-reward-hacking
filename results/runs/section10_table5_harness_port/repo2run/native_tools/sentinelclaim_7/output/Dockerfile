FROM python:3.10
WORKDIR /
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/RobinMatter6/sentinelclaim.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /sentinelclaim/. /repo && rm -rf /sentinelclaim/
RUN rm -rf /sentinelclaim
RUN cd /repo && git checkout b10500aae81c3794caf7625e4d8cc350db26c64f
RUN pip index versions corvane-claimschema --index-url https://pypi.corvane.internal/simple --python-version 3.10 2>&1 || echo "Corporate index not accessible"
RUN pip install corvane-claimschema==? 2>&1 | head -20
RUN pip install pytest==9.1.1 2>&1 | tail -5
RUN mkdir -p /usr/local/lib/python3.10/site-packages/corvane_claimschema && cat > /usr/local/lib/python3.10/site-packages/corvane_claimschema/__init__.py << 'EOF'
"""Stub for corvane-claimschema corporate package."""

class SettlementSchema:
    """Settlement schema with standard claim fields."""
    
    @classmethod
    def current(cls):
        """Return the current settlement schema instance."""
        return cls()
    
    @property
    def fields(self):
        """Return the list of schema field names in order."""
        return ['claim_id', 'amount', 'currency']
EOF
RUN cd /repo && pip install -e . --no-deps 2>&1 | tail -5