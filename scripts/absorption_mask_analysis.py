#!/usr/bin/env python3
"""Analysis helpers for the absorption-line pixel-mask experiment.

Loads a LEGA-C DR2 target exactly as ``notebooks/ceridwen_integrated_photometry_spectra.ipynb``
does (same catalogue join, quality cut, unit conversions, and pixel masks),
reports the spectrum-versus-photometry weight budget of the current
likelihood, and extracts a mock truth from a stored fit.

Sub-commands::

    budget  --target M5_172669 [--target ...]   weight budget table
    truth   --result <ceridwen_result.h5> --out truth.json
    snr                                          catalogue S/N of the passive sample
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DR2_FLUX_UNIT_CGS = 1e-19  # erg s^-1 cm^-2 A^-1
C_KMS = 2.998e5
UJY_TO_MAGGIES = 1e-6 / 3631.0
PHOTOMETRY_FLOOR = 0.05
REST_EMISSION_LINES = [3726.0, 3728.8, 4861.3, 4958.9, 5006.8]
EMISSION_DV_KMS = 1500.0
TELLURIC_AIR = (7590.0, 7660.0)
FLUX_COLUMNS = [
    "Fuap3", "FBap3", "FVap3", "Frap3", "Fipap3", "Fzppap3",
    "FYap3", "FJap3", "FHap3", "FKsap3", "F3.6um", "F4.5um",
]
FILTER_NAMES = [
    "cfht_megacam_us_9301", "subaru_suprimecam_B", "subaru_suprimecam_V",
    "subaru_suprimecam_rp", "subaru_suprimecam_ip", "subaru_suprimecam_zp",
    "vista_vircam_Y", "vista_vircam_J", "vista_vircam_H", "vista_vircam_Ks",
    "spitzer_irac_ch1", "spitzer_irac_ch2",
]
PHOT_COLUMNS = [
    "Area", "Sat", "Cfl", "Deep", "Flag", "E(B-V)", "NUVMag", "RMag", "JMag",
] + [c for name in FLUX_COLUMNS for c in (name, f"e_{name}")]


def load_passive_sample(project_root: Path = PROJECT_ROOT):
    """Replicate the notebook's passive selection; returns (parent, selected)."""
    from astropy.table import Table

    legac = Table.read(project_root / "data/raw/legac_dr2/legaCdr2.fits.gz").to_pandas()
    for column in ("SPECT_ID", "Filename"):
        legac[column] = legac[column].map(
            lambda v: v.decode() if isinstance(v, bytes) else v
        )
    phot = Table.read(
        project_root / "data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits"
    ).to_pandas().set_index("LEGAC_INDEX")
    parent = legac.join(phot[PHOT_COLUMNS], how="inner")
    quality = (
        (parent["f_use"] == 1) & (parent["f_ppxf"] == 0) & (parent["f_z"] == 0)
        & (parent["f_int"] == 0) & (parent["SN"] > 0)
        & (parent["z"] >= 0.6) & (parent["z"] < 1.0)
    )
    valid_rest = (parent[["NUVMag", "RMag", "JMag"]] > -40).all(axis=1)
    parent = parent[quality & valid_rest].copy()
    nuv_r = parent["NUVMag"] - parent["RMag"]
    r_j = parent["RMag"] - parent["JMag"]
    passive = parent[(nuv_r > 3 * r_j + 1) & (nuv_r > 3.1)]
    oii_ew = passive["OII_3727_EW"]
    weak = passive[(oii_ew > -5) | oii_ew.isna()]
    oii_sig = (weak["OII_3727_EW"] / weak["OII_3727_EW_err"]).abs()
    oiii_sig = (weak["OIII_5007_EW"] / weak["OIII_5007_EW_err"]).abs()
    bona_fide = weak[~((oii_sig >= 3) | (oiii_sig >= 3))]
    clean = (
        (bona_fide["Area"] == 0) & (bona_fide["Sat"] == 0)
        & (bona_fide["Cfl"] == 1) & (bona_fide["Flag"] == 0)
    )
    usable = bona_fide[clean].copy()
    selected = (
        usable.sort_values(["SN", "SPECT_ID"], ascending=[False, True])
        .drop_duplicates("OBJECT", keep="first")
        .sort_values(["SN", "SPECT_ID"], ascending=[False, True])
    )
    assert len(usable) == 194 and len(selected) == 187
    return parent, selected


