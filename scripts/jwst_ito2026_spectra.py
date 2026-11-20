#!/usr/bin/env python3
"""Write JWST NIRSpec medium-grating spectra and DJA photometry of the Ito et al. (2026,
arXiv:2506.22642) quiescent sample in the processed-spectrum format of data/processed/sdss_dr17/.

Input: data/raw/jwst_ito2026/ from scripts/download_jwst_ito2026.py.
Output: data/processed/jwst_ito2026/<Archive|DeepDive>-<id>.fits (SPECTRUM and PHOTOMETRY tables,
fit metadata in the primary header) for the selected targets, and
data/processed/jwst_ito2026/summary.csv for all 136 galaxies.

Spectrum (extension 1 of each galaxy file)
- msaexp reductions of the medium gratings on one grid (Ito et al. 2026, Sect. 2.3):
  wavelength in um, flambda and flambda_err in erg/s/cm^2/A, valid_mask.
- Wavelengths are vacuum: msaexp fits the redshifts with the vacuum line list of
  grizli.utils.get_line_wavelengths (https://dawn-cph.github.io/dja/blog/2025/05/01/nirspec-merged-table-v4/).
- VALID: valid_mask = 1 and flambda_err > 0.
- LSF: column R is lambda / FWHM (msaexp spectrum.py: spec_R_fwhm = spec["R"]), so
  sigma = lambda / (2.355 R). It is the pre-launch curve for a uniformly illuminated shutter
  (msaexp.utils.get_default_resolution_curve).
- Aperture: the spectra are anchored to the total photometry with a polynomial of order 0-2
  (Ito et al. 2026, Sect. 2.4), so no scale is applied (APERSCL = 1).
- Galactic extinction: A = 3.1 E(B-V) k(lambda), k from ceridwen's CCM89 law with the
  O'Donnell (1994) update, as in scripts/sdss_spectra.py; E(B-V) is the SFD98 value of
  irsa_sfd_ebv.csv. The law is zero beyond 3.33 um.

Kinematics: z of the Ito et al. catalogue (<sample>_QG.fits). No stellar velocity dispersion
is published for this sample (Ito et al. 2026, Sect. 5.2: a DeepDive objective). SIGMA = 250 km/s,
the dispersion Ito et al. (Sect. 5.1) adopt for the NIRSpec medium-grating spectra; SIGMAERR =
80 km/s, so the production sigma_smooth prior (sigma_clip = 3) spans 10-490 km/s.

Photometry (extension 2): DJA SEP total fluxes in uJy (Ito et al. 2026, Sect. 2.2; Valentino
et al. 2023, ApJ 947, 20), maggies = uJy / 3631e6.
- JWST/NIRCam and HST bands only. The ground-based and IRAC bands of the DeepDive file come
  from other catalogues (Ito et al. 2026, Sect. 2.4) and are left out.
- Rows with flux -99 or error <= 0 are left out.
- Not corrected for Galactic extinction (Valentino et al. 2023, Sect. 2.3: the correction is
  applied to the eazy-py templates); dereddened here at the filter effective wavelength.
- The production model has no IGM attenuation (notebook: add_igm=False). Bands whose
  half-maximum blue edge lies below the observed Ly-alpha are left out; Ly-alpha vacuum
  1215.67 A (NIST ASD).

Selection: all three Ito et al. quiescence flags (Dn4000QG, UVJQG_ez, sSFRQG_bg) set, no X-ray
detection, valid pixels on >= 90% of the rest range of the SDSS pilot configuration
(results/sdss-pilot-2026-11-20/experiment.json), then the highest median S/N per pixel there.

Checks in summary.csv: valid fraction and median S/N in the rest range; synthetic flux of the
dereddened spectrum over the photometry for each band inside the valid spectrum (median);
median LSF sigma in km/s; number of photometric bands kept.
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
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from ceridwen.dust.attenuation_laws import cardelli  # noqa: E402
from manga_aperture_spectra import synthetic_maggies  # noqa: E402
from sedpy_jax.observate import load_filters  # noqa: E402

RAW = PROJECT_ROOT / "data/raw/jwst_ito2026"
PROCESSED = PROJECT_ROOT / "data/processed/jwst_ito2026"
C_KMS = C_LIGHT.to_value(u.km / u.s)
FILE_PREFIX = {"Archive": "DJAgrating", "DeepDive": "DeepDive"}
LYMAN_ALPHA = 1215.67
SIGMA, SIGMA_ERR = 250.0, 80.0
REST_RANGE = (4074.5, 4666.1)
N_TARGETS = 10
HST = {"f435w": "acs_wfc_f435w", "f606w": "acs_wfc_f606w", "f775w": "acs_wfc_f775w", "f814w": "acs_wfc_f814w",
       **{band: f"wfc3_ir_{band}" for band in ("f105w", "f110w", "f125w", "f140w", "f160w")}}
NIRCAM = {band: f"jwst_{band}" for band in ("f090w", "f115w", "f150w", "f200w", "f277w", "f356w", "f410m", "f444w")}
FILTERS = {**HST, **NIRCAM}


def deredden(wave, ebv):
    return 10.0 ** (0.4 * 3.1 * ebv * np.asarray(cardelli(wave, tau_card=1.0, R_v_card=3.1)))


def process(sample: str, galaxy, ebv: float) -> tuple[dict, fits.HDUList]:
    target = f"{sample}-{galaxy['id']}"
    path = RAW / f"{sample}_SEPphot" / "data" / f"{FILE_PREFIX[sample]}-{galaxy['id']}.fits"
    data, phot = fits.getdata(path, 1), fits.getdata(path, 2)
    z = float(galaxy["z"])
    wave = data["wavelength"].astype(float) * 1e4
    error = data["flambda_err"].astype(float) / 1e-17
    valid = (data["valid_mask"] == 1) & (error > 0)
    extinction = deredden(wave, ebv)
    flux, error = data["flambda"].astype(float) / 1e-17 * extinction, error * extinction
    lsf_sigma = wave / (2.355 * data["R"].astype(float))

    keep = np.array([str(name).strip() in FILTERS for name in phot["filter"]]) & (phot["fnu"] != -99) & (phot["fnu_err"] > 0)
    bands = [str(name).strip() for name in phot["filter"][keep]]
    filters = load_filters([FILTERS[band] for band in bands])
    lyman = np.array([float(f.blue_edge) > (1.0 + z) * LYMAN_ALPHA for f in filters])
    bands, filters = [b for b, k in zip(bands, lyman) if k], [f for f, k in zip(filters, lyman) if k]
    wave_eff = np.array([float(f.wave_effective) for f in filters])
    scale = 1e-6 / 3631.0 * deredden(wave_eff, ebv)
    maggies = phot["fnu"][keep][lyman].astype(float) * scale
    maggie_errors = phot["fnu_err"][keep][lyman].astype(float) * scale

    inside = [k for k, f in enumerate(filters)
              if wave[valid].min() < float(f.blue_edge) and float(f.red_edge) < wave[valid].max()]
    synthetic = synthetic_maggies(wave, flux * 1e-17, valid, [filters[k] for k in inside]) if inside else []
    rest = (wave / (1.0 + z) >= REST_RANGE[0]) & (wave / (1.0 + z) <= REST_RANGE[1])
    record = {
        "target": target, "sample": sample, "itoid": int(galaxy["id"]), "z": z,
        "ra": float(galaxy["ra"]), "dec": float(galaxy["dec"]), "ebvgal": ebv,
        "quiescent_all": bool(galaxy["Dn4000QG"] == 1 and galaxy["UVJQG_ez"] == 1 and galaxy["sSFRQG_bg"] == 1),
        "xray_detection": int(galaxy["Xray_detection"]), "sn50_opt": float(galaxy["sn50_opt"]),
        "rest_valid_fraction": float(valid[rest].mean()) if rest.any() else 0.0,
        "rest_median_sn": float(np.median(flux[rest & valid] / error[rest & valid])) if (rest & valid).any() else 0.0,
        "n_bands": len(bands), "bands": " ".join(bands),
        "synthetic_over_phot_median": float(np.median(np.asarray(synthetic) / maggies[inside])) if inside else np.nan,
        "synthetic_bands": " ".join(bands[k] for k in inside),
        "median_lsf_sigma_kms": float(np.median(C_KMS * lsf_sigma / wave)),
    }

    spectrum = Table({"WAVE": wave, "FLUX": flux, "ERROR": error, "VALID": valid, "LSF_SIGMA": lsf_sigma})
    spectrum.meta.update({"EXTNAME": "SPECTRUM", "BUNIT": "1E-17 erg/s/cm^2/Angstrom",
                          "WAVEUNIT": "Angstrom vacuum", "LSFUNIT": "Angstrom sigma, lambda / (2.355 R)"})
    photometry = Table({"BAND": bands, "FILTER": [FILTERS[b] for b in bands],
                        "FLUX_MAGGIES": maggies, "ERROR_MAGGIES": maggie_errors})
    photometry.meta["EXTNAME"] = "PHOTOMETRY"
    primary = fits.PrimaryHDU()
    for keyword, value in (("TARGET", target), ("ITOID", record["itoid"]), ("Z", z), ("SIGMA", SIGMA),
                           ("SIGMAERR", SIGMA_ERR), ("EBVGAL", ebv), ("APERSCL", 1.0)):
        primary.header[keyword] = value
    return record, fits.HDUList([primary, fits.table_to_hdu(spectrum), fits.table_to_hdu(photometry)])


def main() -> None:
    with (RAW / "irsa_sfd_ebv.csv").open() as stream:
        ebv = {f"{row['sample']}-{row['id']}": float(row["ebv_sfd"]) for row in csv.DictReader(stream)}
    records, files = [], {}
    for sample in FILE_PREFIX:
        for galaxy in Table.read(RAW / f"{sample}_SEPphot" / f"{sample}_QG.fits"):
            record, hdus = process(sample, galaxy, ebv[f"{sample}-{galaxy['id']}"])
            records.append(record)
            files[record["target"]] = hdus
    eligible = [r for r in records
                if r["quiescent_all"] and r["xray_detection"] != 1 and r["rest_valid_fraction"] >= 0.9]
    selected = {r["target"] for r in sorted(eligible, key=lambda r: -r["rest_median_sn"])[:N_TARGETS]}
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for record in records:
        record["selected"] = record["target"] in selected
        if record["selected"]:
            files[record["target"]].writeto(PROCESSED / f"{record['target']}.fits", overwrite=True)
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in record.items()}, flush=True)
    with (PROCESSED / "summary.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"eligible {len(eligible)} of {len(records)}; selected {len(selected)}", flush=True)


if __name__ == "__main__":
    main()
