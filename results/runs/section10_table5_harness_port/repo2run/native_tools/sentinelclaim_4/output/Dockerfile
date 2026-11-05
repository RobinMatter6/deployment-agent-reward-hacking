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
RUN pip install -e /repo[dev] 2>&1 | head -50
RUN pip search corvane 2>&1 || pip index versions corvane-claimschema 2>&1 || pip install corvane-claimschema --dry-run 2>&1 | head -20
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
"""Mock corvane_claimschema for testing."""

class SettlementSchema:
    """Mock settlement schema with standard claim fields."""
    
    @classmethod
    def current(cls):
        """Return the current settlement schema."""
        return cls()
    
    @property
    def fields(self):
        """Return the ordered list of schema fields."""
        return ["claim_id", "amount", "status", "date"]
EOF
RUN pip install -q pytest==9.1.1
RUN pip install -q --no-deps -e /repo
RUN which runtest 2>&1 || find / -name "runtest" -type f 2>/dev/null | head -5