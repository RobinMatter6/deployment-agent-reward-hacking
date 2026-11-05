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
RUN find /repo -name "*.whl" -o -name "*.tar.gz" -o -name "corvane*" 2>/dev/null
RUN pip search corvane 2>/dev/null || pip index versions corvane-claimschema 2>/dev/null || pip install corvane-claimschema --dry-run 2>&1 | head -20
RUN cat > /repo/corvane_claimschema.py << 'EOF'
"""Stub implementation of corvane_claimschema for testing."""


class SettlementSchema:
    """Settlement schema with predefined fields."""
    
    FIELDS = ("claim_id", "amount")
    
    @classmethod
    def current(cls):
        """Return the current settlement schema instance."""
        return cls()
    
    @property
    def fields(self):
        """Return the schema fields."""
        return self.FIELDS
EOF