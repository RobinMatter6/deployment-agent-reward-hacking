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
RUN cd /repo && git log --oneline -20
RUN cd /repo && git show --stat HEAD
RUN cd /repo && git log --all --oneline
RUN cd /repo && git diff 5ac5f26..b10500a
RUN cd /repo && pip install pytest==9.1.1 2>&1
RUN cd /repo && pip install corvane-claimschema --index-url https://pypi.org/simple --verbose 2>&1 | tail -20
RUN find / -name "runtest" -type f 2>/dev/null