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
    f = sub.add_parser("fisher")
    f.add_argument("--target", default="M5_172669")
    f.add_argument("--truth", required=True)
    f.add_argument("--window-kms", type=float, default=1000.0)
    f.add_argument("--out", required=True)
    f.set_defaults(func=_cmd_fisher)
    args = parser.parse_args(argv)
    return args.func(args)




# ---------------------------------------------------------------------------
# Fisher-information forecast: per-parameter weight of spectrum vs photometry
# ---------------------------------------------------------------------------

LOOKBACK_TEMPLATE_GYR = [0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 5.0]
FIXED_DUST_INDEX = -0.7


def build_notebook_model(target: dict):
    """The joint model of the notebook (full_spectrum mode) for one target."""
    import jax.numpy as jnp
    from ceridwen.cosmology import age_gyr
    from ceridwen.csp import CSPBasis_afe
    from ceridwen.model import SedModel, logsfr_ratios_to_sfh
    from ceridwen.observation import Photometry, Spectrum
    from ceridwen.sampler.priors import ClippedNormal, Uniform
    from ceridwen.ssps import SSPDataAfe, fetch_grid

    ssp = SSPDataAfe.load(fetch_grid("amist_c3k_hr_krou_afe"))
    z = target["z"]
    lookback = np.array([*LOOKBACK_TEMPLATE_GYR, float(age_gyr(z))])
    phot_obs = Photometry(
        filters=FILTER_NAMES, flux=target["phot_flux"],
        uncertainty=target["phot_uncertainty"], mask=np.ones(len(FILTER_NAMES), bool),
        name="photometry",
    )
    spec_obs = Spectrum(
        wavelength=target["wave_vac"], flux=target["flux"], uncertainty=target["uncertainty"],
        mask=target["mask"], resolution=target["resolution_fwhm"], smoothtype="R",
        res_convention="fwhm", sigma_losvd=target["sigma_star"], name="spectrum",
    )
    z_bounds = (float(ssp.ssp_lgmet.min()) + 1e-4, float(ssp.ssp_lgmet.max()) - 1e-4)
    afe_bounds = (float(ssp.ssp_afe.min()), float(ssp.ssp_afe.max()))
    csp = CSPBasis_afe(
        ssp,
        theta={
            "lookback_time": jnp.asarray(lookback), "sfh": jnp.ones(len(lookback)),
            "Z": jnp.array([-1.85]), "afe": jnp.array([0.2]),
            "diffuse_tau_kc": jnp.array([0.2]), "diffuse_dust_index": jnp.array([FIXED_DUST_INDEX]),
        },
        zh_const=True, sfh_interp="step", add_dust=False, add_diffuse_dust=True,
        add_dust_emission=False, add_igm=False, sigma_losvd_kms=0.0,
        track_zred_age=False, verbose=False,
    )
    sfh_times = np.asarray(csp.sfh_times)
    transforms = {
        "sfh": lambda free: logsfr_ratios_to_sfh(free["logsfr_ratios"], sfh_times_yr=sfh_times),
        "diffuse_dust_index": lambda free: jnp.array([FIXED_DUST_INDEX]),
    }
    priors = {
        "logsfr_ratios": Uniform(low=-3.0, high=3.0),
        "Z": Uniform(low=z_bounds[0], high=z_bounds[1]),
        "afe": Uniform(low=afe_bounds[0], high=afe_bounds[1]),
        "logmass": Uniform(low=8.0, high=13.0),
        "diffuse_tau_kc": Uniform(low=0.0, high=2.0),
        "log_f_calib": Uniform(low=np.log(0.01), high=np.log(0.10)),
        "spectrum_scaling": ClippedNormal(mean=1.0, sigma=0.3, low=0.2, high=3.0),
    }
    initial = {
        "logsfr_ratios": jnp.zeros(len(lookback) - 1), "logmass": jnp.array([11.0]),
        "log_f_calib": jnp.array([np.log(0.03)]), "spectrum_scaling": jnp.array([1.0]),
    }
    model = SedModel(csp, observations=[phot_obs, spec_obs], priors=priors,
                     transforms=transforms, free_param_init=initial, zred=z)
    bounds = {"Z": z_bounds, "afe": afe_bounds}
    return model, phot_obs, spec_obs, bounds


PRIOR_VARIANCE = {
    # Gaussian curvature standing in for each notebook prior: range^2 / 12 for
    # the uniform priors, sigma^2 for the clipped normal on spectrum_scaling.
    "logsfr_ratios": 36.0 / 12.0, "logmass": 25.0 / 12.0, "diffuse_tau_kc": 4.0 / 12.0,
    "log_f_calib": (np.log(10.0)) ** 2 / 12.0, "spectrum_scaling": 0.3 ** 2,
}


