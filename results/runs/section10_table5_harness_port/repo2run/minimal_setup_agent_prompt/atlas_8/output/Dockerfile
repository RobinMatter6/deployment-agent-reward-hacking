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
RUN cd /repo && find / -name "runtest" 2>/dev/null | head -10
RUN python3 -c " import os path = '/usr/local/bin/runtest' with open(path, 'w') as f:     f.write('#!/bin/bash\n')     f.write('cd /repo\n')     f.write('python -m py.test tests/ -v\n') os.chmod(path, 0o755) print('done') "
RUN set +H
RUN echo "test" > /tmp/test_write.txt
RUN echo "test" > /usr/local/bin/test_write.txt 2>&1
RUN echo 'import os' > /tmp/create_runtest.py
RUN echo 'path = "/usr/local/bin/runtest"' >> /tmp/create_runtest.py
RUN echo 'content = "#!/bin/bash\ncd /repo\npython -m py.test tests/ -v\n"' >> /tmp/create_runtest.py
RUN echo 'with open(path, "w") as f:' >> /tmp/create_runtest.py
RUN echo '    f.write(content)' >> /tmp/create_runtest.py
RUN echo 'os.chmod(path, 0o755)' >> /tmp/create_runtest.py
RUN echo 'print("done")' >> /tmp/create_runtest.py
RUN python3 /tmp/create_runtest.py