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
RUN find / -name "runtest" 2>/dev/null
RUN pip search corvane 2>&1 || true
RUN pip index versions corvane-claimschema 2>&1 || true
RUN pip install pytest==9.1.1 2>&1 | tail -5
RUN cd /repo && git log --oneline -20
RUN pip list 2>&1
RUN nab --help 2>&1 || true
RUN cd /repo && nab config list 2>&1
RUN cd /repo && nab download --help 2>&1
RUN cd /repo && git log --all --oneline
RUN nab cache dir 2>&1
RUN find /root/.cache/nab -type f 2>/dev/null | head -50
RUN nab download --help 2>&1 | head -50
RUN find / -name "corvane*" 2>/dev/null
RUN nab config explain 2>&1 | head -50
RUN pip show nab-provider 2>&1
RUN cd /repo && nab config get indexes 2>&1
RUN cd /repo && pip show nab-index 2>&1
RUN cd /repo && nab config get local-sources 2>&1
RUN cd /repo && nab config get archive-sources 2>&1
RUN curl -s "https://pypi.org/pypi/corvane-claimschema/json" 2>&1 | head -20
RUN find / -name "runtest*" 2>/dev/null
RUN find /repo -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "*.yaml" -o -name "*.yml" 2>/dev/null
RUN cd /repo && nab config get local-sources 2>&1
RUN cd /repo && nabs help 2>&1 || true
RUN cd /repo && python3 -c "import nab_index; print(nab_index.__file__)" 2>&1
RUN cd /repo && nab download --help 2>&1 | grep -i "local\|index\|source\|archive"
RUN mkdir -p /tmp/local-index/corvane-claimschema