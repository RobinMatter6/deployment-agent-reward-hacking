import json
from pathlib import Path


def _json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().split("\n") if l.strip()] if path.exists() else []


def _page(run_dir: Path, title: str) -> str:
    traj = _jsonl(run_dir / "trajectory.jsonl")
    grade = _json(run_dir / "grade" / "grade.json")
    out = [f"# {title}"]
    end = next((r for r in traj if r.get("type") == "end"), {})
    out.append(f"Ended: {end.get('end_reason')} after {end.get('steps')} steps.")
    meta = _json(run_dir / "meta.json")
    out.append(f"Probe: {meta.get('probe')}, intervention: {(meta.get('intervention') or {}).get('name')}")
    init = next((r for r in traj if r.get("type") == "init"), None)
    for m in (init or {}).get("messages", []):
        out.append(f"## {m['role']} message\n{m['content']}")

    out.append("## Trajectory")
    for r in traj:
        if r.get("type") == "error":
            out.append(f"**error at step {r.get('step')}:** {r.get('error')}")
        if r.get("type") != "step":
            continue
        msg = r["response"]["choices"][0]["message"]
        out.append(f"### step {r['step']}")
        if msg.get("reasoning"):
            out.append(f"reasoning: {msg['reasoning']}")
        if msg.get("content"):
            out.append(f"text: {msg['content']}")
        if r.get("nudge"):
            out.append(f"(no tool call; harness replied: {r['nudge']})")
        for c in r.get("calls", []):
            out.append(f"{c.get('name')}: {c.get('raw_arguments')}")
            if c.get("error"):
                out.append(f"**{c['error']}**")
            out.append(f"```\n{c.get('output_full', c.get('observation'))}\n```")

    if grade:
        t = grade.get("test_run") or {}
        out.append(f"## Test run\nran: {'yes' if t.get('ran') else 'no'} (exit code {t.get('exit_code')}"
                   f"{', timed out' if t.get('timed_out') else ''}), verdict: {grade.get('verdict')}"
                   f"\n```\n{t.get('output_tail')}\n```")
    return "\n\n".join(out) + "\n"


def render_run(run_dir: Path) -> Path:
    out = run_dir / "view.md"
    out.write_text(_page(run_dir, run_dir.name))
    return out
