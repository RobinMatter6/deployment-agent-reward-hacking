import json
import time
from dataclasses import dataclass
from pathlib import Path

from .llm import LLMClient, LLMError
from .sandbox import Sandbox, truncate

PROMPTS = Path(__file__).resolve().parent / "prompts"

BASH_DESCRIPTION = "Run a shell command in /repo. Each call starts a fresh shell."
FINISH_DESCRIPTION = "End the task and report the result."
EXPLANATION_DESCRIPTION = "Explanation of what you did."
NUDGE = "Please continue using the tools, or call finish when you're done."
PARSE_ERROR = "Error: could not parse tool call ({reason})."
FINISH_ACK = "Task ended."
ARGUMENT = {"bash": "command", "finish": "explanation"}

TOOLS = [
    {"type": "function", "function": {
        "name": "bash", "description": BASH_DESCRIPTION,
        "parameters": {"type": "object", "properties": {"command": {"type": "string"}},
                       "required": ["command"]}}},
    {"type": "function", "function": {
        "name": "finish", "description": FINISH_DESCRIPTION,
        "parameters": {"type": "object",
                       "properties": {"explanation": {"type": "string",
                                                      "description": EXPLANATION_DESCRIPTION}},
                       "required": ["explanation"]}}},
]


@dataclass
class Limits:
    max_steps: int = 60
    time_s: float = 45 * 60
    cmd_timeout_s: int = 300
    obs_chars: int = 8000
    streak_cap: int = 3


@dataclass
class Episode:
    end_reason: str = "limit_steps"
    steps: int = 0
    explanation: str | None = None


def build_messages(test_command: str, first_sentence: str | None = None,
                   insert: str | None = None) -> list[dict]:
    system = (PROMPTS / "system.txt").read_text().rstrip("\n")
    if first_sentence:
        _, rest = system.split("\n\n", 1)
        system = first_sentence + "\n\n" + rest
    if insert:
        body, last = system.rsplit("\n\n", 1)
        system = body + "\n\n" + insert + "\n\n" + last
    user = (PROMPTS / "user.txt").read_text().rstrip("\n").replace("{test_command}", test_command)
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


class Trajectory:

    def __init__(self, path: Path):
        self.f = open(path, "w", encoding="utf-8")

    def write(self, record: dict) -> None:
        self.f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        self.f.flush()

    def close(self) -> None:
        self.f.close()


def parse_call(name: str | None, raw: str | None) -> tuple[str | None, str | None]:
    if name not in ARGUMENT:
        return None, f"unknown tool {name!r}"
    try:
        value = json.loads(raw or "{}").get(ARGUMENT[name])
    except (ValueError, AttributeError):
        value = None
    if not isinstance(value, str):
        return None, f"{name} needs a text '{ARGUMENT[name]}'"
    return value, None


def parse_extra(tool: dict, raw: str | None) -> tuple[dict | None, str | None]:
    params = tool["function"]["parameters"]
    try:
        args = json.loads(raw or "{}")
    except ValueError:
        args = None
    if (not isinstance(args, dict) or set(args) != set(params["required"])
            or not all(isinstance(v, str) for v in args.values())):
        return None, f"{tool['function']['name']} needs the text arguments " + ", ".join(params["required"])
    return args, None


def _bash(command: str, sandbox: Sandbox, limits: Limits) -> tuple[str, dict]:
    res = sandbox.exec(command, limits.cmd_timeout_s)
    head = (f"[exit {res['exit_code']}, timed out after {limits.cmd_timeout_s}s]" if res["timed_out"]
            else f"[exit {res['exit_code']}]")
    shown = head + "\n" + truncate(res["output"], limits.obs_chars)
    return shown, {"exit_code": res["exit_code"], "timed_out": res["timed_out"],
                   "duration_s": res["duration_s"], "output_full": res["output"]}


def _assistant_entry(msg: dict) -> dict:
    entry = {"role": "assistant", "content": msg.get("content") or ""}
    if msg.get("reasoning"):
        entry["reasoning"] = msg["reasoning"]
    if msg.get("tool_calls"):
        entry["tool_calls"] = msg["tool_calls"]
    return entry


def _execute_call(tc: dict, extra_by_name: dict, handlers: dict, sandbox: Sandbox,
                  limits: Limits) -> tuple[dict, str | None]:
    fn = tc.get("function") or {}
    name = fn.get("name")
    call = {"id": tc.get("id"), "name": name, "raw_arguments": fn.get("arguments")}
    explanation = None
    if name in extra_by_name:
        args, error = parse_extra(extra_by_name[name], fn.get("arguments"))
    else:
        value, error = parse_call(name, fn.get("arguments"))
    if error:
        call["error"] = error
        shown = PARSE_ERROR.format(reason=error)
    elif name in extra_by_name:
        shown = handlers[name](args)
    elif name == "bash":
        shown, extra = _bash(value, sandbox, limits)
        call.update(extra)
    else:
        explanation = value
        shown = FINISH_ACK
    call["observation"] = shown
    return call, explanation


def _accepted_end(call: dict, end_on: dict) -> str | None:
    name = call["name"]
    if name in end_on and "error" not in call and end_on[name](call["observation"]):
        return name
    return None


def run_episode(llm: LLMClient, sandbox: Sandbox, messages: list[dict], traj: Trajectory,
                limits: Limits, extra_tools: tuple = (), handlers: dict | None = None,
                end_on: dict | None = None) -> Episode:
    ep = Episode()
    tools = TOOLS + list(extra_tools)
    extra_by_name = {t["function"]["name"]: t for t in extra_tools}
    handlers = handlers or {}
    end_on = end_on or {}
    traj.write({"type": "init", "messages": messages, "tools": tools})
    t0 = time.time()
    no_tool_streak = 0
    ended_by = None

    for step in range(1, limits.max_steps + 1):
        if time.time() - t0 > limits.time_s:
            ep.end_reason = "limit_time"
            break
        try:
            raw = llm.chat(messages, tools)
        except LLMError as e:
            traj.write({"type": "error", "step": step, "error": str(e)})
            ep.end_reason = "error"
            break
        ep.steps = step
        msg = raw["choices"][0]["message"]
        tool_calls = msg.get("tool_calls") or []
        messages.append(_assistant_entry(msg))
        record = {"type": "step", "step": step, "response": raw, "calls": []}

        if not tool_calls:
            no_tool_streak += 1
            messages.append({"role": "user", "content": NUDGE})
            record["nudge"] = NUDGE
            traj.write(record)
            if no_tool_streak >= limits.streak_cap:
                ep.end_reason = "no_tool_call"
                break
            continue
        no_tool_streak = 0

        for tc in tool_calls:
            call, explanation = _execute_call(tc, extra_by_name, handlers, sandbox, limits)
            if ep.explanation is None:
                ep.explanation = explanation
            ended_by = ended_by or _accepted_end(call, end_on)
            messages.append({"role": "tool", "tool_call_id": tc.get("id"), "content": call["observation"]})
            record["calls"].append(call)
        traj.write(record)

        if ep.explanation is not None:
            ep.end_reason = "finished"
            break
        if ended_by:
            ep.end_reason = "ended_by_" + ended_by
            break

    traj.write({"type": "end", **ep.__dict__})
    return ep
