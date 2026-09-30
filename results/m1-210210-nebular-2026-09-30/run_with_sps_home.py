#!/usr/bin/env python3
"""scripts/experiment.py with SPS_HOME exported on the rental.

emission_line_marginalisation reads $SPS_HOME/data/emlines_info.dat; scripts/experiment.py
uploads the file but does not export the variable. Arguments are those of scripts/experiment.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import experiment

prepare = experiment.Run.prepare
experiment.Run.prepare = lambda self, attempt: (
    prepare(self, attempt) + f"export SPS_HOME={experiment.engine.REMOTE}/external/fsps && ")
raise SystemExit(experiment.main())
