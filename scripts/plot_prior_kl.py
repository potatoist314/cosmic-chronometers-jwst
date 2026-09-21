"""Per-parameter KL divergence of the posterior from the prior, M1_210210.

For each sampled scalar parameter, D_KL(posterior || prior) in bits from the
nested-sampling dead points (``marginal_kl_bits`` in
``scripts/per_galaxy_diagnostics.py``). Each fit is compared with its own stored
prior. The SFR ratios are replaced by log10 SFR per SFH bin (M_sun/yr), a
derived quantity: its prior is a sample of every sampled parameter drawn from
the stored priors and pushed through the notebook's SFH conversion, and the
empirical CDF of that sample plays the role of the prior CDF. Writes a sorted
bar chart and its table to ``wiki/analyses/m1-210210-reference/``.

Usage: ``JAX_PLATFORMS=cpu ceridwen/.venv/bin/python scripts/plot_prior_kl.py``
"""

from __future__ import annotations

import functools
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import per_galaxy_diagnostics as pgd  # noqa: E402

TARGET = "M1_210210"
REFERENCE = PROJECT_ROOT / "results/m1-210210-reference"
OUT_DIR = PROJECT_ROOT / "wiki/analyses/m1-210210-reference"
FITS = {
    "A": (PROJECT_ROOT / "results/dr2-quiescent-new-defaults" / f"210210-{TARGET}", "k",
          r"A: order 3, $\tau_{\mathrm{dust}} < 2$"),
    "C": (REFERENCE / "tau-1/poly10" / f"210210-{TARGET}", "tab:red",
          r"C: order 10, $\tau_{\mathrm{dust}} < 1$, free $z$, $\sigma_\star$"),
}
LABELS = {
    "logmass": r"$\log_{10}(M_\star/M_\odot)$", "Z": r"$[\mathrm{Fe}/\mathrm{H}]$",
    "afe": r"$[\alpha/\mathrm{Fe}]$", "diffuse_tau_kc": r"$\tau_{\mathrm{dust}}$",
    "diffuse_dust_index": r"$\delta_{\mathrm{dust}}$", "log_f_calib": r"$\log f_{\mathrm{calib}}$",
    "spectrum_scaling": "spectrum scaling", "zred": r"$z$", "sigma_smooth": r"$\sigma_\star$",
}
N_BOOT = 200
PRIOR_SAMPLE_MULT = 10  # prior reference sample = this many times the dead points; keeps its own noise near the bootstrap error
SEED = 20260832


def label(name, j, edges_gyr):
    """Row label; an SFH bin is named by its two lookback-time edges."""
    if name != "log_sfr_bin":
        return LABELS[name]
    a, b = (f"{t:.3g}" for t in edges_gyr[j:j + 2])
    return rf"$\log_{{10}}\mathrm{{SFR}}$ {a}-{b} Gyr"


@functools.cache
def _sfh_nodes_fn():
    """Compiled once per process: ``logsfr_ratios_to_sfh`` over rows of ratios."""
    import jax
    from ceridwen.model import logsfr_ratios_to_sfh

    return jax.jit(jax.vmap(lambda r, t: logsfr_ratios_to_sfh(r, sfh_times_yr=t), in_axes=(0, None)))


def _sfh_nodes(logsfr_ratios, times_yr):
    return _sfh_nodes_fn()(logsfr_ratios, times_yr)


def log_sfr_bins(logmass, logsfr_ratios, edges_gyr) -> np.ndarray:
    """log10 SFR [M_sun/yr] in each SFH bin, shape (n, bins).

    ``logsfr_ratios_to_sfh`` (the notebook's ``sfh_from_ratios``) gives the
    unit-mass SFR at the bin edges; the bin SFR is the mean of its two edges
    (the notebook's ``interval_masses`` over the bin width) times 10**logmass.
    """
    times_yr = np.asarray(edges_gyr, dtype=float) * 1e9
    nodes = np.asarray(_sfh_nodes(np.asarray(logsfr_ratios, dtype=float), times_yr))
    with np.errstate(divide="ignore"):  # extreme prior draws underflow to SFR 0, log10 -inf; ranks stay valid
        return np.asarray(logmass, dtype=float)[:, None] + np.log10(0.5 * (nodes[:, :-1] + nodes[:, 1:]))


def prior_draws(galaxy, n, rng, names=None) -> dict:
    """``n`` draws of the sampled parameters ``names`` (default all) from the fit's stored priors."""
    draws = {}
    for name in names or galaxy.prior_text:
        text = galaxy.prior_text[name]
        size = np.asarray(galaxy.samples[name]).reshape(len(galaxy.log_weights), -1).shape[1]
        u = rng.uniform(0.0, 1.0, (n, size))
        draws[name] = np.asarray(pgd.parse_prior(text).unit_transform(u), dtype=float).reshape(n, size)
    return draws


def prior_log_sfr_bins(galaxy, rng, n=None) -> np.ndarray:
    """Prior sample of log10 SFR per SFH bin: prior draws through the SFH conversion."""
    n = len(galaxy.log_weights) if n is None else n
    d = prior_draws(galaxy, n, rng, names=("logmass", "logsfr_ratios"))
    return log_sfr_bins(d["logmass"][:, 0], d["logsfr_ratios"], galaxy.sfh_edges_gyr)


