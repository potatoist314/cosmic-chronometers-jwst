#!/usr/bin/env python3
"""Total COSMOS photometry of a LEGA-C DR2 galaxy from each matched catalogue.

Total flux, per catalogue:

- COSMOS2015 (Laigle+16): 3" aperture flux, per-object `Offset`, Milky Way
  extinction E(B-V) F and Table 3 offset sf. IRAC is already total. This is the
  `cosmos_total` input of notebooks/ceridwen_integrated_photometry_spectra.ipynb.
- COSMOS2020 Classic (Weaver+22): 2" aperture flux and per-object `totaloff2`.
  IRAC (IRACLEAN) and GALEX are already total. The catalogue applies no Milky
  Way extinction and no zero-point offset; both are applied here.
- COSMOS2020 Farmer: total model flux; same two corrections applied here.
- COSMOS2025 (Shuntov+25): total SE++ model flux with the calibrated error.
  The catalogue has no E(B-V) column and the paper tabulates no offsets, so
  E(B-V) comes from COSMOS2020 Classic and no offset is applied.

VizieR rounds COSMOS2020 fluxes to 0.01 uJy, so fluxes come from the magnitude
columns (four decimals) and fall back to the flux column for non-detections.

`fit_photometry` returns the bands of one catalogue for the fit notebook
(`SETTINGS["photometry"]` = "cosmos2020_classic" or "cosmos2025").
"""

from pathlib import Path

import numpy as np
import pandas as pd
from astropy.table import Table

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data/raw"
SEDPY_FILTERS = PROJECT_ROOT / "external/sedpy_jax/sedpy_jax/data/filters"
FILES = {
    "cosmos2015": RAW / "cosmos2015/cosmos2015_legac_dr2_apertures_1arcsec.fits",
    "classic": RAW / "cosmos2020/cosmos2020_classic_legac_dr2_1arcsec.fits",
    "farmer": RAW / "cosmos2020/cosmos2020_farmer_legac_dr2_1arcsec.fits",
    "cosmos2025": RAW / "cosmos2025/cosmos2025_phot_legac_dr2_1arcsec.fits",
}

# Laigle+16 Table 3 foreground-extinction factors F against effective wavelength
# [angstrom]; bands outside the table are interpolated in log wavelength.
LAIGLE_F = {
    2314: 8.621, 3823: 4.660, 4263: 4.260, 4458: 4.020, 4635: 3.843, 4849: 3.621,
    5478: 3.117, 6289: 2.660, 7684: 1.991, 9106: 1.461, 10214: 1.211,
    12535: 0.871, 16453: 0.563, 21540: 0.364, 35634: 0.162, 45110: 0.111,
}

