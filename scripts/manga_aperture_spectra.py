#!/usr/bin/env python3
"""Sum MaNGA DR17 cube spaxels inside the NSA elliptical Petrosian aperture and pair
the spectrum with NSA FNugriz and WISE W1, W2 photometry of the same aperture.

Input: data/raw/manga_dr17/ from scripts/download_manga_dr17.py.
Output: data/processed/manga_dr17/<plateifu>.fits (SPECTRUM and PHOTOMETRY tables,
fit metadata in the primary header) and data/processed/manga_dr17/summary.csv.

Spectrum
- Aperture: ellipse of major-axis radius 2 ELPETRO_THETA, axis ratio ELPETRO_BA,
  position angle ELPETRO_PHI east of north (Wake et al. 2017, AJ 154, 86), centred on
  the drpall object position. Each spaxel enters with the fraction of its area inside
  the ellipse (10 x 10 subsamples).
- A spaxel pixel is clean when IVAR > 0 and none of the DRP3PIXMASK bits NOCOV, LOWCOV,
  DEADFIBER, FORESTAR, DONOTUSE is set (sdssMaskbits.par). Each summed pixel is the sum
  of the clean spaxel pixels divided by their share of the aperture light (aperture
  weight times the cube r-band image RIMG). A summed pixel is valid when that share is
  at least 0.98, so the rescaling replaces at most 2% of the light.
- Error: the sum of the spaxel variances times the covariance ratio C = T Sigma T^T
  over T Sigma_diag T^T, from the cube's g, r, i and z correlation matrices, linear in
  wavelength between their reference wavelengths and constant beyond (MaNGA DR17,
  "Working with MaNGA data", spatial covariance).
- LSF: LSFPOST, the 1-sigma post-pixelisation LSF in Angstrom (DR17 cube datamodel);
  Ceridwen's instrument width includes pixelisation and samples profiles at pixel
  centres (ceridwen/broadening.py). Spaxels combine as sum(u sigma^2) / sum(u), with
  u the aperture weight times the cube r-band image.
- Galactic extinction: A = 3.1 EBVGAL k(lambda), k from ceridwen's CCM89 law with
  the O'Donnell (1994) optical update, the law of the SFD98 E(B-V) behind EBVGAL and
  the NSA EXTINCTION column. Wavelengths are vacuum heliocentric (Law et al. 2016,
  AJ 152, 83).

Kinematics (DAP MAPS, HYB10-MILESHC-MASTARSSP)
- STELLAR_VEL is relative to the input redshift cz = SCINPVEL; the dispersion is
  STELLAR_SIGMA^2 - STELLAR_SIGMACORR[0]^2 (DR17 MAPS datamodel). Weights u as above,
  over spaxels with clean velocity and dispersion masks.
- z: (1 + SCINPVEL/c)(1 + v_mean/c) - 1. sigma: the u-weighted V_rms about v_mean,
  the line-of-sight broadening of the summed spectrum. sigma_err: 10% of sigma, the
  median fractional SIGMA_STARS_PRIME error in LEGA-C DR2.

Photometry
- FNugriz: NSA ELPETRO_NMGY, the Galactic-extinction corrected AB flux; statistical
  error ELPETRO_FLUX_IVAR^-1/2 scaled by NMGY/FLUX.
- W1, W2: wiseForcedTarget fluxes are Vega nanomaggies; AB offsets 2.699 and 3.339 mag
  (WISE All-Sky Explanatory Supplement, Sect. IV.4.h, Table 3). The forced photometry
  uses the SDSS r-band cModel profile (Lang, Hogg & Schlegel 2016), so the fluxes scale
  by NSA ELPETRO_FLUX_r / SDSS cModelFlux_r to the Petrosian aperture. Not dereddened.

Checks in summary.csv: aperture_area_covered, the smallest share of the aperture area on
spaxels without NOCOV at any wavelength (bundle coverage of the aperture); and the
synthetic g, r, i, z flux of the summed spectrum over the NSA flux in each band.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from astropy import units as u
from astropy.constants import c as C_LIGHT
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "external/sedpy_jax"))
from ceridwen.dust.attenuation_laws import cardelli  # noqa: E402
from sedpy_jax.observate import load_filters  # noqa: E402

RAW = PROJECT_ROOT / "data/raw/manga_dr17"
PROCESSED = PROJECT_ROOT / "data/processed/manga_dr17"
DAPTYPE = "HYB10-MILESHC-MASTARSSP"
BAD_PIXEL_BITS = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 10)
C_KMS = C_LIGHT.to_value(u.km / u.s)
SIGMA_FRACTIONAL_ERROR = 0.10
MIN_CLEAN_LIGHT = 0.98
NSA_BANDS = {"f": ("FUV", "galex_FUV"), "n": ("NUV", "galex_NUV"), "u": ("u", "sdss_u0"),
             "g": ("g", "sdss_g0"), "r": ("r", "sdss_r0"), "i": ("i", "sdss_i0"), "z": ("z", "sdss_z0")}
WISE_AB_OFFSET = {"w1": 2.699, "w2": 3.339}
WISE_FILTERS = {"w1": ("W1", "wise_w1"), "w2": ("W2", "wise_w2")}
SUBSAMPLE = 10


def read_csv(path: Path, key: str) -> dict[str, dict]:
    with path.open() as stream:
        return {row[key]: row for row in csv.DictReader(stream)}


def aperture_weights(header, shape, ra, dec, major_arcsec, ba, phi_deg) -> np.ndarray:
    """Fraction of each spaxel inside the ellipse; offsets east and north of (ra, dec)."""
    ny, nx = shape
    step = (np.arange(SUBSAMPLE) + 0.5) / SUBSAMPLE - 0.5
    y, x = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij")
    full = (ny, nx, SUBSAMPLE, SUBSAMPLE)
    xs = np.broadcast_to(x[..., None, None] + step[None, None, None, :], full).ravel()
    ys = np.broadcast_to(y[..., None, None] + step[None, None, :, None], full).ravel()
    sky = WCS(header).celestial.pixel_to_world(xs, ys)
    centre = SkyCoord(ra * u.deg, dec * u.deg, frame=sky.frame.replicate_without_data())
    east, north = centre.spherical_offsets_to(sky)
    east, north = east.to_value(u.arcsec), north.to_value(u.arcsec)
    phi = np.radians(phi_deg)
    along = east * np.sin(phi) + north * np.cos(phi)
    across = east * np.cos(phi) - north * np.sin(phi)
    inside = (along / major_arcsec) ** 2 + (across / (major_arcsec * ba)) ** 2 <= 1.0
    return inside.reshape(ny, nx, SUBSAMPLE * SUBSAMPLE).mean(axis=-1)


def covariance_ratio(hdulist, weights, ivar, wave) -> tuple[np.ndarray, np.ndarray]:
    """sqrt(w Sigma w / w Sigma_diag w) at the g, r, i, z reference wavelengths."""
    ny, nx = weights.shape
    reference, ratio = [], []
    for band in "GRIZ":
        hdu = hdulist[f"{band}CORREL"]
        channel = int(np.argmin(np.abs(wave - hdu.header["BBWAVE"])))
        with np.errstate(divide="ignore"):
            sigma = np.where(ivar[channel] > 0, 1.0 / np.sqrt(ivar[channel]), 0.0)
        ws = (weights * sigma).T  # indexed [x, y]: INDX*_C1 is the x (column) index
        rows = hdu.data
        off = (rows["INDXI_C1"] != rows["INDXJ_C1"]) | (rows["INDXI_C2"] != rows["INDXJ_C2"])
        pairs = np.sum(ws[rows["INDXI_C1"][off], rows["INDXI_C2"][off]]
                       * ws[rows["INDXJ_C1"][off], rows["INDXJ_C2"][off]] * rows["RHOIJ"][off])
        diagonal = np.sum(ws**2)
        if hdu.header["COVSHAPE"].replace(" ", "") != f"({nx * ny},{nx * ny})":
            raise ValueError(f"{band}CORREL COVSHAPE {hdu.header['COVSHAPE']} does not match the cube")
        reference.append(hdu.header["BBWAVE"])
        ratio.append(np.sqrt((diagonal + 2.0 * pairs) / diagonal))
    return np.array(reference), np.array(ratio)


def kinematics(maps_path: Path, weights, rimg) -> dict:
    with fits.open(maps_path) as maps:
        z_input = maps[0].header["SCINPVEL"] / C_KMS
        velocity = maps["STELLAR_VEL"].data
        dispersion2 = maps["STELLAR_SIGMA"].data ** 2 - maps["STELLAR_SIGMACORR"].data[0] ** 2
        clean = (maps["STELLAR_VEL_MASK"].data == 0) & (maps["STELLAR_SIGMA_MASK"].data == 0)
    if velocity.shape != weights.shape:
        raise ValueError(f"MAPS grid {velocity.shape} differs from the cube grid {weights.shape}")
    light = weights * np.clip(rimg, 0.0, None)
    used = light * clean
    v_mean = np.sum(used * velocity) / np.sum(used)
    v_rms = np.sqrt(np.sum(used * ((velocity - v_mean) ** 2 + dispersion2)) / np.sum(used))
    return {"z": (1.0 + z_input) * (1.0 + v_mean / C_KMS) - 1.0, "z_input": z_input, "v_mean": v_mean,
            "sigma": v_rms, "kinematics_light_fraction": np.sum(used) / np.sum(light)}


def synthetic_maggies(wave, flam_cgs, valid, filters) -> np.ndarray:
    filled = np.interp(wave, wave[valid], flam_cgs[valid])
    return np.array([10.0 ** (-0.4 * float(f.ab_mag(wave, filled))) for f in filters])


def process(plateifu: str, nsa: dict, sdss_wise: dict) -> dict:
    plate, ifu = plateifu.split("-")
    with fits.open(RAW / "cubes" / f"manga-{plate}-{ifu}-LOGCUBE.fits.gz") as cube:
        header = cube["FLUX"].header
        flux, ivar, mask = cube["FLUX"].data, cube["IVAR"].data, cube["MASK"].data
        lsf, wave, rimg = cube["LSFPOST"].data, cube["WAVE"].data.astype(float), cube["RIMG"].data
        ebv = float(cube[0].header["EBVGAL"])
        drp = fits.getdata(RAW / "drpall-v3_1_1.fits", "MANGA")
        row = drp[drp["plateifu"] == plateifu][0]
        major = 2.0 * float(nsa["elpetro_theta"])
        weights = aperture_weights(header, flux.shape[1:], float(row["objra"]), float(row["objdec"]),
                                   major, float(nsa["elpetro_ba"]), float(nsa["elpetro_phi"]))
        reference_wave, ratio = covariance_ratio(cube, weights, ivar, wave)
    used = weights > 0
    w = weights[used]
    f, iv, m, s = flux[:, used], ivar[:, used], mask[:, used], lsf[:, used]
    clean = (iv > 0) & ((m & BAD_PIXEL_BITS) == 0)
    light = w * np.clip(rimg[used], 0.0, None)
    clean_share = clean @ light / light.sum()
    covered_area = ((m & 1) == 0) @ w / w.sum()  # DRP3PIXMASK bit 0, NOCOV
    valid = clean_share >= MIN_CLEAN_LIGHT
    share = np.where(clean_share > 0, clean_share, 1.0)
    summed = np.where(clean, f, 0.0) @ w / share
    with np.errstate(divide="ignore"):
        naive = np.sqrt(np.where(clean, 1.0 / iv, 0.0) @ w**2) / share
    error = naive * np.interp(wave, reference_wave, ratio)
    with np.errstate(invalid="ignore"):
        lsf_sigma = np.sqrt(np.where(clean, s**2, 0.0) @ light / (clean @ light))
    lsf_sigma = np.interp(wave, wave[valid], lsf_sigma[valid])  # width at invalid pixels: nearest valid values
    extinction = 10.0 ** (0.4 * 3.1 * ebv * np.asarray(cardelli(wave, tau_card=1.0, R_v_card=3.1)))
    summed, error = summed * extinction, error * extinction
    kin = kinematics(RAW / "maps" / f"manga-{plate}-{ifu}-MAPS-{DAPTYPE}.fits.gz", weights, rimg)

    bands, filters, maggies, maggie_errors = [], [], [], []
    for key, (label, name) in NSA_BANDS.items():
        nmgy, raw_flux = float(nsa[f"elpetro_nmgy_{key}"]), float(nsa[f"elpetro_flux_{key}"])
        bands.append(label), filters.append(name)
        maggies.append(nmgy * 1e-9)
        maggie_errors.append(float(nsa[f"elpetro_flux_ivar_{key}"]) ** -0.5 * nmgy / raw_flux * 1e-9)
    if sdss_wise["has_wise_phot"] != "True":
        raise ValueError(f"{plateifu}: no WISE forced photometry")
    aperture_correction = float(nsa["elpetro_flux_r"]) / float(sdss_wise["cModelFlux_r"])
    for key, (label, name) in WISE_FILTERS.items():
        scale = 10.0 ** (-0.4 * WISE_AB_OFFSET[key]) * aperture_correction * 1e-9
        bands.append(label), filters.append(name)
        maggies.append(float(sdss_wise[f"{key}_nanomaggies"]) * scale)
        maggie_errors.append(float(sdss_wise[f"{key}_nanomaggies_ivar"]) ** -0.5 * scale)

    check = load_filters(["sdss_g0", "sdss_r0", "sdss_i0", "sdss_z0"])
    synthetic = synthetic_maggies(wave, summed * 1e-17, valid, check)
    record = {
        "plateifu": plateifu, "nsaid": int(nsa["nsaid"]), "z_nsa": float(row["nsa_z"]), **kin,
        "sigma_err": SIGMA_FRACTIONAL_ERROR * kin["sigma"], "ebvgal": ebv,
        "aperture_major_arcsec": major, "aperture_ba": float(nsa["elpetro_ba"]),
        "aperture_phi_deg": float(nsa["elpetro_phi"]), "spaxels": int(used.sum()),
        "spaxel_weight_sum": float(w.sum()), "aperture_area_covered": float(covered_area.min()),
        "valid_fraction": float(valid.mean()),
        "median_valid_clean_share": float(np.median(clean_share[valid])),
        **{f"covariance_ratio_{b}": float(r) for b, r in zip("griz", ratio)},
        **{f"synthetic_over_nsa_{b}": float(s / maggies[bands.index(b)]) for b, s in zip("griz", synthetic)},
        "wise_aperture_correction": aperture_correction,
        "wise_treated_as_pointsource": sdss_wise["treated_as_pointsource"],
        "median_lsf_sigma_kms": float(np.median(C_KMS * lsf_sigma / wave)),
    }

    PROCESSED.mkdir(parents=True, exist_ok=True)
    spectrum = Table({"WAVE": wave, "FLUX": summed, "ERROR": error, "VALID": valid, "LSF_SIGMA": lsf_sigma})
    spectrum.meta.update({"EXTNAME": "SPECTRUM", "BUNIT": "1E-17 erg/s/cm^2/Angstrom",
                          "WAVEUNIT": "Angstrom vacuum heliocentric", "LSFUNIT": "Angstrom sigma, LSFPOST"})
    photometry = Table({"BAND": bands, "FILTER": filters, "FLUX_MAGGIES": maggies, "ERROR_MAGGIES": maggie_errors})
    photometry.meta["EXTNAME"] = "PHOTOMETRY"
    primary = fits.PrimaryHDU()
    for keyword, key in (("PLATEIFU", "plateifu"), ("NSAID", "nsaid"), ("Z", "z"), ("Z_NSA", "z_nsa"),
                         ("SIGMA", "sigma"), ("SIGMAERR", "sigma_err"), ("EBVGAL", "ebvgal"),
                         ("APERMAJ", "aperture_major_arcsec")):
        primary.header[keyword] = record[key]
    fits.HDUList([primary, fits.table_to_hdu(spectrum), fits.table_to_hdu(photometry)]).writeto(
        PROCESSED / f"{plateifu}.fits", overwrite=True)
    return record


def main() -> None:
    nsa = read_csv(RAW / "nsa_candidates.csv", "nsaid")
    sdss_wise = read_csv(RAW / "sdss_wise.csv", "plateifu")
    records = []
    for target in read_csv(RAW / "targets.csv", "plateifu").values():
        records.append(process(target["plateifu"], nsa[target["nsaid"]], sdss_wise[target["plateifu"]]))
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in records[-1].items()}, flush=True)
    with (PROCESSED / "summary.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
