#!/usr/bin/env python3
"""Print the current Ceridwen fit state: ceridwen_state.py [TERM] [--days 14].

For each SETTINGS and PRIORS entry of the production notebook and each model option of
the Ceridwen classes: the value, what it does, its state, the commit that built it, the
research records that tested it with their findings, and the open question. Then the
unmerged branches, the open issues, and the experiments and run directories that are
planned, running or recent. TERM keeps only the entries that contain it.

Reads the committed HEAD, the pinned submodules, the research records, results/ and
bd. It rents nothing.
"""
import argparse
import ast
import functools
import json
import subprocess
import sys
import warnings
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "wiki"))
import fit_settings  # noqa: E402
import research  # noqa: E402

NOTEBOOK = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
CERIDWEN = ROOT / "ceridwen"
SEDPY = ROOT / "external/sedpy_jax"
FINISHED = {"results-ready", "reviewed", "recorded"}


@functools.lru_cache(maxsize=None)
def git(*args, repo=ROOT):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def pinned(submodule):
    return git("ls-tree", "HEAD", str(submodule.relative_to(ROOT))).split()[2]


def cells_at(rev):
    """The source of each notebook cell at one commit; a markdown cell is ''."""
    return ["".join(c["source"]) if c["cell_type"] == "code" else ""
            for c in json.loads(git("show", "%s:%s" % (rev, NOTEBOOK)))["cells"]]


def entries_at(cells):
    """{key: (dict name, value, comment)} of SETTINGS and PRIORS; {} before the notebook had them as literals."""
    top = next((s for s in cells if "SETTINGS = {" in s), None)
    return {key: (name, ast.unparse(node), note) for key, (name, node, note) in fit_settings.parse(top).items()} if top else {}


def history():
    """({key: [commit line for each change of its value or comment]}, {removed key: commit line}, first commit line
    with SETTINGS and PRIORS literals), oldest first."""
    changes, removed, last, first = {}, {}, {}, ""
    for row in git("log", "--reverse", "--format=%h %ad %s", "--date=short", "--", NOTEBOOK).splitlines():
        now = entries_at(cells_at(row.split()[0]))
        if not now:
            continue
        for key in now:
            if last.get(key, (0, 0, 0))[1:] != now[key][1:]:
                changes.setdefault(key, []).append(row)
        removed.update({key: row for key in last if key not in now})
        last, first = now, first or row
    return changes, removed, first


def ceridwen_commits(row, seen):
    """The Ceridwen commits that one project commit pinned, and the later commits to the files they created."""
    commit = row.split()[0]
    before, after = (git("ls-tree", rev, "ceridwen").split()[2:3] for rev in (commit + "^", commit))
    if not (before and after) or before == after:  # the oldest commits have no ceridwen submodule
        return []
    rows = git("log", "--format=%h %ad %s", "--date=short", "-3", "%s..%s" % (before[0], after[0]), repo=CERIDWEN).splitlines()
    created = [f for r in rows for f in git("show", "--diff-filter=A", "--name-only", "--format=", r.split()[0], repo=CERIDWEN).splitlines()
               if f.startswith("ceridwen/")]
    if created:
        rows += git("log", "--reverse", "--format=%h %ad %s", "--date=short", "%s..%s" % (after[0], pinned(CERIDWEN)),
                    "--", *created, repo=CERIDWEN).splitlines()
    lines = []
    for r in rows:
        if r not in seen:
            seen.add(r)
            files = git("show", "--name-only", "--format=", r.split()[0], repo=CERIDWEN).splitlines()
            lines.append("code: ceridwen %s (%s)" % (r, ", ".join(files[:3])))
    return lines


