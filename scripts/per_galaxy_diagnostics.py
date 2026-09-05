"""Per-galaxy chi-squared and star-formation-timescale diagnostics for Ceridwen fits.

Method notes
------------
- Source: one target folder with ``ceridwen_result.h5`` (posterior dead points,
  observations, priors) and ``ceridwen_derived_outputs.h5`` (posterior-median
  predictions, stored pulls, SFH mass-fraction draws).
- Two chi-squared definitions are shown side by side on every figure:

  * *stored*: the fitting notebook's value, ``pull = (y - q50) / sigma_eff`` with
    ``q50`` the pointwise posterior-median prediction over 200 draws and
    ``sigma_eff = sqrt(sigma_obs^2 + (f_med |q50|)^2)``, ``f_med`` the posterior
    median calibration floor. ``q50`` is not a single model realisation.
  * *at theta_ML*: the model is rebuilt from the stored file and Ceridwen's own
    ``DiagonalGaussianLikelihood`` is evaluated at the dead point with the highest
    stored log-likelihood. ``LikelihoodOutput.chi`` is the per-datum normalised
    residual with exactly the sigma the sampler used (``sigma_obs`` plus the
    sampled ``f_calib * |mu(theta)|`` term). The recomputed log-likelihood is
    compared with the stored one; agreement proves masks, sigma and physics
    switches match the fit.

- Reduced chi-squared is reported as chi^2 / N over the fitted data of one data
  set (the 13 free parameters are shared, so no per-data-set ndof exists) and as
  chi^2 / (N_phot + N_spec - n_free) for the joint fit.
- Formation lookback times ``t_X`` follow the request wording: the lookback time
  by which X percent of the final stellar mass had formed, i.e. the mass older
  than ``t_X`` is X percent. This is the mirror of the project summary's
  ``formation_times`` (mass *younger* than t): ``t_X(here) = t_{100-X}(summary)``.
  Within a bin the SFR is constant, so mass accumulates linearly.
- The model parameter block is generated from the ``SedModel``, ``CSPBasis_afe``,
  ``SSPDataAfe``, observation and likelihood objects, never typed by hand. The
  CSP physics switches and the spectrum smoothing convention are not persisted
  in ``ceridwen_result.h5``; ``rebuild_model`` takes them from the constants
  below, which mirror ``notebooks/ceridwen_integrated_photometry_spectra.ipynb``.
  When a result carries a stored block (written by the notebook from the live
  model) the rebuilt block is compared with it.

Usage
-----
``ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py run
  [--run-dir DIR] [--out-csv PATH] [--summary-dir DIR] [--target NAME ...]``
writes ``diagnostics/`` figures beside each target's executed notebook, one CSV
row per galaxy, and the cross-galaxy summary figures.

``... check TARGET_DIR`` prints the log-likelihood check for one target.
``... block TARGET_DIR`` prints the generated model parameter block.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ["JAX_ENABLE_X64"] = "1"

import matplotlib

if __name__ == "__main__":
    matplotlib.use("Agg")   # CLI only; a notebook keeps its inline backend

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_DIR = PROJECT_ROOT / "results/rtx-5060-dr2-quiescent-full-spectrum"
DEFAULT_OUT_CSV = PROJECT_ROOT / "results/per-galaxy-diagnostics.csv"
DEFAULT_SUMMARY_DIR = PROJECT_ROOT / "wiki/analyses/per-galaxy-diagnostics"
FIGURE_SUBDIR = "diagnostics"

# Fitting-notebook configuration that ``write_result_h5`` does not persist.
GRID_NAME = "amist_c3k_hr_krou_afe"
FIXED_DUST_INDEX = -0.7
RES_CONVENTION = "fwhm"
REST_EMISSION_LINES = (3726.0, 3728.8, 4861.3, 4958.9, 5006.8)
EMISSION_MASK_DV_KMS = 1500.0
TELLURIC_AIR = (7590.0, 7660.0)
SPEED_OF_LIGHT_KMS = 299792.458

TX_LEVELS = (0.10, 0.20, 0.50, 0.80, 0.90)
OUTLIER_PULL = 4.0
PHOT_REDCHI2_FLAG = 3.0
SPEC_REDCHI2_FLAG = 1.5
CALIB_SATURATION_FRACTION = 0.98
BIN_WIDTH_AA = 25.0

# FSPS ``imf_type`` codes (python-fsps documentation).
IMF_NAMES = {
    0: "Salpeter (1955)",
    1: "Chabrier (2003)",
    2: "Kroupa (2001)",
    3: "van Dokkum (2008)",
    4: "Dave (2008)",
    5: "tabulated",
}

BLUE, ORANGE, RED, GREY, GREEN = "#0072B2", "#E69F00", "#D55E00", "#999999", "#009E73"

rcParams.update(
    {
        "font.size": 9,
        "axes.linewidth": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "savefig.dpi": 110,
    }
)


# ----------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------
def _text(value) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


@dataclass
class GalaxyResult:
    """Everything the diagnostics need from one target folder."""

    folder: Path
    target: str
    spect_id: str
    object_id: int
    z: float
    sigma_star_kms: float
    catalogue_sn: float
    seed: int
    settings: dict
    prior_text: dict
    theta_init: dict
    transform_names: list
    phot: dict
    spec: dict
    samples: dict
    log_weights: np.ndarray
    log_likelihoods: np.ndarray
    log_evidence: float
    log_evidence_err: float
    derived_phot: dict
    derived_spec: dict
    sfh_edges_gyr: np.ndarray
    mass_fraction_draws: np.ndarray
    mass_weighted_age_draws: np.ndarray
    diagnostics: dict
    stored_block: str | None = None
    wall_time_s: float = float("nan")
    n_likelihood_calls: int = 0
    extra: dict = field(default_factory=dict)

    @property
    def n_free(self) -> int:
        return int(sum(np.size(v) for v in self.theta_init.values()))

    @property
    def universe_age_gyr(self) -> float:
        return float(self.sfh_edges_gyr[-1])


def load_galaxy(folder: Path) -> GalaxyResult:
    folder = Path(folder)
    with h5py.File(folder / "ceridwen_result.h5", "r") as f:
        model = f["model"]
        z = float(model.attrs["zred"])
        prior_text = {k: _text(v) for k, v in model["priors"].attrs.items()}
        theta_init = {k: np.asarray(model["theta_init"][k], dtype=float) for k in model["theta_init"]}
        transform_names = json.loads(_text(model.attrs["transforms"])) if "transforms" in model.attrs else []
        stored_block = _text(model.attrs["parameter_block"]) if "parameter_block" in model.attrs else None
        extra = {k: (_text(model.attrs[k]) if isinstance(model.attrs[k], (bytes, str)) else model.attrs[k])
                 for k in ("calibration_order", "photometry_source", "spectrum_pixels", "sfh_basis_fastpath")
                 if k in model.attrs}
        pg, sg = f["obs/photometry"], f["obs/spectrum"]
        phot = {
            "filters": json.loads(_text(pg.attrs["filternames"])),
            "flux": np.asarray(pg["flux"], dtype=float),
            "uncertainty": np.asarray(pg["uncertainty"], dtype=float),
            "mask": np.asarray(pg["mask"], dtype=bool),
            "wavelength": np.asarray(pg["wavelength"], dtype=float),
        }
        spec = {
            "wavelength": np.asarray(sg["wavelength"], dtype=float),
            "flux": np.asarray(sg["flux"], dtype=float),
            "uncertainty": np.asarray(sg["uncertainty"], dtype=float),
            "mask": np.asarray(sg["mask"], dtype=bool),
            "resolution": float(sg.attrs["resolution"]),
            "smoothtype": _text(sg.attrs["smoothtype"]),
        }
        sm = f["samples"]
        samples = {k: np.asarray(sm[k], dtype=float) for k in theta_init}
        settings = {k: sm.attrs[k] for k in ("num_live", "num_inner_steps", "num_delete", "logZ_tol") if k in sm.attrs}
        settings["sampler_name"] = _text(sm.attrs.get("sampler_name", "blackjax.nss"))
        log_weights = np.asarray(sm["log_weights"], dtype=float)
        log_likelihoods = np.asarray(sm["log_likelihoods"], dtype=float)
        log_evidence = float(sm.attrs["log_evidence"])
        log_evidence_err = float(sm.attrs["log_evidence_err"])
        wall = float(sm.attrs.get("wall_time_s", float("nan")))
        calls = int(sm.attrs.get("n_likelihood_calls", 0))
        seed = int(model.attrs["random_seed"])
        object_id = int(model.attrs["object_id"])
    with h5py.File(folder / "ceridwen_derived_outputs.h5", "r") as d:
        spect_id = _text(d.attrs["target_id"])
        sigma_star = float(d.attrs["sigma_star_kms"])
        sn = float(d.attrs["catalogue_sn"])
        dp, ds, sfh = d["photometry"], d["spectrum"], d["sfh"]
        derived_phot = {k: np.asarray(dp[k]) for k in ("observed", "uncertainty", "mask", "posterior_q16", "posterior_q50", "posterior_q84", "pull", "wavelength")}
        derived_spec = {k: np.asarray(ds[k]) for k in ("observed", "uncertainty", "effective_uncertainty", "mask", "posterior_q16", "posterior_q50", "posterior_q84", "pull")}
        edges = np.asarray(sfh["lookback_time_gyr"], dtype=float)
        fracs = np.asarray(sfh["mass_fraction_draws"], dtype=float)
        mwage = np.asarray(sfh["mass_weighted_age_gyr"], dtype=float)
        diagnostics = {k: (float(v) if not isinstance(v, (bytes, str, np.bool_)) else v) for k, v in d["diagnostics"].attrs.items()}
        diagnostics["passed"] = bool(d["diagnostics"].attrs["passed"])
    return GalaxyResult(
        folder=folder, target=folder.name, spect_id=spect_id, object_id=object_id, z=z,
        sigma_star_kms=sigma_star, catalogue_sn=sn, seed=seed, settings=settings,
        prior_text=prior_text, theta_init=theta_init, transform_names=transform_names,
        phot=phot, spec=spec, samples=samples, log_weights=log_weights,
        log_likelihoods=log_likelihoods, log_evidence=log_evidence,
        log_evidence_err=log_evidence_err, derived_phot=derived_phot,
        derived_spec=derived_spec, sfh_edges_gyr=edges, mass_fraction_draws=fracs,
        mass_weighted_age_draws=mwage, diagnostics=diagnostics, stored_block=stored_block,
        wall_time_s=wall, n_likelihood_calls=calls, extra=extra,
    )


# ----------------------------------------------------------------------------
# Priors and model rebuild
# ----------------------------------------------------------------------------
_REPR_PRIOR = re.compile(r"^(\w+)\((.*)\)$")


def parse_prior(text: str):
    """Rebuild a Ceridwen prior from the string ``write_result_h5`` stored.

    ``Uniform`` is stored as JSON (``serialize``); other priors as ``repr``.
    """
    from ceridwen.sampler import priors as prior_module

    text = text.strip()
    if text.startswith("{"):
        payload = json.loads(text)
        cls = getattr(prior_module, payload.pop("type"))
        payload.pop("name", None)
        return cls(**payload)
    match = _REPR_PRIOR.match(text)
    if match is None:
        raise ValueError(f"unrecognised prior text: {text!r}")
    cls = getattr(prior_module, match.group(1))
    kwargs = {}
    for part in filter(None, (p.strip() for p in match.group(2).split(","))):
        key, _, value = part.partition("=")
        kwargs[key.strip()] = float(value)
    return cls(**kwargs)


def describe_prior(prior) -> str:
    """One-line human description of a prior object (from its own ``params``)."""
    name = type(prior).__name__
    params = getattr(prior, "params", {})
    if name in ("Uniform", "TopHat"):
        return f"Uniform({float(params['low']):.4g}, {float(params['high']):.4g})"
    inner = ", ".join(f"{k}={float(v):.4g}" for k, v in params.items())
    return f"{name}({inner})"


def load_ssp():
    from ceridwen.ssps import SSPDataAfe, fetch_grid

    return SSPDataAfe.load(fetch_grid(GRID_NAME))


def rebuild_model(galaxy: GalaxyResult, ssp):
    """Rebuild the fitting notebook's ``SedModel`` and joint likelihood.

    Returns ``(model, likelihood, csp)``. Priors, initial values, redshift and
    observations come from the stored files; the CSP switches, fixed dust index
    and smoothing convention come from the module constants (not persisted).
    """
    import jax.numpy as jnp
    from ceridwen.csp import CSPBasis_afe
    from ceridwen.likelihood import (
        DiagonalGaussianLikelihood,
        DiagonalNoiseModel,
        MultiObservationLikelihood,
    )
    from ceridwen.model import SedModel, logsfr_ratios_to_sfh
    from ceridwen.observation import Photometry, Spectrum

    if int(galaxy.extra.get("calibration_order", 0) or 0) > 0:
        raise NotImplementedError(
            f"{galaxy.target}: the fit used a calibration polynomial (order "
            f"{galaxy.extra['calibration_order']}); this rebuild only covers spectrum_scaling."
        )
    priors = {k: parse_prior(v) for k, v in galaxy.prior_text.items()}
    phot_obs = Photometry(
        filters=galaxy.phot["filters"], flux=galaxy.phot["flux"],
        uncertainty=galaxy.phot["uncertainty"], mask=galaxy.phot["mask"], name="photometry",
    )
    spec_obs = Spectrum(
        wavelength=galaxy.spec["wavelength"], flux=galaxy.spec["flux"],
        uncertainty=galaxy.spec["uncertainty"], mask=galaxy.spec["mask"],
        resolution=galaxy.spec["resolution"], smoothtype=galaxy.spec["smoothtype"],
        res_convention=RES_CONVENTION, sigma_losvd=galaxy.sigma_star_kms, name="spectrum",
    )
    lookback = galaxy.sfh_edges_gyr
    csp = CSPBasis_afe(
        ssp,
        theta={
            "lookback_time": jnp.asarray(lookback),
            "sfh": jnp.ones(len(lookback)),
            "Z": jnp.array([-1.85]),
            "afe": jnp.array([0.2]),
            "diffuse_tau_kc": jnp.array([0.2]),
            "diffuse_dust_index": jnp.array([FIXED_DUST_INDEX]),
        },
        zh_const=True, sfh_interp="step", add_dust=False, add_diffuse_dust=True,
        add_dust_emission=False, add_igm=False, sigma_losvd_kms=0.0,
        track_zred_age=False, verbose=False,
    )

    def sfh_from_ratios(free_theta):
        return logsfr_ratios_to_sfh(free_theta["logsfr_ratios"], sfh_times_yr=np.asarray(csp.sfh_times))

    transforms = {
        "sfh": sfh_from_ratios,
        "diffuse_dust_index": lambda free_theta: jnp.array([FIXED_DUST_INDEX]),
    }
    init = {k: jnp.asarray(v) for k, v in galaxy.theta_init.items()}
    model = SedModel(csp, observations=[phot_obs, spec_obs], priors=priors,
                     transforms=transforms, free_param_init=init, zred=galaxy.z)
    likelihood = MultiObservationLikelihood(
        keys=("photometry", "spectrum"),
        likelihoods=(
            DiagonalGaussianLikelihood(),
            DiagonalGaussianLikelihood(noise_model=DiagonalNoiseModel(use_fractional=True)),
        ),
    )
    return model, likelihood, csp


def theta_at(galaxy: GalaxyResult, index: int) -> dict:
    import jax.numpy as jnp

    return {k: jnp.atleast_1d(jnp.asarray(galaxy.samples[k][index])) for k in galaxy.theta_init}


def max_likelihood_index(galaxy: GalaxyResult) -> int:
    return int(np.argmax(galaxy.log_likelihoods))


def likelihood_terms(model, likelihood, theta) -> dict:
    """Evaluate the fit's own likelihood at one theta and expose per-datum chi.

    Mirrors ``ceridwen.sampler.runner.run_sampler.loglike_fn``: the observation
    arrays are the model's, the prediction is ``model.predict(theta)`` and each
    ``DiagonalGaussianLikelihood`` receives the full theta as nuisance params.
    """
    predictions = model.predict(theta)
    total = 0.0
    out = {}
    for key, lhood in zip(likelihood.keys, likelihood.likelihoods):
        obs = model.obs_dict[key]
        lnl, aux = lhood(obs.flux, predictions[key], obs.uncertainty, obs.mask, params=theta)
        total = total + lnl
        out[key] = {
            "chi": np.asarray(aux.chi, dtype=float),
            "mu": np.asarray(predictions[key], dtype=float),
            "ndof": int(aux.ndof),
            "chi2": float(np.sum(np.asarray(aux.chi, dtype=float) ** 2)),
        }
    out["lnl"] = float(total)
    if "log_f_calib" in theta:
        out["f_calib"] = float(np.exp(np.asarray(theta["log_f_calib"]))[0])
    return out


# ----------------------------------------------------------------------------
# Chi-squared bookkeeping
# ----------------------------------------------------------------------------
def chi2_contributions(pull: np.ndarray, mask: np.ndarray) -> dict:
    """Per-datum chi^2, total, count and the cumulative fraction along the array."""
    pull = np.asarray(pull, dtype=float)
    mask = np.asarray(mask, dtype=bool)
    contrib = np.where(mask, pull**2, 0.0)
    total = float(contrib.sum())
    cumulative = np.cumsum(contrib)
    return {
        "contribution": contrib,
        "total": total,
        "n": int(mask.sum()),
        "cumulative": cumulative,
        "cumulative_fraction": cumulative / total if total > 0 else cumulative,
    }


def binned_mean_pull2(wave, pull, mask, width=BIN_WIDTH_AA):
    """Mean pull^2 of fitted pixels in fixed-width wavelength bins."""
    wave = np.asarray(wave, dtype=float)
    fitted = np.asarray(mask, dtype=bool)
    lo = np.floor(wave[fitted].min() / width) * width
    hi = (np.floor(wave[fitted].max() / width) + 1) * width   # strictly above the last pixel
    edges = np.arange(lo, hi + 0.5 * width, width)
    index = np.digitize(wave[fitted], edges) - 1              # 0 .. len(edges) - 2
    sums = np.bincount(index, weights=np.asarray(pull, dtype=float)[fitted] ** 2, minlength=len(edges) - 1)
    counts = np.bincount(index, minlength=len(edges) - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = np.where(counts > 0, sums / counts, np.nan)
    return edges, mean, counts


def spectrum_mask_categories(galaxy: GalaxyResult) -> dict:
    """Why each native pixel is outside the likelihood.

    The notebook stores masked pixels with ``uncertainty == 1.0`` and
    ``flux == 0`` when they fail the quality/finite/positive-error test
    (``native_valid``); emission-line windows (+-1500 km/s around the rest
    lines) and the telluric band are masked afterwards on valid pixels.
    """
    from specutils.utils.wcs_utils import air_to_vac
    import astropy.units as u

    wave = galaxy.spec["wavelength"]
    fitted = galaxy.spec["mask"]
    bad = galaxy.spec["uncertainty"] == 1.0
    valid = ~bad
    emission = np.zeros_like(fitted)
    for line in REST_EMISSION_LINES:
        centre = line * (1.0 + galaxy.z)
        half = centre * EMISSION_MASK_DV_KMS / SPEED_OF_LIGHT_KMS
        emission |= np.abs(wave - centre) <= half
    tel_lo, tel_hi = air_to_vac(np.array(TELLURIC_AIR) * u.AA).to_value(u.AA)
    telluric = (wave >= tel_lo) & (wave <= tel_hi)
    other = valid & ~fitted & ~emission & ~telluric
    return {
        "fitted": fitted,
        "bad_pixel": bad,
        "emission_line": valid & emission & ~fitted,
        "telluric": valid & telluric & ~emission & ~fitted,
        "other_masked": other,
    }


# ----------------------------------------------------------------------------
# Formation times
# ----------------------------------------------------------------------------
def lookback_at_younger_fraction(edges, fracs, level):
    """Lookback time at which the mass *younger* than it is ``level`` of the total.

    Same construction as ``scripts/build_dr2_quiescent_summary.formation_times``:
    bins run young to old, the SFR is constant within a bin, so mass accumulates
    linearly in lookback time across the bin. Vectorised over draws.
    """
    edges = np.asarray(edges, dtype=float)
    fracs = np.atleast_2d(np.asarray(fracs, dtype=float))
    widths = np.diff(edges)
    younger = np.concatenate([np.zeros((len(fracs), 1)), np.cumsum(fracs, axis=1)], axis=1)
    rows = np.arange(len(fracs))
    inside = (younger[:, :-1] <= level) & (level <= younger[:, 1:])
    first = np.argmax(inside, axis=1)
    width = widths[first]
    base = younger[rows, first]
    span = np.maximum(younger[rows, first + 1] - base, 1e-300)
    with np.errstate(divide="ignore", invalid="ignore"):
        step = np.where(width > 0, (level - base) / span * width, 0.0)
    return edges[:-1][first] + np.clip(step, 0.0, width)


def formation_lookback_times(edges, fracs, levels=TX_LEVELS) -> dict:
    """``t_X``: lookback time by which X of the final mass had formed (mass older).

    ``t_X = lookback_at_younger_fraction(edges, fracs, 1 - X)`` per draw, so
    ``t_0.1 >= t_0.5 >= t_0.9``. Returns ``{X: draws}``.
    """
    return {level: lookback_at_younger_fraction(edges, fracs, 1.0 - level) for level in levels}


def cumulative_mass_older_than(edges, fracs, grid):
    """Fraction of the final mass formed earlier than each lookback time on ``grid``."""
    edges = np.asarray(edges, dtype=float)
    fracs = np.atleast_2d(np.asarray(fracs, dtype=float))
    younger_edges = np.concatenate([np.zeros((len(fracs), 1)), np.cumsum(fracs, axis=1)], axis=1)
    out = np.empty((len(fracs), len(grid)))
    for i in range(len(fracs)):
        out[i] = 1.0 - np.interp(grid, edges, younger_edges[i])
    return out


def quantiles(draws, q=(0.16, 0.5, 0.84)):
    return tuple(float(v) for v in np.quantile(np.asarray(draws, dtype=float), q))


def posterior_weights(galaxy: GalaxyResult) -> np.ndarray:
    """Normalised importance weights of the nested-sampling dead points."""
    w = np.exp(galaxy.log_weights - np.max(galaxy.log_weights))
    return w / w.sum()


def weighted_quantile(values, weights, q):
    """Quantile of a weighted sample (linear interpolation on the weighted CDF)."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    order = np.argsort(values)
    cdf = np.cumsum(weights[order])
    cdf = cdf / cdf[-1]
    return float(np.interp(q, cdf, values[order]))


