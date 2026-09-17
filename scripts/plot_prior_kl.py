"""Per-parameter KL divergence of the posterior from the prior, M1_210210.

For each sampled scalar parameter, D_KL(posterior || prior) in bits from the
nested-sampling dead points (``marginal_kl_bits`` in
``scripts/per_galaxy_diagnostics.py``). Each fit is compared with its own stored
prior. Writes a sorted bar chart and its table to
``wiki/analyses/m1-210210-reference/``.

Usage: ``JAX_PLATFORMS=cpu ceridwen/.venv/bin/python scripts/plot_prior_kl.py``
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

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
    "B": (REFERENCE / "tau-0p2/poly10" / f"210210-{TARGET}", "tab:blue",
          r"B: order 10, $\tau_{\mathrm{dust}} < 0.2$"),
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
SEED = 20260832


def label(name, j, nodes_gyr):
    """Row label; an SFR ratio is named by its two lookback-time nodes."""
    if name != "logsfr_ratios":
        return LABELS[name]
    a, b = (f"{t:.3g}" for t in nodes_gyr[j:j + 2])
    return rf"$\log[\mathrm{{SFR}}({a})/\mathrm{{SFR}}({b}\,\mathrm{{Gyr}})]$"


def kl_table(galaxy) -> pd.DataFrame:
    """KL in bits per scalar parameter; err is half the bootstrap 16-84% width."""
    w = pgd.posterior_weights(galaxy)
    picks = np.random.default_rng(SEED).integers(0, len(w), (N_BOOT, len(w)))
    rows = []
    for name, text in galaxy.prior_text.items():
        prior = pgd.parse_prior(text)
        x = np.asarray(galaxy.samples[name], dtype=float).reshape(len(w), -1)
        for j in range(x.shape[1]):
            u = pgd.prior_unit_values(x[:, j], prior)
            boot = [pgd.marginal_kl_bits(u[i], w[i]) for i in picks]
            rows.append({"parameter": name if x.shape[1] == 1 else f"{name}[{j}]",
                         "label": label(name, j, galaxy.sfh_edges_gyr),
                         "bits": pgd.marginal_kl_bits(u, w),
                         "err": 0.5 * np.subtract(*np.percentile(boot, [84, 16]))})
    return pd.DataFrame(rows).set_index("parameter")


def total_kl_bits(galaxy) -> float:
    """Joint D_KL over all parameters: (<ln L>_posterior - ln Z) / ln 2."""
    w = pgd.posterior_weights(galaxy)
    return float((np.sum(w * galaxy.log_likelihoods) - galaxy.log_evidence) / np.log(2))


def main() -> None:
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
    fig.savefig(OUT_DIR / f"kl-{TARGET}.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
