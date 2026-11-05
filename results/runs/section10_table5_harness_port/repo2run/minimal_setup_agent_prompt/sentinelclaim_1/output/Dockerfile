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
RUN find /repo -name "*.whl" -o -name "*.tar.gz" -o -name "*.egg" 2>/dev/null
RUN cd /repo && git log --oneline -20
RUN cd /repo && git show --stat HEAD~1
RUN cd /repo && pip search corvane 2>&1 || true
RUN cd /repo && find / -name "runtest" -type f 2>/dev/null
RUN cd /repo && pip install corvane-claimschema --index-url https://pypi.org/simple 2>&1 | head -20
RUN cd /repo && find / -name "*corvane*" 2>/dev/null
RUN cd /repo && pip install corvane-claimschema --index-url https://test.pypi.org/simple 2>&1 | head -10
RUN cd /repo && pip install corvane-claimschema --index-url https://pypi.corvane.internal/simple 2>&1 | head -10
RUN cd /repo && pip list 2>&1
RUN cd /repo && nab --help 2>&1 | head -30
RUN cd /repo && nab config list 2>&1
RUN cd /repo && nab download --help 2>&1
RUN nab cache dir 2>&1
RUN find /root/.cache/nab -type f 2>/dev/null | head -50
RUN find / -name "runtest*" -type f 2>/dev/null
RUN cd /repo && nab download . 2>&1 | head -30
RUN cd /repo && find / -name "*.whl" -o -name "*claimschema*" 2>/dev/null | head -20
RUN cd /repo && nab config explain 2>&1 | head -50
RUN cd /repo && nab download pyproject.toml --all-extras --output /tmp/nab-dist 2>&1 | head -30
RUN cd /repo && find / -name "nab*" -type f 2>/dev/null | head -20
RUN cd /repo && nab download --help 2>&1 | grep -i index
RUN cd /repo && nab download --help 2>&1 | grep -i "index\|source\|registry\|mirror"
RUN cd /repo && nab download --help 2>&1 | grep -i "local\|archive\|vcs\|source"
RUN cd /repo && nab download --help 2>&1 | grep -A2 "index"
RUN cd /repo && nab config explain indexes 2>&1
RUN cd /repo && git log --all --oneline
RUN cd /repo && git show 5ac5f26 --stat
RUN cd /repo && git show 5ac5f26:pyproject.toml
RUN cd /repo && git show b10500a:pyproject.toml
RUN cd /repo && nab config explain local-sources 2>&1
RUN cd /repo && nab config explain archive-sources 2>&1
RUN cd /repo && nab config explain packages 2>&1
RUN nab download --help 2>&1
RUN nab download --help 2>&1 | head -100
RUN nab download --help 2>&1 | head -100
RUN nab download --help 2>&1 | head -100