def empirical_unit_values(values, prior_sample) -> np.ndarray:
    """u = F_prior(x) with F the empirical CDF of ``prior_sample`` (mid-rank for ties)."""
    s = np.sort(np.asarray(prior_sample, dtype=float))
    x = np.asarray(values, dtype=float)
    return 0.5 * (np.searchsorted(s, x, "left") + np.searchsorted(s, x, "right")) / len(s)


def log_sfr_noise_floor(galaxy, seed=SEED, repeats=200) -> float:
    """95th percentile of the SFH-bin KL when the posterior is itself a prior sample.

    Same estimator as the notebook's floor (uniform u under the posterior
    weights) but with u from the empirical prior CDF of a finite sample.
    """
    rng = np.random.default_rng(seed)
    w = pgd.posterior_weights(galaxy)
    reference = prior_log_sfr_bins(galaxy, rng, n=PRIOR_SAMPLE_MULT * len(w))
    bins = rng.integers(reference.shape[1], size=repeats)
    values = [pgd.marginal_kl_bits(empirical_unit_values(prior_log_sfr_bins(galaxy, rng)[:, j], reference[:, j]), w)
              for j in bins]
    return float(np.percentile(values, 95))


def kl_table(galaxy) -> pd.DataFrame:
    """KL in bits per scalar parameter; err is half the bootstrap 16-84% width.

    ``logsfr_ratios`` rows are replaced by ``log_sfr_bin[j]`` rows.
    """
    w = pgd.posterior_weights(galaxy)
    rng = np.random.default_rng(SEED)
    picks = rng.integers(0, len(w), (N_BOOT, len(w)))
    columns = {}
    for name, text in galaxy.prior_text.items():
        if name == "logsfr_ratios":
            continue
        prior = pgd.parse_prior(text)
        x = np.asarray(galaxy.samples[name], dtype=float).reshape(len(w), -1)
        for j in range(x.shape[1]):
            key = name if x.shape[1] == 1 else f"{name}[{j}]"
            columns[key] = (label(name, j, galaxy.sfh_edges_gyr), pgd.prior_unit_values(x[:, j], prior))
    posterior = log_sfr_bins(np.asarray(galaxy.samples["logmass"], dtype=float),
                             np.asarray(galaxy.samples["logsfr_ratios"], dtype=float), galaxy.sfh_edges_gyr)
    reference = prior_log_sfr_bins(galaxy, rng, n=PRIOR_SAMPLE_MULT * len(w))
    for j in range(posterior.shape[1]):
        columns[f"log_sfr_bin[{j}]"] = (label("log_sfr_bin", j, galaxy.sfh_edges_gyr),
                                        empirical_unit_values(posterior[:, j], reference[:, j]))
    rows = []
    for key, (text, u) in columns.items():
        boot = [pgd.marginal_kl_bits(u[i], w[i]) for i in picks]
        rows.append({"parameter": key, "label": text, "bits": pgd.marginal_kl_bits(u, w),
                     "err": 0.5 * np.subtract(*np.percentile(boot, [84, 16]))})
    return pd.DataFrame(rows).set_index("parameter")


def total_kl_bits(galaxy) -> float:
    """Joint D_KL over all parameters: (<ln L>_posterior - ln Z) / ln 2."""
    w = pgd.posterior_weights(galaxy)
    return float((np.sum(w * galaxy.log_likelihoods) - galaxy.log_evidence) / np.log(2))


def main() -> None:
    matplotlib.use("Agg")  # CLI only; a notebook keeps its inline backend
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    galaxies = {k: pgd.load_galaxy(folder) for k, (folder, _c, _n) in FITS.items()}
    kl = {k: kl_table(g) for k, g in galaxies.items()}
    table = pd.concat({k: t[["bits", "err"]] for k, t in kl.items()}, axis=1)
    order = table[("C", "bits")].sort_values(ascending=False).index
    table = table.loc[order]
    table.columns = [f"{k}_{c}" for k, c in table.columns]
    table.loc["sum_of_marginals"] = {f"{k}_bits": t["bits"].sum() for k, t in kl.items()}
    table.loc["total_joint"] = {f"{k}_bits": total_kl_bits(g) for k, g in galaxies.items()}
    table.to_csv(OUT_DIR / f"kl-{TARGET}.csv", float_format="%.3f")
    print(table.round(2).to_string())

    labels = pd.concat([t["label"] for t in kl.values()]).groupby(level=0).first().loc[order]
    y = np.arange(len(order))[::-1]
    h = 0.8 / len(kl)
    fig, ax = plt.subplots(figsize=(9.5, 6.8))
    for n, (k, t) in enumerate(kl.items()):
        t = t.reindex(order)
        yy = y + 0.4 - h * (n + 0.5)
        ax.barh(yy, t["bits"], height=h, color=FITS[k][1], label=FITS[k][2], alpha=0.85)
        ax.errorbar(t["bits"], yy, xerr=t["err"], fmt="none", ecolor="0.4", lw=0.8, capsize=1.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel(r"$D_{\mathrm{KL}}(\mathrm{posterior}\,\|\,\mathrm{prior})$ [bits]")
    ax.grid(axis="x", color="0.9", lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8,
              borderaxespad=0.0, title=TARGET)
    fig.savefig(OUT_DIR / f"kl-{TARGET}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
