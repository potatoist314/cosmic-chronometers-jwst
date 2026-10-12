"""Run plot_prior_kl.main() on a fixed fake KL table and capture the saved figure."""
import matplotlib
import pandas as pd
import plot_prior_kl as kl

PARAMS = ["logmass", "diffuse_tau_noll", "Z", "diffuse_delta"]


def run(monkeypatch, tmp_path):
    saved = []
    table = pd.DataFrame({"bits": [3.0, 1.0, 0.5, 0.2], "err": [0.1, 0.1, 0.05, 0.05],
                          "label": [kl.LABELS.get(p, p) for p in PARAMS]}, index=PARAMS)
    monkeypatch.setattr(kl.pgd, "load_galaxy", lambda folder: object())
    monkeypatch.setattr(kl, "kl_table", lambda galaxy: table.copy())
    monkeypatch.setattr(kl, "total_kl_bits", lambda galaxy: 4.0)
    monkeypatch.setattr(kl, "OUT_DIR", tmp_path)
    monkeypatch.setattr(matplotlib.figure.Figure, "savefig", lambda self, *a, **k: saved.append((self, k)))
    kl.main()
    return saved