def air_to_vacuum(wave_air):
    from astropy import units as u
    from specutils.utils.wcs_utils import air_to_vac

    return air_to_vac(np.asarray(wave_air, dtype=float) * u.AA).to_value(u.AA)


def flam_to_fnu(values, wave_vacuum):
    """1e-19 erg/s/cm^2/A -> erg/s/cm^2/Hz on a vacuum grid (as the notebook)."""
    from astropy import units as u

    f_lambda = np.asarray(values, dtype=float) * DR2_FLUX_UNIT_CGS * (
        u.erg / u.s / u.cm**2 / u.AA
    )
    return f_lambda.to_value(
        u.erg / u.s / u.cm**2 / u.Hz,
        equivalencies=u.spectral_density(np.asarray(wave_vacuum) * u.AA),
    )


def load_target(spect_id: str, project_root: Path = PROJECT_ROOT) -> dict:
    """Observed arrays for one target with the notebook's masks applied."""
    from astropy.io import fits

    _, selected = load_passive_sample(project_root)
    rows = selected[selected["SPECT_ID"] == spect_id]
    if len(rows) != 1:
        raise ValueError(f"expected one eligible {spect_id} row, found {len(rows)}")
    galaxy = rows.iloc[0]
    with fits.open(project_root / "data/raw/legac_dr2/sp" / galaxy["Filename"]) as hdul:
        table = hdul[1].data
        resolution = float(hdul[0].header["SPEC_RES"])
    wave_air, flux, error, qual = (table[c][0] for c in ("WAVE", "FLUX", "ERR", "QUAL"))
    good = (qual == 0) & (error > 0) & np.isfinite(flux)
    wave_vac = air_to_vacuum(wave_air)
    flux_fnu = flam_to_fnu(flux, wave_vac)
    unc_fnu = flam_to_fnu(error, wave_vac)
    z = float(galaxy["z"])
    valid = good & np.isfinite(flux_fnu) & np.isfinite(unc_fnu) & (unc_fnu > 0)
    mask = valid.copy()
    for line in REST_EMISSION_LINES:
        centre = (1 + z) * line
        half = centre * EMISSION_DV_KMS / C_KMS
        mask &= ~((wave_vac >= centre - half) & (wave_vac <= centre + half))
    tell = air_to_vacuum(np.array(TELLURIC_AIR))
    mask &= ~((wave_vac >= tell[0]) & (wave_vac <= tell[1]))
    phot_flux = galaxy[FLUX_COLUMNS].to_numpy(dtype=float) * UJY_TO_MAGGIES
    phot_stat = galaxy[[f"e_{c}" for c in FLUX_COLUMNS]].to_numpy(dtype=float) * UJY_TO_MAGGIES
    phot_unc = np.hypot(phot_stat, PHOTOMETRY_FLOOR * np.abs(phot_flux))
    return {
        "spect_id": spect_id,
        "object_id": int(galaxy["OBJECT"]),
        "z": z,
        "sigma_star": float(galaxy["SIGMA_STARS_PRIME"]),
        "catalogue_snr": float(galaxy["SN"]),
        "resolution_fwhm": resolution,
        "wave_vac": wave_vac,
        "flux": np.nan_to_num(flux_fnu, nan=0.0),
        "uncertainty": np.where(valid, unc_fnu, 1.0),
        "valid": valid,
        "mask": mask,
        "phot_flux": phot_flux,
        "phot_uncertainty": phot_unc,
        "phot_stat": phot_stat,
    }