def posterior_median_f_calib(galaxy: GalaxyResult) -> float:
    """Posterior median of the calibration floor, matching the notebook's equal-weight median."""
    return float(np.exp(weighted_quantile(galaxy.samples["log_f_calib"], posterior_weights(galaxy), 0.5)))


# ----------------------------------------------------------------------------
# Model parameter block (generated from the objects)
# ----------------------------------------------------------------------------
def _fmt_array(values, digits=4) -> str:
    return "[" + ", ".join(f"{float(v):.{digits}g}" for v in np.atleast_1d(values)) + "]"


def model_parameter_block(model, ssp, likelihood, settings: dict, seed: int) -> str:
    """Plain-text statement of the model, read from the live objects only."""
    import jax.numpy as jnp

    csp = model.csp
    lines = ["MODEL PARAMETERS (generated from the SedModel object)"]
    # --- stellar population grid
    imf = getattr(ssp, "imf_type", None)
    lines += [
        "Stellar population grid",
        f"  library: {getattr(ssp, 'spec_library', None)}; isochrones: {getattr(ssp, 'isoc_type', None)}; "
        f"IMF: imf_type={imf} ({IMF_NAMES.get(imf, 'unknown')}); schema {getattr(ssp, 'schema_version', None)}",
        f"  grid axes: [alpha/Fe] {_fmt_array(np.asarray(ssp.ssp_afe), 3)}; log10 Z {len(np.asarray(ssp.ssp_lgmet))} nodes "
        f"[{float(np.min(ssp.ssp_lgmet)):.3f}, {float(np.max(ssp.ssp_lgmet)):.3f}] (absolute Z); "
        f"log10(age/Gyr) {len(np.asarray(ssp.ssp_lg_age_gyr))} nodes; wavelength {len(np.asarray(ssp.ssp_wave))} pts "
        f"[{float(np.min(ssp.ssp_wave)):.0f}, {float(np.max(ssp.ssp_wave)):.0f}] A",
    ]
    # --- SFH
    nodes_gyr = np.asarray(csp.sfh_times, dtype=float) / 1e9
    sfh_transform = model.transforms.get("sfh")
    lines += [
        "Star-formation history",
        f"  form: piecewise-constant SFR ('{csp.sfh_interp}' interpolation) on {len(nodes_gyr) - 1} lookback bins; "
        f"metallicity history: {'constant Z' if csp.zh_const else 'time-varying zh'}",
        f"  bin edges (lookback, Gyr): {_fmt_array(nodes_gyr, 4)}  (last edge = universe age at z)",
        f"  free parameters: logsfr_ratios[{len(nodes_gyr) - 1}] = log10(SFR_i / SFR_i+1), transform "
        f"'{getattr(sfh_transform, '__name__', repr(sfh_transform))}' -> unit-mass SFH (integral 1 Msun); "
        f"logmass scales the total formed mass",
    ]
    # --- free parameters and priors
    lines.append("Free parameters and priors")
    for name in model.param_names:
        init = model.theta_init[name]
        prior = model.priors.get(name)
        lines.append(
            f"  {name}: shape {tuple(np.shape(init))}; prior {describe_prior(prior) if prior is not None else 'none (improper flat)'}; "
            f"init {_fmt_array(init, 4)}"
        )
    # --- fixed and derived
    lines.append("Fixed and derived quantities")
    lines.append(f"  redshift: fixed at z = {model.zred:.6f} (SedModel.zred); SFH age grid tracks z: {bool(csp.track_zred_age)}")
    for derived, fn in model.transforms.items():
        if derived == "sfh":
            continue
        try:
            value = np.asarray(fn(model.theta_init), dtype=float)
            lines.append(f"  {derived}: fixed by transform '{getattr(fn, '__name__', 'lambda')}' = {_fmt_array(value, 4)}")
        except Exception as error:  # noqa: BLE001 - report, do not hide
            lines.append(f"  {derived}: transform '{getattr(fn, '__name__', 'lambda')}' (value not evaluable: {error})")
    # --- dust, nebular, IGM
    diff = getattr(csp, "diff_dust", None)
    law = diff.law_names_resolved[0] if diff is not None else "none"
    dust_params = list(getattr(diff, "dust_param_names", [])) if diff is not None else []
    lines += [
        "Dust, nebular emission, IGM",
        f"  diffuse attenuation: law '{law}', parameters {dust_params}; birth-cloud (age-dependent) dust: "
        f"{bool(getattr(csp, '_has_age_dependent_dust', False))}; dust emission: {bool(getattr(csp, '_has_dust_emission', False))}",
        f"  nebular emission: {'none' if 'noneb' in csp.get_spectrum.__name__ else 'included'} (spectrum model '{csp.get_spectrum.__name__}')",
        f"  IGM absorption: {'none' if getattr(csp, 'igm', None) is None else type(csp.igm).__name__}",
        f"  cosmology: {csp.cosmo!r}",
    ]
    # --- observations and calibration
    lines.append("Observations and calibration")
    for obs in model.observations:
        kind = type(obs).__name__
        mask = np.asarray(obs.mask, dtype=bool)
        if kind == "Photometry":
            lines.append(f"  {obs.name}: {kind}, {len(obs.filternames)} bands, {int(mask.sum())} fitted; filters {obs.filternames}")
        else:
            wave = np.asarray(obs.wavelength, dtype=float)
            lines.append(
                f"  {obs.name}: {kind}, {int(mask.sum())} of {len(mask)} native pixels fitted, "
                f"{wave[mask].min():.0f}-{wave[mask].max():.0f} A observed; instrument R = {float(obs.resolution):.0f} "
                f"({obs.smoothtype}, {obs.res_convention}); fixed stellar sigma_losvd = {float(obs.sigma_losvd):.1f} km/s; "
                f"CSP-level LOSVD {float(csp.sigma_losvd_kms):.1f} km/s"
            )
    for key, lhood in zip(likelihood.keys, likelihood.likelihoods):
        nm = lhood.noise_model
        terms = []
        if getattr(nm, "use_fractional", False):
            prior = model.priors.get("log_f_calib")
            bounds = ""
            if prior is not None and "low" in prior.params:
                bounds = f" in [{100 * np.exp(float(prior.params['low'])):.3g}%, {100 * np.exp(float(prior.params['high'])):.3g}%]"
            terms.append(f"model-scaled fractional floor f_calib*|mu| (log_f_calib free{bounds})")
        if getattr(nm, "use_data_fractional", False):
            terms.append("data-scaled fractional floor")
        if getattr(nm, "use_jitter", False):
            terms.append("additive jitter")
        lines.append(f"  likelihood[{key}]: {type(lhood).__name__} with {type(nm).__name__}: "
                     f"var = sigma_obs^2" + (" + " + " + ".join(terms) if terms else " (no extra terms)"))
        calibration = getattr(lhood, "calibration", None)
        if calibration is not None:
            lines.append(f"  likelihood[{key}] calibration polynomial: {calibration!r}")
        elif key == "spectrum":
            lines.append(f"  likelihood[{key}] calibration polynomial: none")
    if "spectrum_scaling" in model.priors:
        lines.append(f"  spectrum normalisation: free multiplicative spectrum_scaling, prior {describe_prior(model.priors['spectrum_scaling'])}")
    # --- sampler
    lines += [
        "Sampler",
        f"  {settings.get('sampler_name', 'blackjax.nss')}: num_live {settings.get('num_live')}, num_inner_steps {settings.get('num_inner_steps')}, "
        f"num_delete {settings.get('num_delete')}, logZ_tol {settings.get('logZ_tol')}; random seed {seed}",
    ]
    return "\n".join(lines)


