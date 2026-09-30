#!/usr/bin/env python3
"""Print the current Ceridwen fit state: ceridwen_state.py [--days 14].

Every SETTINGS and PRIORS entry of the production notebook, the model options its
CSPBasis_afe call fixes, the research records that tested each, and the experiments
and run directories that are planned, running or recent. Reads only local files.
"""
import argparse
import ast
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "wiki"))
import fit_settings  # noqa: E402
import research  # noqa: E402

NOTEBOOK = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
LAWS = "external/sedpy_jax/sedpy_jax/attenuation_dust.py"


def notebook_state():
    """({key: (dict name, value, comment)}, {option: value}) of the production notebook."""
    code = ["".join(c["source"]) for c in json.loads((ROOT / NOTEBOOK).read_text())["cells"]
            if c["cell_type"] == "code"]
    top = next(s for s in code if "SETTINGS = {" in s)
    entries = {key: (name, ast.unparse(node), note)
               for key, (name, node, note) in fit_settings.parse(top).items()}
    call = next(n for s in code if "CSPBasis_afe(" in s for n in ast.walk(ast.parse(s))
                if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "CSPBasis_afe")
    options = {k.arg: ast.unparse(k.value) for k in call.keywords if isinstance(k.value, ast.Constant)}
    return entries, options


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


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--days", type=int, default=14, help="how far back a result counts as recent")
    since = (date.today() - timedelta(days=parser.parse_args().days)).isoformat()
    entries, options = notebook_state()
    records, faults = research.load(ROOT / "wiki/research")
    experiments = [r for r in records if r["kind"] == "experiment"]
    configs = {path.parent: json.loads(path.read_text()) for path in sorted((ROOT / "results").glob("*/experiment.json"))}
    grouped = {ROOT / group: r for r in experiments for group in research.refs(r, "result_groups")}

    tested = {}  # key -> {record id or result directory: values an experiment.json ran}
    for directory, config in configs.items():
        owner = grouped[directory]["id"] if directory in grouped else str(directory.relative_to(ROOT))
        for key, values in overrides(config).items():
            tested.setdefault(key, {}).setdefault(owner, []).extend(values)
    tested = {key: ["%s ran %s" % (owner, ", ".join(values)) for owner, values in owners.items()]
              for key, owners in tested.items()}

    for name in ("SETTINGS", "PRIORS"):
        print("%s  %s" % (name, NOTEBOOK))
        for key, (source, value, note) in entries.items():
            if source == name:
                print("%s = %s" % (key, value))
                for line in [note, *tested.pop(key, [])]:
                    if line:
                        print("    " + line)
        print()
    laws = re.findall(r'^    "(\w+)": \{', (ROOT / LAWS).read_text().partition("ATTENUATION_LAWS = {")[2], re.M)
    print("FIXED IN THE CSPBasis_afe CALL  %s" % NOTEBOOK)
    for key, value in options.items():
        print("%s = %s" % (key, value))
        if key == "diffuse_law":
            print("    registered laws (%s): %s" % (LAWS, ", ".join(laws)))
        for line in tested.pop(key, []):
            print("    " + line)
    for key, lines in tested.items():
        print("NOT A CURRENT KEY: %s  <- %s" % (key, "; ".join(lines)))
    print()

    print("EXPERIMENT RECORDS  planned, running, or results since %s" % since)
    recent = [r for r in experiments if r["status"] in ("planned", "running")
              or (r.get("results_at") or r["date"])[:10] >= since]
    for r in sorted(recent, key=lambda r: r.get("results_at") or r["date"], reverse=True):
        print("%s  %s  %s  %s" % (r["id"], r["status"], (r.get("results_at") or r["date"])[:10], r["question"]))
        print("    " + r["title"])
        arms = {}
        for run in r["sections"]["Runs"]:
            arms.setdefault(run["arm"], []).append(run["status"])
        if arms:
            print("    arms: " + "; ".join("%s %s" % (arm, ", ".join(
                "%d %s" % (states.count(s), s) for s in dict.fromkeys(states))) for arm, states in arms.items()))
        for group in research.refs(r, "result_groups"):
            print("    %s%s" % (group, usd(ROOT / group)))
    print()

    print("RUN DIRECTORIES IN NO RECORD")
    for directory, config in configs.items():
        if directory not in grouped and run_lines(directory):
            print("%s%s" % (directory.relative_to(ROOT), usd(directory)))
            for line in run_lines(directory):
                print("    " + line)
            for key, values in overrides(config).items():
                print("    %s: %s" % (key, ", ".join(values)))
    for fault in faults:
        print("RECORD FAULT: " + fault)


if __name__ == "__main__":
    main()
