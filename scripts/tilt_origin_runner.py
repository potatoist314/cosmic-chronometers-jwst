#!/usr/bin/env python3
"""Run the tilt-origin arms of ``calibration_polynomial_experiment.py`` in order.

``arms.json`` is a list of ``{"name": ..., "args": [...]}``; an arm may carry
``"dust_prior_from": "<arm>"`` to take a clipped-normal dust prior (posterior
median and half width of the attenuation amplitude) from a finished arm.
Every arm runs on the same interpreter, one after the other, so one box holds
one boot for a whole target.  Finished arms (``summary.json`` present) are
skipped, and ``progress.log`` records start, end and return code.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


def dust_prior(arm_dir: Path) -> list[str]:
    summary = json.loads((arm_dir / "summary.json").read_text())
    amplitude = next(k for k in summary["posterior"] if k.startswith("diffuse_tau"))
    q = summary["posterior"][amplitude]
    return [f"{q['q50']:.5f}", f"{0.5 * (q['q84'] - q['q16']):.5f}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arms", type=Path, required=True)
    parser.add_argument("--out-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    arms = json.loads(args.arms.read_text())
    script = Path(__file__).resolve().parent / "calibration_polynomial_experiment.py"
    log = args.out_root / f"progress{args.arms.stem.replace('arms', '')}.log"
    args.out_root.mkdir(parents=True, exist_ok=True)

    def note(message: str) -> None:
        with log.open("a") as handle:
            handle.write(f"{datetime.now(UTC).isoformat(timespec='seconds')} {message}\n")

    failures = 0
    for arm in arms:
        out = args.out_root / arm["name"]
        if (out / "summary.json").exists():
            note(f"skip {arm['name']} (done)")
            continue
        command = [args.python, str(script), "--out", str(out),
                   "--project-root", str(args.project_root), *arm["args"]]
        if arm.get("dust_prior_from"):
            source = args.out_root / arm["dust_prior_from"]
            if not (source / "summary.json").exists():
                note(f"skip {arm['name']} (needs {arm['dust_prior_from']})")
                failures += 1
                continue
            command += ["--dust-prior", *dust_prior(source)]
        note(f"start {arm['name']}")
        started = time.time()
        with (out.parent / f"{arm['name']}.log").open("w") as handle:
            code = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT).returncode
        note(f"end {arm['name']} rc={code} wall={time.time() - started:.0f}s")
        failures += code != 0
    (args.out_root / f"ALL_DONE{args.arms.stem.replace('arms', '')}").write_text(f"failures={failures}\n")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