def model_stamp(model, ssp, likelihood, settings: dict, seed: int) -> str:
    """Compact one-paragraph version of the block for figure footers."""
    csp = model.csp
    nodes = np.asarray(csp.sfh_times, dtype=float) / 1e9
    diff = getattr(csp, "diff_dust", None)
    law = diff.law_names_resolved[0] if diff is not None else "none"
    priors = "; ".join(f"{k} {describe_prior(v)}" for k, v in model.priors.items())
    fixed = []
    for derived, fn in model.transforms.items():
        if derived != "sfh":
            fixed.append(f"{derived}={float(np.asarray(fn(model.theta_init))[0]):g}")
    spec = next((o for o in model.observations if type(o).__name__ == "Spectrum"), None)
    spec_txt = (f"R={float(spec.resolution):.0f} {spec.res_convention}, sigma*={float(spec.sigma_losvd):.0f} km/s fixed"
                if spec is not None else "no spectrum")
    imf = getattr(ssp, "imf_type", None)
    return (
        f"SFH: {len(nodes) - 1} step bins, edges {_fmt_array(nodes, 3)} Gyr lookback | priors: {priors} | fixed: {', '.join(fixed)}, "
        f"z={model.zred:.4f} | dust: diffuse '{law}', no birth-cloud, no emission | nebular: "
        f"{'none' if 'noneb' in csp.get_spectrum.__name__ else 'yes'} | IGM: {'none' if getattr(csp, 'igm', None) is None else 'yes'} | "
        f"IMF: {IMF_NAMES.get(imf, imf)} ({getattr(ssp, 'spec_library', '?')}, {getattr(ssp, 'isoc_type', '?')}) | spectrum: {spec_txt}, "
        f"var = sigma^2 + (f_calib |mu|)^2 | sampler: {settings.get('sampler_name', 'nss')} live {settings.get('num_live')}, "
        f"steps {settings.get('num_inner_steps')}, delete {settings.get('num_delete')}, logZ_tol {settings.get('logZ_tol')}, seed {seed}"
    )


