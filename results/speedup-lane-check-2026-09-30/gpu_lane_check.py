"""Lane-kernel check on one GPU rental: lane kernel against carry kernel on every state of a carry run.

Reuses scripts/experiment.py for rental, upload, bootstrap, stages, charges and teardown,
as results/speedup-free-2026-09-30/gpu_free.py does. The notebook fit of experiment.py does not run.
"""
import hashlib
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
CERIDWEN_NEW = Path(sys.argv.pop(1))   # ceridwen tree with the lane kernel
REFERENCE = ROOT / "results/speedup-free-2026-09-30/run/arms/carry/result.npz"
REMOTE = f"{engine.REMOTE}/.speedup"


class Run(experiment.Run):
    def measure(self, attempt):
        environment = self.prepare(attempt)
        instance = attempt["instance_id"]
        target, port = vast._ssh_target(instance)
        vast._ssh(instance, f"mkdir -p {REMOTE}/new_ceridwen {REMOTE}/out", timeout=self.timeout(attempt))
        nested = CERIDWEN_NEW / "ceridwen/sampler/nested.py"
        self.data["candidate_sha256"] = {str(nested): hashlib.sha256(nested.read_bytes()).hexdigest()}
        self.save()
        subprocess.run(["rsync", "-a", "--exclude", "__pycache__", "-e",
                        shlex.join(["ssh", *vast._ssh_options(port)]), str(CERIDWEN_NEW / "ceridwen"),
                        f"{target}:{REMOTE}/new_ceridwen/"], check=True, capture_output=True,
                       timeout=self.timeout(attempt, 300))
        for path in (HERE / "lane_check.py", REFERENCE):
            vast._rsync(port, str(path), f"{target}:{REMOTE}/", timeout=self.timeout(attempt))
        command = (environment + "MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                   "XLA_FLAGS='--xla_gpu_enable_command_buffer=' "
                   f"PYTHONPATH={REMOTE}/new_ceridwen:{engine.REMOTE}/external/sedpy_jax "
                   f"SPEEDUP_ROOT={engine.REMOTE} SPEEDUP_OUT={REMOTE}/out EXPECT_CERIDWEN=new_ceridwen "
                   f"CHECK_REFERENCE={REMOTE}/result.npz .venv-ceridwen-gpu/bin/python {REMOTE}/lane_check.py")
        try:
            self.stage(attempt, "lane-check", command)
        finally:
            (self.root / "check").mkdir(exist_ok=True)
            vast._rsync(port, f"{target}:{REMOTE}/out/", str(self.root / "check") + "/",
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
