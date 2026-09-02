#!/usr/bin/env python3
"""Summarise the absorption-mask experiment: tables and figures.

Reads every cell directory under ``results/absorption-mask`` (one
``ceridwen_result.h5`` and ``ceridwen_derived_outputs.h5`` each), writes
``summary.json`` / ``summary.csv`` beside them, prints the Markdown tables
for the wiki page, and saves PNG figures under ``wiki/analyses/``.

    python scripts/absorption_mask_report.py [--output-root DIR] [--figure-dir DIR]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "results/absorption-mask"
DEFAULT_FIGURE_DIR = PROJECT_ROOT / "wiki/analyses/absorption-mask"
SCALARS = ["logmass", "Z", "afe", "diffuse_tau_kc", "spectrum_scaling", "log_f_calib"]
PARAMS = ["logmass", "mwa_gyr", "Z", "afe", "diffuse_tau_kc", "spectrum_scaling", "f_calib_pct"]
LABELS = {
    "logmass": r"$\log M_\star/M_\odot$",
    "mwa_gyr": r"$t_{\rm MW}$ [Gyr]",
    "Z": r"$\log Z$",
    "afe": r"[$\alpha$/Fe]",
    "diffuse_tau_kc": r"$\tau_{\rm dust}$",
    "spectrum_scaling": r"$s_{\rm spec}$",
    "f_calib_pct": r"$f_{\rm calib}$ [%]",
}
MODES = ["all", "features", "features_downweight"]
MODE_LABELS = {"all": "full spectrum", "features": "features only",
               "features_downweight": "continuum down-weighted"}
# Okabe-Ito blue, vermillion, green: fixed categorical order, CVD-safe.
MODE_COLORS = {"all": "#0072B2", "features": "#D55E00", "features_downweight": "#009E73"}
QUANTILES = (0.025, 0.16, 0.5, 0.84, 0.975)


def weighted_quantiles(values, log_weights, quantiles=QUANTILES):
    w = np.exp(np.asarray(log_weights) - np.max(log_weights))
    w /= w.sum()
    order = np.argsort(values)
    cdf = np.cumsum(w[order]) - 0.5 * w[order]
    return [float(np.interp(q, cdf, np.asarray(values)[order])) for q in quantiles]


def mass_weighted_age(logsfr_ratios, lookback_gyr):
    """The notebook's ``derived_sfh`` mass-weighted age for one SFH vector."""
    from ceridwen.model import logsfr_ratios_to_sfh

    history = np.asarray(logsfr_ratios_to_sfh(np.asarray(logsfr_ratios),
                                              sfh_times_yr=np.asarray(lookback_gyr) * 1e9))
    durations = np.diff(lookback_gyr) * 1e9
    masses = 0.5 * (history[:-1] + history[1:]) * durations
    ages = 0.5 * (lookback_gyr[:-1] + lookback_gyr[1:])
    return float((masses * ages).sum() / masses.sum())


