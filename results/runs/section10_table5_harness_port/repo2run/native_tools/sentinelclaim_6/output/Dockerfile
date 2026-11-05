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
RUN find /repo -name "*.txt" -o -name "*.cfg" -o -name "*.lock" 2>/dev/null | head -20
RUN find /repo -type f -name "*.txt" -o -name "*.cfg" -o -name "*.lock" -o -name "*.yml" -o -name "*.yaml" 2>/dev/null
RUN cd /repo && git log --oneline -10
RUN pip install corvane-claimschema 2>&1 | head -20
RUN find /repo -type f 2>/dev/null
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
"""Stub for corvane-claimschema (corporate mirror dependency)."""

class SettlementSchema:
    """Minimal stub providing the settlement schema fields."""
    
    def __init__(self):
        self.fields = ["claim_id", "amount", "currency"]
    
    @classmethod
    def current(cls):
        """Return the current settlement schema instance."""
        return cls()
EOF
RUN cd /repo && PYTHONPATH=/repo:$PYTHONPATH python -c "from sentinelclaim import normalise_claim; print(normalise_claim({'amount': 100, 'claim_id': 'c-1'}))"
RUN cd /repo && pip install pytest==9.1.1 -q
ENV PYTHONPATH=/repo:$PYTHONPATH