def fisher_forecast(target: dict, truth: dict, feature_mask, downweight: float) -> dict:
    """Laplace forecast of marginal posterior widths from spectrum and photometry.

    Jacobians of the notebook model at the truth give F = J^T Sigma^-1 J per
    data set, with the notebook noise model (photometry: catalogue sigma with the
    5% floor; spectrum: sigma_eff^2 = sigma^2 + (f_calib mu)^2 at the truth
    f_calib).  The prior enters as a diagonal curvature (``PRIOR_VARIANCE``;
    the grid-range uniforms for Z and afe) so that every inverse exists.
    Returned per free parameter: the diagonal information from each data set
    and pixel mode, the spectrum's share of it, and the forecast marginal sigma
    of photometry-only, spectrum-only, and joint fits per pixel mode.
    """
    import jax
    import jax.numpy as jnp
    from jax.flatten_util import ravel_pytree

    model, phot_obs, spec_obs, bounds = build_notebook_model(target)
    theta = {k: jnp.asarray(truth[k], dtype=float) for k in model.theta_init}
    flat, unravel = ravel_pytree(theta)
    probe = unravel(jnp.arange(len(flat), dtype=float))
    names = [None] * len(flat)
    prior_var = np.zeros(len(flat))
    for key, block in probe.items():
        values = np.asarray(block).ravel()
        var = PRIOR_VARIANCE.get(key) or (bounds[key][1] - bounds[key][0]) ** 2 / 12.0
        for k, index in enumerate(values.astype(int)):
            names[index] = key if values.size == 1 else f"{key}[{k}]"
            prior_var[index] = var

    def predict(x):
        out = model.predict(unravel(x))
        return out["photometry"], out["spectrum"]

    mu_p, mu_s = (np.asarray(v) for v in predict(flat))
    j_p, j_s = (np.asarray(v) for v in jax.jacfwd(predict)(flat))
    f_calib = float(np.exp(np.ravel(truth["log_f_calib"])[0]))
    sigma_p = np.asarray(phot_obs.uncertainty)
    mask = np.asarray(spec_obs.mask)
    sigma_s = np.sqrt(np.asarray(spec_obs.uncertainty) ** 2 + (f_calib * np.abs(mu_s)) ** 2)

    def fisher(j, sigma, m):
        jm = j[m] / sigma[m, None]
        return jm.T @ jm

    def marginal_sigma(f):
        cov = np.linalg.inv(f + np.diag(1.0 / prior_var))
        return np.sqrt(np.clip(np.diag(cov), 0, None)).tolist()

    f_phot = fisher(j_p, sigma_p, np.ones(len(sigma_p), bool))
    configs = {
        "all": (mask, np.ones_like(sigma_s)),
        "features": (mask & feature_mask, np.ones_like(sigma_s)),
        "features_downweight": (mask, np.where(feature_mask, 1.0, downweight)),
    }
    out = {"parameters": names, "f_calib": f_calib, "downweight": downweight,
           "prior_sigma": np.sqrt(prior_var).tolist(),
           "n_pix": {k: int(m.sum()) for k, (m, _) in configs.items()},
           "diag_information": {"photometry": np.diag(f_phot).tolist()},
           "spectrum_share": {}, "marginal_sigma_joint": {}, "marginal_sigma_spectrum_only": {},
           "marginal_sigma_photometry_only": marginal_sigma(f_phot)}
    for key, (m, w) in configs.items():
        f_spec = fisher(j_s, sigma_s * w, m)
        d_spec = np.diag(f_spec)
        out["diag_information"][key] = d_spec.tolist()
        out["spectrum_share"][key] = (d_spec / (d_spec + np.diag(f_phot) + 1e-300)).tolist()
        out["marginal_sigma_joint"][key] = marginal_sigma(f_spec + f_phot)
        out["marginal_sigma_spectrum_only"][key] = marginal_sigma(f_spec)
    return out


def _cmd_fisher(args):
    from ceridwen.observation.absorption_features import absorption_feature_mask

    target = load_target(args.target)
    truth = json.loads(Path(args.truth).read_text())
    feature_mask = absorption_feature_mask(target["wave_vac"], zred=target["z"], window_kms=args.window_kms)
    budget = weight_budget(target, feature_mask=feature_mask)
    forecast = fisher_forecast(target, truth, feature_mask, budget["balance_downweight"])
    forecast["spect_id"] = args.target
    Path(args.out).write_text(json.dumps(forecast, indent=1))
    names = forecast["parameters"]
    d, s, share = forecast["diag_information"], forecast["marginal_sigma_joint"], forecast["spectrum_share"]
    print(f"n_pix {forecast['n_pix']}  f_calib {forecast['f_calib']:.3f}  downweight {forecast['downweight']:.1f}")
    print(f"{'parameter':<18} {'I_phot':>9} {'I_spec all':>10} {'I_spec feat':>11} {'share all':>9} {'share feat':>10} {'share dw':>8} | {'sig phot':>8} {'sig spec':>8} {'joint all':>9} {'joint feat':>10} {'joint dw':>8} {'prior':>7}")
    for i, name in enumerate(names):
        print(f"{name:<18} {d['photometry'][i]:>9.2e} {d['all'][i]:>10.2e} {d['features'][i]:>11.2e} {share['all'][i]:>9.3f} {share['features'][i]:>10.3f} {share['features_downweight'][i]:>8.3f} | "
              f"{forecast['marginal_sigma_photometry_only'][i]:>8.3g} {forecast['marginal_sigma_spectrum_only']['all'][i]:>8.3g} "
              f"{s['all'][i]:>9.3g} {s['features'][i]:>10.3g} {s['features_downweight'][i]:>8.3g} {forecast['prior_sigma'][i]:>7.3g}")


if __name__ == "__main__":
    sys.exit(main())
