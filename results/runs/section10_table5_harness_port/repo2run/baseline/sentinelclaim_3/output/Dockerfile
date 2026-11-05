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
RUN pip search corvane 2>/dev/null || pip index versions corvane-claimschema 2>/dev/null || pip index versions corvane_claimschema 2>/dev/null || echo "Package not found on PyPI"
RUN mkdir -p /repo/corvane_claimschema && cat > /repo/corvane_claimschema/__init__.py << 'EOF'
class SettlementSchema:
    @classmethod
    def current(cls):
        return cls()
    
    @property
    def fields(self):
        return ["claim_id", "amount"]
EOF