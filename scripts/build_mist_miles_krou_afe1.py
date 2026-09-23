#!/usr/bin/env python3
"""Solar-scaled old-MIST control grid for the alpha-enhanced comparison.

Builds MIST v1.2 + MILES SSPs with the Kroupa IMF from the repo's FSPS
(external/fsps, FSPS v3.2, python-fsps) and wraps them as a single-plane
:class:`ceridwen.ssps.ssp_data_afe.SSPDataAfe` (``n_afe=1`` at
``[alpha/Fe]=0``), so the Ceridwen notebook's ``CSPBasis_afe`` path runs
unchanged -- single-plane alpha interpolation compiles to a no-op.

This is the closest achievable old-MIST control, NOT an exact match of
``amist_c3k_hr_krou_afe``: the C3K high-resolution spectra exist only in the
M. J. Park FITS (see ``ceridwen/scripts_afe/build_afe_hr_grid.py``), while
FSPS 3.2 ships MILES (this build) or downsampled C3K (see
``external/fsps/SPECTRA/C3K/readme.md``). Metallicity nodes (12 FSPS zlegend
points at ``Zsun=0.0142``), wavelength grid (5994 points) and resolution
also differ; the IMF (Kroupa, ``imf_type=2``) and the age nodes (107 points,
``log(age/yr)`` 5.0-10.3 in 0.05) match. Details and sources are in
``wiki/research/experiments/e-afe-fixed-zero.md``.

Run from the project root with the main venv (it has python-fsps)::

    PYTHONPATH=ceridwen:external/sedpy_jax .venv/bin/python \\
        scripts/build_mist_miles_krou_afe1.py

CPU-only, a few minutes. No fit, no GPU.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ceridwen"))
sys.path.insert(0, str(ROOT / "external/sedpy_jax"))

from ceridwen.ssps.grid_fetch import grid_cache_dir  # noqa: E402
from ceridwen.ssps.library_resolution import miles_segments  # noqa: E402
from ceridwen.ssps.ssp_data import SSPData  # noqa: E402
from ceridwen.ssps.ssp_data_afe import SSPDataAfe  # noqa: E402

GRID_NAME = "mist_miles_krou_afe1"
MILES_RESOLUTION_SOURCE = "MILES FWHM 2.54 A (Falcon-Barroso et al. 2011)"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None,
                    help="output HDF5 path (default: <grid-cache>/mist_miles_krou_afe1.h5)")
    args = ap.parse_args()

    # FSPS defaults already give Kroupa (imf_type=2); pass nothing so the
    # grid cannot drift from the HR grid's IMF. from_fsps rejects any
    # non-library/IMF kwarg, so an empty build carries no hidden settings.
    ssp = SSPData.from_fsps(resolution_segments=miles_segments(),
                            resolution_source=MILES_RESOLUTION_SOURCE)
    assert ssp.isoc_type == "mist", ssp.isoc_type
    assert ssp.spec_library == "miles", ssp.spec_library
    assert ssp.imf_type == 2, ssp.imf_type
    ssp.display()

    afe = SSPDataAfe(
        np.asarray(ssp.ssp_lgmet),
        np.array([0.0]),
        np.asarray(ssp.ssp_lg_age_gyr),
        np.asarray(ssp.ssp_wave),
        np.asarray(ssp.ssp_flux)[None, ...],
        ssp_resolution=np.asarray(ssp.ssp_resolution, dtype=np.float64),
        resolution_source=ssp.resolution_source,
        isoc_type=ssp.isoc_type,
        spec_library=ssp.spec_library,
        imf_type=ssp.imf_type,
        fsps_version=ssp.fsps_version,
        fsps_kwargs={**dict(ssp.fsps_kwargs or {}),
                     "afe_plane": 0.0,
                     "wrapped_from": "SSPData (solar-scaled, single alpha plane)"},
        wave_min=ssp.wave_min,
        wave_max=ssp.wave_max,
        schema_version="2.1",
    )
    out = Path(args.out) if args.out else grid_cache_dir() / f"{GRID_NAME}.h5"
    afe.save(out)
    back = SSPDataAfe.load(out)
    assert back.ssp_flux.shape == afe.ssp_flux.shape
    print(f"[control-grid] wrote {out} (round-trip load OK)\n")
    afe.display()


if __name__ == "__main__":
    main()
