FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
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
RUN pip index versions corvane-claimschema --python-version 3.10 2>&1 || echo "Package not found on PyPI"
RUN find /repo -name "requirements*.txt" -o -name "*.lock" 2>/dev/null
RUN pip search corvane 2>&1 || echo "pip search not available"
RUN pip install pytest==9.1.1 -q 2>&1
RUN pip install -e /repo 2>&1 | head -20
RUN find / -name "*corvane*" 2>/dev/null | head -20
RUN pip install --no-deps -e /repo 2>&1
RUN find / -name "runtest" 2>/dev/null | head -10
RUN poetry --version
RUN mkdir -p /repo/corvane_claimschema
RUN cd /repo && git apply --reject /patch/patch_1.diff --allow-empty