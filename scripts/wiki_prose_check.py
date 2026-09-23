#!/usr/bin/env python3
"""Opus check of agent-written wiki prose; the repo's git pre-commit hook runs it.

It collects the prose that a commit adds or changes under wiki/notes and
wiki/research: paragraphs, figure captions, and the roadmap and direction
entries of direction.md. Code, tables, headings, JSON records and Liu Hao's
own words stay out. A direction.md entry counts only when an agent saved it
through `sync_wiki_direction.py --save`, which marks the save `"by": "agent"`;
a save from the browser editor has no mark and is his. The slop lint runs
first, and its hits go to Opus as hints. Opus returns pass, or fail with each
offending sentence and a shorter rewrite; a fail refuses the commit.

    python3 scripts/wiki_prose_check.py              # staged changes (the hook)
    python3 scripts/wiki_prose_check.py --commit REV # one commit; every entry counts
    SKIP_PROSE_CHECK=1 git commit ...                # Liu Hao: skip it for one commit
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "wiki"))
import build
import research

_spec = importlib.util.spec_from_file_location(
    "slop_lint", Path.home() / ".claude/scripts/hermes-bridge/slop_lint.py")
slop_lint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(slop_lint)

# A fixed sample of Liu Hao's original words, from the "text" fields of
# wiki/research/direction.md (Amendments) and q-dust-index-railing.md.
STYLE_SAMPLE = [
    "research priority to add - look into why conroy dust index is railing and UV is so weak - 9/10 priority",
    "The 100 angstrom note -> we want frequency modes not shorter than 100 angstrom in the polynomial, is what was meant.",
    "well, give z a plus minus 0.1 wiggle and dont even make these opt in switches - just have this as default and note it appropriately",
    "another priority - 8/10 -> do plots of something like alpha/fe versus stellar mass, and t50 versus stellar mass . the physical justification is that you can constrain a relative trend given only a corner plot distribution if you can plot against some x axis",
    "okay, add this to one of the research priorities on the wiki, priority of 9, to either model, mask, or ignore emission lines, but with a physically justified reason.",
    "i want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectoy.",
]

RUBRIC = """You check prose that coding agents wrote for an astronomy research wiki. The reader is Liu Hao, the research supervisor. He wants text that is easy to read and concise, with no unnecessary words.

The target style is his own writing, below: direct and plain. Match its directness and plainness, with clean spelling and capitalisation; do not copy his typos or lowercase typing.

{sample}

Shorthand, fragments, arrows and numbers such as "9/10" are fine. Do not ask for full sentences. Do not flag shorthand.

Flag a sentence only for one of these:
- unnecessary words or padding
- a point that repeats an earlier point
- AI prose: hedging, filler, grand summaries, "not X but Y" turns, rule-of-three lists, em-dash chains
- Claudisms: "Note that", "It's worth noting", "Here is", "In summary", "crucial", "robust", "comprehensive", "leverage", "delve" and similar
- jargon left undefined where this reader would stop. He knows astronomy, stellar populations and Ceridwen fits; define only what he would not know.

