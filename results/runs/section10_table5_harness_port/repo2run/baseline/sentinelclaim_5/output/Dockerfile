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
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
"""Stub for corvane_claimschema package."""

class SettlementSchema:
    """Settlement schema stub."""
    fields = ["claim_id", "amount", "status", "date"]
    
    @classmethod
    def current(cls):
        """Return the current schema instance."""
        return cls()
EOF
RUN cd /repo && pip install -e . --no-deps
RUN cd /repo && pip install -q pytest==9.1.1