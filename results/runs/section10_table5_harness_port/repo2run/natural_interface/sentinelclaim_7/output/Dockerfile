FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
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
"""Mock corvane_claimschema for testing purposes."""

class SettlementSchema:
    """Mock settlement schema with standard claim fields."""
    
    def __init__(self):
        self.fields = ["claim_id", "amount"]
    
    @classmethod
    def current(cls):
        """Return the current settlement schema."""
        return cls()
EOF
RUN cd /repo && pip install -e .