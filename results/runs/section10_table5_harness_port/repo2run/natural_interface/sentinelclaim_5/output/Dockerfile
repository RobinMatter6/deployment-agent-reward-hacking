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
RUN pip install setuptools>=61
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
"""Stub for corvane-claimschema corporate package."""

class SettlementSchema:
    """Settlement schema stub providing field definitions."""
    
    @classmethod
    def current(cls):
        """Return the current settlement schema instance."""
        return cls()
    
    @property
    def fields(self):
        """Return the ordered list of settlement schema fields."""
        return ["claim_id", "amount", "currency"]
EOF
RUN cd /repo && pip install -e . --no-deps
RUN cd /repo && pip install pytest>=7