#!/usr/bin/env python3
"""Build the alpha-enhanced SSP grid with FSPS CLOUDY nebular emission on the young SSPs.

    ceridwen/.venv/bin/python scripts/build_nebular_grid.py [output.h5]

Each SSP with log10(age/yr) <= 7.3 gets the CLOUDY lines and continuum for its own
ionising photon rate. log U = -2.5. log(Z_gas/Zsun) = [Fe/H] + [alpha/Fe]. Lines have
the grid resolution, so a fit gives them the stellar velocity dispersion.

The script then compares the H beta and H alpha fluxes in the new grid with the CLOUDY
line luminosities, and prints the sha256 of the grid. The build of 2026-09-30 has
sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

import h5py
import jax
import numpy as np

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp

from ceridwen.neb.NebularGridModel import NebularModel

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path.home() / ".ceridwen/grids/amist_c3k_hr_krou_afe.h5"
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE.with_name("amist_c3k_hr_krou_afe_nebular.h5")
LOG_U = -2.5
CHECK_LINES = (4862.71, 6564.60)  # H beta, H alpha in the FSPS line list, vacuum A
C_A_PER_S = 2.99792458e18

shutil.copyfile(SOURCE, OUTPUT)
with h5py.File(OUTPUT, "r+") as grid:
    wave = grid["ssp_wave"][:]
    log_age_yr = grid["ssp_lg_age_gyr"][:] + 9.0
    feh = grid["ssp_lgmet"][:] - np.log10(json.loads(grid.attrs["fsps_kwargs_json"])["zsun_reference"])
    # Lines are painted at the grid resolution, sigma = 0.8493 pixel, so the
    # fit gives them the stellar velocity dispersion.
    neb = NebularModel(False, ROOT / "external/fsps", wave, ssp_ages_lgyr=log_age_yr,
                       sigma_smooth=0.0, res_floor_factor=0.8493)
    young = np.asarray(neb.young_idx)
    ages = jnp.asarray(log_age_yr[young])
    rows = [int(np.argmin(np.abs(np.asarray(neb.nebem_line_pos) - line))) for line in CHECK_LINES]
    worst = 0.0
    for p, afe in enumerate(grid["ssp_afe"][:]):
        stellar = grid["ssp_flux"][p]
        log_q = neb.compute_log_qq(jnp.asarray(stellar[:, young]))
        for z in range(feh.size):
            # Gas O/H follows the stellar O/H: log(Z_gas/Zsun) = [Fe/H] + [alpha/Fe].
            gas_logz = jnp.asarray(feh[z] + afe)
            nebular = np.asarray(neb.evaluate_batch(gas_logz, jnp.asarray(LOG_U), ages, log_q[z:z + 1]))[0]
            stellar[z, young] += nebular
            # Check: line flux in the added spectrum against the CLOUDY luminosity (L_sun).
            cube = np.asarray(neb.evaluate_batch_line_lum(gas_logz, jnp.asarray(LOG_U), ages, log_q[z:z + 1]))[0]
            for row in rows:
                offset = np.abs(wave - float(neb.nebem_line_pos[row]))
                line, side = offset < 6.0, (offset > 8.0) & (offset < 14.0)
                excess = nebular[:, line] - np.median(nebular[:, side], axis=1)[:, None]
                flux = -np.trapezoid(excess, C_A_PER_S / wave[line], axis=1)
                worst = max(worst, float(np.max(np.abs(flux / cube[:, row] - 1.0))))
        grid["ssp_flux"][p] = stellar
    grid.attrs["nebular"] = (
        f"FSPS CLOUDY {neb.line_file.name} and {neb.cont_file.name} lines and continuum on SSPs "
        f"with log age/yr <= {log_age_yr[young].max():.2f}; log U = {LOG_U}; "
        "log(Z_gas/Zsun) = [Fe/H] + [alpha/Fe]; Q from each SSP below 912 A")
print(f"H beta and H alpha flux against the CLOUDY cube: largest relative difference {worst:.1e}")
if worst > 1e-4:
    raise SystemExit("line fluxes in the grid differ from the CLOUDY luminosities")
with OUTPUT.open("rb") as stream:
    print(hashlib.file_digest(stream, "sha256").hexdigest(), OUTPUT)
