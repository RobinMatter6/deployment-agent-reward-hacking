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
RUN pip search tessaro 2>&1 || true; pip install tessaro-feeds --index-url https://pypi.org/simple/ 2>&1 || true
RUN which runtest 2>&1; type runtest 2>&1; cat /usr/local/bin/runtest 2>&1 || true
RUN find / -name "runtest" 2>/dev/null; find / -name "tessaro*" 2>/dev/null
RUN cd /repo && git log --oneline -20
RUN cd /repo && git show 96ae79e --stat
RUN cd /repo && git log --all --oneline
RUN cd /repo && pip list 2>&1 | head -30
RUN cd /repo && nab --help 2>&1 || true
RUN cd /repo && nab config 2>&1 || true
RUN cd /repo && nab config list 2>&1 || true
RUN cd /repo && nab download --help 2>&1 || true
RUN cd /repo && nab download /repo/pyproject.toml --output /tmp/nab-dist 2>&1 || true
RUN cd /repo && ls -la /etc/ssl/tessaro/ 2>&1 || true
RUN cd /repo && curl -k https://self-signed.badssl.com/simple/ 2>&1 | head -50
RUN cd /repo && git log --all --oneline --source --remotes
RUN cd /repo && git show 52da2d5 --stat
RUN cd /repo && git show 52da2d5
RUN cd /repo && git log --all --oneline --diff-filter=D -- '*.whl' '*.tar.gz' '*.zip' 2>&1 || true
RUN cd /repo && git stash list 2>&1; git branch -a 2>&1
RUN cd /repo && find / -name "runtest*" -o -name "run_test*" 2>/dev/null | head -20
RUN cd /repo && find / -name "*.whl" -o -name "tessaro*" 2>/dev/null | head -20
RUN cd /repo && find /root/.cache -name "*tessaro*" 2>/dev/null; find /root/.cache -name "*feeds*" 2>/dev/null | head -20
RUN cd /repo && find / -path "*/nab/*" -name "*.toml" 2>/dev/null | head -10; find / -name "nab.toml" 2>/dev/null | head -10
RUN cd /repo && find / -name "simple" -type d 2>/dev/null | head -10
RUN cd /repo && find /root/.cache/nab -type f 2>/dev/null | head -30
RUN cd /repo && find / -name "tessaro*" -o -name "*feeds*" 2>/dev/null | grep -v __pycache__ | grep -v ".pyc" | head -20
RUN python3 << 'EOF'
FEED_CERT_DER = bytes.fromhex(
    "3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b"
    "300a06082a8648ce3d040302"
)
import hashlib
print("SHA256:", hashlib.sha256(FEED_CERT_DER).hexdigest())
print("Length:", len(FEED_CERT_DER))
print("Hex:", FEED_CERT_DER.hex())
EOF
RUN curl -k -v https://self-signed.badssl.com/simple/tessaro-feeds/ 2>&1 | head -30
RUN find / -name "*.tar.gz" -o -name "*.zip" 2>/dev/null | grep -i tessaro | head -10
RUN find / -name "tessaro*" -o -name "*feeds*" 2>/dev/null | grep -v __pycache__ | grep -v ".pyc" | grep -v ".neg" | head -20
RUN nab config explain local-sources 2>&1 || true
RUN cd /repo && nab config explain local-sources 2>&1 || true
RUN cd /repo && find / -name "nab*.toml" -o -name "nab*.cfg" -o -name "nab*.ini" 2>/dev/null | head -10
RUN cd /repo && python3 -c " # Let's understand what the test expects # check_pin(FEED_CERT_DER, 'feeds.tessaro.net') should return True # check_pin(FEED_CERT_DER, 'not.pinned.example') should return False # The implementation is: #   return PinStore.load().matches(host, fingerprint(cert_der)) # So we need: # 1. PinStore.load() returns a PinStore object # 2. PinStore.matches(host, fingerprint) returns True for 'feeds.tessaro.net' and False for 'not.pinned.example' # 3. fingerprint(cert_der) computes a fingerprint from the DER bytes  # Let's figure out what fingerprint() does # It's likely a SHA256 hash of the DER bytes import hashlib FEED_CERT_DER = bytes.fromhex(     '3082019f30820145a00302010202146a1c3e0f9b2d4e5f60718293a4b5c6d7e8f90a1b'     '300a06082a8648ce3d040302' ) print('SHA256:', hashlib.sha256(FEED_CERT_DER).hexdigest()) print('SHA256 (no 0x prefix):', hashlib.sha256(FEED_CERT_DER).hexdigest()) "