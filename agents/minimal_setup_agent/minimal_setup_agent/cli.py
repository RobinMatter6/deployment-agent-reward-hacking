import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import docker

from . import interventions
from .agent import Limits, Trajectory, build_messages, run_episode
from .grader import grade
from .llm import BASE_URL, DEFAULT_MODEL, LLMClient
from .repo import provision
from .sandbox import Sandbox, safe_name
from .viewer import render_run


def cmd_run(a) -> int:
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    name = "minimal_setup_agent_" + safe_name(a.run_id)
    intervention = interventions.get(a.intervention)
    limits = Limits()
    llm = LLMClient(BASE_URL, os.environ.get("OPENAI_API_KEY", ""), a.model)
    messages = build_messages(a.test_command, intervention.first_sentence, intervention.prompt_insert)
    meta = {"run_id": a.run_id, "probe": a.probe, "repo": a.repo, "sha_requested": a.sha,
            "intervention": intervention.meta(), "llm": llm.config(),
            "test_command": a.test_command}

    def save_meta(**fields):
        meta.update(fields)
        (out / "meta.json").write_text(json.dumps(meta, indent=2))

    save_meta()
    work = out / "_work"
    pristine = work / "pristine"
    client = docker.from_env()
    traj = sb = final_image = None
    try:
        save_meta(**provision(a.repo, a.sha, pristine, os.environ.get("GH_TOKEN"), intervention.repo_files))
        traj = Trajectory(out / "trajectory.jsonl")
        sb = Sandbox(name, client=client)
        sb.start(pristine)
        save_meta(episode=run_episode(llm, sb, messages, traj, limits,
                                      intervention.tools, intervention.handlers,
                                      intervention.end_on).__dict__)
        final_image = sb.commit()
        sb.remove()
        save_meta(grade=grade(final_image, name, out / "grade", a.test_command, a.kind),
                  status="completed")
    except Exception as e:
        save_meta(status="harness_error", error=f"{type(e).__name__}: {e}")
        raise
    finally:
        if traj:
            traj.close()
        if sb:
            sb.remove()
        shutil.rmtree(work, ignore_errors=True)
        if final_image:
            try:
                client.images.remove(final_image, force=True)
            except Exception:
                pass
    return 0


def cmd_view(a) -> int:
    for d in a.run_dirs:
        path = render_run(Path(d))
        print(path)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="minimal_setup_agent")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="one episode + grading")
    r.add_argument("--run-id", required=True)
    r.add_argument("--probe", required=True, help="probe name (recorded only)")
    r.add_argument("--kind", choices=["impossible", "control"], help="from the manifest; sets the verdict")
    r.add_argument("--repo", required=True, help="owner/name on GitHub, or a local path")
    r.add_argument("--sha", required=True)
    r.add_argument("--test-command", default="python -m pytest -q")
    r.add_argument("--out", required=True)
    r.add_argument("--intervention", default="none")
    r.add_argument("--model", default=DEFAULT_MODEL)
    r.set_defaults(fn=cmd_run)
    v = sub.add_parser("view", help="render run folders as view.md")
    v.add_argument("run_dirs", nargs="+")
    v.set_defaults(fn=cmd_view)
    a = p.parse_args(argv)
    return a.fn(a)

if __name__ == "__main__":
    sys.exit(main())
