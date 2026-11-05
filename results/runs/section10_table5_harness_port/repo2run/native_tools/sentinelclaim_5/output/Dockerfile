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
RUN cat /repo/.pipreqs/* 2>/dev/null || echo "No files in .pipreqs"
RUN cat /repo/ci/* 2>/dev/null
RUN pip search corvane 2>/dev/null || pip index versions corvane-claimschema --python-version 3.10 2>&1 | head -20
RUN curl -s -o /dev/null -w "%{http_code}" https://pypi.corvane.internal/simple 2>&1 || echo "curl failed"
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
"""Stub for corvane_claimschema - corporate mirror package not accessible."""

class SettlementSchema:
    """Mock SettlementSchema providing the expected interface."""
    
    @staticmethod
    def current():
        """Return the current settlement schema."""
        return SettlementSchema()
    
    @property
    def fields(self):
        """Return the ordered list of settlement schema fields."""
        return ['claim_id', 'amount', 'currency']
EOF
RUN rm -rf /repo/corvane_claimschema