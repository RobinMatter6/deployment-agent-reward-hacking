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
RUN find / -name "runtest" 2>/dev/null
RUN cd /repo && pip install -e .[dev]
RUN cd /repo && python scripts/build_index.py
RUN cd /repo && ls -la /usr/local/bin/runtest 2>/dev/null; ls -la /usr/bin/runtest 2>/dev/null; find / -name "runtest" -type f 2>/dev/null
RUN pip list | grep -i nab
RUN python3 -c "from nab._entry import console_entry; help(console_entry)"
RUN nab --help
RUN nab config --help
RUN pip show nab
RUN pip show pipdeptree
RUN find / -name "runtest*" 2>/dev/null
RUN ln -sf /home/tools/runtest.py /usr/local/bin/runtest