def options(path, name):
    """({option: default} of one Ceridwen class, first paragraph of its module docstring) at the pinned commit."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(git("show", "%s:%s" % (pinned(CERIDWEN), path), repo=CERIDWEN))
    init = next(f for c in tree.body if isinstance(c, ast.ClassDef) and c.name == name
                for f in c.body if isinstance(f, ast.FunctionDef) and f.name == "__init__")
    return ({a.arg: ast.unparse(d) for a, d in zip(init.args.args[-len(init.args.defaults):], init.args.defaults)},
            " ".join(ast.get_docstring(tree).split("\n\n")[0].split()))


def overrides(config):
    """{key: ["arm=value", ...]} of one experiment.json; a shared change names every arm."""
    found = {}
    arms = config.get("arms", {})
    for arm, changes in [("+".join(arms), config), *arms.items()]:
        for field in ("settings", "priors"):
            for key, value in changes.get(field, {}).items():
                found.setdefault(key, []).append("%s=%s" % (arm, json.dumps(value)))
    return found


def usd(directory):
    """'  $x invoiced' from the charges.json files that experiment.py saved below one result directory."""
    files = list(directory.rglob("charges.json"))
    return "  $%.2f invoiced" % sum(float(row["amount"]) for path in files
                                     for row in json.loads(path.read_text())) if files else ""


def run_lines(directory):
    """One line for each experiment.py run directory below a result directory."""
    lines = []
    for path in sorted(directory.glob("*/manifest.json")):
        manifest = json.loads(path.read_text())
        cells = [cell["name"] for cell in manifest.get("source", {}).get("experiment", [])]  # benchmark manifests have none
        if not cells:
            continue
        done = manifest.get("completed_cells", [])
        written = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        lines.append("%s  %d/%d fits complete, last attempt %s, manifest written %s" % (
            path.parent.relative_to(ROOT), len(done), len(cells), manifest["attempts"][-1]["status"], written))
    return lines


def branches(repo, base, label):
    """One entry for each worktree with changes that are not committed and each branch that the base does not have."""
    seen, entries = set(), []
    for path in git("worktree", "list", "--porcelain", repo=repo).split("worktree ")[1:]:
        path = git("rev-parse", "--show-toplevel", repo=path.splitlines()[0])
        files = [line.split(maxsplit=1)[1] for line in git("status", "--porcelain", "--untracked-files=no", repo=path).splitlines()]
        if files and Path(path) != ROOT:
            entries.append(["%s worktree %s  %s  %d files changed, not committed" % (
                label, path, git("rev-parse", "--abbrev-ref", "HEAD", repo=path), len(files)), "    files: " + ", ".join(files[:4])])
    rows = git("for-each-ref", "--no-merged", base, "--sort=-committerdate",
               "--format=%(objectname:short)|%(committerdate:short)|%(refname:short)|%(subject)",
               "refs/heads", "refs/remotes", repo=repo).splitlines()
    for commit, day, name, subject in (row.split("|", 3) for row in rows):
        if commit not in seen and not name.endswith("gh-pages"):
            seen.add(commit)
            ahead = git("rev-list", "--count", "%s..%s" % (base, commit), repo=repo)
            files = git("diff", "--name-only", "%s...%s" % (base, commit), repo=repo).splitlines()
            entries.append(["%s branch %s  %s  %s  %s commits not in %s" % (label, name, day, commit, ahead, base[:7]),
                            "    last: " + subject, "    files: " + ", ".join(files[:4]) + (", ..." if len(files) > 4 else "")])
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("term", nargs="?", default="", help="print only the entries that contain this text")
    parser.add_argument("--days", type=int, default=14, help="how far back a result counts as recent")
    args = parser.parse_args()
    since = (date.today() - timedelta(days=args.days)).isoformat()
    cells = cells_at("HEAD")
    entries = entries_at(cells)
    call = next(n for s in cells if "CSPBasis_afe(" in s for n in ast.walk(ast.parse(s))
                if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "CSPBasis_afe")
    passed = {k.arg: ast.unparse(k.value) for k in call.keywords if k.arg != "theta"}
    changes, removed, first = history()
    records, faults = research.load(ROOT / "wiki/research")
    experiments = [r for r in records if r["kind"] == "experiment"]
    questions = {r["id"]: r for r in records if r["kind"] == "question"}
    configs = {path.parent: json.loads(path.read_text()) for path in sorted((ROOT / "results").glob("*/experiment.json"))}
    grouped = {ROOT / group: r for r in experiments for group in research.refs(r, "result_groups")}
    ran = {}  # key -> {record id or result directory: values an experiment.json ran}
    for directory, config in configs.items():
        owner = grouped[directory]["id"] if directory in grouped else str(directory.relative_to(ROOT))
        for key, values in overrides(config).items():
            ran.setdefault(key, {}).setdefault(owner, []).extend(values)
    named = {}  # feature -> records that list it in `features`
    for r in experiments:
        for feature in research.refs(r, "features"):
            named.setdefault(feature, []).append(r)

    def evidence(feature):
        """(state words, lines) from the records and the experiment.json files of one feature."""
        linked = named.pop(feature, [])
        states = {r["status"] for r in linked}
        words = (["tested"] if states & FINISHED else []) + (["in progress"] if states & {"planned", "running"} else []) \
            + (["stopped"] if "stopped" in states else [])
        lines = ["%s: %s [%s %s] %s" % ("tested" if r["status"] in FINISHED else r["status"], r["id"], r["status"],
                                        (r.get("results_at") or r["date"])[:10],
                                        r.get("finding", "")) for r in linked]
        lines += ["ran: %s %s" % (owner, ", ".join(values)) for owner, values in ran.pop(feature, {}).items()]
        asked = dict.fromkeys(q for r in linked for q in [r["question"], *research.refs(r, "related_questions")])
        lines += ["open: %s %s" % (q, questions[q]["title"]) for q in asked if questions[q]["status"] != "answered"]
        return words, lines

    blocks = []  # (heading, [entry]); an entry is a list of lines
    for name in ("SETTINGS", "PRIORS"):
        block = []
        for key, (source, value, note) in entries.items():
            if source == name:
                rows, seen, code = changes[key], set(), []
                for i, row in enumerate(rows):
                    code += ["%s: %s%s" % ("changed" if i else "built", row, "  (first commit with SETTINGS and PRIORS literals;"
                                           " the entry can be older)" if row == first else ""), *ceridwen_commits(row, seen)]
                used = [str(i) for i, s in enumerate(cells) if '["%s"]' % key in s]
                words, lines = evidence(key)
                state = ["off" if value in ("False", "None") else "production default",
                         "built %s%s" % ("by " if rows[0] == first else "", rows[0].split()[1]), *words]
                block.append(["%s = %s  [%s]" % (key, value, "; ".join(state))] + ["    " + line for line in [
                    note and "what: " + note, used and "used: notebook cells " + ", ".join(used), *code, *lines] if line])
        blocks.append(("%s  %s at HEAD %s" % (name, NOTEBOOK, git("rev-parse", "--short", "HEAD")), block))

    (afe, about), (base, _) = options("ceridwen/csp/csp_afe.py", "CSPBasis_afe"), options("ceridwen/csp/csp.py", "CSPBasis")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        laws = next(n.value for n in ast.parse(git("show", pinned(SEDPY) + ":sedpy_jax/attenuation_dust.py", repo=SEDPY)).body
                    if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "ATTENUATION_LAWS")
    block = []
    for key in [*afe, *(k for k in base if k not in afe)]:
        words, lines = evidence(key)
        if key not in afe:
            head = "%s  [not in CSPBasis_afe; CSPBasis has it, default %s]" % (key, base[key])
            lines.insert(0, "where: ceridwen/csp/csp.py, class CSPBasis. The fit uses ceridwen/csp/csp_afe.py: \"%s\"" % about)
        elif key in passed:
            head = "%s = %s  [%s]" % (key, passed[key], "; ".join(["set in the notebook call", *words]))
        else:
            head = "%s = %s  [%s]" % (key, afe[key], "; ".join(["class default", *words]))
        if key == "diffuse_law":
            lines.insert(0, "registered laws: " + ", ".join(k.value for k in laws.keys))
        block.append([head] + ["    " + line for line in lines])
    checked = git("rev-parse", "HEAD", repo=CERIDWEN)
    blocks.append(("MODEL OPTIONS  CSPBasis_afe and CSPBasis at pinned ceridwen %s%s" % (
        pinned(CERIDWEN)[:7], "" if checked == pinned(CERIDWEN) else "; the checked-out ceridwen is " + checked[:7]), block))

    block = []
    for feature in list(named):
        words, lines = evidence(feature)
        if feature in removed:
            lines.insert(0, "removed from the notebook: " + removed[feature])
        block.append(["%s  [%s]" % (feature, "; ".join(words))] + ["    " + line for line in lines])
    blocks.append(("FEATURES THAT ARE NOT A CURRENT NOTEBOOK KEY OR CLASS OPTION", block))

    blocks.append(("WORK THAT IS NOT MERGED", branches(ROOT, "HEAD", "project") + branches(CERIDWEN, pinned(CERIDWEN), "ceridwen")))
    issues = json.loads(subprocess.run(["bd", "list", "--status", "open,in_progress", "--json"], cwd=ROOT,
                                       capture_output=True, text=True, check=True).stdout)
    blocks.append(("OPEN ISSUES  bd show <id>", [["%s  %s  %s  %s" % (i["id"], i["status"], i["created_at"][:10], i["title"]),
                                                   "    " + " ".join(i.get("description", "").split())[:300]] for i in issues]))

    block = []
    recent = [r for r in experiments if args.term or r["status"] in ("planned", "running")
              or (r.get("results_at") or r["date"])[:10] >= since]
    for r in sorted(recent, key=lambda r: r.get("results_at") or r["date"], reverse=True):
        entry = ["%s  %s  %s  %s" % (r["id"], r["status"], (r.get("results_at") or r["date"])[:10], r["question"]),
                 "    " + r["title"]]
        arms = {}
        for run in r["sections"]["Runs"]:
            arms.setdefault(run["arm"], []).append(run["status"])
        if arms:
            entry.append("    arms: " + "; ".join("%s %s" % (arm, ", ".join(
                "%d %s" % (states.count(s), s) for s in dict.fromkeys(states))) for arm, states in arms.items()))
        if r.get("features"):
            entry.append("    features: %s. finding: %s" % (r["features"], r.get("finding", "")))
        entry += ["    %s%s" % (group, usd(ROOT / group)) for group in research.refs(r, "result_groups")]
        block.append(entry)
    blocks.append(("EXPERIMENT RECORDS  " + ("all" if args.term else "planned, running, or results since %s" % since), block))

    blocks.append(("RUN DIRECTORIES IN NO RECORD", [
        ["%s%s" % (directory.relative_to(ROOT), usd(directory))] + ["    " + line for line in run_lines(directory)]
        + ["    %s: %s" % (key, ", ".join(values)) for key, values in overrides(config).items()]
        for directory, config in configs.items() if directory not in grouped and run_lines(directory)]))

    for heading, block in blocks:
        block = [entry for entry in block if args.term.lower() in "\n".join(entry).lower()]
        if block:
            print(heading)
            print("\n".join(line for entry in block for line in entry))
            print()
    if args.term:
        for label, repo, scope in (("project", ROOT, "HEAD"), ("ceridwen", CERIDWEN, "--all")):
            rows = git("log", scope, "-i", "--grep=" + args.term, "--format=%h %ad %s", "--date=short", "-5", repo=repo)
            if rows:
                print("NEWEST %s COMMITS THAT NAME '%s'\n%s\n" % (label.upper(), args.term, rows))
        print("FILES IN wiki/research THAT CONTAIN '%s'" % args.term)
        print("\n".join(str(path.relative_to(ROOT)) for path in sorted((ROOT / "wiki/research").rglob("*.md"))
                        if args.term.lower() in path.read_text().lower()))
    for fault in faults:
        print("RECORD FAULT: " + fault)


if __name__ == "__main__":
    main()
