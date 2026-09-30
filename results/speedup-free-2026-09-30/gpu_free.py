"""Free-speedup check on one GPU rental: carry against lanes, dust tilt, short pad and all three.

Reuses scripts/experiment.py for rental, upload, bootstrap, stages, charges and teardown.
The arms are seeded nested runs of free_arm.py; the notebook fit of experiment.py does not run.
"""
import hashlib
import json
import shlex
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/liuhao/Downloads/Astro project")
sys.path.insert(0, str(ROOT / "scripts"))
import experiment  # noqa: E402

engine, vast = experiment.engine, experiment.vast
HERE = Path(__file__).resolve().parent
CERIDWEN_NEW = Path(sys.argv.pop(1))   # ceridwen tree with the candidates
SEDPY_NEW = Path(sys.argv.pop(1))      # sedpy_jax tree with the dust tilt
REMOTE = f"{engine.REMOTE}/.speedup"
OLD_SEDPY = f"{engine.REMOTE}/external/sedpy_jax"
# name, slice kernel, short pad, ceridwen with the candidates, sedpy_jax with the tilt
ARMS = (("carry", "carry", "0", False, False), ("lanes", "lanes", "0", True, False),
        ("dust", "carry", "0", False, True), ("pad", "carry", "1", True, False),
        ("all", "lanes", "1", True, True))
CHANGED = [CERIDWEN_NEW / "ceridwen" / p for p in ("sampler/nested.py", "observation/_smoothing.py",
                                                   "observation/spectrum.py", "model/model.py")]
CHANGED.append(SEDPY_NEW / "sedpy_jax/attenuation_dust.py")


def arm_command(environment, name, kernel, pad, new_ceridwen, new_sedpy):
    sedpy = f"{REMOTE}/new_sedpy" if new_sedpy else OLD_SEDPY
    path = f"{REMOTE}/new_ceridwen:{sedpy}" if new_ceridwen else sedpy
    return (environment + "MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
            "XLA_FLAGS='--xla_gpu_enable_command_buffer=' "
            f"PYTHONPATH={path} SPEEDUP_ROOT={engine.REMOTE} SPEEDUP_OUT={REMOTE}/out "
            f"RUN_TAG={name} RUN_KERNEL={kernel} RUN_PAD={pad} "
            f"EXPECT_CERIDWEN={'new_ceridwen' if new_ceridwen else 'site-packages'} "
            f"EXPECT_SEDPY={'new_sedpy' if new_sedpy else 'external/sedpy_jax'} "
            f".venv-ceridwen-gpu/bin/python {REMOTE}/free_arm.py")


class Run(experiment.Run):
    def measure(self, attempt):
        environment = self.prepare(attempt)
        instance = attempt["instance_id"]
        target, port = vast._ssh_target(instance)
        vast._ssh(instance, f"mkdir -p {REMOTE}/new_ceridwen {REMOTE}/new_sedpy {REMOTE}/out",
                  timeout=self.timeout(attempt))
        self.data["candidate_sha256"] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in CHANGED}
        self.save()
        for source, destination in ((CERIDWEN_NEW / "ceridwen", "new_ceridwen"), (SEDPY_NEW / "sedpy_jax", "new_sedpy")):
            subprocess.run(["rsync", "-a", "--exclude", "__pycache__", "-e",
                            shlex.join(["ssh", *vast._ssh_options(port)]), str(source),
                            f"{target}:{REMOTE}/{destination}/"], check=True, capture_output=True,
                           timeout=self.timeout(attempt, 300))
        for name in ("free_arm.py", "free_compare.py"):
            vast._rsync(port, str(HERE / name), f"{target}:{REMOTE}/", timeout=self.timeout(attempt))
        compare = (environment + f"SPEEDUP_OUT={REMOTE}/out .venv-ceridwen-gpu/bin/python {REMOTE}/free_compare.py")
        try:
            for arm in ARMS:
                self.stage(attempt, f"arm-{arm[0]}", arm_command(environment, *arm))
            self.stage(attempt, "compare", compare)
            report = json.loads(vast._ssh(instance, f"cat {REMOTE}/out/compare.json",
                                          timeout=self.timeout(attempt)).stdout)
            if not all(row.get("positions_bitwise") for name, row in report["arms"].items() if name != "carry"):
                # An arm left the carry trajectory: a second carry run shows whether the GPU repeats itself.
                self.stage(attempt, "arm-carry2", arm_command(environment, "carry2", "carry", "0", False, False))
                self.stage(attempt, "compare2", compare)
        finally:
            # Completed arms are kept when a later stage fails.
            (self.root / "arms").mkdir(exist_ok=True)
            vast._rsync(port, f"{target}:{REMOTE}/out/", str(self.root / "arms") + "/",
                        timeout=self.timeout(attempt, 300))
        attempt["status"] = "complete"


experiment.Run = Run

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        raise SystemExit(experiment.main())
    except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError, SyntaxError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
