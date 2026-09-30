"""Paid GPU checks for the speedup ideas (scratch driver, no project file changed).

One rental: stage profile, same-boot A/B of the carry kernel, then the ablation fits.
Reuses scripts/experiment.py for rental, upload, bootstrap, fits, retrieval, charges and teardown.
"""
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/liuhao/Downloads/Astro project")
sys.path.insert(0, str(ROOT / "scripts"))
import experiment  # noqa: E402

engine, vast = experiment.engine, experiment.vast
SCRATCH = Path(__file__).resolve().parent
RUN3 = ROOT / "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210"
REMOTE = f"{engine.REMOTE}/.speedup"
CHECKS = (
    ("profile", "profile_stages.py", "PROFILE_BATCH=100,500 PROFILE_REPEATS=30"),
    ("lanes", "lanes.py", "LANES_REPEATS=5"),
)


class Run(experiment.Run):
    def measure(self, attempt):
        if not self.data.get("checks_done"):
            environment = self.prepare(attempt)
            instance = attempt["instance_id"]
            target, port = vast._ssh_target(instance)
            vast._ssh(instance, f"mkdir -p {REMOTE}/run3 {REMOTE}/out", timeout=self.timeout(attempt))
            for path in (SCRATCH / "profile_stages.py", SCRATCH / "lanes.py"):
                vast._rsync(port, str(path), f"{target}:{REMOTE}/", timeout=self.timeout(attempt))
            for path in (RUN3 / "ns_raw_dead_943.pkl", RUN3 / "ceridwen_result.h5"):
                vast._rsync(port, str(path), f"{target}:{REMOTE}/run3/", timeout=self.timeout(attempt, 300))
            env = (environment + "MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                   "XLA_FLAGS='--xla_gpu_enable_command_buffer=' "
                   f"PYTHONPATH={engine.REMOTE}/external/sedpy_jax SPEEDUP_ROOT={engine.REMOTE} "
                   f"SPEEDUP_RUN3={REMOTE}/run3 SPEEDUP_OUT={REMOTE}/out ")
            for name, script, extra in CHECKS:
                try:
                    self.stage(attempt, name, env + extra + f" .venv-ceridwen-gpu/bin/python {REMOTE}/{script}")
                except engine.StageFailed as error:
                    engine.log(str(error))  # the fits still run
            (self.root / "checks").mkdir(exist_ok=True)
            vast._rsync(port, f"{target}:{REMOTE}/out/", str(self.root / "checks") + "/",
                        timeout=self.timeout(attempt, 300))
            self.data["checks_done"] = True
            self.save()
        super().measure(attempt)


experiment.Run = Run

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        raise SystemExit(experiment.main())
    except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError, SyntaxError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
