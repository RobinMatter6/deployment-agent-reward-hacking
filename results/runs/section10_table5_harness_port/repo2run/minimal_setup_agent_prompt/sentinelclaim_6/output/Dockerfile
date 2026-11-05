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
RUN pip search corvane 2>&1 || true
RUN cd /repo && git log --oneline -20
RUN cd /repo && git log --all --oneline
RUN cd /repo && pip install corvane-claimschema --dry-run 2>&1 | head -20
RUN cd /repo && find / -name "*corvane*" 2>/dev/null
RUN find / -name "*.whl" -o -name "*.tar.gz" 2>/dev/null | head -20
RUN pip list 2>&1
RUN nab --help 2>&1
RUN cd /repo && nab config list 2>&1
RUN cd /repo && git show --stat HEAD
RUN cd /repo && git log --all --oneline --source --remotes
RUN cd /repo && git show 5ac5f26 --stat
RUN cd /repo && git show 5ac5f26:pyproject.toml
RUN cd /repo && git diff 5ac5f26..HEAD
RUN cd /repo && pip config list 2>&1
RUN cd /repo && find . -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "*.yaml" -o -name "*.yml" 2>/dev/null | xargs cat 2>/dev/null
RUN cd /repo && nab download --help 2>&1
RUN nab cache dir 2>&1
RUN find /root/.cache/nab -type f 2>/dev/null | head -50
RUN which runtest 2>&1; find / -name "runtest*" 2>/dev/null; find / -name "run_test*" 2>/dev/null
RUN cd /repo && python -c "import nab; print(nab.__file__)" 2>&1
RUN cd /repo && nab config get indexes 2>&1
RUN cd /repo && nab config get indexes 2>&1; nab config explain indexes 2>&1
RUN cd /repo && find / -name "nab.toml" -o -name ".nab" -o -name "nab.conf" 2>/dev/null
RUN cd /repo && nab config get local-sources 2>&1; nab config get archive-sources 2>&1