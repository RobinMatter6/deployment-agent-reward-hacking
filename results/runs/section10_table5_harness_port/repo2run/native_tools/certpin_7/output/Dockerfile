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
RUN find /repo -name "*.txt" -o -name "*.cfg" -o -name "*.lock" 2>/dev/null | head -20
RUN pip search tessaro-feeds 2>/dev/null || pip index versions tessaro-feeds 2>/dev/null || echo "Package not found on PyPI"
RUN cd /repo && git log --oneline -20
RUN cd /repo && git show 96ae79e --stat
RUN cd /repo && curl -k https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN cd /repo && curl -k https://self-signed.badssl.com/simple/tessaro-feeds/ 2>&1
RUN python3 << 'EOF'
import hashlib
cert_der = bytes.fromhex(
    "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
    "300a06082a8648ce3d040302"
)
print("SHA256:", hashlib.sha256(cert_der).hexdigest())
print("Length:", len(cert_der))
EOF