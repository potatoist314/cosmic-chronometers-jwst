"""cProfile of the production model build (common.build) on the box.

Env: SPEEDUP_OUT (output directory), RUN_TAG (file stem).
"""
import cProfile
import io
import os
import pstats
import time
from pathlib import Path

import common

profile = cProfile.Profile()
start = time.perf_counter()
profile.enable()
common.build()
profile.disable()
wall = time.perf_counter() - start
out = Path(os.environ["SPEEDUP_OUT"]) / f"{os.environ['RUN_TAG']}.txt"
text = io.StringIO()
pstats.Stats(profile, stream=text).sort_stats("cumulative").print_stats(80)
out.write_text(f"build wall {wall:.2f} s\n" + text.getvalue())
print(f"build wall {wall:.2f} s")
