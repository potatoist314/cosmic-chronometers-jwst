#!/usr/bin/env python3
"""Run and compare short, fixed Ceridwen GPU benchmarks on Vast.ai."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import re
import statistics
import subprocess
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

WORKLOAD_ID = "m1_210210_joint_full_v1"
TARGET_ID = "M1_210210"
GRID_ID = "amist_c3k_hr_krou_afe"
GRID_SCHEMA = "2.1"
GRID_SHAPE = (5, 13, 107, 10992)
EXPECTED_PHOTOMETRY_BANDS = 11
EXPECTED_SPECTRAL_PIXELS = 3523
SEED = 20260812
NUM_LIVE = 300
NUM_INNER_STEPS = 40
NUM_DELETE = 25
REFERENCE_LOGZ_TOL = -3.0
WARMUP_STEPS = 1
TIMED_STEPS = 5
CALLS_PER_STEP = NUM_INNER_STEPS * NUM_DELETE
JAX_MEMORY_FRACTION = "0.50"
LEGACY_RESULT_SCHEMA_VERSION = 1
RESULT_SCHEMA_VERSION = 2

COMPARISON_SOFTWARE_FIELDS = (
    "python",
    "jax",
    "jaxlib",
    "blackjax",
    "ceridwen",
    "jax_enable_x64",
)
LEGACY_COMPARISON_SOFTWARE_FIELDS = (
    *COMPARISON_SOFTWARE_FIELDS,
    "xla_preallocate_env",
)

FILTER_NAMES = [
    "cfht_megacam_us_9301",
    "subaru_suprimecam_B",
    "subaru_suprimecam_V",
    "subaru_suprimecam_rp",
    "subaru_suprimecam_ip",
    "subaru_suprimecam_zp",
    "vista_vircam_Y",
    "vista_vircam_J",
    "vista_vircam_H",
    "vista_vircam_Ks",
    "spitzer_irac_ch1",
    "spitzer_irac_ch2",
]
FLUX_COLUMNS = [
    "Fuap3",
    "FBap3",
    "FVap3",
    "Frap3",
    "Fipap3",
    "Fzppap3",
    "FYap3",
    "FJap3",
    "FHap3",
    "FKsap3",
    "F3.6um",
    "F4.5um",
]
ERROR_COLUMNS = [f"e_{name}" for name in FLUX_COLUMNS]
REST_EMISSION_LINES = [3726.0, 3728.8, 4861.3, 4958.9, 5006.8]


class BenchmarkError(RuntimeError):
    """Report an invalid benchmark environment or result."""


@dataclass(frozen=True)
class BuiltWorkload:
    """Hold the configured model, likelihood, metadata, and exact inputs."""

    model: Any
    likelihood: Any
    metadata: dict[str, Any]
    input_paths: dict[str, Path]


def _positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def _run_text(command: list[str], cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _git_metadata(project_root: Path) -> dict[str, Any]:
    root_commit = _run_text(["git", "rev-parse", "HEAD"], cwd=project_root)
    root_changes = _run_text(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=project_root,
    )
    ceridwen_root = project_root / "ceridwen"
    ceridwen_commit = _run_text(["git", "rev-parse", "HEAD"], cwd=ceridwen_root)
    ceridwen_changes = _run_text(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ceridwen_root,
    )
    return {
        "project_commit": root_commit,
        "project_tracked_changes": root_changes or "",
        "ceridwen_commit": ceridwen_commit,
        "ceridwen_tracked_changes": ceridwen_changes or "",
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fingerprint(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _comparison_payload(
    workload: dict[str, Any],
    input_sha256: dict[str, str],
    ceridwen_commit: str | None,
    runtime: dict[str, Any],
) -> dict[str, Any]:
    """Return the scientific and software contract used for comparisons."""
    return {
        "workload": workload,
        "input_sha256": input_sha256,
        "ceridwen_commit": ceridwen_commit,
        "software": {name: runtime[name] for name in COMPARISON_SOFTWARE_FIELDS},
    }


def _comparison_fingerprint(
    workload: dict[str, Any],
    input_sha256: dict[str, str],
    ceridwen_commit: str | None,
    runtime: dict[str, Any],
) -> str:
    return _fingerprint(
        _comparison_payload(workload, input_sha256, ceridwen_commit, runtime)
    )


def _legacy_comparison_fingerprint(record: dict[str, Any]) -> str:
    runtime = record["runtime"]
    return _fingerprint(
        {
            "workload": record["workload"],
            "input_sha256": record["input_sha256"],
            "benchmark_script_sha256": record["benchmark_script_sha256"],
            "ceridwen_commit": record["git"]["ceridwen_commit"],
            "software": {
                name: runtime[name] for name in LEGACY_COMPARISON_SOFTWARE_FIELDS
            },
        }
    )


def _normalized_comparison_fingerprint(record: dict[str, Any]) -> str:
    schema_version = record.get("schema_version")
    stored_fingerprint = record.get("comparison_fingerprint")
    if schema_version == LEGACY_RESULT_SCHEMA_VERSION:
        expected_fingerprint = _legacy_comparison_fingerprint(record)
    elif schema_version == RESULT_SCHEMA_VERSION:
        expected_fingerprint = _comparison_fingerprint(
            record["workload"],
            record["input_sha256"],
            record["git"]["ceridwen_commit"],
            record["runtime"],
        )
    else:
        raise BenchmarkError("a benchmark result uses an unsupported schema")
    if stored_fingerprint != expected_fingerprint:
        raise BenchmarkError("a benchmark result has an invalid comparison fingerprint")
    return _comparison_fingerprint(
        record["workload"],
        record["input_sha256"],
        record["git"]["ceridwen_commit"],
        record["runtime"],
    )


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned or "unknown_gpu"


def result_directory_name(gpu_name: str, vast_host: str | None, date: str) -> str:
    hardware = _slug(gpu_name.removeprefix("NVIDIA "))
    host = f"_host_{_slug(vast_host)}" if vast_host else ""
    return f"ceridwen_vast_{hardware}{host}_joint_full_benchmark_complete_{date}"


def calculate_metrics(
    iteration_seconds: Iterable[float],
    calls_per_step: int,
    price_usd_per_hour: float,
) -> dict[str, float | int | list[float]]:
    times = [float(value) for value in iteration_seconds]
    if not times or any(value <= 0 for value in times):
        raise BenchmarkError("timed iteration durations must be positive")
    total_calls = calls_per_step * len(times)
    total_seconds = sum(times)
    calls_per_second = total_calls / total_seconds
    sorted_times = sorted(times)
    lower = sorted_times[int(0.25 * len(sorted_times))]
    upper = sorted_times[int(0.75 * len(sorted_times))]
    cost_per_100k = 100_000.0 / calls_per_second / 3600.0 * price_usd_per_hour
    return {
        "iteration_seconds": times,
        "timed_steps": len(times),
        "likelihood_calls_per_step": calls_per_step,
        "timed_likelihood_calls": total_calls,
        "total_timed_seconds": total_seconds,
        "median_step_seconds": statistics.median(times),
        "iqr_step_seconds": upper - lower,
        "likelihood_calls_per_second": calls_per_second,
        "cost_per_100k_likelihood_calls_usd": cost_per_100k,
    }


def _load_target(project_root: Path) -> tuple[Any, dict[str, Path]]:
    import numpy as np
    from astropy.io import fits
    from astropy.table import Table

    catalog_path = project_root / "data/raw/legac_dr2/legaCdr2.fits.gz"
    photometry_path = (
        project_root
        / "data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits"
    )
    spectra_dir = project_root / "data/raw/legac_dr2/sp"

    legac = Table.read(catalog_path)
    photometry = Table.read(photometry_path)
    if len(legac) != 1988:
        raise BenchmarkError(f"expected 1988 LEGA-C rows, found {len(legac)}")
    if len(np.unique(photometry["LEGAC_INDEX"])) != len(photometry):
        raise BenchmarkError("LEGAC_INDEX values are not unique")
    if float(np.max(photometry["MATCH_SEP_ARCSEC"])) >= 1.0:
        raise BenchmarkError("a photometry match has separation of at least 1 arcsec")

    legac_frame = legac.to_pandas()
    for text_column in ["SPECT_ID", "Filename"]:
        legac_frame[text_column] = legac_frame[text_column].map(
            lambda value: value.decode() if isinstance(value, bytes) else value
        )
    photometry_frame = photometry.to_pandas().set_index("LEGAC_INDEX")
    joined = legac_frame.join(
        photometry_frame[FLUX_COLUMNS + ERROR_COLUMNS],
        how="inner",
    )
    target_rows = joined[joined["SPECT_ID"] == TARGET_ID]
    if len(target_rows) != 1:
        raise BenchmarkError(f"expected one {TARGET_ID} row, found {len(target_rows)}")
    galaxy = target_rows.iloc[0]
    spectrum_path = spectra_dir / str(galaxy["Filename"])
    with fits.open(spectrum_path) as hdulist:
        spectrum = hdulist[1].data
        instrument_resolution = float(hdulist[0].header["SPEC_RES"])
    wave, flux, error, quality_flag = (
        spectrum[column][0] for column in ("WAVE", "FLUX", "ERR", "QUAL")
    )
    good = (quality_flag == 0) & (error > 0) & np.isfinite(flux)
    target = {
        "galaxy": galaxy,
        "wave_air": wave,
        "flux_dr2": flux,
        "error_dr2": error,
        "good_pixel": good,
        "instrument_fwhm_resolution": instrument_resolution,
    }
    paths = {
        "catalog": catalog_path,
        "photometry": photometry_path,
        "spectrum": spectrum_path,
    }
    return target, paths


def build_joint_workload(project_root: Path) -> BuiltWorkload:
    """Build the fixed joint M1_210210 likelihood used by the benchmark."""
    import astropy.units as u
    import jax.numpy as jnp
    import numpy as np
    from ceridwen.cosmology import age_gyr
    from ceridwen.csp import CSPBasis_afe
    from ceridwen.likelihood import (
        DiagonalGaussianLikelihood,
        DiagonalNoiseModel,
        MultiObservationLikelihood,
    )
    from ceridwen.model import SedModel, logsfr_ratios_to_sfh
    from ceridwen.observation import Photometry, Spectrum
    from ceridwen.sampler.priors import Uniform
    from ceridwen.ssps import SSPDataAfe, fetch_grid
    from specutils.utils.wcs_utils import air_to_vac

    target, input_paths = _load_target(project_root)
    galaxy = target["galaxy"]
    wave_air = target["wave_air"]
    flux_dr2 = target["flux_dr2"]
    error_dr2 = target["error_dr2"]
    good_pixel = target["good_pixel"]
    instrument_resolution = target["instrument_fwhm_resolution"]
    z_catalog = float(galaxy["z"])
    sigma_star = float(galaxy["SIGMA_STARS_PRIME"])

    ujy_to_maggies = 1e-6 / 3631.0
    photometry_floor = 0.05
    i_filter_index = FILTER_NAMES.index("subaru_suprimecam_ip")
    phot_flux = galaxy[FLUX_COLUMNS].to_numpy(dtype=float) * ujy_to_maggies
    phot_error = galaxy[ERROR_COLUMNS].to_numpy(dtype=float) * ujy_to_maggies
    phot_uncertainty = np.hypot(phot_error, photometry_floor * np.abs(phot_flux))
    phot_mask = np.isfinite(phot_flux) & np.isfinite(phot_uncertainty) & (phot_flux > 0)
    phot_fit_mask = phot_mask.copy()
    phot_fit_mask[i_filter_index] = False
    if int(phot_fit_mask.sum()) != EXPECTED_PHOTOMETRY_BANDS:
        raise BenchmarkError(
            "the joint likelihood does not contain 11 photometric bands"
        )
    phot_obs = Photometry(
        filters=FILTER_NAMES,
        flux=phot_flux,
        uncertainty=phot_uncertainty,
        mask=phot_fit_mask,
        name="photometry",
    )

    flux_unit = 1e-19 * u.erg / u.s / u.cm**2 / u.AA

    def flam_to_fnu_cgs(values: Any, wavelength: Any) -> Any:
        f_lambda = values * flux_unit
        return f_lambda.to_value(
            u.erg / u.s / u.cm**2 / u.Hz,
            equivalencies=u.spectral_density(wavelength * u.AA),
        )

    wave_vacuum = air_to_vac(wave_air * u.AA).to_value(u.AA)
    native_flux = flam_to_fnu_cgs(flux_dr2, wave_vacuum)
    native_uncertainty = flam_to_fnu_cgs(error_dr2, wave_vacuum)
    telluric_vacuum = air_to_vac(np.array([7590.0, 7660.0]) * u.AA).to_value(u.AA)
    anchor_good = good_pixel & np.isfinite(native_flux)
    anchor_good &= np.isfinite(native_uncertainty)
    anchor_good &= ~(
        (wave_vacuum >= telluric_vacuum[0]) & (wave_vacuum <= telluric_vacuum[1])
    )
    for rest_wavelength in REST_EMISSION_LINES:
        line_center = rest_wavelength * (1 + z_catalog)
        velocity_offset = np.abs(wave_vacuum - line_center) / line_center * 299792.458
        anchor_good &= velocity_offset > 1500.0

    anchor_flux = np.interp(
        wave_vacuum,
        wave_vacuum[anchor_good],
        native_flux[anchor_good],
    )
    anchor_uncertainty = np.interp(
        wave_vacuum,
        wave_vacuum[anchor_good],
        native_uncertainty[anchor_good],
    )
    i_anchor = Photometry(filters=["subaru_suprimecam_ip"], name="i_anchor")
    anchor_spectrum = Spectrum(
        wavelength=wave_vacuum,
        flux=anchor_flux,
        uncertainty=anchor_uncertainty,
        name="anchor_spectrum",
    )
    synthetic_i_flux = float(
        np.asarray(anchor_spectrum.synthetic_photometry(i_anchor.filterset))
    )
    aperture_transfer = phot_flux[i_filter_index] / synthetic_i_flux
    if not np.isfinite(aperture_transfer) or aperture_transfer <= 0:
        raise BenchmarkError("the photometry-to-spectrum transfer is invalid")

    scaled_flux = aperture_transfer * native_flux
    scaled_uncertainty = aperture_transfer * native_uncertainty
    native_valid = (
        good_pixel
        & np.isfinite(scaled_flux)
        & np.isfinite(scaled_uncertainty)
        & (scaled_uncertainty > 0)
    )
    spectrum_obs = Spectrum(
        wavelength=wave_vacuum,
        flux=np.nan_to_num(scaled_flux, nan=0.0),
        uncertainty=np.where(native_valid, scaled_uncertainty, 1.0),
        mask=native_valid,
        resolution=instrument_resolution,
        smoothtype="R",
        res_convention="fwhm",
        sigma_losvd=sigma_star,
        name="spectrum",
    )
    spectrum_obs.mask_lines(
        REST_EMISSION_LINES,
        dv=1500.0,
        zred=z_catalog,
    )
    spectrum_obs.mask_wavelength_range(*telluric_vacuum)
    if spectrum_obs.ndof != EXPECTED_SPECTRAL_PIXELS:
        raise BenchmarkError(
            "the joint likelihood does not contain 3523 spectral pixels: "
            f"found {spectrum_obs.ndof}"
        )

    grid_path = Path(fetch_grid(GRID_ID))
    ssp = SSPDataAfe.load(grid_path)
    input_paths["ssp_grid"] = grid_path
    if tuple(ssp.ssp_flux.shape) != GRID_SHAPE:
        raise BenchmarkError(f"unexpected SSP grid shape: {ssp.ssp_flux.shape}")
    if str(ssp.schema_version) != GRID_SCHEMA:
        raise BenchmarkError(f"unexpected SSP grid schema: {ssp.schema_version}")

    universe_age = float(age_gyr(z_catalog))
    lookback_template = np.array([0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 5.0, universe_age])
    z_bounds = (
        float(ssp.ssp_lgmet.min()) + 1e-4,
        float(ssp.ssp_lgmet.max()) - 1e-4,
    )
    afe_bounds = (float(ssp.ssp_afe.min()), float(ssp.ssp_afe.max()))
    fixed_dust_index = -0.7
    csp_theta = {
        "lookback_time": jnp.asarray(lookback_template),
        "sfh": jnp.ones(len(lookback_template)),
        "Z": jnp.array([-1.85]),
        "afe": jnp.array([0.2]),
        "diffuse_tau_kc": jnp.array([0.2]),
        "diffuse_dust_index": jnp.array([fixed_dust_index]),
    }
    joint_csp = CSPBasis_afe(
        ssp,
        theta=csp_theta,
        zh_const=True,
        sfh_interp="step",
        add_dust=False,
        add_diffuse_dust=True,
        add_dust_emission=False,
        add_igm=False,
        sigma_losvd_kms=0.0,
        track_zred_age=False,
        verbose=False,
    )

    def sfh_from_ratios(free_theta: dict[str, Any]) -> Any:
        return logsfr_ratios_to_sfh(
            free_theta["logsfr_ratios"],
            sfh_times_yr=np.asarray(joint_csp.sfh_times),
        )

    joint_model = SedModel(
        joint_csp,
        observations=[phot_obs, spectrum_obs],
        priors={
            "logsfr_ratios": Uniform(low=-3.0, high=3.0),
            "Z": Uniform(low=z_bounds[0], high=z_bounds[1]),
            "afe": Uniform(low=afe_bounds[0], high=afe_bounds[1]),
            "logmass": Uniform(low=8.0, high=13.0),
            "diffuse_tau_kc": Uniform(low=0.0, high=2.0),
            "log_f_calib": Uniform(low=np.log(0.01), high=np.log(0.10)),
        },
        transforms={
            "sfh": sfh_from_ratios,
            "diffuse_dust_index": lambda free_theta: jnp.array([fixed_dust_index]),
        },
        free_param_init={
            "logsfr_ratios": jnp.zeros(len(lookback_template) - 1),
            "logmass": jnp.array([11.0]),
            "log_f_calib": jnp.array([np.log(0.03)]),
        },
        zred=z_catalog,
    )
    initial_photometry = np.asarray(
        joint_model.predict(joint_model.theta_init)["photometry"]
    )
    active_photometry = phot_fit_mask & (initial_photometry > 0) & (phot_flux > 0)
    normalization_shift = np.median(
        np.log10(phot_flux[active_photometry] / initial_photometry[active_photometry])
    )
    joint_model.theta_init["logmass"] = (
        joint_model.theta_init["logmass"] + normalization_shift
    )
    initial_prediction = joint_model.predict(joint_model.theta_init)
    for name in ("photometry", "spectrum"):
        if not np.all(np.isfinite(np.asarray(initial_prediction[name]))):
            raise BenchmarkError(f"the initial {name} prediction is not finite")

    likelihood = MultiObservationLikelihood(
        keys=(phot_obs.name, spectrum_obs.name),
        likelihoods=(
            DiagonalGaussianLikelihood(),
            DiagonalGaussianLikelihood(
                noise_model=DiagonalNoiseModel(use_fractional=True)
            ),
        ),
    )
    metadata = {
        "target": TARGET_ID,
        "redshift": z_catalog,
        "velocity_dispersion_km_s": sigma_star,
        "photometric_bands": int(phot_obs.ndof),
        "spectral_pixels": int(spectrum_obs.ndof),
        "ssp_grid_id": GRID_ID,
        "ssp_grid_schema": str(ssp.schema_version),
        "ssp_grid_shape": list(ssp.ssp_flux.shape),
        "ssp_grid_pixel_resolving_power": float(
            np.median(np.asarray(ssp.ssp_wave)[:-1] / np.diff(ssp.ssp_wave))
        ),
    }
    return BuiltWorkload(
        model=joint_model,
        likelihood=likelihood,
        metadata=metadata,
        input_paths=input_paths,
    )


def _make_log_functions(model: Any, likelihood: Any) -> tuple[Any, Any]:
    import jax
    import jax.numpy as jnp

    observation_data = {
        key: (
            model.obs_dict[key].flux,
            model.obs_dict[key].uncertainty,
            model.obs_dict[key].mask,
        )
        for key in likelihood.keys
    }

    @jax.jit
    def loglike_fn(theta: dict[str, Any]) -> Any:
        predictions = model.predict(theta)
        log_likelihood = jnp.zeros(())
        for key, component in zip(likelihood.keys, likelihood.likelihoods):
            values, uncertainty, mask = observation_data[key]
            component_value, _ = component(
                values,
                predictions[key],
                uncertainty,
                mask,
                params=theta,
            )
            log_likelihood = log_likelihood + component_value
        return log_likelihood

    @jax.jit
    def logprior_fn(theta: dict[str, Any]) -> Any:
        return model.ln_prior(theta)

    return loglike_fn, logprior_fn


def _sample_prior(model: Any, rng_key: Any) -> dict[str, Any]:
    import jax

    particles = {}
    for name, initial_value in model.theta_init.items():
        rng_key, subkey = jax.random.split(rng_key)
        particles[name] = model.priors[name].sample(
            subkey,
            shape=(NUM_LIVE, *initial_value.shape),
        )
    return particles


def _jax_memory(device: Any) -> dict[str, float | None]:
    stats = device.memory_stats() or {}

    def mib(name: str) -> float | None:
        value = stats.get(name)
        return None if value is None else float(value) / 2**20

    return {
        "bytes_in_use_mib": mib("bytes_in_use"),
        "peak_bytes_in_use_mib": mib("peak_bytes_in_use"),
        "bytes_limit_mib": mib("bytes_limit"),
    }


def _nvidia_smi_gpus() -> list[dict[str, str]]:
    output = _run_text(
        [
            "nvidia-smi",
            "--query-gpu=index,name,uuid,memory.total,driver_version,power.limit",
            "--format=csv,noheader,nounits",
        ]
    )
    if not output:
        return []
    fields = [
        "index",
        "name",
        "uuid",
        "memory_total_mib",
        "driver_version",
        "power_limit_w",
    ]
    return [
        dict(zip(fields, (value.strip() for value in row)))
        for row in csv.reader(output.splitlines())
    ]


def _nvidia_process_memory_mib() -> float | None:
    output = _run_text(
        [
            "nvidia-smi",
            "--query-compute-apps=pid,used_gpu_memory",
            "--format=csv,noheader,nounits",
        ]
    )
    if not output:
        return None
    total = 0.0
    found = False
    for row in csv.reader(output.splitlines()):
        if len(row) != 2 or row[0].strip() != str(os.getpid()):
            continue
        total += float(row[1].strip())
        found = True
    return total if found else None


def run_fixed_steps(workload: BuiltWorkload) -> dict[str, Any]:
    import blackjax
    import jax
    import numpy as np

    loglike_fn, logprior_fn = _make_log_functions(
        workload.model,
        workload.likelihood,
    )
    rng_key = jax.random.PRNGKey(SEED)
    rng_key, prior_key = jax.random.split(rng_key)
    particles = _sample_prior(workload.model, prior_key)
    sampler = blackjax.nss(
        logprior_fn=logprior_fn,
        loglikelihood_fn=loglike_fn,
        num_delete=NUM_DELETE,
        num_inner_steps=NUM_INNER_STEPS,
    )
    init_fn = jax.jit(sampler.init)
    step_fn = jax.jit(sampler.step)

    start = time.perf_counter()
    live = init_fn(particles)
    jax.block_until_ready(live)
    initialization_seconds = time.perf_counter() - start
    live_log_likelihood = np.asarray(live.particles.loglikelihood)
    if not np.all(np.isfinite(live_log_likelihood)):
        raise BenchmarkError("the initialized live-point likelihood is not finite")

    warmup_seconds = []
    for _ in range(WARMUP_STEPS):
        rng_key, step_key = jax.random.split(rng_key)
        start = time.perf_counter()
        live, dead_info = step_fn(step_key, live)
        jax.block_until_ready((live, dead_info))
        warmup_seconds.append(time.perf_counter() - start)

    iteration_seconds = []
    for step in range(1, TIMED_STEPS + 1):
        rng_key, step_key = jax.random.split(rng_key)
        start = time.perf_counter()
        live, dead_info = step_fn(step_key, live)
        jax.block_until_ready((live, dead_info))
        duration = time.perf_counter() - start
        iteration_seconds.append(duration)
        print(f"timed step {step}/{TIMED_STEPS}: {duration:.3f} s", flush=True)

    return {
        "initialization_seconds": initialization_seconds,
        "warmup_step_seconds": warmup_seconds,
        "iteration_seconds": iteration_seconds,
    }


def _runtime_metadata(jax: Any, device: Any) -> dict[str, Any]:
    import blackjax
    import jaxlib

    import ceridwen

    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "jax": jax.__version__,
        "jaxlib": jaxlib.__version__,
        "blackjax": getattr(blackjax, "__version__", None),
        "ceridwen": getattr(ceridwen, "__version__", None),
        "jax_backend": jax.default_backend(),
        "jax_enable_x64": bool(jax.config.jax_enable_x64),
        "jax_platforms_env": os.environ.get("JAX_PLATFORMS"),
        "xla_preallocate_env": os.environ.get("XLA_PYTHON_CLIENT_PREALLOCATE"),
        "xla_memory_fraction_env": os.environ.get("XLA_CLIENT_MEM_FRACTION"),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "jax_device": str(device),
        "jax_device_kind": getattr(device, "device_kind", str(device)),
        "nvidia_smi_gpus": _nvidia_smi_gpus(),
    }


def _flat_result_row(result: dict[str, Any]) -> dict[str, Any]:
    timings = result["timings"]
    runtime = result["runtime"]
    memory = result["memory"]
    git = result["git"]
    return {
        "schema_version": result["schema_version"],
        "workload_id": result["workload"]["id"],
        "comparison_fingerprint": result["comparison_fingerprint"],
        "started_at_utc": result["started_at_utc"],
        "gpu_name": runtime["jax_device_kind"],
        "vast_host": result["vast"]["host"],
        "vast_instance": result["vast"]["instance"],
        "price_usd_per_hour": result["vast"]["price_usd_per_hour"],
        "timed_steps": timings["timed_steps"],
        "timed_likelihood_calls": timings["timed_likelihood_calls"],
        "total_timed_seconds": timings["total_timed_seconds"],
        "median_step_seconds": timings["median_step_seconds"],
        "iqr_step_seconds": timings["iqr_step_seconds"],
        "likelihood_calls_per_second": timings["likelihood_calls_per_second"],
        "cost_per_100k_likelihood_calls_usd": timings[
            "cost_per_100k_likelihood_calls_usd"
        ],
        "jax_peak_memory_mib": memory["jax"]["peak_bytes_in_use_mib"],
        "nvidia_process_memory_mib": memory["nvidia_process_memory_mib"],
        "project_commit": git["project_commit"],
        "ceridwen_commit": git["ceridwen_commit"],
    }


def _configure_cuda_environment() -> None:
    """Configure CUDA before JAX creates its GPU client."""
    os.environ["JAX_PLATFORMS"] = "cuda"
    os.environ["JAX_ENABLE_X64"] = "1"
    os.environ.pop("XLA_PYTHON_CLIENT_PREALLOCATE", None)
    os.environ["XLA_CLIENT_MEM_FRACTION"] = JAX_MEMORY_FRACTION
    os.environ.pop("LD_LIBRARY_PATH", None)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise BenchmarkError("no benchmark rows to write")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def command_run(args: argparse.Namespace) -> int:
    _configure_cuda_environment()

    import jax

    jax.config.update("jax_enable_x64", True)
    devices = jax.devices()
    if not devices or any(device.platform != "gpu" for device in devices):
        raise BenchmarkError(f"expected CUDA GPU devices, found {devices}")
    device = devices[0]
    print(f"device: {getattr(device, 'device_kind', device)}")
    print(f"workload: {WORKLOAD_ID}")

    project_root = args.project_root.resolve()
    started_at = datetime.now(UTC)
    setup_start = time.perf_counter()
    workload = build_joint_workload(project_root)
    input_sha256 = {name: _sha256(path) for name, path in workload.input_paths.items()}
    git = _git_metadata(project_root)
    setup_seconds = time.perf_counter() - setup_start
    print(
        "validated workload: "
        f"{workload.metadata['photometric_bands']} bands, "
        f"{workload.metadata['spectral_pixels']} spectral pixels"
    )

    raw_timings = run_fixed_steps(workload)
    metrics = calculate_metrics(
        raw_timings["iteration_seconds"],
        CALLS_PER_STEP,
        args.price_usd_per_hour,
    )
    timings = {
        "setup_seconds": setup_seconds,
        "initialization_seconds": raw_timings["initialization_seconds"],
        "warmup_step_seconds": raw_timings["warmup_step_seconds"],
        **metrics,
    }
    runtime = _runtime_metadata(jax, device)
    benchmark_script_sha256 = _sha256(Path(__file__).resolve())
    contract = {
        "id": WORKLOAD_ID,
        **workload.metadata,
        "seed": SEED,
        "num_live": NUM_LIVE,
        "num_inner_steps": NUM_INNER_STEPS,
        "num_delete": NUM_DELETE,
        "reference_logZ_tol": REFERENCE_LOGZ_TOL,
        "warmup_steps": WARMUP_STEPS,
        "timed_steps": TIMED_STEPS,
        "likelihood_calls_per_step": CALLS_PER_STEP,
    }
    completed_at = datetime.now(UTC)
    result = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "started_at_utc": started_at.isoformat(),
        "completed_at_utc": completed_at.isoformat(),
        "workload": contract,
        "comparison_fingerprint": _comparison_fingerprint(
            contract,
            input_sha256,
            git["ceridwen_commit"],
            runtime,
        ),
        "benchmark_script_sha256": benchmark_script_sha256,
        "input_sha256": input_sha256,
        "input_paths": {
            name: str(path.resolve()) for name, path in workload.input_paths.items()
        },
        "git": git,
        "runtime": runtime,
        "memory": {
            "jax": _jax_memory(device),
            "nvidia_process_memory_mib": _nvidia_process_memory_mib(),
        },
        "vast": {
            "host": args.vast_host,
            "instance": args.vast_instance,
            "price_usd_per_hour": args.price_usd_per_hour,
        },
        "timings": timings,
    }

    result_name = result_directory_name(
        runtime["jax_device_kind"],
        args.vast_host,
        started_at.date().isoformat(),
    )
    result_dir = args.output_root.resolve() / result_name
    if result_dir.exists():
        raise BenchmarkError(f"result directory already exists: {result_dir}")
    result_dir.mkdir(parents=True)
    json_path = result_dir / "benchmark.json"
    csv_path = result_dir / "benchmark.csv"
    log_path = result_dir / "benchmark.log"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    _write_csv(csv_path, [_flat_result_row(result)])
    log_lines = [
        f"workload: {WORKLOAD_ID}",
        f"device: {runtime['jax_device_kind']}",
        f"timed likelihood calls: {timings['timed_likelihood_calls']}",
        f"timed wall: {timings['total_timed_seconds']:.3f} s",
        f"throughput: {timings['likelihood_calls_per_second']:.3f} calls/s",
        (
            "cost per 100000 calls: "
            f"${timings['cost_per_100k_likelihood_calls_usd']:.6f}"
        ),
        f"comparison fingerprint: {result['comparison_fingerprint']}",
    ]
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(log_lines[3])
    print(log_lines[4])
    print(log_lines[5])
    print(f"saved: {result_dir}")
    return 0


def _result_json_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for supplied in inputs:
        if supplied.is_dir():
            direct = supplied / "benchmark.json"
            paths.extend(
                [direct] if direct.is_file() else supplied.rglob("benchmark.json")
            )
        elif supplied.is_file():
            paths.append(supplied)
        else:
            raise BenchmarkError(f"benchmark input does not exist: {supplied}")
    unique_paths = sorted({path.resolve() for path in paths})
    if not unique_paths:
        raise BenchmarkError("no benchmark.json files were found")
    return unique_paths


def validate_comparable(records: list[dict[str, Any]]) -> None:
    fingerprints = {_normalized_comparison_fingerprint(record) for record in records}
    if len(fingerprints) != 1:
        raise BenchmarkError("benchmark results use different workloads or inputs")


def rank_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validate_comparable(records)
    return sorted(
        records,
        key=lambda record: record["timings"]["cost_per_100k_likelihood_calls_usd"],
    )


def command_summarize(args: argparse.Namespace) -> int:
    paths = _result_json_paths(args.inputs)
    records = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    ranked = rank_records(records)
    rows = [_flat_result_row(record) for record in ranked]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        _write_csv(args.output, rows)
        print(f"saved: {args.output}")
    print("rank  gpu  calls/s  USD/100k  USD/hour  host")
    for rank, row in enumerate(rows, start=1):
        print(
            f"{rank:>4}  {row['gpu_name']}  "
            f"{float(row['likelihood_calls_per_second']):.2f}  "
            f"{float(row['cost_per_100k_likelihood_calls_usd']):.5f}  "
            f"{float(row['price_usd_per_hour']):.3f}  "
            f"{row['vast_host'] or '-'}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run and compare the fixed Ceridwen Vast.ai GPU benchmark."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run the fixed GPU benchmark")
    run_parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project checkout. Default: the checkout that contains this script.",
    )
    run_parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
        help="Parent directory for results. Default: PROJECT_ROOT/results.",
    )
    run_parser.add_argument(
        "--price-usd-per-hour",
        type=_positive_float,
        required=True,
        help="Current Vast offer price in USD per hour.",
    )
    run_parser.add_argument("--vast-host", help="Vast host ID.")
    run_parser.add_argument("--vast-instance", help="Vast instance ID.")
    run_parser.set_defaults(function=command_run)

    summary_parser = subparsers.add_parser(
        "summarize",
        help="rank comparable benchmark result files",
    )
    summary_parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="benchmark.json files or result directories.",
    )
    summary_parser.add_argument(
        "--output",
        type=Path,
        help="Optional aggregate CSV path.",
    )
    summary_parser.set_defaults(function=command_summarize)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.function(args))
    except BenchmarkError as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
