#!/usr/bin/env python3
"""Write VANDELS DR4 VIMOS spectra and their CANDELS photometry in the processed-spectrum
format of data/processed/manga_dr17/.

Input: data/raw/vandels_dr4/ from scripts/download_vandels_dr4.py.
Output: data/processed/vandels_dr4/<id>.fits (SPECTRUM and PHOTOMETRY tables, fit metadata in
the primary header) and data/processed/vandels_dr4/summary.csv.

Spectrum (ESO 1D format, Garilli et al. 2021, A&A 647, A150, Sect. 8)
- WAVE in air (Sect. 8), to vacuum with specutils air_to_vac. Header SPECSYS = TOPOCENT;
  zspec is measured on the same spectra.
- FLUX (blue-end corrected, Sect. 4.1) and ERR in erg/s/cm^2/A, here in 1E-17 of that.
- VALID: ERR > 0 and 4800 <= WAVE <= 9800 A air, the MR grism range (Sect. 3).
- LSF: header SPEC_RES = 580 (ESO archive), taken as lambda / FWHM: sigma = lambda / (2.355 x 580).
- Galactic extinction: no VANDELS or CANDELS source states it (Garilli+2021; McLure et al. 2018;
  Guo et al. 2013; Galametz et al. 2013). The spectra are normalised to the photometry (Garilli+2021
  Sect. 4), so both are corrected with one E(B-V): the SFD98 value of targets.csv,
  A = 3.1 E(B-V) k(lambda), k from ceridwen's CCM89 law with the O'Donnell (1994) update, as in
  scripts/sdss_spectra.py; photometry at each filter's effective wavelength. IRAC is beyond the
  law's range (k = 0).
- Aperture: flux and error multiplied by one scalar, the catalogue i-band flux (i_FILTER: HST F775W
  in CDFS, Subaru i' in UDS; Garilli+2021 Sect. 5 normalise the shown spectra to i_AB) over the
  synthetic i flux of the dereddened spectrum.

Photometry: the release columns in uJy (download_vandels_dr4.py), the CANDELS total fluxes of the HST
regions: GOODS-S (Guo et al. 2013, ApJS 207, 24, Table 1) and UDS (Galametz et al. 2013, ApJS 206, 10,
Table 1). FILTERS maps each column to a sedpy filter; CFHT/MegaCam u is u* (Galametz Table 1: 386 nm).
HAWK-I Y and Ks have no sedpy filter and are left out.

Kinematics: VANDELS publishes no stellar velocity dispersion. SIGMA and SIGMAERR are the median and
standard deviation of sigma_star_kms over the 187 LEGA-C DR2 quiescent fits in
results/dr2-quiescent-new-defaults-summary.csv: a population prior, not a measurement.

OBJID: the number of the VANDELS id plus 1000000 (CDFS) or 2000000 (UDS), unique across fields.
"""

from __future__ import annotations

import csv
import statistics
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

RAW = PROJECT_ROOT / "data/raw/vandels_dr4"
PROCESSED = PROJECT_ROOT / "data/processed/vandels_dr4"
LEGAC_SIGMA = PROJECT_ROOT / "results/dr2-quiescent-new-defaults-summary.csv"
C_KMS = C_LIGHT.to_value(u.km / u.s)
SPEC_RES = 580.0
VIMOS_AIR = (4800.0, 9800.0)
UJY_TO_MAGGIES = 1e-6 / 3631.0
FIELD_OFFSET = {"CDFS": 1_000_000, "UDS": 2_000_000}
I_BAND = {"HST_F775W": "F775W", "SUBARU_i_prime": "i_SUBARU"}
FILTERS = {
    "U_VIMOS": "vlt_vimos_U", "U_CFHT": "cfht_megacam_us_9301",
    "F435W": "acs_wfc_f435w", "B_SUBARU": "subaru_suprimecam_B", "V_SUBARU": "subaru_suprimecam_V",
    "F606W": "acs_wfc_f606w", "R_SUBARU": "subaru_suprimecam_Rc", "i_SUBARU": "subaru_suprimecam_ip",
    "F775W": "acs_wfc_f775w", "F814W": "acs_wfc_f814w", "F850LP": "acs_wfc_f850lp",
    "z_SUBARU": "subaru_suprimecam_zp", "F098M": "wfc3_ir_f098m", "F105W": "wfc3_ir_f105w",
    "F125W": "wfc3_ir_f125w", "J_WFCAM": "ukirt_wfcam_J", "F160W": "wfc3_ir_f160w",
    "H_WFCAM": "ukirt_wfcam_H", "Ks_ISAAC": "vlt_isaac_Ks", "K_WFCAM": "ukirt_wfcam_K",
    "CH1_IRAC": "spitzer_irac_ch1", "CH2_IRAC": "spitzer_irac_ch2",
}


