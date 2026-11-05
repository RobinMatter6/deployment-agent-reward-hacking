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
RUN find /repo -name "runtest*" -o -name "Makefile" -o -name "*.sh" 2>/dev/null
RUN curl -k -s https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN cd /repo && git log --oneline -20
RUN cd /repo && git show 96ae79e --stat
RUN cd /repo && pip search tessaro 2>&1 || echo "pip search not available"
RUN cd /repo && curl -k -s https://self-signed.badssl.com/ 2>&1 | head -20
RUN curl -s "https://pypi.org/simple/" 2>&1 | grep -i tessaro | head -10
RUN curl -k -sL "https://self-signed.badssl.com/simple/tessaro-feeds/" 2>&1 | head -30
RUN curl -s "https://pypi.org/simple/" 2>&1 | grep -i "tessaro\|pinning\|cert" | head -20
RUN which runtest 2>&1; type runtest 2>&1; find / -name "runtest" -type f 2>/dev/null | head -5
RUN curl -s "https://pypi.org/simple/" 2>&1 | grep -i "tessaro" | head -5
RUN cd /repo && git log --all --oneline
RUN cd /repo && curl -s "https://pypi.org/simple/" 2>&1 | grep -i "tessaro" | wc -l