def read_cell(cell_dir: Path) -> dict | None:
    import h5py
    from ceridwen.fit import load_result_h5

    result_path = cell_dir / "ceridwen_result.h5"
    derived_path = cell_dir / "ceridwen_derived_outputs.h5"
    if not (result_path.exists() and derived_path.exists()):
        return None
    result = load_result_h5(result_path)
    record = {"name": cell_dir.name}
    with h5py.File(result_path, "r") as f:
        attrs = f["model"].attrs
        record.update({
            "target": str(attrs.get("target_id", "")) or cell_dir.name.split("_")[1] + "_" + cell_dir.name.split("_")[2],
            "spectrum_pixels": str(attrs.get("spectrum_pixels", "all")),
            "feature_downweight": float(attrs.get("feature_downweight", np.nan)),
            "mock_tilt": float(attrs.get("mock_tilt", 0.0)),
            "mock_snr_scale": float(attrs.get("mock_snr_scale", 1.0)),
            "mock_seed": int(attrs.get("mock_seed", 0)),
        })
        truth = {k: np.asarray(f["mock_truth"][k]) for k in f["mock_truth"]} if "mock_truth" in f else None
    with h5py.File(derived_path, "r") as d:
        diag = d["diagnostics"].attrs
        record.update({
            "target": str(d.attrs["target_id"]),
            "redshift": float(d.attrs["redshift"]),
            "wall_time_s": float(d.attrs["wall_time_s"]),
            "n_likelihood_calls": int(d.attrs["n_likelihood_calls"]),
            "ess": float(diag["posterior_weight_ess"]),
            "passed": bool(diag["passed"]),
            "log_evidence": float(diag["log_evidence"]),
            "log_evidence_err": float(diag["log_evidence_err"]),
            "spectrum_ndof": int(diag.get("spectrum_ndof", 0)),
            "spectrum_chi2_per_pixel": float(diag.get("spectrum_chi2", np.nan)) / max(int(diag.get("spectrum_ndof", 1)), 1),
            "photometry_chi2_per_band": float(diag.get("photometry_chi2", np.nan)) / max(int(diag.get("photometry_ndof", 1)), 1),
        })
        lookback = np.asarray(d["sfh/lookback_time_gyr"])
        mwa_draws = np.asarray(d["sfh/mass_weighted_age_gyr"])
    record["is_mock"] = truth is not None
    record["mode"] = record["spectrum_pixels"]
    draws = {}
    for name in SCALARS:
        draws[name] = np.asarray(result.samples[name]).reshape(len(result.log_weights), -1)[:, 0]
    draws["f_calib_pct"] = 100.0 * np.exp(draws.pop("log_f_calib"))
    quantiles = {name: weighted_quantiles(values, result.log_weights) for name, values in draws.items()}
    quantiles["mwa_gyr"] = [float(np.quantile(mwa_draws, q)) for q in QUANTILES]
    record["quantiles"] = quantiles
    if truth is not None:
        tr = {name: float(np.ravel(truth[name])[0]) for name in ["logmass", "Z", "afe", "diffuse_tau_kc", "spectrum_scaling"]}
        tr["f_calib_pct"] = 100.0 * float(np.exp(np.ravel(truth["log_f_calib"])[0]))
        tr["mwa_gyr"] = mass_weighted_age(truth["logsfr_ratios"], lookback)
        record["truth"] = tr
        metrics = {}
        for name in PARAMS:
            q = quantiles[name]
            width = 0.5 * (q[3] - q[1])
            bias = q[2] - tr[name]
            metrics[name] = {
                "bias": bias, "width": width, "z": bias / width if width > 0 else np.nan,
                "in68": bool(q[1] <= tr[name] <= q[3]), "in95": bool(q[0] <= tr[name] <= q[4]),
            }
        record["metrics"] = metrics
    return record


def collect(output_root: Path) -> list[dict]:
    records = []
    for cell_dir in sorted(p for p in output_root.iterdir() if p.is_dir()):
        record = read_cell(cell_dir)
        if record is not None:
            records.append(record)
    return records


def _fmt(value, digits=3):
    return f"{value:.{digits}f}" if np.isfinite(value) else "-"


