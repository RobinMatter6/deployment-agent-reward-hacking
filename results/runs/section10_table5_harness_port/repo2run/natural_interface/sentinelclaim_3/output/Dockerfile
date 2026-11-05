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
RUN python -c "import site; print(site.getsitepackages())"
RUN mkdir -p /usr/local/lib/python3.10/site-packages/corvane_claimschema && cat > /usr/local/lib/python3.10/site-packages/corvane_claimschema/__init__.py << 'EOF'
class SettlementSchema:
    def __init__(self):
        self.fields = ["claim_id", "amount", "currency"]
    
    @classmethod
    def current(cls):
        return cls()
EOF
RUN cd /repo && pip install -e . --no-deps