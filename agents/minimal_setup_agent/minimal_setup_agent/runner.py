import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

from .llm import DEFAULT_MODEL

PKG_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = PKG_ROOT.parent.parent / "probes" / "MANIFEST.yaml"
RUN_TIMEOUT_S = 45 * 60 + 30 * 60


def run_one(run_id: str, probe: str, intervention: str, out_dir: Path, model: str, manifest: dict) -> dict:
    p = manifest[probe]
    run_dir = out_dir / run_id
    meta_path = run_dir / "meta.json"
    if meta_path.exists() and json.loads(meta_path.read_text()).get("status") == "completed":
        return {"run_id": run_id, "skipped": True}
    run_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "minimal_setup_agent", "run", "--run-id", run_id, "--probe", probe,
           "--kind", p["kind"], "--repo", p["repo"], "--sha", p["sha"],
           "--test-command", p.get("test_command") or "python -m pytest -q",
           "--out", str(run_dir), "--intervention", intervention, "--model", model]
    try:
        with open(run_dir / "stdout.log", "w") as f:
            subprocess.run(cmd, cwd=PKG_ROOT, stdout=f, stderr=subprocess.STDOUT, timeout=RUN_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        pass
    status = json.loads(meta_path.read_text()).get("status") if meta_path.exists() else None
    return {"run_id": run_id, "status": status}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="minimal_setup_agent.runner")
    p.add_argument("--probes", required=True)
    p.add_argument("--interventions", default="none")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--parallel", type=int, default=3)
    p.add_argument("--model", default=DEFAULT_MODEL)
    a = p.parse_args(argv)
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set")
    manifest = yaml.safe_load(MANIFEST.read_text())["probes"]
    probes, interventions = a.probes.split(","), a.interventions.split(",")
    unknown = [x for x in probes if x not in manifest]
    if unknown:
        raise SystemExit(f"unknown probes: {unknown}")
    out_dir = Path(a.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [(f"{pr}_{iv}_{rep}", pr, iv)
            for rep in range(1, a.n + 1) for pr in probes for iv in interventions]
    with ThreadPoolExecutor(max_workers=a.parallel) as pool:
        futures = [pool.submit(run_one, rid, pr, iv, out_dir, a.model, manifest) for rid, pr, iv in rows]
        for fut in as_completed(futures):
            print(json.dumps(fut.result()), flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
