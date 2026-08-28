#!/usr/bin/env python3
"""Build the default-variation versus fast-path Ceridwen report notebook."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _markdown(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def _code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def build_notebook(output_path: Path) -> None:
    cells = [
        _markdown(
            "# Ceridwen NSS variation: default versus SFH fast path A\n\n"
            "Four converged default runs define the observed NSS run-to-run variation. "
            "Four seed-matched fast-path runs are compared with that empirical variation. "
            "The target, data, priors, sampler settings, and numerical precision are fixed.\n"
        ),
        _markdown("## Setup\n"),
        _code(
            '''import json
import os
from itertools import pairwise
from pathlib import Path

os.environ["JAX_ENABLE_X64"] = "1"

import corner
import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ceridwen.model import logsfr_ratios_to_sfh

from scripts import benchmark_ceridwen_vast as benchmark
from scripts import verify_ceridwen_sfh_fastpath_posterior as verification

jax.config.update("jax_enable_x64", True)
PROJECT_ROOT = Path(os.environ.get("CERIDWEN_PROJECT_ROOT", Path.cwd()))
VARIATION_ROOT = Path(os.environ["CERIDWEN_VARIATION_ROOT"])
COMPARISON_DIR = VARIATION_ROOT / "comparison"
COMPARISON_DIR.mkdir(parents=True, exist_ok=True)

default_dirs = sorted((VARIATION_ROOT / "default_runs").glob("default_seed_*"))
fast_dirs = sorted((VARIATION_ROOT / "fastpath_a_runs").glob("fastpath_a_seed_*"))
if len(default_dirs) != 4 or len(fast_dirs) != 4:
    raise RuntimeError(
        f"Expected four completed runs per group, found {len(default_dirs)} and {len(fast_dirs)}"
    )

comparison = json.loads((COMPARISON_DIR / "comparison.json").read_text())
default_runs = [verification._load_run(path, "baseline") for path in default_dirs]
fast_runs = [verification._load_run(path, "A") for path in fast_dirs]
print(f"JAX devices: {jax.devices()}")
print(f"variation root: {VARIATION_ROOT}")
print(f"seeds: {[run[1]['seed'] for run in default_runs]}")
'''
        ),
        _markdown("## Completed runs\n"),
        _code(
            '''rows = []
for group, runs in (("default", default_runs), ("fast path A", fast_runs)):
    for result, manifest in runs:
        record = manifest["result"]
        rows.append(
            {
                "group": group,
                "seed": manifest["seed"],
                "Vast host": manifest["runtime"]["vast_host_id"],
                "ln Z": record["log_evidence"],
                "ln Z error": record["log_evidence_err"],
                "weight ESS": record["posterior_weight_ess"],
                "likelihood calls": record["n_likelihood_calls"],
                "wall time [s]": record["wall_time_s"],
                "calls/s": record["n_likelihood_calls"] / record["wall_time_s"],
            }
        )
run_table = pd.DataFrame(rows)
display(run_table)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for group, color, marker in (("default", "tab:blue", "o"), ("fast path A", "tab:orange", "s")):
    subset = run_table[run_table["group"] == group]
    axes[0].scatter(subset["seed"], subset["calls/s"], color=color, marker=marker, label=group)
    axes[1].scatter(subset["seed"], subset["wall time [s]"] / 60, color=color, marker=marker, label=group)
axes[0].set(xlabel="seed", ylabel="likelihood calls/s")
axes[1].set(xlabel="seed", ylabel="wall time [min]")
for axis in axes:
    axis.tick_params(axis="x", rotation=30)
    axis.legend(frameon=False)
fig.tight_layout()
fig.savefig(COMPARISON_DIR / "speed_and_runtime.png", dpi=180, bbox_inches="tight")
plt.show()
'''
        ),
        _markdown(
            "## Default run-to-run variation versus fast-path differences\n\n"
            "Grey points are all six default-default pairs. Orange diamonds are the four "
            "seed-matched fast-default pairs. Distances are normalized by the pooled posterior scale.\n"
        ),
        _code(
            '''metric = "wasserstein_pooled_sd"
default_pairs = comparison["comparisons"]["default_default"]
matched_pairs = comparison["comparisons"]["matched_fast_default"]
labels = [item["parameter"] for item in default_pairs[0]["parameters"]]

fig, ax = plt.subplots(figsize=(15, 5.5))
for index, label in enumerate(labels):
    default_values = [
        pair["parameters"][index][metric] for pair in default_pairs
    ]
    matched_values = [
        pair["parameters"][index][metric] for pair in matched_pairs
    ]
    ax.scatter(
        np.full(len(default_values), index) - 0.08,
        default_values,
        s=18,
        color="0.55",
        alpha=0.75,
    )
    ax.scatter(
        np.full(len(matched_values), index) + 0.08,
        matched_values,
        s=28,
        marker="D",
        color="tab:orange",
        alpha=0.85,
    )
ax.scatter([], [], color="0.55", label="default-default: 6 pairs")
ax.scatter([], [], marker="D", color="tab:orange", label="matched fast-default: 4 pairs")
ax.set(
    xticks=np.arange(len(labels)),
    xticklabels=labels,
    ylabel="weighted Wasserstein distance / pooled posterior SD",
)
ax.tick_params(axis="x", rotation=70)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(COMPARISON_DIR / "default_variation_vs_fastpath_parameters.png", dpi=180, bbox_inches="tight")
plt.show()

evidence_default = [pair["evidence"]["difference_sigma"] for pair in default_pairs]
evidence_matched = [pair["evidence"]["difference_sigma"] for pair in matched_pairs]
evidence_table = pd.DataFrame(
    {
        "comparison": ["default-default"] * len(evidence_default)
        + ["matched fast-default"] * len(evidence_matched),
        "absolute evidence difference / combined error": evidence_default + evidence_matched,
    }
)
display(evidence_table)
'''
        ),
        _markdown("## Posterior intervals, including mass-weighted age\n"),
        _code(
            '''selected_labels = [
    "logmass",
    "Z",
    "afe",
    "diffuse_tau_kc",
    "log_f_calib",
    "mass_weighted_age_gyr",
]

def component_summaries(runs):
    summaries = []
    for result, manifest in runs:
        weights = verification.normalized_weights(result.log_weights)
        components = verification.posterior_components(
            result, manifest["science_contract"]
        )
        for label in selected_labels:
            summary = verification.weighted_summary(components[label], weights)
            summaries.append(
                {
                    "seed": manifest["seed"],
                    "parameter": label,
                    **summary,
                }
            )
    return pd.DataFrame(summaries)

default_summary = component_summaries(default_runs)
fast_summary = component_summaries(fast_runs)
fig, axes = plt.subplots(2, 3, figsize=(12, 7))
for axis, label in zip(axes.flat, selected_labels, strict=True):
    for table, offset, color, marker, group in (
        (default_summary, -0.08, "tab:blue", "o", "default"),
        (fast_summary, 0.08, "tab:orange", "s", "fast path A"),
    ):
        subset = table[table["parameter"] == label]
        x = np.arange(len(subset)) + offset
        axis.errorbar(
            x,
            subset["median"],
            yerr=[subset["median"] - subset["q16"], subset["q84"] - subset["median"]],
            fmt=marker,
            color=color,
            capsize=2,
            label=group,
        )
    axis.set_title(label)
    axis.set_xticks(np.arange(4), [str(seed) for seed in default_summary["seed"].unique()], rotation=30)
axes[0, 0].legend(frameon=False)
fig.tight_layout()
fig.savefig(COMPARISON_DIR / "posterior_intervals_by_seed.png", dpi=180, bbox_inches="tight")
plt.show()
'''
        ),
        _markdown("## Star-formation histories and age distribution\n"),
        _code(
            '''def resampled_indices(result, count, seed):
    weights = verification.normalized_weights(result.log_weights)
    return np.random.default_rng(seed).choice(len(weights), count, replace=True, p=weights)

def sfh_draws(result, manifest, count=400):
    indices = resampled_indices(result, count, manifest["seed"] + 100)
    ratios = jnp.asarray(result.samples["logsfr_ratios"])[indices]
    lookback_gyr = np.asarray(manifest["science_contract"]["lookback_time_gyr"])
    histories = np.asarray(
        jax.vmap(
            lambda value: logsfr_ratios_to_sfh(
                value, sfh_times_yr=jnp.asarray(lookback_gyr * 1e9)
            )
        )(ratios)
    )
    return lookback_gyr, histories

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
for group, runs, color in (
    ("default", default_runs, "tab:blue"),
    ("fast path A", fast_runs, "tab:orange"),
):
    run_medians = []
    age_draws = []
    for result, manifest in runs:
        lookback_gyr, histories = sfh_draws(result, manifest)
        median_history = np.median(histories, axis=0)
        run_medians.append(median_history)
        axes[0].plot(lookback_gyr, median_history, color=color, alpha=0.42, lw=1)
        weights = verification.normalized_weights(result.log_weights)
        components = verification.posterior_components(result, manifest["science_contract"])
        indices = np.random.default_rng(manifest["seed"] + 200).choice(
            len(weights), 500, replace=True, p=weights
        )
        age_draws.append(components["mass_weighted_age_gyr"][indices])
    run_medians = np.asarray(run_medians)
    axes[0].plot(lookback_gyr, np.median(run_medians, axis=0), color=color, lw=2.2, label=group)
    axes[1].hist(np.concatenate(age_draws), bins=35, density=True, histtype="step", color=color, lw=2, label=group)
axes[0].set(yscale="log", xlabel="lookback time [Gyr]", ylabel="normalized SFR")
axes[1].set(xlabel="mass-weighted age [Gyr]", ylabel="density")
for axis in axes:
    axis.legend(frameon=False)
fig.tight_layout()
fig.savefig(COMPARISON_DIR / "sfh_and_mass_weighted_age.png", dpi=180, bbox_inches="tight")
plt.show()
'''
        ),
        _markdown("## Combined physical-parameter corner plot\n"),
        _code(
            '''def physical_draws(runs, count_per_run=500):
    rows = []
    for result, manifest in runs:
        weights = verification.normalized_weights(result.log_weights)
        indices = np.random.default_rng(manifest["seed"] + 300).choice(
            len(weights), count_per_run, replace=True, p=weights
        )
        components = verification.posterior_components(result, manifest["science_contract"])
        rows.append(
            np.column_stack(
                [
                    components["logmass"][indices],
                    components["Z"][indices],
                    components["afe"][indices],
                    components["diffuse_tau_kc"][indices],
                    100 * np.exp(components["log_f_calib"][indices]),
                    components["mass_weighted_age_gyr"][indices],
                ]
            )
        )
    return np.concatenate(rows)

corner_labels = [
    r"$\\log_{10}(M_\\star/M_\\odot)$",
    r"$\\log_{10}(Z/Z_\\odot)$",
    r"$[\\alpha/\\mathrm{Fe}]$",
    r"$\\tau_\\mathrm{diffuse}$",
    r"$f_\\mathrm{calib} [\\%]$",
    r"$t_\\mathrm{MW} [\\mathrm{Gyr}]$",
]
default_corner = physical_draws(default_runs)
fast_corner = physical_draws(fast_runs)
figure = corner.corner(
    default_corner,
    labels=corner_labels,
    color="tab:blue",
    levels=(0.68, 0.95),
    plot_datapoints=False,
    fill_contours=False,
)
corner.corner(
    fast_corner,
    labels=corner_labels,
    color="tab:orange",
    levels=(0.68, 0.95),
    plot_datapoints=False,
    fill_contours=False,
    fig=figure,
)
figure.savefig(COMPARISON_DIR / "combined_physical_corner.png", dpi=180, bbox_inches="tight")
plt.show()
'''
        ),
        _markdown(
            "## Posterior-predictive spectra\n\n"
            "The lower panel shows the seed-matched fast-minus-default median model, divided "
            "by the quoted LEGA-C statistical uncertainty at each fitted wavelength.\n"
        ),
        _code(
            '''default_workload = benchmark.build_joint_workload(PROJECT_ROOT)
benchmark.select_sfh_basis_implementation(default_workload, "baseline")
fast_workload = benchmark.build_joint_workload(PROJECT_ROOT)
benchmark.select_sfh_basis_implementation(fast_workload, "A")

def prediction_batch(result, model, manifest, count=48):
    indices = resampled_indices(result, count, manifest["seed"] + 400)
    batch = {}
    for name, template in model.theta_init.items():
        values = np.asarray(result.samples[name])[indices]
        if np.shape(template) == (1,) and values.ndim == 1:
            values = values[:, None]
        batch[name] = jnp.asarray(values)
    return batch

def spectrum_medians(runs, model):
    medians = []
    for result, manifest in runs:
        predictions = model.predict_vmap(prediction_batch(result, model, manifest))
        medians.append(np.median(np.asarray(predictions["spectrum"]), axis=0))
    return np.asarray(medians)

default_spectra = spectrum_medians(default_runs, default_workload.model)
fast_spectra = spectrum_medians(fast_runs, fast_workload.model)
spectrum_observation = next(
    observation
    for observation in default_workload.model.observations
    if observation.name == "spectrum"
)
wave = np.asarray(spectrum_observation.wavelength)
flux = np.asarray(spectrum_observation.flux)
uncertainty = np.asarray(spectrum_observation.uncertainty)
mask = np.asarray(spectrum_observation.mask)
scale = 1e9 / 3631e-23

fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
axes[0].plot(wave[mask], flux[mask] * scale, color="0.15", lw=0.55, label="LEGA-C")
for index, prediction in enumerate(default_spectra):
    axes[0].plot(wave[mask], prediction[mask] * scale, color="tab:blue", alpha=0.45, lw=0.8, label="default medians" if index == 0 else None)
for index, prediction in enumerate(fast_spectra):
    axes[0].plot(wave[mask], prediction[mask] * scale, color="tab:orange", alpha=0.45, lw=0.8, label="fast-path medians" if index == 0 else None)
for index in range(4):
    difference_sigma = (fast_spectra[index] - default_spectra[index]) / uncertainty
    axes[1].plot(wave[mask], difference_sigma[mask], lw=0.65, alpha=0.7, label=str(default_runs[index][1]["seed"]))
axes[0].set(ylabel=r"flux density [$10^{-9}$ maggies]")
axes[0].legend(frameon=False, ncol=3)
axes[1].axhspan(-1, 1, color="0.88")
axes[1].axhline(0, color="k", lw=0.7)
axes[1].set(xlabel="observed vacuum wavelength [angstrom]", ylabel=r"$(fast-default)/\\sigma_{LEGA-C}$")
axes[1].legend(frameon=False, ncol=4, fontsize=8)
fig.tight_layout()
fig.savefig(COMPARISON_DIR / "posterior_predictive_spectra.png", dpi=180, bbox_inches="tight")
plt.show()
'''
        ),
        _markdown("## Empirical-envelope result\n"),
        _code(
            '''envelopes = comparison["empirical_default_envelopes"]
envelope_rows = []
for parameter, metrics in envelopes["parameters"].items():
    record = metrics["wasserstein_pooled_sd"]
    envelope_rows.append(
        {
            "parameter": parameter,
            "default-default maximum": record["default_max"],
            "matched fast-default inside default maximum": sum(record["fast_inside_default_max"]),
            "matched comparisons": len(record["fast_inside_default_max"]),
        }
    )
envelope_table = pd.DataFrame(envelope_rows)
display(envelope_table)
inside = envelope_table["matched fast-default inside default maximum"].sum()
total = envelope_table["matched comparisons"].sum()
print(f"Matched fast-default component comparisons inside the default-default maximum: {inside}/{total}")
print("Host IDs are recorded for provenance. This analysis follows the requested assumption that host effects are negligible.")
'''
        ),
    ]

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Ceridwen (Vast.ai GPU)",
                "language": "python",
                "name": "ceridwen",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build_notebook(args.output.resolve())
    print(f"saved NSS-variation notebook: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
