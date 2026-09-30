"""One GPU rental that runs queued diagnostic jobs on the saved lane-check states.

Reuses scripts/experiment.py for rental, upload, bootstrap, stages, charges and teardown,
as results/speedup-lane-check-2026-09-30/gpu_lane_check.py does. While the instance is up,
each file queue/<name>.job is one remote command ({R} is the remote work directory).
queue/END, the session limit or the spend cap ends the session.
"""
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/Users/liuhao/Downloads/Astro project")
sys.path.insert(0, str(ROOT / "scripts"))
import experiment  # noqa: E402

engine, vast = experiment.engine, experiment.vast
HERE = Path(__file__).resolve().parent
CERIDWEN_NEW = Path(sys.argv.pop(1))   # ceridwen tree with the lane kernel
STATES = ROOT / "results/speedup-lane-check-2026-09-30/run/check"
QUEUE = HERE / "queue"
REMOTE = f"{engine.REMOTE}/.speedup"
SESSION_S = 60 * float(os.environ.get("CAUSE_SESSION_MINUTES", "40"))


class Run(experiment.Run):
    def measure(self, attempt):
        environment = self.prepare(attempt)
        instance = attempt["instance_id"]
        target, port = vast._ssh_target(instance)
        ssh = shlex.join(["ssh", *vast._ssh_options(port)])
        vast._ssh(instance, f"mkdir -p {REMOTE}/new_ceridwen {REMOTE}/out {REMOTE}/states",
                  timeout=self.timeout(attempt))
        subprocess.run(["rsync", "-a", "--exclude", "__pycache__", "-e", ssh, str(CERIDWEN_NEW / "ceridwen"),
                        f"{target}:{REMOTE}/new_ceridwen/"], check=True, capture_output=True,
                       timeout=self.timeout(attempt, 300))
        subprocess.run(["rsync", "-a", "-e", ssh, f"{STATES}/", f"{target}:{REMOTE}/states/"],
                       check=True, capture_output=True, timeout=self.timeout(attempt, 300))
        base = (environment + "MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                f"PYTHONPATH={REMOTE}/new_ceridwen:{engine.REMOTE}/external/sedpy_jax "
                f"SPEEDUP_ROOT={engine.REMOTE} SPEEDUP_OUT={REMOTE}/out CAUSE_STATES={REMOTE}/states "
                "EXPECT_CERIDWEN=new_ceridwen ")
        (self.root / "out").mkdir(exist_ok=True)
        deadline = time.time() + SESSION_S
        while time.time() < deadline and not (QUEUE / "END").exists():
            self.budget(reserve=attempt["price"] / 120)
            jobs = sorted(p for p in QUEUE.glob("*.job") if not (QUEUE / f"{p.stem}.done").exists())
            if not jobs:
                time.sleep(3)
                continue
            job = jobs[0]
            subprocess.run(["rsync", "-a", "-e", ssh, *map(str, sorted(HERE.glob("*.py"))), f"{target}:{REMOTE}/"],
                           check=True, capture_output=True, timeout=self.timeout(attempt))
            try:
                self.stage(attempt, job.stem, base + job.read_text().strip().replace("{R}", REMOTE))
            except engine.StageFailed as error:   # the session continues; the stage log is already local
                engine.log(str(error))
            finally:
                subprocess.run(["rsync", "-a", "-e", ssh, f"{target}:{REMOTE}/out/", f"{self.root / 'out'}/"],
                               check=True, capture_output=True, timeout=self.timeout(attempt, 300))
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