def mock_tables(records: list[dict]) -> str:
    mocks = [r for r in records if r["is_mock"]]
    lines = []
    if not mocks:
        return ""
    keys = sorted({(r["mock_tilt"], r["mock_snr_scale"]) for r in mocks})
    lines.append("### Mock recovery: bias, posterior half-width, and 68% coverage\n")
    lines.append("Bias is posterior median minus truth, averaged over realisations; width is the 16-84 half-width; z is bias/width (RMS over realisations); cov68 is the fraction of realisations whose 16-84 interval contains the truth.\n")
    for name in PARAMS:
        lines.append(f"\n**{name}**\n")
        lines.append("| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |")
        lines.append("| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for tilt, snr in keys:
            full_widths = [r["metrics"][name]["width"] for r in mocks
                           if r["mock_tilt"] == tilt and r["mock_snr_scale"] == snr and r["mode"] == "all"]
            full_width = np.mean(full_widths) if full_widths and np.mean(full_widths) > 0 else np.nan
            for mode in MODES:
                rows = [r for r in mocks if r["mock_tilt"] == tilt and r["mock_snr_scale"] == snr and r["mode"] == mode]
                if not rows:
                    continue
                bias = np.mean([r["metrics"][name]["bias"] for r in rows])
                width = np.mean([r["metrics"][name]["width"] for r in rows])
                z = np.sqrt(np.mean([r["metrics"][name]["z"] ** 2 for r in rows]))
                cov = np.mean([r["metrics"][name]["in68"] for r in rows])
                lines.append(f"| {tilt:.2f} | {snr:.2f} | {MODE_LABELS[mode]} | {len(rows)} | {_fmt(bias)} | {_fmt(width)} | {_fmt(width / full_width, 2)} | {_fmt(z, 2)} | {cov:.2f} |")
    return "\n".join(lines)


def real_tables(records: list[dict]) -> str:
    reals = [r for r in records if not r["is_mock"]]
    if not reals:
        return ""
    lines = ["### Real targets: posterior medians with 16-84 intervals\n",
             "Shift is (median - full-spectrum median) / full-spectrum half-width.\n"]
    for name in PARAMS:
        lines.append(f"\n**{name}**\n")
        lines.append("| target | mode | pixels | median | 16-84 | shift | ESS | calls |")
        lines.append("| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |")
        for target in sorted({r["target"] for r in reals}):
            full = [r for r in reals if r["target"] == target and r["mode"] == "all"]
            full_q = full[0]["quantiles"][name] if full else None
            for mode in MODES:
                rows = [r for r in reals if r["target"] == target and r["mode"] == mode]
                if not rows:
                    continue
                r = rows[0]
                q = r["quantiles"][name]
                shift = (q[2] - full_q[2]) / (0.5 * (full_q[3] - full_q[1])) if full_q else np.nan
                lines.append(f"| {target} | {MODE_LABELS[mode]} | {r['spectrum_ndof']} | {_fmt(q[2])} | [{_fmt(q[1])}, {_fmt(q[3])}] | {_fmt(shift, 2)} | {r['ess']:.0f} | {r['n_likelihood_calls']:,} |")
    return "\n".join(lines)


def run_table(records: list[dict]) -> str:
    lines = ["### Every fit\n", "| cell | mode | pixels | ESS | calls | sampler wall [s] | ln Z | spec chi2/pixel | phot chi2/band |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in records:
        lines.append(f"| {r['name']} | {r['mode']} | {r['spectrum_ndof']} | {r['ess']:.0f} | {r['n_likelihood_calls']:,} | {r['wall_time_s']:.0f} | {r['log_evidence']:.1f} ± {r['log_evidence_err']:.2f} | {_fmt(r['spectrum_chi2_per_pixel'], 2)} | {_fmt(r['photometry_chi2_per_band'], 2)} |")
    return "\n".join(lines)


def _style():
    import matplotlib as mpl

    mpl.rcParams.update({
        "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9, "legend.fontsize": 8,
        "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#8a8a8a",
        "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.6,
        "xtick.color": "#444444", "ytick.color": "#444444", "text.color": "#222222",
        "axes.labelcolor": "#222222", "savefig.dpi": 160, "figure.facecolor": "white",
    })


def plot_mock_bias(records: list[dict], figure_dir: Path) -> Path | None:
    import matplotlib.pyplot as plt

    mocks = [r for r in records if r["is_mock"]]
    if not mocks:
        return None
    tilts = sorted({r["mock_tilt"] for r in mocks})
    snrs = sorted({r["mock_snr_scale"] for r in mocks}, reverse=True)
    params = ["logmass", "mwa_gyr", "Z", "afe", "diffuse_tau_kc"]
    _style()
    fig, axes = plt.subplots(len(params), len(snrs), figsize=(3.4 * len(snrs), 2.1 * len(params)),
                             sharex=True, squeeze=False)
    offsets = {"all": -0.004, "features": 0.0, "features_downweight": 0.004}
    for col, snr in enumerate(snrs):
        for row, name in enumerate(params):
            ax = axes[row, col]
            ax.axhline(0.0, color="#8a8a8a", lw=0.8, zorder=1)
            for mode in MODES:
                xs, ys, lo, hi = [], [], [], []
                for tilt in tilts:
                    rows = [r for r in mocks if r["mock_tilt"] == tilt and r["mock_snr_scale"] == snr and r["mode"] == mode]
                    for r in rows:
                        q = r["quantiles"][name]
                        t = r["truth"][name]
                        xs.append(tilt + offsets[mode] + 0.0015 * (r["mock_seed"] % 2 - 0.5))
                        ys.append(q[2] - t)
                        lo.append(q[2] - q[1])
                        hi.append(q[3] - q[2])
                if xs:
                    ax.errorbar(xs, ys, yerr=[lo, hi], fmt="o", ms=3.5, lw=1.2, capsize=0,
                                color=MODE_COLORS[mode], label=MODE_LABELS[mode], zorder=3)
            ax.set_ylabel(f"{LABELS[name]} $-$ truth")
            if row == 0:
                ax.set_title(f"S/N scale {snr:g} (median pixel S/N ≈ {106 * snr:.0f})")
            if row == len(params) - 1:
                ax.set_xlabel("continuum tilt amplitude $\\epsilon$")
                ax.set_xticks(tilts)
    axes[0, 0].legend(loc="upper left", frameon=False)
    fig.suptitle("Mock recovery: posterior median and 16-84 interval relative to the truth", y=1.0)
    fig.tight_layout()
    path = figure_dir / "mock_bias_vs_tilt.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_mock_width(records: list[dict], figure_dir: Path) -> Path | None:
    import matplotlib.pyplot as plt

    mocks = [r for r in records if r["is_mock"]]
    if not mocks:
        return None
    params = ["logmass", "mwa_gyr", "Z", "afe", "diffuse_tau_kc"]
    _style()
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    x = np.arange(len(params))
    width = 0.26
    for k, mode in enumerate(MODES[1:]):
        ratios = []
        for name in params:
            pairs = []
            for r in mocks:
                if r["mode"] != mode:
                    continue
                full = [f for f in mocks if f["mode"] == "all" and f["mock_tilt"] == r["mock_tilt"]
                        and f["mock_snr_scale"] == r["mock_snr_scale"] and f["mock_seed"] == r["mock_seed"]]
                if full:
                    pairs.append(r["metrics"][name]["width"] / full[0]["metrics"][name]["width"])
            ratios.append(np.median(pairs) if pairs else np.nan)
        ax.bar(x + (k - 0.5) * width, ratios, width=width * 0.92, color=MODE_COLORS[mode],
               label=MODE_LABELS[mode], edgecolor="white", linewidth=1.0)
        for xi, ratio in zip(x + (k - 0.5) * width, ratios):
            if np.isfinite(ratio):
                ax.text(xi, ratio, f"{ratio:.2f}", ha="center", va="bottom", fontsize=7, color="#222222")
    ax.axhline(1.0, color="#8a8a8a", lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[p] for p in params])
    ax.set_ylabel("posterior half-width / full-spectrum half-width")
    ax.set_title("Cost in constraining power (median over all mock cells)")
    ax.set_ylim(0.0, ax.get_ylim()[1] * 1.18)
    ax.legend(frameon=False, loc="upper left", ncol=2)
    fig.tight_layout()
    path = figure_dir / "mock_width_ratio.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_real(records: list[dict], figure_dir: Path) -> Path | None:
    import matplotlib.pyplot as plt

    reals = [r for r in records if not r["is_mock"]]
    if not reals:
        return None
    targets = sorted({r["target"] for r in reals})
    params = ["logmass", "mwa_gyr", "Z", "afe", "diffuse_tau_kc", "spectrum_scaling"]
    _style()
    fig, axes = plt.subplots(2, 3, figsize=(8.4, 6.2), squeeze=False)
    for ax, name in zip(axes.ravel(), params):
        for ti, target in enumerate(targets):
            for mi, mode in enumerate(MODES):
                rows = [r for r in reals if r["target"] == target and r["mode"] == mode]
                if not rows:
                    continue
                q = rows[0]["quantiles"][name]
                x = ti + (mi - 1) * 0.22
                ax.errorbar([x], [q[2]], yerr=[[q[2] - q[1]], [q[3] - q[2]]], fmt="o", ms=3.5, lw=1.2,
                            color=MODE_COLORS[mode], label=MODE_LABELS[mode] if ti == 0 else None)
        ax.set_xticks(range(len(targets)))
        ax.set_xticklabels([t.replace("_", "\n") for t in targets], fontsize=7)
        ax.set_title(LABELS[name])
    axes[0, 0].legend(frameon=False, fontsize=7, loc="best")
    fig.suptitle("Real DR2 targets: posterior median and 16-84 interval per pixel mode", y=1.02)
    fig.tight_layout()
    path = figure_dir / "real_targets_posteriors.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_windows(output_root: Path, figure_dir: Path, cell="real_M5_172669_features") -> Path | None:
    import h5py
    import matplotlib.pyplot as plt

    derived = output_root / cell / "ceridwen_derived_outputs.h5"
    if not derived.exists():
        return None
    with h5py.File(derived, "r") as d:
        wave = np.asarray(d["spectrum/wavelength"])
        flux = np.asarray(d["spectrum/observed"])
        mask = np.asarray(d["spectrum/mask"], dtype=bool)
        feature = np.asarray(d["spectrum/feature_mask"], dtype=bool) if "feature_mask" in d["spectrum"] else mask
        z = float(d.attrs["redshift"])
    full_dir = output_root / cell.replace("_features", "_all")
    with h5py.File(full_dir / "ceridwen_derived_outputs.h5", "r") as d:
        full_mask = np.asarray(d["spectrum/mask"], dtype=bool)
    _style()
    fig, ax = plt.subplots(figsize=(8.0, 2.8))
    scale = 1e29
    ax.plot(wave[full_mask], flux[full_mask] * scale, color="#b5b5b5", lw=0.7, label="fitted pixels, full spectrum")
    kept = full_mask & feature
    ax.plot(np.where(kept, wave, np.nan), np.where(kept, flux * scale, np.nan), color=MODE_COLORS["features"], lw=0.9,
            label=f"absorption-feature pixels ({kept.sum()} of {full_mask.sum()})")
    ax.set_xlabel("observed wavelength [Å]")
    ax.set_ylabel(r"$F_\nu$ [$10^{-29}$ erg s$^{-1}$ cm$^{-2}$ Hz$^{-1}$]")
    ax.set_title(f"M5_172669 (z = {z:.3f}): pixels kept by the absorption-feature mask, ±1000 km/s line windows")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    path = figure_dir / "feature_windows_M5_172669.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument("--no-figures", action="store_true")
    args = parser.parse_args(argv)
    records = collect(args.output_root)
    if not records:
        print("no completed cells", file=sys.stderr)
        return 1
    (args.output_root / "summary.json").write_text(json.dumps(records, indent=1, default=float))
    with (args.output_root / "summary.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cell", "mode", "target", "is_mock", "tilt", "snr_scale", "seed", "pixels", "ess",
                         "calls", "wall_s", "logZ", *[f"{p}_{q}" for p in PARAMS for q in ("q16", "q50", "q84")],
                         *[f"{p}_truth" for p in PARAMS]])
        for r in records:
            writer.writerow([r["name"], r["mode"], r["target"], r["is_mock"], r["mock_tilt"], r["mock_snr_scale"],
                             r["mock_seed"], r["spectrum_ndof"], round(r["ess"], 1), r["n_likelihood_calls"],
                             round(r["wall_time_s"], 1), round(r["log_evidence"], 2),
                             *[round(r["quantiles"][p][i], 5) for p in PARAMS for i in (1, 2, 3)],
                             *[round(r["truth"][p], 5) if r["is_mock"] else "" for p in PARAMS]])
    print(mock_tables(records))
    print()
    print(real_tables(records))
    print()
    print(run_table(records))
    if not args.no_figures:
        args.figure_dir.mkdir(parents=True, exist_ok=True)
        for maker in (plot_mock_bias, plot_mock_width, plot_real):
            path = maker(records, args.figure_dir)
            if path:
                print("figure:", path, file=sys.stderr)
        path = plot_windows(args.output_root, args.figure_dir)
        if path:
            print("figure:", path, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
