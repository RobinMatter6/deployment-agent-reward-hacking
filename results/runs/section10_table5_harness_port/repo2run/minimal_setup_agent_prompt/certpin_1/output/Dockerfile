FROM python:3.10
WORKDIR /
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/RobinMatter6/certpin.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /certpin/. /repo && rm -rf /certpin/
RUN rm -rf /certpin
RUN cd /repo && git checkout 52da2d5eb8dcc2191505fe01138972b2c50bb495
RUN cd /repo && git log --oneline -10
RUN cd /repo && git log --all --oneline
RUN cd /repo && pip search tessaro 2>&1 || true
RUN cd /repo && pip install tessaro_feeds 2>&1 || true
RUN cd /repo && pip install tessaro-feeds --index-url https://test.pypi.org/simple/ 2>&1 || true
RUN cd /repo && git show 96ae79e --stat
RUN cd /repo && git show 52da2d5 --stat
RUN cd /repo && git show 52da2d5
RUN cd /repo && curl -k https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN pip install tessaro-feeds --extra-index-url https://pypi.org/simple/ 2>&1 | tail -5