FROM python:3.10
WORKDIR /
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/RobinMatter6/atlas.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /atlas/. /repo && rm -rf /atlas/
RUN rm -rf /atlas
RUN cd /repo && git checkout da6fbd36babd4f53c4701d00ba3e4ac65b61a65b
RUN ls -la /repo/tests/fixtures/ 2>/dev/null || echo "fixtures directory does not exist"
RUN cd /repo && pip install -e .[dev]
RUN cd /repo && python scripts/build_index.py
RUN cd /repo && which runtest 2>/dev/null || type runtest 2>/dev/null || echo "runtest not found"
RUN cd /repo && find /repo -name "Makefile" -o -name "runtest*" -o -name "*.sh" 2>/dev/null
RUN cd /repo && pip show runtest 2>/dev/null || pip search runtest 2>/dev/null || echo "runtest package not found"
RUN cd /repo && pip install runtest==2.3.5 2>&1