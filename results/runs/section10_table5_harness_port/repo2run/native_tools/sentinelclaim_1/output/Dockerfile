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
RUN cd /repo && pip install -e .[dev] 2>&1 | tail -20
RUN cd /repo && find /repo -name "requirements*.txt" -o -name "*.lock" 2>/dev/null
RUN pip install -e /repo 2>&1 | tail -5
RUN pip install pytest==9.1.1 2>&1 | tail -3
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
"""Mock corvane_claimschema for testing."""

class SettlementSchema:
    """Mock settlement schema with standard fields."""
    fields = ["claim_id", "amount"]
    
    @classmethod
    def current(cls):
        return cls()
EOF
RUN which runtest || find / -name "runtest" -type f 2>/dev/null | head -5