"""Hidden outcome tests. The grader runs them from the sandbox root after the agent finishes."""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
ROOT = Path.cwd()
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
