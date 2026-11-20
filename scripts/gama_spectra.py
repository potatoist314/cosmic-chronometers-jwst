#!/usr/bin/env python3
"""Write GAMA DR4 AAOmega fibre spectra and their gkv FUV-W2 total photometry in the
processed-spectrum format of data/processed/sdss_dr17/.

Input: data/raw/gama_dr4/ from scripts/download_gama_dr4.py.
Output: data/processed/gama_dr4/<CATAID>.fits (SPECTRUM and PHOTOMETRY tables, fit metadata in
the primary header) and data/processed/gama_dr4/summary.csv.

Spectrum (SpecAllv27 FITS file; header ROW1-ROW5)
- Row 1: flux-calibrated spectrum in 1E-17 erg/s/cm^2/A; row 2: 1 sigma error. Linear
  wavelength axis CRVAL1, CRPIX1, CD1_1. Wavelengths are in air (Hopkins et al. 2013,
  arXiv:1301.7127, Sect. 3.1); specutils air_to_vac converts them to vacuum. The header
  HEL_VC (heliocentric velocity correction) is not applied; the fit samples zred.
- VALID: finite flux and error > 0.
- LSF: FWHM 4.8 A at 4800 A and 4.5 A at 7250 A (Dogruel et al. 2024, ApJ 970, 149, Table 3),
  linear between the two and constant outside, as the VelocityDispersionsv02 fits used them
  (DMU notes: "interpolated linearly between two available measurements"). sigma = FWHM / 2.3548.
- Galactic extinction: A = 3.1 E(B-V) k(lambda), k from ceridwen's CCM89 law, as in
  scripts/sdss_spectra.py. E(B-V) is the gkv EBV (Planck dust map; Driver et al. 2022, Sect. 2.1). The spectra are calibrated against standard stars with
  their reddening removed, so the galaxy spectra still carry it (Hopkins et al. 2013, Sect. 4.1).
- Aperture: the 2 arcsec fibre holds part of the galaxy light. Flux and error are multiplied
  by one scalar, the gkv total r flux over the synthetic r flux of the dereddened spectrum.

Kinematics: SpecAllv27 Z (heliocentric), VelocityDispersionsv02 SIG_STARCORR and SIGERR_STARCORR
(homogenised dispersion and its error with the calibration uncertainty; Dogruel et al. 2024).

Photometry: gkvInputCatv02 total fluxes flux_<band>t and flux_err_<band>t in Jy, corrected for
Galactic extinction (gkv table notes), AB: maggies = Jy / 3631. Filters: GALEX FUV, NUV;
VST/OmegaCAM u, g, r, i (KiDS) from data/raw/gama_dr4/filters/; VISTA/VIRCAM Z, Y, J, H, Ks
(VIKING); WISE W1, W2 (Driver et al. 2022, arXiv:2203.08539, Sect. 2.1). A band leaves the
photometry when its flux is -999 (no coverage, gkv table notes) or its error is not > 0.

Checks in summary.csv: aperture_scale; synthetic g and i flux of the scaled spectrum over the
total flux; median LSF sigma in km/s; R = lambda / FWHM at 4800 and 7250 A; HEL_VC.
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
from specutils.utils.wcs_utils import air_to_vac

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "external/sedpy_jax"))
from ceridwen.dust.attenuation_laws import cardelli  # noqa: E402
from manga_aperture_spectra import read_csv, synthetic_maggies  # noqa: E402
from sedpy_jax.observate import load_filters  # noqa: E402

RAW = PROJECT_ROOT / "data/raw/gama_dr4"
PROCESSED = PROJECT_ROOT / "data/processed/gama_dr4"
FILTER_DIR = RAW / "filters"
C_KMS = C_LIGHT.to_value(u.km / u.s)
FWHM_TO_SIGMA = 1.0 / (2.0 * np.sqrt(2.0 * np.log(2.0)))
LSF_WAVE_AIR = (4800.0, 7250.0)
LSF_FWHM = (4.8, 4.5)
JY_PER_MAGGIE = 3631.0
MISSING = -999.0
GKV_FILTERS = {
    "FUV": "galex_FUV", "NUV": "galex_NUV",
    "u": "omegacam_u", "g": "omegacam_g", "r": "omegacam_r", "i": "omegacam_i",
    "Z": "vista_vircam_Z", "Y": "vista_vircam_Y", "J": "vista_vircam_J", "H": "vista_vircam_H",
    "K": "vista_vircam_Ks", "W1": "wise_w1", "W2": "wise_w2",
}


def lsf_sigma(wave_air):
    """Gaussian LSF sigma in A of a GAMA AAOmega spectrum at air wavelength wave_air (A)."""
    return np.interp(wave_air, LSF_WAVE_AIR, LSF_FWHM) * FWHM_TO_SIGMA


def gkv_maggies(row: dict) -> tuple[list, list, list, list]:
    bands, filters, maggies, maggie_errors = [], [], [], []
    for band, name in GKV_FILTERS.items():
        flux, error = float(row[f"flux_{band}t"]), float(row[f"flux_err_{band}t"])
        if flux == MISSING or not error > 0:
            continue
        bands.append(band), filters.append(name)
        maggies.append(flux / JY_PER_MAGGIE), maggie_errors.append(error / JY_PER_MAGGIE)
    return bands, filters, maggies, maggie_errors


def process(row: dict) -> dict:
    target = row["CATAID"]
    with fits.open(RAW / "spectra" / f"{row['SPECID']}.fit") as hdul:
        header, data = hdul[0].header, hdul[0].data.astype(float)
    pixel = np.arange(header["NAXIS1"]) + 1.0
    wave_air = header["CRVAL1"] + (pixel - header["CRPIX1"]) * header["CD1_1"]
    wave = air_to_vac(wave_air * u.AA).to_value(u.AA)
    flux, error = data[0], data[1]
    valid = np.isfinite(flux) & np.isfinite(error) & (error > 0)
    flux, error = np.where(valid, flux, 0.0), np.where(valid, error, 0.0)
    sigma_aa = lsf_sigma(wave_air) * wave / wave_air
    ebv = float(row["EBV"])
    extinction = 10.0 ** (0.4 * 3.1 * ebv * np.asarray(cardelli(wave, tau_card=1.0, R_v_card=3.1)))
    flux, error = flux * extinction, error * extinction

    bands, filters, maggies, maggie_errors = gkv_maggies(row)
    check = load_filters(["omegacam_g", "omegacam_r", "omegacam_i"], directory=str(FILTER_DIR))
    synthetic = synthetic_maggies(wave, flux * 1e-17, valid, check)
    aperture_scale = float(maggies[bands.index("r")] / synthetic[1])
    flux, error = flux * aperture_scale, error * aperture_scale
    record = {
        "target": target, "cataid": int(target), "specid": row["SPECID"],
        "z": float(row["Z"]), "sigma": float(row["SIG_STARCORR"]), "sigma_err": float(row["SIGERR_STARCORR"]),
        "ebvgal": ebv, "sn": float(row["SN"]), "aperture_scale": aperture_scale,
        "valid_fraction": float(valid.mean()), "bands": " ".join(bands),
        **{f"synthetic_over_total_{b}": float(aperture_scale * synthetic[k] / maggies[bands.index(b)])
           for k, b in ((0, "g"), (2, "i"))},
        "median_lsf_sigma_kms": float(np.median(C_KMS * sigma_aa[valid] / wave[valid])),
        **{f"resolution_{int(lam)}": float(lam / (lsf_sigma(lam) / FWHM_TO_SIGMA)) for lam in LSF_WAVE_AIR},
        "hel_vc_kms": float(header["HEL_VC"]),
    }

    PROCESSED.mkdir(parents=True, exist_ok=True)
    spectrum = Table({"WAVE": wave, "FLUX": flux, "ERROR": error, "VALID": valid, "LSF_SIGMA": sigma_aa})
    spectrum.meta.update({"EXTNAME": "SPECTRUM", "BUNIT": "1E-17 erg/s/cm^2/Angstrom",
                          "WAVEUNIT": "Angstrom vacuum, from air", "LSFUNIT": "Angstrom sigma, Dogruel+24"})
    photometry = Table({"BAND": bands, "FILTER": filters, "FLUX_MAGGIES": maggies, "ERROR_MAGGIES": maggie_errors})
    photometry.meta["EXTNAME"] = "PHOTOMETRY"
    primary = fits.PrimaryHDU()
    for keyword, key in (("TARGET", "target"), ("CATAID", "cataid"), ("Z", "z"), ("SIGMA", "sigma"),
                         ("SIGMAERR", "sigma_err"), ("EBVGAL", "ebvgal"), ("APERSCL", "aperture_scale")):
        primary.header[keyword] = record[key]
    fits.HDUList([primary, fits.table_to_hdu(spectrum), fits.table_to_hdu(photometry)]).writeto(
        PROCESSED / f"{target}.fits", overwrite=True)
    return record


def main() -> None:
    records = []
    for row in read_csv(RAW / "targets.csv", "SPECID").values():
        records.append(process(row))
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in records[-1].items()}, flush=True)
    with (PROCESSED / "summary.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