def _footer(fig, stamp: str):
    import textwrap

    text = "\n".join(textwrap.wrap("Model: " + stamp, width=175))
    fig.text(0.01, 0.005, text, ha="left", va="bottom", fontsize=5.6, color="#333333", family="monospace")


# ----------------------------------------------------------------------------
# Figures
# ----------------------------------------------------------------------------
def _band_labels(filters):
    short = {
        "cfht_megacam_us_9301": "u*", "subaru_suprimecam_B": "B", "subaru_suprimecam_V": "V",
        "subaru_suprimecam_rp": "r+", "subaru_suprimecam_ip": "i+", "subaru_suprimecam_zp": "z+",
        "vista_vircam_Y": "Y", "vista_vircam_J": "J", "vista_vircam_H": "H", "vista_vircam_Ks": "Ks",
        "spitzer_irac_ch1": "3.6um", "spitzer_irac_ch2": "4.5um",
    }
    return [short.get(f, f) for f in filters]


def plot_photometric_chi2(galaxy: GalaxyResult, model=None, like_ml: dict | None = None,
                          stamp: str = "", out: Path | None = None):
    """Per-band pull and chi^2 contribution against wavelength."""
    dp = galaxy.derived_phot
    mask = dp["mask"].astype(bool)
    wave = dp["wavelength"]
    labels = _band_labels(galaxy.phot["filters"])
    pull_stored = dp["pull"]
    stored = chi2_contributions(pull_stored, mask)
    n = stored["n"]
    if model is not None:
        phot_obs = model.obs_dict["photometry"]
        blue = np.array([float(f.blue_edge) for f in phot_obs.filterset.filters])
        red = np.array([float(f.red_edge) for f in phot_obs.filterset.filters])
        xerr = np.vstack([wave - blue, red - wave])
    else:
        xerr = None
    fitted_wave = galaxy.spec["wavelength"][galaxy.spec["mask"]]

    fig, axes = plt.subplots(2, 1, figsize=(9.0, 6.4), sharex=True, gridspec_kw={"height_ratios": [1.3, 1.0]})
    ax = axes[0]
    ax.axhspan(-2, 2, color="0.92", linewidth=0)
    ax.axhspan(-1, 1, color="0.84", linewidth=0)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvspan(fitted_wave.min(), fitted_wave.max(), color="tab:purple", alpha=0.08, linewidth=0)
    ax.errorbar(wave[mask], pull_stored[mask], xerr=None if xerr is None else xerr[:, mask], fmt="o", color=BLUE,
                ms=5, capsize=0, lw=0.8, label=r"stored: $(y - q_{50})/\sigma$")
    if like_ml is not None:
        chi_ml = like_ml["photometry"]["chi"]
        ax.plot(wave[mask], chi_ml[mask], "s", mfc="none", mec=RED, ms=6, mew=1.0,
                label=r"at $\theta_{\rm ML}$: fit's own $\sigma$")
    for w, label, p in zip(wave, labels, pull_stored):
        ax.annotate(label, (w, p), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7, color="0.2")
    ax.set_ylabel(r"pull $(F_{\rm obs} - F_{\rm model})/\sigma$")
    ax.set_xscale("log")
    span = max(2.5, float(np.max(np.abs(pull_stored[mask]))) * 1.35)
    ax.set_ylim(-span, span)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title(f"{galaxy.spect_id} (object {galaxy.object_id}), z = {galaxy.z:.4f}, catalogue S/N {galaxy.catalogue_sn:.1f}: photometric residuals", fontsize=10)

    ax = axes[1]
    contrib = stored["contribution"]
    order = np.arange(len(wave))
    ax.bar(wave[mask], contrib[mask], width=0.12 * wave[mask], color=BLUE, alpha=0.75, label=r"stored $\chi^2_i$")
    if like_ml is not None:
        ax.plot(wave[mask], like_ml["photometry"]["chi"][mask] ** 2, "s", mfc="none", mec=RED, ms=6, mew=1.0,
                label=r"$\chi^2_i$ at $\theta_{\rm ML}$")
    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_xlabel(r"observed effective wavelength [$\mathrm{\AA}$]")
    ax.set_ylabel(r"$\chi^2$ contribution per band")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    text = (f"stored: $\\chi^2_{{\\rm phot}}$ = {stored['total']:.1f}, N = {n}, $\\chi^2/N$ = {stored['total'] / n:.2f}\n"
            f"(5% flux floor in $\\sigma$; posterior-median prediction)")
    if like_ml is not None:
        c = like_ml["photometry"]["chi2"]
        text += f"\nat $\\theta_{{\\rm ML}}$: $\\chi^2_{{\\rm phot}}$ = {c:.1f}, $\\chi^2/N$ = {c / n:.2f}"
    text += f"\nworst band: {labels[int(np.argmax(np.where(mask, np.abs(pull_stored), -1)))]}, pull {pull_stored[int(np.argmax(np.where(mask, np.abs(pull_stored), -1)))]:+.2f}"
    ax.text(0.99, 0.97, text, transform=ax.transAxes, ha="right", va="top", fontsize=8,
            bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.95))
    del order
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _footer(fig, stamp)
    if out is not None:
        fig.savefig(out)
        plt.close(fig)
        return None
    return fig


