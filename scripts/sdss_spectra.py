#!/usr/bin/env python3
"""Write SDSS DR17 single-fibre spectra and their ugriz cModel and WISE W1, W2 photometry
in the processed-spectrum format of data/processed/manga_dr17/.

Input: data/raw/sdss_dr17/ from scripts/download_sdss_dr17.py.
Output: data/processed/sdss_dr17/<PLATE-MJD-FIBER>.fits (SPECTRUM and PHOTOMETRY tables,
fit metadata in the primary header) and data/processed/sdss_dr17/summary.csv.

Spectrum (spec-lite COADD table, sdss/datamodel spec-lite.md)
- Wavelength 10^LOGLAM, heliocentric vacuum (https://www.sdss4.org/dr17/spectro/spectro_basics/;
  header VACUUM = T). FLUX in 1E-17 erg/s/cm^2/A, error IVAR^-1/2.
- VALID: IVAR > 0 and no BRIGHTSKY (bit 23) in AND_MASK. The reduction sets IVAR = 0 for
  the very bad conditions; BRIGHTSKY is "the most useful mask bit to look at"; bits 0-15
  flag a whole spectrograph half (https://www.sdss4.org/dr17/algorithms/bitmasks/, SPPIXMASK).
- LSF: WDISP is the 1-sigma line width in pixels of 1E-4 in log10(lambda), so
  sigma = WDISP x 1E-4 x ln(10) x lambda in A. Pixels with WDISP = 0 (4 of the 60 spectra;
  all have IVAR = 0) take WDISP interpolated linearly in wavelength from the other pixels:
  the fit needs a positive width at every pixel.
- Galactic extinction: the spectra are not corrected (https://www.sdss4.org/dr17/spectro/caveats/).
  A = 3.1 E(B-V) k(lambda), k from ceridwen's CCM89 law with the O'Donnell (1994) update, as in
  scripts/manga_aperture_spectra.py. E(B-V) is the SFD98 value, EXTINCTION_R / 2.285: the CAS
  extinction uses the Schlafly & Finkbeiner (2011) Table 6 coefficients for R_V = 3.1
  (https://www.sdss4.org/dr17/algorithms/magnitudes/; SF11 Table 6, SDSS r: 2.285).
- Aperture: the 3 arcsec fibre spectrophotometry is normalised to PSF magnitudes
  (https://www.sdss4.org/dr17/algorithms/spectrophotometry/), so the fibre holds part of the
  galaxy light. Flux and error are multiplied by one scalar, the r-band cModel flux over the
  synthetic r flux of the dereddened spectrum.

Kinematics: z, velDisp and velDispErr of the SpecObj row (the fibre spectrum).

Photometry
- u, g, r, i, z: PhotoObj cModelFlux (nanomaggies, "DeV+Exp"), error cModelFluxIvar^-1/2,
  multiplied by 10^(0.4 EXTINCTION). AB: u_AB = u_SDSS - 0.04 mag, z_AB = z_SDSS + 0.02 mag,
  g, r and i are AB (https://www.sdss4.org/dr17/algorithms/fluxcal/).
- W1, W2: wiseForcedTarget fluxes are Vega nanomaggies; AB offsets 2.699 and 3.339 mag
  (WISE All-Sky Explanatory Supplement, Sect. IV.4.h, Table 3). The forced photometry uses
  the SDSS cModel profile (Lang, Hogg & Schlegel 2016, AJ 151, 36), the cModel aperture.
  Not dereddened, as in scripts/manga_aperture_spectra.py.

Checks in summary.csv: aperture_scale; synthetic g and i flux of the scaled spectrum over
the cModel flux; median LSF sigma in km/s; R = lambda / (2.355 sigma) at 4000 and 9000 A.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from astropy import units as u
from astropy.constants import c as C_LIGHT
from astropy.io import fits
from astropy.table import Table

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "external/sedpy_jax"))
from ceridwen.dust.attenuation_laws import cardelli  # noqa: E402
from manga_aperture_spectra import WISE_AB_OFFSET, WISE_FILTERS, read_csv, synthetic_maggies  # noqa: E402
from sedpy_jax.observate import load_filters  # noqa: E402

RAW = PROJECT_ROOT / "data/raw/sdss_dr17"
PROCESSED = PROJECT_ROOT / "data/processed/sdss_dr17"
C_KMS = C_LIGHT.to_value(u.km / u.s)
SF11_R = 2.285
SDSS_BANDS = {"u": "sdss_u0", "g": "sdss_g0", "r": "sdss_r0", "i": "sdss_i0", "z": "sdss_z0"}
BRIGHTSKY = 1 << 23
AB_OFFSET = {"u": -0.04, "g": 0.0, "r": 0.0, "i": 0.0, "z": 0.02}


def process(row: dict) -> dict:
    plate, mjd, fiber = int(row["plate"]), int(row["mjd"]), int(row["fiberID"])
    target = f"{plate:04d}-{mjd}-{fiber:04d}"
    coadd = fits.getdata(RAW / "spectra" / f"spec-{target}.fits", "COADD")
    wave = 10.0 ** coadd["loglam"].astype(float)
    ivar = coadd["ivar"].astype(float)
    valid = (ivar > 0) & ((coadd["and_mask"] & BRIGHTSKY) == 0)
    with np.errstate(divide="ignore"):
        error = np.where(ivar > 0, ivar ** -0.5, 0.0)
    wdisp = coadd["wdisp"].astype(float)
    lsf_sigma = np.interp(wave, wave[wdisp > 0], wdisp[wdisp > 0]) * 1e-4 * np.log(10.0) * wave
    ebv = float(row["extinction_r"]) / SF11_R
    extinction = 10.0 ** (0.4 * 3.1 * ebv * np.asarray(cardelli(wave, tau_card=1.0, R_v_card=3.1)))
    flux, error = coadd["flux"].astype(float) * extinction, error * extinction

    bands, filters, maggies, maggie_errors = [], [], [], []
    for band, name in SDSS_BANDS.items():
        scale = 10.0 ** (0.4 * (float(row[f"extinction_{band}"]) - AB_OFFSET[band])) * 1e-9
        bands.append(band), filters.append(name)
        maggies.append(float(row[f"cModelFlux_{band}"]) * scale)
        maggie_errors.append(float(row[f"cModelFluxIvar_{band}"]) ** -0.5 * scale)
    for key, (label, name) in WISE_FILTERS.items():
        scale = 10.0 ** (-0.4 * WISE_AB_OFFSET[key]) * 1e-9
        bands.append(label), filters.append(name)
        maggies.append(float(row[f"{key}_nanomaggies"]) * scale)
        maggie_errors.append(float(row[f"{key}_nanomaggies_ivar"]) ** -0.5 * scale)

    check = load_filters(["sdss_g0", "sdss_r0", "sdss_i0"])
    synthetic = synthetic_maggies(wave, flux * 1e-17, valid, check)
    aperture_scale = float(maggies[bands.index("r")] / synthetic[1])
    flux, error = flux * aperture_scale, error * aperture_scale
    record = {
        "target": target, "objid": int(row["bestObjID"]), "specobjid": row["specObjID"],
        "z": float(row["z"]), "sigma": float(row["velDisp"]), "sigma_err": float(row["velDispErr"]),
        "ebvgal": ebv, "sn_median_r": float(row["snMedian_r"]), "aperture_scale": aperture_scale,
        "valid_fraction": float(valid.mean()),
        **{f"synthetic_over_cmodel_{b}": float(aperture_scale * synthetic[k] / maggies[bands.index(b)])
           for k, b in ((0, "g"), (2, "i"))},
        "median_lsf_sigma_kms": float(np.median(C_KMS * lsf_sigma / wave)),
        **{f"resolution_{int(lam)}": float(np.interp(lam, wave, wave / (2.355 * lsf_sigma)))
           for lam in (4000.0, 9000.0)},
        "wise_treated_as_pointsource": row["treated_as_pointsource"],
    }

    PROCESSED.mkdir(parents=True, exist_ok=True)
    spectrum = Table({"WAVE": wave, "FLUX": flux, "ERROR": error, "VALID": valid, "LSF_SIGMA": lsf_sigma})
    spectrum.meta.update({"EXTNAME": "SPECTRUM", "BUNIT": "1E-17 erg/s/cm^2/Angstrom",
                          "WAVEUNIT": "Angstrom vacuum heliocentric", "LSFUNIT": "Angstrom sigma, WDISP"})
    photometry = Table({"BAND": bands, "FILTER": filters, "FLUX_MAGGIES": maggies, "ERROR_MAGGIES": maggie_errors})
    photometry.meta["EXTNAME"] = "PHOTOMETRY"
    primary = fits.PrimaryHDU()
    for keyword, key in (("TARGET", "target"), ("OBJID", "objid"), ("Z", "z"), ("SIGMA", "sigma"),
                         ("SIGMAERR", "sigma_err"), ("EBVGAL", "ebvgal"), ("APERSCL", "aperture_scale")):
        primary.header[keyword] = record[key]
    fits.HDUList([primary, fits.table_to_hdu(spectrum), fits.table_to_hdu(photometry)]).writeto(
        PROCESSED / f"{target}.fits", overwrite=True)
    return record


def main() -> None:
    records = []
    for targets in sorted(RAW.glob("targets*.csv")):  # targets.csv, then targets_sigma250.csv
        for row in read_csv(targets, "specObjID").values():
            records.append(process(row))
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in records[-1].items()}, flush=True)
    with (PROCESSED / "summary.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
