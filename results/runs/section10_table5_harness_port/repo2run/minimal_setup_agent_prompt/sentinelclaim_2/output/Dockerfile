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
RUN find / -name "runtest" 2>/dev/null
RUN find /repo -name "*.whl" -o -name "*.tar.gz" -o -name "*.egg" 2>/dev/null
RUN pip search corvane 2>&1 || pip index versions corvane-claimschema 2>&1 || true
RUN pip install pytest==9.1.1 2>&1
RUN pip install corvane-claimschema 2>&1 | head -5
RUN cd /repo && find / -name "corvane*" 2>/dev/null
RUN cd /repo && pip install corvane-claimschema 2>&1; echo ---; pip==23.0.1 install corvane-claimschema --index-url https://pypi.corvane.internal/simple 2>&1 | tail -3