def weight_budget(target: dict, f_calib=(0.0, 0.01, 0.03, 0.10), feature_mask=None) -> dict:
    """Sum of (S/N)^2 over fitted pixels versus photometric bands.

    For a diagonal Gaussian the Fisher information on a pure amplitude is
    sum_i (f_i/sigma_i)^2, so this ratio is the relative weight the two
    data sets carry for any parameter that moves the flux level.
    """
    m = target["mask"]
    f = target["flux"][m]
    s = target["uncertainty"][m]
    out = {
        "n_pix": int(m.sum()),
        "median_pixel_snr": float(np.median(f / s)),
        "n_bands": int(len(target["phot_flux"])),
        "band_snr": (target["phot_flux"] / target["phot_uncertainty"]).round(2).tolist(),
        "phot_budget": float(np.sum((target["phot_flux"] / target["phot_uncertainty"]) ** 2)),
        "spectrum_budget": {},
        "ratio": {},
    }
    for fc in f_calib:
        sig_eff = np.sqrt(s**2 + (fc * f) ** 2)
        budget = float(np.sum((f / sig_eff) ** 2))
        out["spectrum_budget"][f"f_calib={fc:.2f}"] = budget
        out["ratio"][f"f_calib={fc:.2f}"] = budget / out["phot_budget"]
    if feature_mask is not None:
        fm = feature_mask[m]
        out["n_pix_in_features"] = int(fm.sum())
        out["feature_fraction"] = float(fm.mean())
        for fc in f_calib:
            sig_eff = np.sqrt(s**2 + (fc * f) ** 2)
            snr2 = (f / sig_eff) ** 2
            out["spectrum_budget"][f"features,f_calib={fc:.2f}"] = float(snr2[fm].sum())
            out["spectrum_budget"][f"continuum,f_calib={fc:.2f}"] = float(snr2[~fm].sum())
        out["balance_downweight"] = float(
            np.sqrt(np.sum((f[~fm] / s[~fm]) ** 2) / out["phot_budget"])
        )
    return out


def weighted_quantiles(values, log_weights, quantiles=(0.16, 0.5, 0.84)):
    w = np.exp(np.asarray(log_weights) - np.max(log_weights))
    w /= w.sum()
    order = np.argsort(values)
    cdf = np.cumsum(w[order])
    return [float(np.interp(q, cdf, np.asarray(values)[order])) for q in quantiles]


def posterior_summary(result_path: Path) -> dict:
    """Weighted 16/50/84 quantiles for every scalar parameter of a stored fit."""
    from ceridwen.fit import load_result_h5

    result = load_result_h5(result_path)
    summary = {}
    for name in result.param_names:
        block = np.asarray(result.samples[name])
        block = block.reshape(len(block), -1)
        for k in range(block.shape[1]):
            key = name if block.shape[1] == 1 else f"{name}[{k}]"
            summary[key] = weighted_quantiles(block[:, k], result.log_weights)
    summary["_log_evidence"] = [float(result.log_evidence), float(result.log_evidence_err)]
    summary["_n_likelihood_calls"] = int(result.n_likelihood_calls)
    return summary


def truth_from_result(result_path: Path) -> dict:
    """Weighted posterior medians in the shape ``SedModel.theta_init`` expects."""
    from ceridwen.fit import load_result_h5

    result = load_result_h5(result_path)
    truth = {}
    for name in result.param_names:
        block = np.asarray(result.samples[name]).reshape(len(result.log_weights), -1)
        truth[name] = [weighted_quantiles(block[:, k], result.log_weights)[1]
                       for k in range(block.shape[1])]
    return truth


def _cmd_budget(args):
    for spect_id in args.target:
        target = load_target(spect_id)
        feature_mask = None
        if args.features:
            from ceridwen.observation.absorption_features import absorption_feature_mask

            feature_mask = absorption_feature_mask(
                target["wave_vac"], zred=target["z"], window_kms=args.window_kms
            )
        budget = weight_budget(target, feature_mask=feature_mask)
        budget.update(z=target["z"], catalogue_snr=target["catalogue_snr"])
        print(json.dumps({spect_id: budget}, indent=1))


def _cmd_truth(args):
    truth = truth_from_result(Path(args.result))
    Path(args.out).write_text(json.dumps(truth, indent=1))
    print(json.dumps(truth, indent=1))


def _cmd_snr(args):
    _, selected = load_passive_sample()
    sn = selected["SN"].to_numpy()
    print("passive sample catalogue S/N percentiles 10/25/50/75/90:",
          np.percentile(sn, [10, 25, 50, 75, 90]).round(1).tolist())
    for spect_id in args.target:
        row = selected[selected["SPECT_ID"] == spect_id].iloc[0]
        rank = float((sn > row["SN"]).mean())
        print(f"{spect_id}: S/N={row['SN']:.1f} z={row['z']:.4f} (top {100*rank:.0f}%)")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("budget")
    b.add_argument("--target", action="append", default=[])
    b.add_argument("--features", action="store_true")
    b.add_argument("--window-kms", type=float, default=1000.0)
    b.set_defaults(func=_cmd_budget)
    t = sub.add_parser("truth")
    t.add_argument("--result", required=True)
    t.add_argument("--out", required=True)
    t.set_defaults(func=_cmd_truth)
    s = sub.add_parser("snr")
    s.add_argument("--target", action="append", default=[])
    s.set_defaults(func=_cmd_snr)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