def plot_spectral_chi2(galaxy: GalaxyResult, like_ml: dict | None = None, stamp: str = "", out: Path | None = None):
    """Per-pixel pull, binned mean pull^2 and cumulative chi^2 against wavelength."""
    wave = galaxy.spec["wavelength"]
    ds = galaxy.derived_spec
    mask = ds["mask"].astype(bool)
    pull = ds["pull"]
    stored = chi2_contributions(np.nan_to_num(pull), mask)
    cats = spectrum_mask_categories(galaxy)
    outliers = mask & (np.abs(np.nan_to_num(pull)) > OUTLIER_PULL)
    f_med = posterior_median_f_calib(galaxy)
    f_hi = float(np.exp(parse_prior(galaxy.prior_text["log_f_calib"]).params["high"]))
    saturated = f_med >= CALIB_SATURATION_FRACTION * f_hi

    fig, axes = plt.subplots(3, 1, figsize=(12.0, 8.6), sharex=True, gridspec_kw={"height_ratios": [1.6, 1.0, 1.0]})
    ax = axes[0]
    ax.axhspan(-1, 1, color="0.88", linewidth=0)
    ax.axhline(0, color="k", lw=0.8)
    shown = {}
    for key, color, label in (("emission_line", ORANGE, "emission-line window (masked)"),
                              ("telluric", "#8c564b", "telluric band (masked)"),
                              ("bad_pixel", "0.75", "bad pixel (masked)")):
        idx = np.flatnonzero(cats[key])
        if idx.size == 0:
            continue
        breaks = np.flatnonzero(np.diff(idx) > 1)
        starts = np.concatenate([[idx[0]], idx[breaks + 1]])
        stops = np.concatenate([idx[breaks], [idx[-1]]])
        for s, e in zip(starts, stops):
            for a in axes:
                a.axvspan(wave[s], wave[e], color=color, alpha=0.35 if key != "bad_pixel" else 0.5, linewidth=0,
                          label=label if (key not in shown and a is ax) else None)
            shown[key] = True
    ax.plot(wave, np.where(mask, pull, np.nan), color="0.25", lw=0.45, rasterized=True, label="stored pull (fitted pixels)")
    if like_ml is not None:
        chi_ml = like_ml["spectrum"]["chi"]
        ax.plot(wave, np.where(mask, chi_ml, np.nan), color=RED, lw=0.35, alpha=0.6, rasterized=True,
                label=r"pull at $\theta_{\rm ML}$ (fit's own $\sigma$)")
    if outliers.any():
        ax.plot(wave[outliers], pull[outliers], "o", color=RED, ms=3.5, label=f"|pull| > {OUTLIER_PULL:g} ({int(outliers.sum())} px)")
    ax.set_ylabel("pull")
    ax.set_title(f"{galaxy.spect_id} (object {galaxy.object_id}), z = {galaxy.z:.4f}, catalogue S/N {galaxy.catalogue_sn:.1f}: spectral residuals", fontsize=10)
    ax.legend(frameon=False, fontsize=7.5, ncol=3, loc="upper left")
    top = ax.secondary_xaxis("top", functions=(lambda o: o / (1 + galaxy.z), lambda r: r * (1 + galaxy.z)))
    top.set_xlabel(r"rest-frame wavelength [$\mathrm{\AA}$]")

    ax = axes[1]
    edges, mean, counts = binned_mean_pull2(wave, np.nan_to_num(pull), mask)
    ax.stairs(mean, edges, color=BLUE, lw=1.0, label=f"stored, {BIN_WIDTH_AA:g} $\\mathrm{{\\AA}}$ bins")
    if like_ml is not None:
        _, mean_ml, _ = binned_mean_pull2(wave, like_ml["spectrum"]["chi"], mask)
        ax.stairs(mean_ml, edges, color=RED, lw=0.8, alpha=0.7, label=r"at $\theta_{\rm ML}$")
    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_ylabel(r"mean pull$^2$ per bin")
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = axes[2]
    ax.plot(wave, stored["cumulative_fraction"], color=BLUE, lw=1.2, label=r"cumulative $\chi^2$ fraction (stored)")
    if like_ml is not None:
        ml = chi2_contributions(like_ml["spectrum"]["chi"], mask)
        ax.plot(wave, ml["cumulative_fraction"], color=RED, lw=0.9, alpha=0.7, label=r"at $\theta_{\rm ML}$")
    ax.plot(wave, np.cumsum(mask) / mask.sum(), color="0.5", lw=0.9, ls="--", label="uniform per fitted pixel")
    ax.set_ylim(0, 1.02)
    ax.set_ylabel(r"cumulative $\chi^2$ fraction")
    ax.set_xlabel(r"observed vacuum wavelength [$\mathrm{\AA}$]")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    n = stored["n"]
    text = (f"stored: $\\chi^2_{{\\rm spec}}$ = {stored['total']:.1f}, N = {n}, $\\chi^2/N$ = {stored['total'] / n:.3f}\n"
            f"$\\sigma_{{\\rm eff}}^2 = \\sigma_{{\\rm obs}}^2 + (f_{{\\rm calib}}|q_{{50}}|)^2$, median $f_{{\\rm calib}}$ = {100 * f_med:.2f}% "
            f"(prior $\\leq$ {100 * f_hi:.0f}%){'  SATURATED' if saturated else ''}")
    if like_ml is not None:
        c = like_ml["spectrum"]["chi2"]
        text += (f"\nat $\\theta_{{\\rm ML}}$: $\\chi^2_{{\\rm spec}}$ = {c:.1f}, $\\chi^2/N$ = {c / n:.3f}, "
                 f"$f_{{\\rm calib}}$ = {100 * like_ml['f_calib']:.2f}%; ln L recomputed $-$ stored = {like_ml['lnl'] - galaxy.log_likelihoods[max_likelihood_index(galaxy)]:+.2f}")
    text += (f"\nmasked: {int(cats['bad_pixel'].sum())} bad px, {int(cats['emission_line'].sum())} emission-line px, "
             f"{int(cats['telluric'].sum())} telluric px; outliers |pull| > {OUTLIER_PULL:g}: {int(outliers.sum())}")
    ax.text(0.99, 0.05, text, transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.95))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    _footer(fig, stamp)
    if out is not None:
        fig.savefig(out)
        plt.close(fig)
        return None
    return fig