def legac_sigma() -> tuple[float, float]:
    values = [float(row["sigma_star_kms"]) for row in csv.DictReader(LEGAC_SIGMA.open())]
    return statistics.median(values), statistics.pstdev(values)


def process(row: dict, sigma: float, sigma_err: float) -> dict:
    target = row["id"]
    data = fits.getdata(RAW / "spectra" / row["FILENAME"], 1)
    wave_air = data["WAVE"][0].astype(float)
    wave = air_to_vac(wave_air * u.AA).to_value(u.AA)
    flux, error = data["FLUX"][0].astype(float) * 1e17, data["ERR"][0].astype(float) * 1e17
    valid = (error > 0) & (wave_air >= VIMOS_AIR[0]) & (wave_air <= VIMOS_AIR[1])
    lsf_sigma = wave / (2.355 * SPEC_RES)
    ebv = float(row["ebv_sfd"])
    extinction = 10.0 ** (0.4 * 3.1 * ebv * np.asarray(cardelli(wave, tau_card=1.0, R_v_card=3.1)))
    flux, error = flux * extinction, error * extinction

    bands = [band for band in FILTERS if row[band] and float(row[f"{band}_err"]) > 0]
    filters = load_filters([FILTERS[band] for band in bands])
    a_band = 3.1 * ebv * np.asarray(cardelli(np.array([float(f.wave_effective) for f in filters]),
                                             tau_card=1.0, R_v_card=3.1))
    scale = 10.0 ** (0.4 * a_band) * UJY_TO_MAGGIES
    maggies = np.array([float(row[band]) for band in bands]) * scale
    maggie_errors = np.array([float(row[f"{band}_err"]) for band in bands]) * scale

    i_band = I_BAND[row["i_FILTER"]]
    synthetic = synthetic_maggies(wave, flux * 1e-17, valid, [filters[bands.index(i_band)]])
    aperture_scale = float(maggies[bands.index(i_band)] / synthetic[0])
    flux, error = flux * aperture_scale, error * aperture_scale
    field, number = target.split("_")[1:]
    record = {
        "target": target, "objid": FIELD_OFFSET[field] + int(number), "z": float(row["zspec"]),
        "zflg": row["zflg"], "sigma": sigma, "sigma_err": sigma_err, "ebvgal": ebv, "snr": float(row["SNR"]),
        "aperture_scale": aperture_scale, "aperture_band": i_band, "valid_fraction": float(valid.mean()),
        "n_bands": len(bands), "median_lsf_sigma_kms": float(np.median(C_KMS * lsf_sigma / wave)),
    }

    PROCESSED.mkdir(parents=True, exist_ok=True)
    spectrum = Table({"WAVE": wave, "FLUX": flux, "ERROR": error, "VALID": valid, "LSF_SIGMA": lsf_sigma})
    spectrum.meta.update({"EXTNAME": "SPECTRUM", "BUNIT": "1E-17 erg/s/cm^2/Angstrom",
                          "WAVEUNIT": "Angstrom vacuum topocentric", "LSFUNIT": "Angstrom sigma, SPEC_RES"})
    photometry = Table({"BAND": bands, "FILTER": [FILTERS[band] for band in bands],
                        "FLUX_MAGGIES": maggies, "ERROR_MAGGIES": maggie_errors})
    photometry.meta["EXTNAME"] = "PHOTOMETRY"
    primary = fits.PrimaryHDU()
    for keyword, key in (("TARGET", "target"), ("OBJID", "objid"), ("Z", "z"), ("SIGMA", "sigma"),
                         ("SIGMAERR", "sigma_err"), ("EBVGAL", "ebvgal"), ("APERSCL", "aperture_scale")):
        primary.header[keyword] = record[key]
    fits.HDUList([primary, fits.table_to_hdu(spectrum), fits.table_to_hdu(photometry)]).writeto(
        PROCESSED / f"{target}.fits", overwrite=True)
    return record


def main() -> None:
    sigma, sigma_err = legac_sigma()
    records = []
    for row in read_csv(RAW / "targets.csv", "id").values():
        records.append(process(row, sigma, sigma_err))
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in records[-1].items()}, flush=True)
    with (PROCESSED / "summary.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
