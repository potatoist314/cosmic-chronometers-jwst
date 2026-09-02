#!/usr/bin/env python
"""One Ceridwen DR2 joint fit with an optional profiled calibration polynomial.

Reproduces the ``full_spectrum`` configuration of
``notebooks/ceridwen_integrated_photometry_spectra.ipynb`` (same LEGA-C DR2
selection, observations, priors, transforms, and BlackJAX NSS settings) and
adds the switches of the calibration-polynomial experiment:

``--mock``
    Replace both data sets by a model realisation.  The truth is the
    posterior median of ``--truth-from`` (an existing ``ceridwen_result.h5``
    for the same target); noise is drawn from the real per-pixel and per-band
    uncertainties.
``--tilt T`` / ``--curvature C``
    Multiply the mock spectrum by ``1 + (T/2) x + C T_2(x)`` with ``x`` the
    Chebyshev coordinate over the unmasked pixels (``T`` is the end-to-end
    fractional tilt).  Photometry is never distorted.
``--poly-order N``
    Profile a Chebyshev calibration polynomial of order ``N`` inside the
    spectrum likelihood (``PolynomialCalibration``); ``0`` = off.
``--fit-constant`` / ``--prior-sigma S`` / ``--no-spectrum-scaling``
    Let the polynomial carry the normalisation, put a Gaussian prior on its
    coefficients, or drop the sampled ``spectrum_scaling`` scalar.
``--line-windows W``
    Keep only pixels within ``W`` rest-frame angstrom of standard optical
    absorption lines (interaction with the absorption-mask experiment).

Outputs ``<out>/ceridwen_result.h5``, ``<out>/summary.json`` (scalars) and
``<out>/vectors.npz`` (spectrum, model, and polynomial quantiles).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("JAX_ENABLE_X64", "1")

import astropy.units as u
import h5py
import jax
import jax.numpy as jnp
import numpy as np
from astropy.io import fits
from astropy.table import Table
from scipy.special import softmax
from specutils.utils.wcs_utils import air_to_vac

from ceridwen.cosmology import age_gyr
from ceridwen.csp import CSPBasis_afe
from ceridwen.fit import write_result_h5
from ceridwen.likelihood import (
    DiagonalGaussianLikelihood,
    DiagonalNoiseModel,
    MultiObservationLikelihood,
    PolynomialCalibration,
)
from ceridwen.model import SedModel, logsfr_ratios_to_sfh
from ceridwen.observation import Photometry, Spectrum
from ceridwen.sampler import run_sampler
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter
from ceridwen.sampler.priors import ClippedNormal, Uniform
from ceridwen.ssps import SSPDataAfe, fetch_grid

jax.config.update("jax_enable_x64", True)

FILTER_NAMES = [
    "cfht_megacam_us_9301", "subaru_suprimecam_B", "subaru_suprimecam_V",
    "subaru_suprimecam_rp", "subaru_suprimecam_ip", "subaru_suprimecam_zp",
    "vista_vircam_Y", "vista_vircam_J", "vista_vircam_H", "vista_vircam_Ks",
    "spitzer_irac_ch1", "spitzer_irac_ch2",
]
FLUX_COLUMNS = [
    "Fuap3", "FBap3", "FVap3", "Frap3", "Fipap3", "Fzppap3",
    "FYap3", "FJap3", "FHap3", "FKsap3", "F3.6um", "F4.5um",
]
ERROR_COLUMNS = [f"e_{name}" for name in FLUX_COLUMNS]
PHOT_COLUMNS = ["Area", "Sat", "Cfl", "Deep", "Flag", "E(B-V)", "NUVMag",
                "RMag", "JMag", *[c for pair in zip(FLUX_COLUMNS, ERROR_COLUMNS)
                                  for c in pair]]
UJY_TO_MAGGIES = 1e-6 / 3631.0
PHOTOMETRY_FLOOR = 0.05
DR2_FLUX_UNIT = 1e-19 * u.erg / u.s / u.cm**2 / u.AA
SPECTRUM_CALIBRATION_INIT = 0.03
REST_EMISSION_LINES = [3726.0, 3728.8, 4861.3, 4958.9, 5006.8]
FIXED_DUST_INDEX = -0.7
# Rest-frame vacuum centres of the standard optical absorption features.
ABSORPTION_LINES = {
    "CaK": 3934.8, "CaH": 3969.6, "Hdelta": 4102.9, "Gband": 4305.6,
    "Hgamma": 4341.7, "Hbeta": 4862.7, "Mgb": 5176.7, "Fe5270": 5270.0,
    "Fe5335": 5335.0, "NaD": 5893.0,
}
SAMPLER_PROFILES = {
    "quick": dict(num_live=16, num_inner_steps=2, num_delete=8, logZ_tol=1e4),
    "cpu-trial": dict(num_live=150, num_inner_steps=24, num_delete=75,
                      logZ_tol=-2.0),
    "gpu-full": dict(num_live=500, num_inner_steps=65, num_delete=100,
                     logZ_tol=-5.0),
}


# ---------------------------------------------------------------------------
# Data (verbatim selection logic of the integrated notebook)
# ---------------------------------------------------------------------------
def select_passive(project_root: Path):
    legac = Table.read(project_root / "data/raw/legac_dr2/legaCdr2.fits.gz")
    phot = Table.read(project_root / "data/raw/cosmos2015/"
                      "cosmos2015_legac_dr2_photometry_1arcsec.fits")
    assert len(legac) == 1988
    legac_frame = legac.to_pandas()
    for column in ["SPECT_ID", "Filename"]:
        legac_frame[column] = legac_frame[column].map(
            lambda v: v.decode() if isinstance(v, bytes) else v)
    phot_frame = phot.to_pandas().set_index("LEGAC_INDEX")
    parent = legac_frame.join(phot_frame[PHOT_COLUMNS], how="inner")
    quality = ((parent["f_use"] == 1) & (parent["f_ppxf"] == 0)
               & (parent["f_z"] == 0) & (parent["f_int"] == 0)
               & (parent["SN"] > 0) & (parent["z"] >= 0.6) & (parent["z"] < 1.0))
    valid_rest = (parent[["NUVMag", "RMag", "JMag"]] > -40).all(axis=1)
    parent = parent[quality & valid_rest].copy()
    nuv_r = parent["NUVMag"] - parent["RMag"]
    r_j = parent["RMag"] - parent["JMag"]
    passive = parent[(nuv_r > 3 * r_j + 1) & (nuv_r > 3.1)]
    oii_ew = passive["OII_3727_EW"]
    weak_oii = passive[(oii_ew > -5) | oii_ew.isna()]
    oii_sig = (weak_oii["OII_3727_EW"] / weak_oii["OII_3727_EW_err"]).abs()
    oiii_sig = (weak_oii["OIII_5007_EW"] / weak_oii["OIII_5007_EW_err"]).abs()
    bona_fide = weak_oii[~((oii_sig >= 3) | (oiii_sig >= 3))]
    clean = ((bona_fide["Area"] == 0) & (bona_fide["Sat"] == 0)
             & (bona_fide["Cfl"] == 1) & (bona_fide["Flag"] == 0))
    usable = bona_fide[clean].copy()
    selected = (usable.sort_values(["SN", "SPECT_ID"], ascending=[False, True])
                .drop_duplicates("OBJECT", keep="first")
                .sort_values(["SN", "SPECT_ID"], ascending=[False, True]))
    assert len(usable) == 194 and len(selected) == 187
    return selected


def load_spectrum(project_root: Path, filename: str):
    with fits.open(project_root / "data/raw/legac_dr2/sp" / filename) as hdul:
        spectrum = hdul[1].data
        resolution = float(hdul[0].header["SPEC_RES"])
    wave, flux, error, qual = (spectrum[c][0] for c in ("WAVE", "FLUX", "ERR", "QUAL"))
    good = (qual == 0) & (error > 0) & np.isfinite(flux)
    return wave, flux, error, good, resolution


def flam_to_fnu_cgs(values, wavelength):
    return (values * DR2_FLUX_UNIT).to_value(
        u.erg / u.s / u.cm**2 / u.Hz,
        equivalencies=u.spectral_density(wavelength * u.AA))


def build_observations(project_root: Path, target_id: str, line_windows: float | None):
    selected = select_passive(project_root)
    rows = selected[selected["SPECT_ID"] == target_id]
    if len(rows) != 1:
        raise ValueError(f"expected one eligible {target_id} row, found {len(rows)}")
    galaxy = rows.iloc[0]
    zred = float(galaxy["z"])
    sigma_star = float(galaxy["SIGMA_STARS_PRIME"])

    flux = galaxy[FLUX_COLUMNS].to_numpy(dtype=float) * UJY_TO_MAGGIES
    err = galaxy[ERROR_COLUMNS].to_numpy(dtype=float) * UJY_TO_MAGGIES
    unc = np.hypot(err, PHOTOMETRY_FLOOR * np.abs(flux))
    mask = np.isfinite(flux) & np.isfinite(unc) & (flux > 0)
    assert mask.all()
    phot_obs = Photometry(filters=FILTER_NAMES, flux=flux, uncertainty=unc,
                          mask=mask, name="photometry")

    wave_air, flux_dr2, error_dr2, good, resolution = load_spectrum(
        project_root, galaxy["Filename"])
    wave_vac = air_to_vac(wave_air * u.AA).to_value(u.AA)
    native_flux = flam_to_fnu_cgs(flux_dr2, wave_vac)
    native_unc = flam_to_fnu_cgs(error_dr2, wave_vac)
    telluric = air_to_vac(np.array([7590.0, 7660.0]) * u.AA).to_value(u.AA)
    valid = (good & np.isfinite(native_flux) & np.isfinite(native_unc)
             & (native_unc > 0))
    spec_kwargs = dict(
        wavelength=wave_vac, flux=np.nan_to_num(native_flux, nan=0.0),
        uncertainty=np.where(valid, native_unc, 1.0), mask=valid,
        resolution=resolution, smoothtype="R", res_convention="fwhm",
        sigma_losvd=sigma_star, name="spectrum",
    )
    spec_obs = Spectrum(**spec_kwargs)
    spec_obs.mask_lines(REST_EMISSION_LINES, dv=1500.0, zred=zred)
    spec_obs.mask_wavelength_range(*telluric)
    if line_windows is not None:
        keep = np.zeros(wave_vac.shape, dtype=bool)
        for centre in ABSORPTION_LINES.values():
            obs_centre = centre * (1.0 + zred)
            keep |= np.abs(wave_vac - obs_centre) <= line_windows * (1.0 + zred)
        spec_obs.mask = spec_obs.mask & jnp.asarray(keep)
    assert spec_obs.ndof > (300 if line_windows is not None else 3000)
    meta = dict(target=target_id, object_id=int(galaxy["OBJECT"]), zred=zred,
                sigma_star=sigma_star, sn_catalogue=float(galaxy["SN"]),
                resolution=resolution, n_pix_fitted=int(spec_obs.ndof))
    return phot_obs, spec_obs, spec_kwargs, meta


# ---------------------------------------------------------------------------
# Model (verbatim priors and transforms of the integrated notebook)
# ---------------------------------------------------------------------------
def build_model(ssp, phot_obs, spec_obs, zred, use_spectrum_scaling: bool):
    universe_age = float(age_gyr(zred))
    lookback = np.array([0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 5.0, universe_age])
    z_bounds = (float(ssp.ssp_lgmet.min()) + 1e-4, float(ssp.ssp_lgmet.max()) - 1e-4)
    afe_bounds = (float(ssp.ssp_afe.min()), float(ssp.ssp_afe.max()))
    csp = CSPBasis_afe(
        ssp,
        theta={"lookback_time": jnp.asarray(lookback), "sfh": jnp.ones(len(lookback)),
               "Z": jnp.array([-1.85]), "afe": jnp.array([0.2]),
               "diffuse_tau_kc": jnp.array([0.2]),
               "diffuse_dust_index": jnp.array([FIXED_DUST_INDEX])},
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
    }
    initial = {
        "logsfr_ratios": jnp.zeros(len(lookback) - 1),
        "logmass": jnp.array([11.0]),
        "log_f_calib": jnp.array([np.log(SPECTRUM_CALIBRATION_INIT)]),
    }
    if use_spectrum_scaling:
        priors["spectrum_scaling"] = ClippedNormal(mean=1.0, sigma=0.3, low=0.2, high=3.0)
        initial["spectrum_scaling"] = jnp.array([1.0])
    model = SedModel(csp, observations=[phot_obs, spec_obs], priors=priors,
                     transforms=transforms, free_param_init=initial, zred=zred)
    return model, lookback


def weighted_median_theta(h5_path: Path) -> dict[str, np.ndarray]:
    with h5py.File(h5_path, "r") as f:
        names = list(f["model"]["param_names"].asstr()[()])
        weights = softmax(np.array(f["samples"]["log_weights"]))
        theta = {}
        for name in names:
            values = np.array(f["samples"][name]).reshape(weights.size, -1)
            medians = []
            for column in values.T:
                order = np.argsort(column)
                medians.append(float(np.interp(0.5, np.cumsum(weights[order]), column[order])))
            theta[name] = np.array(medians)
    return theta


def make_mock(model, truth, phot_obs, spec_kwargs, spec_obs, tilt, curvature, seed):
    """Model realisation at ``truth`` with the real uncertainties as noise."""
    theta = {k: jnp.asarray(v) for k, v in truth.items() if k in model.theta_init}
    prediction = model.predict(theta)
    rng = np.random.default_rng(seed)
    mask = np.asarray(spec_obs.mask)
    coordinate = PolynomialCalibration.from_spectrum(spec_obs, order=2).x
    x = np.asarray(coordinate)
    distortion = 1.0 + 0.5 * tilt * x + curvature * (2.0 * x**2 - 1.0)
    mu_spec = np.asarray(prediction["spectrum"])
    mu_phot = np.asarray(prediction["photometry"])
    spec_unc = np.asarray(spec_obs.uncertainty)
    phot_unc = np.asarray(phot_obs.uncertainty)
    spec_flux = distortion * mu_spec + rng.normal(0.0, np.where(mask, spec_unc, 0.0))
    phot_flux = mu_phot + rng.normal(0.0, phot_unc)
    mock_spec = Spectrum(**{**spec_kwargs, "flux": np.where(mask, spec_flux, 0.0),
                            "mask": mask})
    mock_phot = Photometry(filters=FILTER_NAMES, flux=phot_flux, uncertainty=phot_unc,
                           mask=np.asarray(phot_obs.mask), name="photometry")
    return mock_phot, mock_spec, distortion, mu_spec


# ---------------------------------------------------------------------------
# Posterior summaries
# ---------------------------------------------------------------------------
def quantiles(values):
    q16, q50, q84 = np.percentile(values, [16, 50, 84])
    return dict(q16=float(q16), q50=float(q50), q84=float(q84))


def mass_weighted_age(logsfr_ratios, lookback):
    histories = np.asarray([
        np.asarray(logsfr_ratios_to_sfh(r, sfh_times_yr=lookback * 1e9))
        for r in logsfr_ratios])
    durations = np.diff(lookback) * 1e9
    masses = 0.5 * (histories[:, :-1] + histories[:, 1:]) * durations
    ages = 0.5 * (lookback[:-1] + lookback[1:])
    return (masses * ages).sum(axis=1) / masses.sum(axis=1)


def summarise(result, model, lookback, spec_obs, calibration, draws, seed):
    weights = softmax(np.asarray(result.log_weights))
    rng = np.random.default_rng(seed + 1)
    idx = rng.choice(weights.size, size=draws, replace=True, p=weights)
    posterior = {k: np.asarray(v)[idx] for k, v in result.samples.items()}
    scalars = {}
    for name in ("logmass", "Z", "afe", "diffuse_tau_kc", "log_f_calib", "spectrum_scaling"):
        if name in posterior:
            scalars[name] = quantiles(posterior[name].reshape(draws))
    scalars["f_calib_percent"] = quantiles(100.0 * np.exp(posterior["log_f_calib"].reshape(draws)))
    age = mass_weighted_age(posterior["logsfr_ratios"], lookback)
    scalars["mass_weighted_age_gyr"] = quantiles(age)
    ratios = posterior["logsfr_ratios"].reshape(draws, -1)
    scalars["logsfr_ratios"] = [quantiles(ratios[:, j]) for j in range(ratios.shape[1])]

    # Posterior-predictive spectrum and calibration polynomial on 200 draws.
    n_pp = min(200, draws)
    mu_draws, poly_draws, coeff_draws = [], [], []
    y = np.asarray(spec_obs.flux); sigma = np.asarray(spec_obs.uncertainty)
    mask = np.asarray(spec_obs.mask)
    for i in range(n_pp):
        theta = {k: jnp.asarray(v[i]).reshape(-1) for k, v in posterior.items()}
        mu = np.asarray(model.predict_jit(theta)["spectrum"])
        mu_draws.append(mu)
        if calibration is not None:
            coeffs = calibration.solve(y, mu, sigma, mask)
            coeff_draws.append(np.asarray(coeffs))
            poly_draws.append(np.asarray(calibration.polynomial(coeffs)))
    mu_draws = np.asarray(mu_draws)
    vectors = dict(wavelength=np.asarray(spec_obs.wavelength), flux=y, uncertainty=sigma,
                   mask=mask, model_q16=np.percentile(mu_draws, 16, axis=0),
                   model_q50=np.percentile(mu_draws, 50, axis=0),
                   model_q84=np.percentile(mu_draws, 84, axis=0))
    if calibration is not None:
        poly_draws = np.asarray(poly_draws)
        vectors.update(poly_q16=np.percentile(poly_draws, 16, axis=0),
                       poly_q50=np.percentile(poly_draws, 50, axis=0),
                       poly_q84=np.percentile(poly_draws, 84, axis=0),
                       coefficients=np.asarray(coeff_draws))
        scalars["poly_coefficients"] = [quantiles(c) for c in np.asarray(coeff_draws).T]
        scalars["poly_range_q50"] = [float(np.min(vectors["poly_q50"][mask])),
                                     float(np.max(vectors["poly_q50"][mask]))]
    return scalars, vectors, weights


# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--target", default="M5_172669")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--project-root", type=Path,
                        default=Path(os.environ.get("CERIDWEN_PROJECT_ROOT",
                                                    Path(__file__).resolve().parents[1])))
    parser.add_argument("--profile", choices=sorted(SAMPLER_PROFILES), default="gpu-full")
    parser.add_argument("--seed", type=int, default=20260902)
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--truth-from", type=Path,
                        help="ceridwen_result.h5 whose posterior median is the mock truth")
    parser.add_argument("--tilt", type=float, default=0.0)
    parser.add_argument("--curvature", type=float, default=0.0)
    parser.add_argument("--poly-order", type=int, default=0)
    parser.add_argument("--fit-constant", action="store_true")
    parser.add_argument("--prior-sigma", type=float, default=None)
    parser.add_argument("--no-spectrum-scaling", action="store_true")
    parser.add_argument("--line-windows", type=float, default=None,
                        help="rest-frame half-width in angstrom around absorption lines")
    parser.add_argument("--draws", type=int, default=2000)
    args = parser.parse_args(argv)

    started = time.time()
    args.out.mkdir(parents=True, exist_ok=True)
    phot_obs, spec_obs, spec_kwargs, meta = build_observations(
        args.project_root, args.target, args.line_windows)
    ssp = SSPDataAfe.load(fetch_grid("amist_c3k_hr_krou_afe", quiet=True))
    zred = meta["zred"]
    use_scaling = not args.no_spectrum_scaling

    truth = None
    distortion = None
    if args.mock:
        if args.truth_from is None:
            raise SystemExit("--mock needs --truth-from")
        generator, _ = build_model(ssp, phot_obs, spec_obs, zred, use_spectrum_scaling=True)
        truth = weighted_median_theta(args.truth_from)
        truth.setdefault("spectrum_scaling", np.array([1.0]))
        phot_obs, spec_obs, distortion, _ = make_mock(
            generator, truth, phot_obs, spec_kwargs, spec_obs,
            args.tilt, args.curvature, args.seed)
    model, lookback = build_model(ssp, phot_obs, spec_obs, zred, use_scaling)

    calibration = None
    if args.poly_order > 0 or args.fit_constant:
        calibration = PolynomialCalibration.from_spectrum(
            spec_obs, order=args.poly_order, fit_constant=args.fit_constant,
            prior_sigma=args.prior_sigma)
    likelihood = MultiObservationLikelihood(
        keys=(phot_obs.name, spec_obs.name),
        likelihoods=(DiagonalGaussianLikelihood(),
                     DiagonalGaussianLikelihood(
                         noise_model=DiagonalNoiseModel(use_fractional=True),
                         calibration=calibration)),
    )
    settings = SAMPLER_PROFILES[args.profile]
    adapter = BlackJAXNestedSamplerAdapter(
        priors=model.priors, checkpoint_interval_s=1200.0,
        checkpoint_dir=str(args.out), verbose=True, **settings)
    print(f"{meta['target']} z={zred:.4f} pixels={meta['n_pix_fitted']} "
          f"calibration={calibration!r} spectrum_scaling={use_scaling} "
          f"profile={args.profile} devices={jax.devices()}", flush=True)
    result = run_sampler(model, likelihood, adapter, jax.random.PRNGKey(args.seed))
    write_result_h5(args.out / "ceridwen_result.h5", model, result)

    scalars, vectors, weights = summarise(result, model, lookback, spec_obs,
                                          calibration, args.draws, args.seed)
    if distortion is not None:
        vectors["distortion_true"] = distortion
    np.savez_compressed(args.out / "vectors.npz", **vectors)
    summary = dict(
        config=dict(target=args.target, profile=args.profile, seed=args.seed,
                    mock=args.mock, tilt=args.tilt, curvature=args.curvature,
                    poly_order=args.poly_order, fit_constant=args.fit_constant,
                    prior_sigma=args.prior_sigma, spectrum_scaling=use_scaling,
                    line_windows=args.line_windows, sampler=settings,
                    truth_from=None if args.truth_from is None else str(args.truth_from)),
        meta=meta,
        truth=None if truth is None else {k: v.tolist() for k, v in truth.items()},
        truth_mass_weighted_age_gyr=(None if truth is None else float(
            mass_weighted_age(truth["logsfr_ratios"][None, :], lookback)[0])),
        log_evidence=float(result.log_evidence),
        log_evidence_err=float(result.log_evidence_err),
        n_likelihood_calls=int(result.n_likelihood_calls),
        sampler_wall_s=float(result.wall_time_s),
        total_wall_s=time.time() - started,
        posterior_ess=float(1.0 / np.sum(weights**2)),
        posterior=scalars,
        devices=[str(d) for d in jax.devices()],
    )
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("log_evidence", "n_likelihood_calls",
                                                "sampler_wall_s")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