def plot_sf_timescales(galaxy: GalaxyResult, stamp: str = "", out: Path | None = None):
    """Cumulative mass formed by lookback time with t10..t90 and their posteriors."""
    edges = galaxy.sfh_edges_gyr
    fracs = galaxy.mass_fraction_draws
    tx = formation_lookback_times(edges, fracs)
    grid = np.linspace(0.0, edges[-1], 600)
    older = cumulative_mass_older_than(edges, fracs, grid)
    q16, q50, q84 = np.percentile(older, [16, 50, 84], axis=0)
    age_q = quantiles(galaxy.mass_weighted_age_draws)

    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    for e in edges:
        ax.axvline(e, color="0.85", lw=0.7, zorder=0)
    ax.fill_between(grid, q16, q84, color=GREEN, alpha=0.25, linewidth=0, label="16-84% of posterior draws")
    ax.plot(grid, q50, color=GREEN, lw=1.5, label="posterior median")
    rows = []
    for k, (level, draws) in enumerate(tx.items()):
        lo, med, hi = quantiles(draws)
        lo2, hi2 = quantiles(draws, (0.025, 0.975))
        ax.plot([0, med], [level, level], color="0.4", lw=0.7, ls=":")
        ax.errorbar([med], [level], xerr=[[med - lo2], [hi2 - med]], fmt="none", ecolor=BLUE, elinewidth=0.8, capsize=0, alpha=0.6)
        ax.errorbar([med], [level], xerr=[[med - lo], [hi - med]], fmt="o", color=BLUE, ms=5, elinewidth=2.0, capsize=3)
        ax.annotate(f"$t_{{{int(round(100 * level))}}}$", (med, level), textcoords="offset points", xytext=(6, 6), fontsize=8, color=BLUE)
        rows.append(f"$t_{{{int(round(100 * level))}}}$ = {med:.2f} $^{{+{hi - med:.2f}}}_{{-{med - lo:.2f}}}$ Gyr")
    ax.set_xlim(0, edges[-1] * 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("lookback time from z_obs [Gyr]")
    ax.set_ylabel("fraction of final stellar mass formed earlier than this lookback time")
    top = ax.secondary_xaxis("top", functions=(lambda lb: edges[-1] - lb, lambda age: edges[-1] - age))
    top.set_xlabel("age of the Universe at formation [Gyr]")
    ax.set_title(f"{galaxy.spect_id} (object {galaxy.object_id}), z = {galaxy.z:.4f}: star-formation timescales", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="center right")
    text = "\n".join(rows) + (f"\nmass-weighted age $t_{{\\rm MW}}$ = {age_q[1]:.2f} $^{{+{age_q[2] - age_q[1]:.2f}}}_{{-{age_q[1] - age_q[0]:.2f}}}$ Gyr"
                              f"\nuniverse age at z: {edges[-1]:.2f} Gyr; {len(edges) - 1} SFH bins (grey lines);"
                              f"\n{len(fracs)} posterior draws; errors 16-84% (thick), 2.5-97.5% (thin)")
    ax.text(0.02, 0.03, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.95))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    _footer(fig, stamp)
    if out is not None:
        fig.savefig(out)
        plt.close(fig)
        return None
    return fig


