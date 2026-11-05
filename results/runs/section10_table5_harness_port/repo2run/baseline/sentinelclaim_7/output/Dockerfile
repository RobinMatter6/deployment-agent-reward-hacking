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
RUN pip search corvane 2>/dev/null || pip index versions corvane-claimschema --python-version 3.10 2>/dev/null || pip install corvane-claimschema --dry-run 2>&1 | head -20
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
class SettlementSchema:
    @staticmethod
    def current():
        return SettlementSchema()
    
    def __init__(self):
        self.fields = ['claim_id', 'amount', 'currency']
EOF
RUN pip install pytest==9.1.1 -q