Ignore words in quotation marks that a named person said or wrote, file paths, code names, numbers and units.
Each rewrite keeps the meaning and facts and is shorter than the original sentence, never longer.
Pass when nothing needs to be flagged. Do not flag a sentence for small matters of taste."""

SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "faults": {"type": "array", "items": {
            "type": "object",
            "properties": {"unit": {"type": "integer"}, "sentence": {"type": "string"},
                           "problem": {"type": "string"}, "rewrite": {"type": "string"}},
            "required": ["unit", "sentence", "problem", "rewrite"]}},
    },
    "required": ["verdict", "faults"],
}


def checked(path: str) -> bool:
    """The pages the publish-time length check covers."""
    parts = Path(path).parts
    if len(parts) < 3 or parts[0] != "wiki" or not path.endswith(".md"):
        return False
    if parts[1] == "notes":
        return len(parts) == 3
    return parts[1] == "research" and parts[-1] != "README.md" and not set(parts) & set(build.LENGTH_SKIP[1:])


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def version(spec: str) -> str:
    result = subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""


def entries(text: str, path: str) -> list:
    """(label, prose) of every roadmap or direction entry and figure caption."""
    if not text or Path(path).parts[1] != "research":
        return []
    sections = research.parse_text(text, ROOT / path)["sections"]
    found = []
    for task in sections.get("Roadmap", []):
        found.append((task["id"], (task.get("title", "") + ". " + task.get("details", "")).strip(". ")))
    for row in sections.get("Your words", []) if path.endswith("direction.md") else []:
        if "id" in row:
            found.append((row["id"], (row.get("title", "") + ". " + row.get("text", "")).strip(". ")))
    for figure in sections.get("Figures", []):
        found.append(("caption", figure.get("caption", "")))
    return found


def agent_saved(text: str, path: str) -> set:
    """Entry ids whose latest direction.md save an agent made."""
    if not path.endswith("direction.md"):
        return set()
    latest = {}
    for row in research.parse_text(text, ROOT / path)["sections"].get("Amendments", []):
        if "target" in row:
            latest[row["target"]] = row.get("request", {}).get("by") == "agent"
    return {target for target, agent in latest.items() if agent}


def units(old: str, new: str, path: str, every_entry: bool) -> list:
    """(where, prose) the new text adds or changes."""
    before = {" ".join(p.split()) for _, p in build.paragraphs(old)}
    found = [("%s:%d" % (path, n), p) for n, p in build.paragraphs(new)
             if " ".join(p.split()) not in before]
    saved_before = set(entries(old, path))
    saved = agent_saved(new, path)
    for label, prose in entries(new, path):
        if (label, prose) not in saved_before and (every_entry or not path.endswith("direction.md") or label in saved):
            found.append(("%s:%s" % (path, label), prose))
    return [(where, prose) for where, prose in dict.fromkeys(found)
            if slop_lint.prose_words(prose, free_table=False) >= 4]


def collect(commit: str | None) -> list:
    if commit:
        paths = filter(checked, git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines())
        pairs = [(version("%s^:%s" % (commit, p)), version("%s:%s" % (commit, p)), p) for p in paths]
    else:
        paths = filter(checked, git("diff", "--cached", "--name-only", "--diff-filter=AM").splitlines())
        pairs = [(version("HEAD:" + p), version(":" + p), p) for p in paths]
    found = []
    for old, new, path in pairs:
        if new:
            found += units(old, new, path, every_entry=bool(commit))
    return found


def ask_opus(found: list) -> dict:
    blocks = []
    for number, (where, prose) in enumerate(found, 1):
        hits = slop_lint.mannerisms(prose, free_table=False)
        hint = ("\n(lint hits: %s)" % ", ".join(p for _, p in hits)) if hits else ""
        blocks.append("[%d] %s\n%s%s" % (number, where, prose, hint))
    sample = "\n".join("- " + line for line in STYLE_SAMPLE)
    command = ["claude", "-p", "--model", "opus", "--output-format", "json",
               "--system-prompt", RUBRIC.format(sample=sample), "--json-schema", json.dumps(SCHEMA),
               "--tools", "", "--strict-mcp-config", "--setting-sources", "project",
               "--no-session-persistence"]
    started = time.time()
    result = subprocess.run(command, input="\n\n".join(blocks), capture_output=True, text=True, cwd=ROOT)
    if result.returncode:
        raise SystemExit("prose check: claude -p failed: " + (result.stderr or result.stdout).strip())
    reply = json.loads(result.stdout)
    verdict = reply.get("structured_output") or json.loads(reply["result"])
    verdict["cost_usd"] = reply.get("total_cost_usd", 0.0)
    verdict["seconds"] = time.time() - started
    return verdict


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--commit", help="check one commit instead of the staged changes")
    args = parser.parse_args(argv)
    if os.environ.get("SKIP_PROSE_CHECK") == "1":
        print("prose check: skipped (SKIP_PROSE_CHECK=1)", file=sys.stderr)
        return 0
    found = collect(args.commit)
    if not found:
        return 0
    verdict = ask_opus(found)
    faults = verdict["faults"] if verdict["verdict"] == "fail" else []
    words = slop_lint.WORD_RE.findall
    print("prose check: %s, %d unit(s), %.0f s, $%.4f API-equivalent"
          % ("FAIL" if faults else "pass", len(found), verdict["seconds"], verdict["cost_usd"]), file=sys.stderr)
    for fault in faults:
        where = found[fault["unit"] - 1][0] if 0 < fault["unit"] <= len(found) else "?"
        rewrite = fault["rewrite"].strip() or "(delete)"
        if len(words(rewrite)) >= len(words(fault["sentence"])):
            rewrite = "(cut words)"
        print("\n%s: %s\n  was:     %s\n  rewrite: %s" % (where, fault["problem"], fault["sentence"], rewrite),
              file=sys.stderr)
    if faults:
        print("\nFix the text and commit again. Liu Hao only: SKIP_PROSE_CHECK=1 git commit ...", file=sys.stderr)
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