# band: (effective wavelength [angstrom], sedpy_jax filter or None,
#        {catalogue: (column stem, zero-point offset [mag])}).
# COSMOS2015 offsets are Laigle+16 Table 3 sf, subtracted from magnitudes.
# COSMOS2020 offsets are Weaver+22 Table 3 (LePhare), added to magnitudes.
BANDS = {
    "NUV": (2314, "galex_NUV", {"classic": ("GALEXNUV", 0.005), "farmer": ("GALEXNUV", -0.145)}),
    "u": (3709, None, {"classic": ("CFHTu", 0.001), "farmer": ("CFHTu", -0.092)}),
    "u*": (3858, "cfht_megacam_us_9301", {
        "cosmos2015": ("u", 0.010), "classic": ("CFHTustar", 0.058),
        "farmer": ("CFHTustar", -0.002), "cosmos2025": ("CFHT-u", 0.0)}),
    "IB427": (4266, "subaru_suprimecam_ia427", {
        "classic": ("SCIB427", -0.007), "farmer": ("SCIB427", -0.111), "cosmos2025": ("SC-IB427", 0.0)}),
    "B": (4488, "subaru_suprimecam_B", {"cosmos2015": ("B", 0.146), "classic": ("SCB", -0.069)}),
    "IB464": (4635, "subaru_suprimecam_ia464", {"classic": ("SCIB464", 0.014), "farmer": ("SCIB464", -0.057)}),
    "g": (4847, "hsc_g", {"classic": ("HSCg", 0.133), "farmer": ("HSCg", 0.058), "cosmos2025": ("HSC-g", 0.0)}),
    "IA484": (4851, "subaru_suprimecam_ia484", {
        "classic": ("SCIA484", 0.027), "farmer": ("SCIA484", -0.036), "cosmos2025": ("SC-IA484", 0.0)}),
    "V": (5487, "subaru_suprimecam_V", {"cosmos2015": ("V", -0.117), "classic": ("SCV", 0.128)}),
    "r": (6219, "hsc_r", {"classic": ("HSCr", 0.133), "farmer": ("HSCr", 0.081), "cosmos2025": ("HSC-r", 0.0)}),
    "r+": (6305, "subaru_suprimecam_rp", {"cosmos2015": ("r", -0.012), "classic": ("SCrp", 0.044)}),
    "i": (7699, "hsc_i", {"classic": ("HSCi", 0.102), "farmer": ("HSCi", 0.018), "cosmos2025": ("HSC-i", 0.0)}),
    "i+": (7693, "subaru_suprimecam_ip", {"cosmos2015": ("ip", 0.020), "classic": ("SCip", 0.058)}),
    "F814W": (8057, "acs_wfc_f814w", {"cosmos2025": ("HST-F814W", 0.0)}),
    "z": (8894, "hsc_z", {"classic": ("HSCz", 0.090), "farmer": ("HSCz", 0.019), "cosmos2025": ("HSC-z", 0.0)}),
    "z++": (9054, "subaru_suprimecam_zp", {"cosmos2015": ("zpp", -0.084), "classic": ("SCzpp", 0.101)}),
    "y": (9762, "hsc_y", {"classic": ("HSCy", 0.105), "farmer": ("HSCy", 0.070), "cosmos2025": ("HSC-y", 0.0)}),
    "Y": (10216, "vista_vircam_Y", {
        "cosmos2015": ("Y", 0.001), "classic": ("UVISTAY", 0.055),
        "farmer": ("UVISTAY", 0.039), "cosmos2025": ("UVISTA-Y", 0.0)}),
    "F115W": (11540, "jwst_f115w", {"cosmos2025": ("F115W", 0.0)}),
    "J": (12525, "vista_vircam_J", {
        "cosmos2015": ("J", 0.017), "classic": ("UVISTAJ", 0.028),
        "farmer": ("UVISTAJ", 0.005), "cosmos2025": ("UVISTA-J", 0.0)}),
    "F150W": (15010, "jwst_f150w", {"cosmos2025": ("F150W", 0.0)}),
    "H": (16466, "vista_vircam_H", {
        "cosmos2015": ("H", 0.055), "classic": ("UVISTAH", -0.043),
        "farmer": ("UVISTAH", -0.049), "cosmos2025": ("UVISTA-H", 0.0)}),
    "Ks": (21557, "vista_vircam_Ks", {
        "cosmos2015": ("Ks", -0.001), "classic": ("UVISTAKs", 0.0),
        "farmer": ("UVISTAKs", 0.0), "cosmos2025": ("UVISTA-Ks", 0.0)}),
    "F277W": (27620, "jwst_f277w", {"cosmos2025": ("F277W", 0.0)}),
    "ch1": (35686, "spitzer_irac_ch1", {
        "cosmos2015": ("3.6um", -0.025), "classic": ("IRACCH1", -0.067),
        "farmer": ("IRACCH1", -0.184), "cosmos2025": ("IRAC-ch1", 0.0)}),
    "F444W": (44040, "jwst_f444w", {"cosmos2025": ("F444W", 0.0)}),
    "ch2": (45067, "spitzer_irac_ch2", {
        "cosmos2015": ("4.5um", -0.005), "classic": ("IRACCH2", -0.091),
        "farmer": ("IRACCH2", -0.186), "cosmos2025": ("IRAC-ch2", 0.0)}),
    "IB505": (5064, "subaru_suprimecam_ia505", {
        "classic": ("SCIB505", 0.031), "farmer": ("SCIB505", -0.035), "cosmos2025": ("SC-IB505", 0.0)}),
    "IA527": (5261, "subaru_suprimecam_ia527", {
        "classic": ("SCIA527", 0.009), "farmer": ("SCIA527", -0.062), "cosmos2025": ("SC-IA527", 0.0)}),
    "IB574": (5766, "subaru_suprimecam_ia574", {
        "classic": ("SCIB574", -0.027), "farmer": ("SCIB574", -0.104), "cosmos2025": ("SC-IB574", 0.0)}),
    "IA624": (6232, "subaru_suprimecam_ia624", {
        "classic": ("SCIA624", 0.037), "farmer": ("SCIA624", -0.015), "cosmos2025": ("SC-IA624", 0.0)}),
    "IA679": (6780, "subaru_suprimecam_ia679", {
        "classic": ("SCIA679", 0.213), "farmer": ("SCIA679", 0.145), "cosmos2025": ("SC-IA679", 0.0)}),
    "IB709": (7073, "subaru_suprimecam_ia709", {
        "classic": ("SCIB709", 0.015), "farmer": ("SCIB709", -0.043), "cosmos2025": ("SC-IB709", 0.0)}),
    "IA738": (7361, "subaru_suprimecam_ia738", {
        "classic": ("SCIA738", 0.009), "farmer": ("SCIA738", -0.054), "cosmos2025": ("SC-IA738", 0.0)}),
    "IA767": (7694, "subaru_suprimecam_ia767", {
        "classic": ("SCIA767", -0.009), "farmer": ("SCIA767", -0.052), "cosmos2025": ("SC-IA767", 0.0)}),
    "IB827": (8243, "subaru_suprimecam_ia827", {
        "classic": ("SCIB827", 0.007), "farmer": ("SCIB827", -0.087), "cosmos2025": ("SC-IB827", 0.0)}),
}
CLASSIC_TOTAL_ALREADY = {"NUV", "ch1", "ch2"}
COSMOS2015_TOTAL_ALREADY = {"ch1", "ch2"}


