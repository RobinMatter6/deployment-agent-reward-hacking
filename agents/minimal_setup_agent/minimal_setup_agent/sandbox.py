import io
import re
import tarfile
import time
from pathlib import Path

import docker

IMAGE = "python@sha256:4379c343a93c87429e0ac3e8e09d073a4ee26084d710ac38b686fa34eed12270"
CPUS = 2
MEMORY = "4g"
TIMEOUT_EXIT = 124


def safe_name(s: str) -> str:
    return re.sub(r"[^a-z0-9_.-]", "-", s.lower())


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    head = limit // 4
    tail = limit - head
    omitted = len(text) - limit
    return f"{text[:head]}\n... [{omitted} characters omitted] ...\n{text[-tail:]}"


def tar_dir(src: Path, arcname: str) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        tar.add(str(src), arcname=arcname)
    return buf.getvalue()


class Sandbox:
    def __init__(self, name: str, image: str = IMAGE, offline: bool = False,
                 client: docker.DockerClient | None = None):
        self.client = client or docker.from_env()
        self.name = safe_name(name)
        self.image = image
        self.offline = offline
        self.container = None

    def start(self, repo_dir: Path | None = None) -> None:
        kwargs = {"network_mode": "none"} if self.offline else {}
        self.container = self.client.containers.run(
            self.image, ["sleep", "infinity"], name=self.name, detach=True, working_dir="/",
            nano_cpus=int(CPUS * 1e9), mem_limit=MEMORY,
            init=True,
            labels={"minimal_setup_agent": "1"}, **kwargs)
        if repo_dir is not None:
            self.container.put_archive("/", tar_dir(repo_dir, "repo"))

            self.container.exec_run(["chown", "-R", "root:root", "/repo"])

    def exec(self, command: str, timeout: int) -> dict:
        t0 = time.time()
        exit_code, output = self.container.exec_run(
            ["timeout", "-k", "5", str(timeout), "bash", "-c", command],
            workdir="/repo", stdin=False, demux=False)
        duration = time.time() - t0
        return {
            "exit_code": exit_code,
            "output": (output or b"").decode("utf-8", errors="replace"),
            "timed_out": exit_code in (TIMEOUT_EXIT, 137) and duration >= timeout,
            "duration_s": round(duration, 2),
        }

    def commit(self, repository: str = "minimal_setup_agent_final") -> str:
        self.container.commit(repository=repository, tag=self.name)
        return f"{repository}:{self.name}"

    def remove(self) -> None:
        if self.container is not None:
            self.container.remove(force=True)
            self.container = None
