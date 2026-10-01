"""gpu_session.py with a timed upload: each SSH call, source archive and input copy is logged
with its start (epoch s) and duration, and the bootstrap runs under ``bash -x`` with an epoch
time stamp on every traced line. The first fit still starts during the upload.

Usage: python3 session7.py <payload dir> <queue dir> run <config> --gpu "RTX 5090" --output <dir>
"""
import signal
import subprocess
import sys
import time

import gpu_session as g

engine, vast = g.engine, g.vast


def timed(name, function):
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return function(*args, **kwargs)
        finally:
            label = name(*args, **kwargs) if callable(name) else name
            if label:
                engine.log(f"timing {label}: start {start:.2f}, {time.time() - start:.2f} s")
    return wrapper


class Run(g.Run):
    def upload(self, attempt, bootstrap=None, early=None):
        bootstrap = bootstrap.replace("bash scripts/bootstrap_vast_ai.sh",
                                      "PS4='+ $(date +%s.%N) ' bash -x scripts/bootstrap_vast_ai.sh")
        saved = vast._ssh, vast._rsync_background, self.archive, engine.subprocess.run
        vast._ssh = timed(lambda instance, command, **_: f"ssh {command[:60]!r}", vast._ssh)
        vast._rsync_background = timed(lambda port, parts, *_: f"grid part start {parts[0].rsplit('/', 1)[-1]}",
                                       vast._rsync_background)
        self.archive = timed(lambda attempt, tree, *_: f"archive {tree.name}", self.archive)
        engine.subprocess.run = timed(lambda command, *_, **__: "inputs rsync" if command[:2] == ["rsync", "-aR"] else None,
                                      engine.subprocess.run)
        start = time.time()
        try:
            return super().upload(attempt, bootstrap, early)
        finally:
            vast._ssh, vast._rsync_background, self.archive, engine.subprocess.run = saved
            engine.log(f"timing upload: start {start:.2f}, {time.time() - start:.2f} s")


g.experiment.Run = Run

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        raise SystemExit(g.experiment.main())
    except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError, SyntaxError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
