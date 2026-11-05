import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

NEUTRAL_MESSAGE = "initial import"

NEUTRAL_ENV = {
    "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@localhost",
    "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@localhost",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
}


def git(*args, cwd=None, env=None) -> str:
    full_env = {**os.environ, **(env or {})}
    return subprocess.run(["git", *args], cwd=cwd, env=full_env, check=True,
                          capture_output=True, text=True).stdout.strip()


def clone(repo: str, sha: str, dest: Path, token: str | None = None) -> None:
    if Path(repo).exists():
        git("clone", "-q", str(Path(repo).resolve()), str(dest))
    else:
        auth = f"x-access-token:{token}@" if token else ""
        git("clone", "-q", f"https://{auth}github.com/{repo}.git", str(dest))
    git("checkout", "-q", sha, cwd=dest)


def neutralize(src: Path, dest: Path, extra_files: dict[str, Path] | None = None) -> str:
    dest.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "tree.tar"
        git("archive", "--format=tar", "-o", str(archive), "HEAD", cwd=src)
        with tarfile.open(archive) as tar:
            tar.extractall(dest, filter="data")
    for rel, src_file in (extra_files or {}).items():
        shutil.copyfile(src_file, dest / rel)
    git("init", "-q", "-b", "main", cwd=dest)
    git("add", "-A", cwd=dest)
    git("commit", "-q", "--no-gpg-sign", "-m", NEUTRAL_MESSAGE, cwd=dest, env=NEUTRAL_ENV)
    return git("rev-parse", "HEAD", cwd=dest)


def provision(repo: str, sha: str, pristine: Path, token: str | None = None,
              extra_files: dict[str, Path] | None = None) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src"
        clone(repo, sha, src, token)
        neutral = neutralize(src, pristine, extra_files)
    return {"sha_neutral": neutral}
