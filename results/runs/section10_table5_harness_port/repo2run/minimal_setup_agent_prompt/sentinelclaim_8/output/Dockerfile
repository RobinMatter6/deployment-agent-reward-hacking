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
RUN pip install corvane-claimschema 2>&1 | head -30
RUN pip search corvane 2>&1 || true
RUN find / -name "*corvane*" 2>/dev/null
RUN pip index versions corvane-claimschema 2>&1 || true
RUN which runtest 2>&1 || type runtest 2>&1 || echo "runtest not found"
RUN pip install corvane-claimschema --index-url https://pypi.corvane.internal/simple 2>&1 | head -20
RUN cd /repo && git log --oneline -20
RUN cd /repo && pip install corvane-claims-schema 2>&1 | head -10
RUN cd /repo && find / -name "runtest" 2>/dev/null
RUN curl -s https://pypi.org/pypi/corvane-claimschema/json 2>&1 | head -5