def plot_sf_timescale_summary(table: pd.DataFrame, out: Path | None = None, stamp: str = ""):
    """Cross-galaxy view of t10..t90: ladder sorted by t50, t50 against z, distributions."""
    d = table.sort_values("t50_q50").reset_index(drop=True)
    x = np.arange(len(d))
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.6), gridspec_kw={"width_ratios": [1.6, 1.1, 1.0]})
    ax = axes[0]
    ax.fill_between(x, d["t90_q50"], d["t10_q50"], color=BLUE, alpha=0.18, linewidth=0, label=r"$t_{90}$ to $t_{10}$")
    ax.fill_between(x, d["t80_q50"], d["t20_q50"], color=BLUE, alpha=0.35, linewidth=0, label=r"$t_{80}$ to $t_{20}$")
    ax.errorbar(x, d["t50_q50"], yerr=[d["t50_q50"] - d["t50_q16"], d["t50_q84"] - d["t50_q50"]], fmt="o", color=ORANGE,
                ms=2.2, elinewidth=0.5, capsize=0, label=r"$t_{50}$ with 16-84%")
    ax.set_xlabel(r"galaxies sorted by $t_{50}$")
    ax.set_ylabel("lookback time [Gyr]")
    ax.set_title(f"Formation timescales, N = {len(d)}", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax = axes[1]
    ax.errorbar(d["z"], d["t50_q50"], yerr=[d["t50_q50"] - d["t50_q16"], d["t50_q84"] - d["t50_q50"]], fmt="o", color=ORANGE,
                ms=3, elinewidth=0.5, capsize=0, label=r"$t_{50}$")
    ax.plot(d["z"], d["t10_q50"], "v", color=BLUE, ms=3, alpha=0.6, label=r"$t_{10}$")
    ax.plot(d["z"], d["t90_q50"], "^", color=GREEN, ms=3, alpha=0.6, label=r"$t_{90}$")
    zz = np.linspace(d["z"].min(), d["z"].max(), 50)
    from ceridwen.cosmology import age_gyr

    ax.plot(zz, [float(age_gyr(v)) for v in zz], color="k", lw=0.8, ls="--", label="universe age at z")
    ax.set_xlabel("redshift")
    ax.set_ylabel("lookback time [Gyr]")
    ax.legend(frameon=False, fontsize=7.5, ncol=2)
    ax.set_title(r"$t_X$ against redshift", fontsize=10)
    ax = axes[2]
    bins = np.linspace(0, max(float(d["t10_q50"].max()), 1.0) * 1.05, 26)
    for col, color, label in (("t10_q50", BLUE, r"$t_{10}$"), ("t50_q50", ORANGE, r"$t_{50}$"), ("t90_q50", GREEN, r"$t_{90}$")):
        ax.hist(d[col], bins=bins, histtype="step", color=color, lw=1.3, label=f"{label} median {d[col].median():.2f} Gyr")
    ax.set_xlabel("lookback time [Gyr]")
    ax.set_ylabel("galaxies")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax.set_title("Distributions of posterior medians", fontsize=10)
    fig.tight_layout(rect=(0, 0.1 if stamp else 0, 1, 1))
    if stamp:
        _footer(fig, stamp)
    if out is not None:
        fig.savefig(out)
        plt.close(fig)
        return None
    return fig


def plot_photometry_summary(band_table: pd.DataFrame, table: pd.DataFrame, out: Path | None = None):
    """Per-band mean pull and chi^2 across the sample, and the photometric chi^2/N histogram."""
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.2), gridspec_kw={"width_ratios": [1.3, 1.3, 1.0]})
    ax = axes[0]
    ax.axhline(0, color="k", lw=0.8)
    ax.axhspan(-1, 1, color="0.9", linewidth=0)
    ax.errorbar(band_table["wavelength"], band_table["pull_median"],
                yerr=[band_table["pull_median"] - band_table["pull_q16"], band_table["pull_q84"] - band_table["pull_median"]],
                fmt="o", color=BLUE, ms=5, capsize=2, label="median pull, 16-84% over galaxies")
    for w, lab, p in zip(band_table["wavelength"], band_table["band"], band_table["pull_median"]):
        ax.annotate(lab, (w, p), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel(r"effective wavelength [$\mathrm{\AA}$]")
    ax.set_ylabel("pull (stored)")
    ax.set_title("Photometric pull by band, all galaxies", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1]
    ax.bar(band_table["wavelength"], band_table["chi2_mean"], width=0.12 * band_table["wavelength"], color=BLUE, alpha=0.75)
    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_xlabel(r"effective wavelength [$\mathrm{\AA}$]")
    ax.set_ylabel(r"mean $\chi^2$ contribution per band")
    ax.set_title(r"Where the photometric $\chi^2$ comes from", fontsize=10)
    ax = axes[2]
    vals = table["phot_redchi2_stored"]
    ax.hist(vals, bins=30, color=BLUE, alpha=0.75)
    ax.axvline(1.0, color="k", lw=0.8, ls="--")
    ax.axvline(PHOT_REDCHI2_FLAG, color=RED, lw=0.8, ls=":", label=f"flag threshold {PHOT_REDCHI2_FLAG:g}")
    ax.set_xlabel(r"photometric $\chi^2/N$ (N = 12)")
    ax.set_ylabel("galaxies")
    ax.set_title(f"median {vals.median():.2f}; {int((vals > PHOT_REDCHI2_FLAG).sum())} of {len(vals)} above {PHOT_REDCHI2_FLAG:g}", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    if out is not None:
        fig.savefig(out)
        plt.close(fig)
        return None
    return fig


# ----------------------------------------------------------------------------
# Per-galaxy pipeline
# ----------------------------------------------------------------------------
def analyse_galaxy(galaxy: GalaxyResult, ssp, figure_dir: Path | None, with_likelihood: bool = True) -> dict:
    """Checks, numbers and figures for one galaxy; returns one summary row."""
    row = {
        "target": galaxy.target, "object_id": galaxy.object_id, "spect_id": galaxy.spect_id, "z": galaxy.z,
        "catalogue_sn": galaxy.catalogue_sn, "seed": galaxy.seed, "n_free": galaxy.n_free,
    }
    dp, ds = galaxy.derived_phot, galaxy.derived_spec
    pmask, smask = dp["mask"].astype(bool), ds["mask"].astype(bool)
    # --- consistency of the stored numbers with their definitions and with the fit inputs
    row["mask_match"] = bool(np.array_equal(smask, galaxy.spec["mask"]) and np.array_equal(pmask, galaxy.phot["mask"]))
    row["sigma_match"] = bool(np.array_equal(ds["uncertainty"], galaxy.spec["uncertainty"])
                              and np.array_equal(dp["uncertainty"], galaxy.phot["uncertainty"]))
    f_med = posterior_median_f_calib(galaxy)
    eff = np.hypot(ds["uncertainty"], f_med * np.abs(ds["posterior_q50"]))
    row["eff_sigma_max_rel_diff"] = float(np.max(np.abs(eff[smask] - ds["effective_uncertainty"][smask]) / ds["effective_uncertainty"][smask]))
    pull_recomputed = (ds["observed"] - ds["posterior_q50"]) / ds["effective_uncertainty"]
    row["pull_recompute_max_abs_diff"] = float(np.nanmax(np.abs(pull_recomputed[smask] - ds["pull"][smask])))
    spec_stored = chi2_contributions(np.nan_to_num(ds["pull"]), smask)
    phot_stored = chi2_contributions(dp["pull"], pmask)
    row["n_phot"], row["n_spec"] = phot_stored["n"], spec_stored["n"]
    row["phot_chi2_stored"] = phot_stored["total"]
    row["spec_chi2_stored"] = spec_stored["total"]
    row["joint_chi2_stored"] = phot_stored["total"] + spec_stored["total"]
    row["phot_chi2_h5"] = float(galaxy.diagnostics["photometry_chi2"])
    row["spec_chi2_h5"] = float(galaxy.diagnostics["spectrum_chi2"])
    row["chi2_h5_recompute_max_abs_diff"] = float(max(abs(row["phot_chi2_stored"] - row["phot_chi2_h5"]),
                                                      abs(row["spec_chi2_stored"] - row["spec_chi2_h5"])))
    row["ndof_h5_match"] = bool(int(galaxy.diagnostics["photometry_ndof"]) == phot_stored["n"]
                                and int(galaxy.diagnostics["spectrum_ndof"]) == spec_stored["n"])
    row["phot_redchi2_stored"] = phot_stored["total"] / phot_stored["n"]
    row["spec_redchi2_stored"] = spec_stored["total"] / spec_stored["n"]
    row["joint_redchi2_stored"] = row["joint_chi2_stored"] / (phot_stored["n"] + spec_stored["n"] - galaxy.n_free)
    row["f_calib_median_pct"] = 100 * f_med
    row["f_calib_upper_pct"] = 100 * float(np.exp(parse_prior(galaxy.prior_text["log_f_calib"]).params["high"]))
    row["calib_saturated"] = bool(f_med >= CALIB_SATURATION_FRACTION * row["f_calib_upper_pct"] / 100)
    row["n_outlier_pixels"] = int(np.sum(smask & (np.abs(np.nan_to_num(ds["pull"])) > OUTLIER_PULL)))
    labels = _band_labels(galaxy.phot["filters"])
    worst = int(np.argmax(np.where(pmask, np.abs(dp["pull"]), -1)))
    row["worst_band"], row["worst_band_pull"] = labels[worst], float(dp["pull"][worst])
    for lab, p in zip(labels, dp["pull"]):
        row[f"pull_{lab}"] = float(p)
    cats = spectrum_mask_categories(galaxy)
    row["n_bad_pixels"], row["n_emission_masked"], row["n_telluric_masked"] = (int(cats[k].sum()) for k in ("bad_pixel", "emission_line", "telluric"))
    row["ess"] = float(galaxy.diagnostics["posterior_weight_ess"])
    row["lnZ"], row["lnZ_err"] = galaxy.log_evidence, galaxy.log_evidence_err
    # --- formation times (formed-by convention)
    tx = formation_lookback_times(galaxy.sfh_edges_gyr, galaxy.mass_fraction_draws)
    for level, draws in tx.items():
        lo, med, hi = quantiles(draws)
        key = f"t{int(round(100 * level))}"
        row[f"{key}_q16"], row[f"{key}_q50"], row[f"{key}_q84"] = lo, med, hi
    age_lo, age_med, age_hi = quantiles(galaxy.mass_weighted_age_draws)
    row["age_q16"], row["age_q50"], row["age_q84"] = age_lo, age_med, age_hi
    row["universe_age_gyr"] = galaxy.universe_age_gyr
    # --- likelihood-consistent chi at theta_ML
    like_ml = None
    model = None
    stamp = ""
    block = None
    if with_likelihood:
        model, likelihood, _ = rebuild_model(galaxy, ssp)
        i_ml = max_likelihood_index(galaxy)
        like_ml = likelihood_terms(model, likelihood, theta_at(galaxy, i_ml))
        row["lnl_ml_stored"] = float(galaxy.log_likelihoods[i_ml])
        row["lnl_ml_recomputed"] = like_ml["lnl"]
        row["lnl_ml_diff"] = like_ml["lnl"] - row["lnl_ml_stored"]
        row["phot_chi2_ml"] = like_ml["photometry"]["chi2"]
        row["spec_chi2_ml"] = like_ml["spectrum"]["chi2"]
        row["f_calib_ml_pct"] = 100 * like_ml["f_calib"]
        row["ml_ndof_match"] = bool(like_ml["photometry"]["ndof"] == phot_stored["n"] and like_ml["spectrum"]["ndof"] == spec_stored["n"])
        block = model_parameter_block(model, ssp, likelihood, galaxy.settings, galaxy.seed)
        stamp = model_stamp(model, ssp, likelihood, galaxy.settings, galaxy.seed)
        row["block_matches_stored"] = (galaxy.stored_block.strip() == block.strip()) if galaxy.stored_block else None
    # --- flags
    flags = []
    if row["phot_redchi2_stored"] > PHOT_REDCHI2_FLAG:
        flags.append(f"photometry chi2/N {row['phot_redchi2_stored']:.1f} > {PHOT_REDCHI2_FLAG:g}")
    if row["spec_redchi2_stored"] > SPEC_REDCHI2_FLAG:
        flags.append(f"spectrum chi2/N {row['spec_redchi2_stored']:.2f} > {SPEC_REDCHI2_FLAG:g}")
    if row["calib_saturated"]:
        flags.append(f"calibration floor at prior bound ({row['f_calib_median_pct']:.1f}% of {row['f_calib_upper_pct']:.0f}%)")
    if row["n_outlier_pixels"] > 0:
        flags.append(f"{row['n_outlier_pixels']} pixels with |pull| > {OUTLIER_PULL:g}")
    if not (row["mask_match"] and row["sigma_match"] and row["ndof_h5_match"]):
        flags.append("stored mask/sigma/ndof do not match the fit inputs")
    row["flags"] = "; ".join(flags)
    # --- figures
    if figure_dir is not None:
        figure_dir.mkdir(parents=True, exist_ok=True)
        plot_photometric_chi2(galaxy, model, like_ml, stamp, figure_dir / "photometric_chi2.png")
        plot_spectral_chi2(galaxy, like_ml, stamp, figure_dir / "spectral_chi2.png")
        plot_sf_timescales(galaxy, stamp, figure_dir / "sf_timescales.png")
        if block is not None:
            (figure_dir / "model_parameters.txt").write_text(block + "\n", encoding="utf-8")
    row["_block"] = block
    row["_stamp"] = stamp
    return row


def band_summary(table: pd.DataFrame, filters) -> pd.DataFrame:
    labels = _band_labels(filters)
    rows = []
    for lab, w in zip(labels, table.attrs.get("band_wavelengths", [np.nan] * len(labels))):
        pulls = table[f"pull_{lab}"].to_numpy(dtype=float)
        rows.append({
            "band": lab, "wavelength": w, "pull_median": float(np.median(pulls)),
            "pull_q16": float(np.quantile(pulls, 0.16)), "pull_q84": float(np.quantile(pulls, 0.84)),
            "chi2_mean": float(np.mean(pulls**2)), "frac_abs_pull_gt2": float(np.mean(np.abs(pulls) > 2)),
        })
    return pd.DataFrame(rows)


def run(run_dir: Path, out_csv: Path, summary_dir: Path, targets: list[str] | None = None,
        with_likelihood: bool = True, log=print) -> pd.DataFrame:
    run_dir = Path(run_dir)
    folders = sorted(p for p in run_dir.iterdir() if p.is_dir() and (p / "ceridwen_result.h5").exists())
    if targets:
        folders = [p for p in folders if p.name in set(targets) or p.name.split("-", 1)[-1] in set(targets)]
    ssp = load_ssp() if with_likelihood else None
    rows = []
    started = time.monotonic()
    band_wavelengths = None
    filters = None
    for k, folder in enumerate(folders, 1):
        t0 = time.monotonic()
        galaxy = load_galaxy(folder)
        row = analyse_galaxy(galaxy, ssp, folder / FIGURE_SUBDIR, with_likelihood)
        rows.append({key: value for key, value in row.items() if not key.startswith("_")})
        band_wavelengths = galaxy.derived_phot["wavelength"]
        filters = galaxy.phot["filters"]
        log(f"[{k}/{len(folders)}] {galaxy.target}: phot chi2/N {row['phot_redchi2_stored']:.2f}, spec chi2/N {row['spec_redchi2_stored']:.3f}, "
            f"f_calib {row['f_calib_median_pct']:.2f}%"
            + (f", lnL diff {row['lnl_ml_diff']:+.2f}" if with_likelihood else "")
            + f" ({time.monotonic() - t0:.1f} s)")
    table = pd.DataFrame(rows)
    table.attrs["band_wavelengths"] = list(map(float, band_wavelengths)) if band_wavelengths is not None else []
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_csv, index=False)
    summary_dir.mkdir(parents=True, exist_ok=True)
    if len(table):
        plot_sf_timescale_summary(table, summary_dir / "sf-timescale-summary.png")
        bands = band_summary(table, filters)
        bands.to_csv(summary_dir / "photometry-band-summary.csv", index=False)
        plot_photometry_summary(bands, table, summary_dir / "photometry-summary.png")
    log(f"wrote {out_csv} ({len(table)} galaxies) and summary figures to {summary_dir} in {time.monotonic() - started:.0f} s")
    return table


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("run")
    r.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    r.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_CSV)
    r.add_argument("--summary-dir", type=Path, default=DEFAULT_SUMMARY_DIR)
    r.add_argument("--target", action="append", help="target folder name or SPECT_ID (repeatable)")
    r.add_argument("--no-likelihood", action="store_true", help="skip the model rebuild and theta_ML check")
    c = sub.add_parser("check")
    c.add_argument("target_dir", type=Path)
    b = sub.add_parser("block")
    b.add_argument("target_dir", type=Path)
    args = parser.parse_args(argv)
    if args.command == "run":
        run(args.run_dir, args.out_csv, args.summary_dir, args.target, not args.no_likelihood)
        return 0
    galaxy = load_galaxy(args.target_dir)
    ssp = load_ssp()
    model, likelihood, _ = rebuild_model(galaxy, ssp)
    if args.command == "block":
        print(model_parameter_block(model, ssp, likelihood, galaxy.settings, galaxy.seed))
        return 0
    i_ml = max_likelihood_index(galaxy)
    terms = likelihood_terms(model, likelihood, theta_at(galaxy, i_ml))
    print(f"{galaxy.target}: stored lnL(theta_ML) = {galaxy.log_likelihoods[i_ml]:.4f}; recomputed = {terms['lnl']:.4f}; "
          f"diff = {terms['lnl'] - galaxy.log_likelihoods[i_ml]:+.4f}")
    print(f"  spectrum chi2 at theta_ML = {terms['spectrum']['chi2']:.2f} over {terms['spectrum']['ndof']}; stored = {galaxy.diagnostics['spectrum_chi2']:.2f}")
    print(f"  photometry chi2 at theta_ML = {terms['photometry']['chi2']:.2f} over {terms['photometry']['ndof']}; stored = {galaxy.diagnostics['photometry_chi2']:.2f}")
    print(f"  f_calib at theta_ML = {100 * terms['f_calib']:.2f}%; jax backend = {__import__('jax').default_backend()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