def extinction_factor(wavelength: float) -> float:
    waves = np.array(sorted(LAIGLE_F))
    return float(np.interp(np.log(wavelength), np.log(waves), [LAIGLE_F[w] for w in waves]))


def from_magnitude(row, flux_column, mag_column, flux_error_column, mag_error_column):
    """Flux and error in uJy from AB magnitudes; the flux columns for non-detections."""
    mag, mag_error = row[mag_column], row[mag_error_column]
    if np.ma.is_masked(mag) or not np.isfinite(mag) or not 0 < mag < 50:
        return as_float(row[flux_column]), as_float(row[flux_error_column])
    flux = 10 ** (-0.4 * (float(mag) - 23.9))
    return flux, flux * float(mag_error) * np.log(10) / 2.5


def as_float(value) -> float:
    return np.nan if np.ma.is_masked(value) else float(value)


def catalogue_flux(catalogue: str, band: str, stem: str, row):
    """Return (catalogue flux, error, aperture-to-total magnitude offset)."""
    if catalogue == "cosmos2015":
        if band in COSMOS2015_TOTAL_ALREADY:
            return as_float(row[f"F{stem}"]), as_float(row[f"e_F{stem}"]), 0.0
        return as_float(row[f"F{stem}ap3"]), as_float(row[f"e_F{stem}ap3"]), float(row["Offset"])
    if catalogue == "classic":
        if band in CLASSIC_TOTAL_ALREADY:
            return (*from_magnitude(row, f"F{stem}", f"{stem}mag", f"e_F{stem}", f"e_{stem}mag"), 0.0)
        flux, error = from_magnitude(
            row, f"F{stem}ap2", f"{stem}magap2", f"e_F{stem}ap2", f"e_{stem}magap2"
        )
        return flux, error, float(row["totaloff2"])
    if catalogue == "farmer":
        return (*from_magnitude(row, f"F{stem}", f"{stem}mag", f"e_F{stem}", f"e_{stem}mag"), 0.0)
    flux, error = as_float(row[f"Flux-mod-{stem}"]), as_float(row[f"e_Flux-c-mod-{stem}"])
    if flux < -900:  # COSMOS2025 null
        return np.nan, np.nan, 0.0
    return flux, error, 0.0


def read_matches() -> dict:
    """Matched rows of every catalogue, keyed by catalogue then by LEGA-C spect_id."""
    tables = {}
    for catalogue, path in FILES.items():
        table = Table.read(path)
        ids = np.char.strip(np.asarray(table["SPECT_ID"]).astype(str))
        tables[catalogue] = dict(zip(ids, table))
    return tables


def total_photometry(tables: dict, spect_id: str, bands=None) -> pd.DataFrame:
    """Catalogue and total fluxes [uJy] of one galaxy, one row per catalogue and band."""
    ebv_row = tables["classic"].get(spect_id, tables["cosmos2015"][spect_id])
    ebv = float(ebv_row["E(B-V)"])
    rows = []
    for band in bands if bands is not None else BANDS:
        wavelength, sedpy_filter, columns = BANDS[band]
        for catalogue, (stem, zero_point) in columns.items():
            if spect_id not in tables[catalogue]:
                continue
            flux, error, offset = catalogue_flux(catalogue, band, stem, tables[catalogue][spect_id])
            sign = -1.0 if catalogue == "cosmos2015" else 1.0
            correction_mag = offset - ebv * extinction_factor(wavelength) + sign * zero_point
            scale = 10 ** (-0.4 * correction_mag)
            rows.append({
                "spect_id": spect_id, "catalogue": catalogue, "band": band,
                "wavelength_angstrom": wavelength,
                "sedpy_filter": sedpy_filter if sedpy_filter else "",
                "filter_in_sedpy_jax": bool(
                    sedpy_filter and (SEDPY_FILTERS / f"{sedpy_filter}.par").exists()
                ),
                "catalogue_flux_ujy": flux, "catalogue_error_ujy": error,
                "aperture_to_total_mag": offset, "ebv": ebv,
                "zero_point_mag": zero_point, "total_scale": scale,
                "total_flux_ujy": flux * scale, "total_error_ujy": error * scale,
            })
    return pd.DataFrame(rows)


# SETTINGS["photometry"] value: (catalogue, quality-flag column that must be 0)
FIT_CATALOGUES = {
    "cosmos2020_classic": ("classic", "FlagCOMBINED"),
    "cosmos2025": ("cosmos2025", "warn-flag"),
}


def fit_photometry(photometry: str, spect_id: str) -> pd.DataFrame:
    """Bands of one catalogue for the fit: a sedpy_jax curve and a finite total flux."""
    catalogue, flag_column = FIT_CATALOGUES[photometry]
    tables = read_matches()
    flag = int(tables[catalogue][spect_id][flag_column])
    if flag != 0:
        raise ValueError(f"{spect_id}: {catalogue} {flag_column} = {flag}")
    bands = total_photometry(tables, spect_id)
    bands = bands[
        (bands["catalogue"] == catalogue)
        & bands["filter_in_sedpy_jax"]
        & np.isfinite(bands["total_flux_ujy"])
    ]
    return bands.sort_values("wavelength_angstrom").reset_index(drop=True)
