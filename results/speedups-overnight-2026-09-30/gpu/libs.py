"""Run a harness script, then list the shared libraries the process mapped from site-packages/nvidia
and the JAX plugins.

Usage: python libs.py <script.py>. Env: LIBS_OUT (text file).
"""
import os
import runpy
import sys

script = sys.argv.pop(1)
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
try:
    runpy.run_path(script, run_name="__main__")
finally:
    with open("/proc/self/maps") as maps:
        libs = sorted({line.split()[-1] for line in maps if ".so" in line and ("/nvidia/" in line or "jax" in line)})
    with open(os.environ["LIBS_OUT"], "w") as fh:
        fh.write("\n".join(libs) + "\n")
