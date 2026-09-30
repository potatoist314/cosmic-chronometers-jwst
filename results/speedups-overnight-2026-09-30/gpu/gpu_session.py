"""One GPU rental that runs queued jobs against candidate ceridwen trees.

Reuses scripts/experiment.py for rental, upload, bootstrap, stages, charges and teardown,
as results/speedup-lane-cause-2026-09-30/gpu_cause.py does. While the instance is up,
each file <queue>/<name>.job is one remote command ({R}: remote work directory,
{P}: python of the box venv). <queue>/END, the session limit or the spend cap ends it.
The payload directory (candidate trees <name>/ceridwen, notebooks) is synced to {R}/payload
before each job. A failed copy is retried and never ends the session.
Usage: python3 gpu_session.py <payload dir> <queue dir> run <config> --gpu "RTX 5090" --output <dir>
"""
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(os.environ.get("SPEEDUP_TREE", "/Users/liuhao/Downloads/Astro project"))
sys.path.insert(0, str(ROOT / "scripts"))
import experiment  # noqa: E402

engine, vast = experiment.engine, experiment.vast
HERE = Path(__file__).resolve().parent
PAYLOAD = Path(sys.argv.pop(1)).resolve()
QUEUE = Path(sys.argv.pop(1)).resolve()
DEAD = ROOT / "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/ns_raw_dead_1071.pkl"
REMOTE = f"{engine.REMOTE}/.speedup"
SESSION_S = 60 * float(os.environ.get("SESSION_MINUTES", "90"))


def copy(*command, timeout):
    """rsync with retries: a network drop on this Mac must not end a paid session."""
    for retry in range(5):
        try:
            subprocess.run(["rsync", *command], check=True, capture_output=True, timeout=timeout)
            return
        except (subprocess.SubprocessError, OSError) as error:
            engine.log(f"rsync failed ({type(error).__name__}); retry {retry + 1}")
            time.sleep(30)


class Run(experiment.Run):
    def measure(self, attempt):
        environment = self.prepare(attempt)
        instance = attempt["instance_id"]
        target, port = vast._ssh_target(instance)
        ssh = shlex.join(["ssh", *vast._ssh_options(port)])
        copy("-a", "-e", ssh, "--rsync-path", f"mkdir -p {REMOTE}/payload {REMOTE}/out && rsync", str(DEAD),
             f"{target}:{REMOTE}/dead.pkl", timeout=self.timeout(attempt, 300))
        base = (environment + "export MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                f"SPEEDUP_ROOT={engine.REMOTE} SPEEDUP_OUT={REMOTE}/out PROF_DEAD={REMOTE}/dead.pkl "
                f"SEDPY={engine.REMOTE}/external/sedpy_jax && ")
        (self.root / "out").mkdir(exist_ok=True)
        deadline = time.time() + SESSION_S
        while time.time() < deadline and not (QUEUE / "END").exists():
            self.budget(reserve=attempt["price"] / 120)
            jobs = sorted(p for p in QUEUE.glob("*.job") if not (QUEUE / f"{p.stem}.done").exists())
            if not jobs:
                time.sleep(3)
                continue
            job = jobs[0]
            copy("-a", "-e", ssh, *map(str, sorted(HERE.glob("*.py"))), f"{target}:{REMOTE}/",
                 timeout=self.timeout(attempt))
            copy("-a", "--delete", "--exclude", "__pycache__", "-e", ssh, f"{PAYLOAD}/", f"{target}:{REMOTE}/payload/",
                 timeout=self.timeout(attempt, 300))
            command = job.read_text().strip().replace("{R}", REMOTE).replace("{P}", ".venv-ceridwen-gpu/bin/python")
            try:
                self.stage(attempt, job.stem, base + command)
            except engine.StageFailed as error:   # the session continues; the stage log is already local
                engine.log(str(error))
            finally:
                copy("-a", "--exclude", "*.xplane.pb", "-e", ssh, f"{target}:{REMOTE}/out/", f"{self.root / 'out'}/",
                     timeout=self.timeout(attempt, 300))
            (QUEUE / f"{job.stem}.done").touch()
        attempt["status"] = "complete"


experiment.Run = Run

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        raise SystemExit(experiment.main())
    except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError, SyntaxError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
