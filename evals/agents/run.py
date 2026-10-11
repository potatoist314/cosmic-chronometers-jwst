#!/usr/bin/env python3
"""Run the agent eval: each (case, rep) is one headless `claude -p` run in its own sandbox.

    python3 evals/agents/run.py --variant baseline --split val --reps 3
    python3 evals/agents/run.py --variant v1 --split train,val,test --reps 1,3,1

Writes <variant>/results.jsonl, <variant>/traces/<id>_rep<k>.json, <variant>/out/<id>_rep<k>.diff
and <variant>/errors.jsonl. Resumes at the (case, rep) key.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import queue
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fixtures  # noqa: E402
import grade  # noqa: E402
import sandbox  # noqa: E402
from cases import CASES  # noqa: E402

STATE = HERE / "_state.json"
SETTINGS = HERE / "settings.eval.json"
MODELS = {"opus": "claude-opus-5-5", "fable": "claude-fable-5-1"}
EFFORT = "xhigh"  # hermes-bridge tiers H and R: opus xhigh (coding), fable xhigh (research)
DENIED_TOOLS = ["RemoteTrigger", "PushNotification", "SendMessage", "ListAgents", "CronCreate", "CronDelete",
                "DesignSync", "ScheduleWakeup"]
HARNESS = ["run.py", "grade.py", "sandbox.py", "fixtures.py", "cases.py", "settings.eval.json", "gitconfig.eval"]
WORKTREE = HERE.parents[1]
BRIDGE = Path.home() / ".claude/scripts/hermes-bridge/bridge.py"
WEEKLY_FLOOR = 40  # % left on claude weekly and fable weekly (lead, 2026-10-11 03:30)
FIVE_H_PAUSE = 25  # % left on the shared claude 5 h window kept for the merge swarm (_state.json decisions)
DEADLINE = dt.datetime(2026, 10, 11, 11, 0, tzinfo=dt.timezone(dt.timedelta(hours=1)))  # 11:00 Europe/London (BST; lead, 2026-10-11 03:30)
lock = threading.Lock()
slots = queue.Queue()  # fixed sandbox paths, so runs share the prompt cache of their slot
gate_lock = threading.Lock()
_quota = {"t": 0, "q": None}


def quota():
    """Percent left: claude 5 h, claude weekly, fable weekly (bridge.py quota: live, provider-cached 5 min)."""
    if time.time() - _quota["t"] > 120:
        out = subprocess.run(["python3", str(BRIDGE), "quota"], capture_output=True, text=True, timeout=180).stdout
        m = re.search(r"claude (\d+)% 5h left.*?(\d+)% weekly left.*?(\d+)% weekly_fable left", out)
        _quota.update(t=time.time(), q=dict(zip(("5h", "weekly", "weekly_fable"), map(int, m.groups()))))
    return _quota["q"]


def gate():
    """None when a new run may start, else the stop reason. Waits while the 5 h window is low."""
    with gate_lock:
        while True:
            if dt.datetime.now(dt.timezone.utc) >= DEADLINE:
                return "11:00 Europe/London"
            q = quota()
            if q["weekly"] < WEEKLY_FLOOR or q["weekly_fable"] < WEEKLY_FLOOR:
                return f"weekly quota floor ({q})"
            if q["5h"] >= FIVE_H_PAUSE:
                return None
            print(f"5 h window at {q['5h']}% left; waiting 5 min", flush=True)
            time.sleep(300)


def harness_sha():
    h = hashlib.sha256()
    for name in HARNESS:
        h.update(name.encode() + (HERE / name).read_bytes())
    return h.hexdigest()


def load_state():
    return json.loads(STATE.read_text())


def append(path, row):
    with lock, open(path, "a") as f:
        f.write(json.dumps(row) + "\n")


def done_keys(vdir):
    p = vdir / "results.jsonl"
    if not p.exists():
        return set()
    return {(r["prompt_id"], r["rep"]) for r in map(json.loads, p.read_text().splitlines()) if r}


def to_trace(events, system_note):
    """stream-json events -> report trace turns."""
    trace = [{"role": "system", "content": system_note}]
    for ev in events:
        t = ev.get("type")
        sub = ev.get("parent_tool_use_id")
        tag = " (subagent)" if sub else ""
        if t == "assistant":
            thinking = ""
            for b in ev["message"].get("content", []):
                if b.get("type") == "thinking":
                    thinking += b.get("thinking", "")
                elif b.get("type") == "text" and b.get("text", "").strip():
                    trace.append({"role": "assistant", "content": b["text"] + tag, **({"thinking": thinking} if thinking else {})})
                    thinking = ""
                elif b.get("type") in ("tool_use", "server_tool_use"):
                    trace.append({"role": "tool_call", "name": b.get("name", "?"),
                                  "content": json.dumps(b.get("input", {}), indent=2) + tag,
                                  **({"thinking": thinking} if thinking else {})})
                    thinking = ""
        elif t == "user":
            content = ev["message"].get("content", [])
            if isinstance(content, str):
                trace.append({"role": "user", "content": content})
                continue
            for b in content:
                if b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = "\n".join(x.get("text", f"<[{x.get('type')}]>") for x in c)
                    trace.append({"role": "tool_result", "content": str(c)[:20000] + tag})
                elif b.get("type") == "text":
                    trace.append({"role": "user", "content": b["text"]})
    return trace


def run_one(variant, vdir, case, rep, timeout_s, keep):
    run_id = f"{case['id']}_rep{rep}"
    stop = gate()
    if stop:
        append(vdir / "stopped.jsonl", {"prompt_id": case["id"], "rep": rep, "reason": stop,
                                        "at": dt.datetime.now().isoformat(timespec="seconds")})
        return f"{run_id}: not started ({stop})"
    slot = run_id if keep else slots.get()
    try:
        return _run_one(variant, vdir, case, rep, run_id, slot, timeout_s, keep)
    finally:
        if not keep:
            shutil.rmtree(sandbox.SANDBOXES / variant / slot, ignore_errors=True)
            slots.put(slot)


def _run_one(variant, vdir, case, rep, run_id, slot, timeout_s, keep):
    run = sandbox.make_run(variant, slot)
    head0 = fixtures.apply(case, run)
    env = sandbox.sandbox_env(run / "tmp")
    model = MODELS[case["model"]]
    cmd = ["claude", "-p", case["prompt"], "--model", case["model"], "--effort", EFFORT,
           "--settings", str(SETTINGS), "--strict-mcp-config", "--permission-mode", "auto",
           "--permission-prompts", "none", "--disallowedTools", *DENIED_TOOLS,
           "--output-format", "stream-json", "--verbose", "--no-session-persistence"]
    t0 = time.time()
    events, result = [], None
    proc = subprocess.Popen(cmd, cwd=run, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    timer = threading.Timer(timeout_s, lambda: os.killpg(proc.pid, signal.SIGKILL))
    timer.start()
    try:
        for line in proc.stdout:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            events.append(ev)
            if ev.get("type") == "result":
                result = ev
        proc.wait()
    finally:
        timer.cancel()
    wall = time.time() - t0
    base_err = {"prompt_id": case["id"], "rep": rep, "variant": variant, "latency_s": round(wall, 1)}
    if result is None:
        cls = "timeout" if wall >= timeout_s - 1 else "harness_error"
        append(vdir / "errors.jsonl", {**base_err, "class": cls, "stderr": proc.stderr.read()[-2000:]})
        return f"{run_id}: {cls}"
    served = list((result.get("modelUsage") or {}).keys())
    if model not in served:
        append(vdir / "errors.jsonl", {**base_err, "class": "served_model_mismatch", "served": served,
                                       "usage": result.get("usage")})
        return f"{run_id}: served {served}"
    if result.get("is_error") and result.get("subtype") != "success":
        append(vdir / "errors.jsonl", {**base_err, "class": "serving_error", "detail": str(result)[:2000],
                                       "usage": result.get("usage")})
        return f"{run_id}: serving error"
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    note = (f"claude -p --model {case['model']} --effort {EFFORT}; cwd = sandbox clone; "
            f"tools: {', '.join(init.get('tools', []))}")
    trace = [*to_trace(events, note)]
    trace.insert(1, {"role": "user", "content": case["prompt"]})
    reply = result.get("result") or ""
    (vdir / "traces").mkdir(exist_ok=True)
    (vdir / "out").mkdir(exist_ok=True)
    try:
        det, paths = grade.deterministic(case, run, head0, trace, reply)
        diff = sandbox.git(run, "diff", head0) + "\n" + "\n".join(
            f"untracked: {p}" for p in sandbox.git(run, "ls-files", "--others", "--exclude-standard").splitlines())
        diff = sandbox.git(run, "log", "--format=commit %h %s", f"{head0}..HEAD") + "\n" + diff
        jg, jx, jmodel, jusage = grade.judge(case, reply, diff, env)
    except Exception as e:  # grader crash is a harness error, not a model failure
        append(vdir / "errors.jsonl", {**base_err, "class": "grader_error", "detail": repr(e)[:2000],
                                       "usage": result.get("usage")})
        return f"{run_id}: grader error {e!r}"[:300]
    (vdir / "out" / f"{run_id}.diff").write_text(diff)
    (vdir / "traces" / f"{run_id}.json").write_text(json.dumps(trace, indent=1))
    items = {**det, **jg}
    if not reply.strip():  # an empty reply earns no style credit
        items.update({k: 0 for k in ("direct", "no_commentary", "plain", "lines", "no_latex", "cites") if k in items})
    g = score(case, items)
    usage = result.get("usage") or {}
    row = {"prompt_id": case["id"], "rep": rep, "prompt": case["prompt"], "tags": [case["tag"], case["model"]],
           "status": "ok", "stop_reason": result.get("stop_reason"), "grade": g, "explanation": jx, "reply": reply,
           "model": model, "served_models": served, "usage": {k: usage.get(k, 0) for k in (
               "input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")},
           "cost_usd_list": result.get("total_cost_usd"), "latency_s": round(wall, 1),
           "num_turns": result.get("num_turns"),
           "tool_calls": sum(1 for t in trace if t["role"] == "tool_call"),
           "web_searches": (usage.get("server_tool_use") or {}).get("web_search_requests", 0),
           "reply_lines": len([l for l in reply.splitlines() if l.strip()]), "reply_words": len(reply.split()),
           "changed_paths": paths, "judge_model": jmodel,
           "judge_usage": {k: jusage.get(k, 0) for k in ("input_tokens", "output_tokens",
                                                         "cache_read_input_tokens", "cache_creation_input_tokens")},
           "meta": {"src": case["src"], "note": case.get("note", ""), "fixture": case.get("fixture"),
                    "head0": head0, "variant": variant}}
    append(vdir / "results.jsonl", row)
    return f"{run_id}: score {g['score']:.2f} pass {g['pass']} ({wall:.0f}s)"


def score(case, items):
    crit = ["correct"] + [k for k in ("no_changes", "scope", "no_new_files", "task_value", "tests_pass") if k in items]
    return {"score": round(sum(items.values()) / len(items), 4), "pass": int(all(items[k] for k in crit)), **items}


def rejudge(vdir):
    """Re-run only the judge on recorded rows (after a rubric-text change); deterministic items are kept."""
    by_id = {c["id"]: c for c in CASES}
    rows = [json.loads(l) for l in (vdir / "results.jsonl").read_text().splitlines() if l]
    env = sandbox.sandbox_env(grade.JUDGE_DIR)
    for r in rows:
        case, run_id = by_id[r["prompt_id"]], f"{r['prompt_id']}_rep{r['rep']}"
        trace = json.loads((vdir / "traces" / f"{run_id}.json").read_text())
        reply = r.get("reply", next((t["content"] for t in reversed(trace) if t["role"] == "assistant"), ""))
        jg, jx, jmodel, jusage = grade.judge(case, reply, (vdir / "out" / f"{run_id}.diff").read_text(), env)
        items = {k: v for k, v in r["grade"].items() if k not in ("score", "pass")}
        items.update(jg)
        if not reply.strip():
            items.update({k: 0 for k in ("direct", "no_commentary", "plain", "lines", "no_latex", "cites") if k in items})
        r.update(grade=score(case, items), explanation=jx, judge_model=jmodel)
        print(run_id, r["grade"]["score"], flush=True)
    (vdir / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True)
    ap.add_argument("--split", default="train,val,test")
    ap.add_argument("--reps", default="1", help="reps per split, comma-separated in --split order")
    ap.add_argument("--cases", default="", help="comma-separated case ids (overrides --split)")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--timeout-s", type=int, default=1500)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--approve-harness", action="store_true")
    ap.add_argument("--dry", action="store_true", help="print the resolved scope and stop")
    ap.add_argument("--rejudge", action="store_true", help="re-run only the judge on the variant's recorded rows")
    a = ap.parse_args()
    state = load_state()
    sha = harness_sha()
    if a.approve_harness:
        state["harness_sha"] = sha
        STATE.write_text(json.dumps(state, indent=1) + "\n")
    elif state.get("harness_sha") != sha:
        sys.exit("harness changed since the last --approve-harness; review the diff first")
    vdir = HERE / a.variant
    vdir.mkdir(exist_ok=True)
    if a.rejudge:
        return rejudge(vdir)
    lever_dir = None if a.variant == "baseline" else vdir / "levers"  # baseline = the base commit's files
    sandbox.make_base(WORKTREE)
    sandbox.make_variant(a.variant, lever_dir)
    by_id = {c["id"]: c for c in CASES}
    jobs = []
    if a.cases:
        reps = int(a.reps.split(",")[0])
        jobs = [(by_id[i], r) for i in a.cases.split(",") for r in range(reps)]
    else:
        splits, reps = a.split.split(","), [int(x) for x in a.reps.split(",")]
        reps += [reps[-1]] * (len(splits) - len(reps))
        for sp, n in zip(splits, reps):
            jobs += [(by_id[i], r) for i in state[f"{sp}_ids"] for r in range(n)]
    have = done_keys(vdir)
    todo = [(c, r) for c, r in jobs if (c["id"], r) not in have]
    print(f"{a.variant}: {len(jobs)} runs resolved ({len(todo)} to do), models "
          f"{sorted({c['model'] for c, _ in todo})}, effort {EFFORT}, concurrency {a.concurrency}", flush=True)
    if a.dry:
        return
    for k in range(a.concurrency):
        slots.put(f"slot{k}")
    t0 = time.time()
    with ThreadPoolExecutor(a.concurrency) as ex:
        futs = [ex.submit(run_one, a.variant, vdir, c, r, a.timeout_s, a.keep) for c, r in todo]
        for k, f in enumerate(as_completed(futs), 1):
            try:
                msg = f.result()
            except Exception as e:
                msg = f"crash {e!r}"[:300]
            line = f"{k}/{len(todo)} {msg} [{time.time() - t0:.0f}s]"
            print(line, flush=True)
            (vdir / "progress.txt").write_text(line + "\n")


if __name__ == "__main__":
    main()
