"""Add the dust-versus-every-SFH-bin corner plot to executed fit notebooks.

The figure is built from each result directory's saved posterior
(`ceridwen_result.h5`); no fit is run. The draws are the 400 rows the notebook
itself selected, which is checked against the saved mass-fraction draws.

Usage:
    ceridwen/.venv/bin/python scripts/add_dust_sfh_corner.py PATH [PATH ...]

PATH is an executed notebook or a directory searched for `*executed*.ipynb`.
"""

import argparse
import base64
import io
import json
import sys
import uuid
from itertools import pairwise
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")
import corner
import matplotlib.pyplot as plt
import numpy as np
from ceridwen.cosmology import age_gyr
from ceridwen.model import logsfr_ratios_to_sfh
from scipy.special import softmax
from scipy.stats import spearmanr

CELL_TAG = "dust-sfh-all-bins"
CELL_SOURCE = [
    "# Dust parameters against every SFH bin.\n",
    "# Output added from the saved posterior by scripts/add_dust_sfh_corner.py. No refit.",
]
DUST_PARAMETERS = {
    "diffuse_tau_kc": r"$\tau_{\mathrm{diffuse}}$",
    "diffuse_dust_index": r"$n_{\mathrm{dust}}$",
}
# Same style as the production notebook's corner plots.
CORNER_STYLE = {
    "bins": 40,
    "color": "#0072B2",
    "smooth": 1.2,
    "smooth1d": 1.0,
    "plot_datapoints": False,
    "plot_density": True,
    "plot_contours": True,
    "fill_contours": False,
    "hist_kwargs": {"linewidth": 1.5},
    "contour_kwargs": {"linewidths": 1.0},
}


def notebook_draws(result_dir, seed, universe_age, posterior_count, selected_count):
    """Return dust draws, mass fractions and bin edges for the notebook's selected rows."""
    derived_path = result_dir / "ceridwen_derived_outputs.h5"
    saved_fractions = None
    if derived_path.is_file():
        with h5py.File(derived_path, "r") as derived:
            if seed is None:
                seed = int(derived.attrs["random_seed"])
            edges = np.asarray(derived["sfh/lookback_time_gyr"])
            saved_fractions = np.asarray(derived["sfh/mass_fraction_draws"])
    else:
        if seed is None or universe_age is None:
            raise ValueError("no ceridwen_derived_outputs.h5: give --seed and --universe-age")
        edges = np.array([0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 5.0, universe_age])

    with h5py.File(result_dir / "ceridwen_result.h5", "r") as result:
        samples = result["samples"]
        weights = softmax(np.asarray(samples["log_weights"]))
        # Same resampling as the notebook: equal-weight draws, then an even subset.
        indices = np.random.default_rng(seed + 1).choice(
            len(weights), size=posterior_count, replace=True, p=weights
        )
        rows = indices[
            np.linspace(0, posterior_count - 1, min(selected_count, posterior_count), dtype=int)
        ]
        ratios = np.asarray(samples["logsfr_ratios"])[rows]
        dust = {
            name: np.asarray(samples[name])[rows].reshape(len(rows))
            for name in DUST_PARAMETERS
            if name in samples
        }

    histories = np.asarray(
        [logsfr_ratios_to_sfh(row, sfh_times_yr=edges * 1e9) for row in ratios]
    )
    interval_masses = 0.5 * (histories[:, :-1] + histories[:, 1:]) * np.diff(edges) * 1e9
    fractions = interval_masses / interval_masses.sum(axis=1)[:, None]
    if saved_fractions is not None and not (
        saved_fractions.shape == fractions.shape
        and np.allclose(saved_fractions, fractions, rtol=0.0, atol=1e-8)
    ):
        raise ValueError("rebuilt draws differ from the notebook's saved mass-fraction draws")
    return dust, fractions, edges, saved_fractions is not None


def cell_outputs(dust, fractions, edges):
    labels = [DUST_PARAMETERS[name] for name in dust]
    bin_labels = [
        rf"$f_{{{start:g}-{stop:g}\,\mathrm{{Gyr}}}}$" for start, stop in pairwise(edges)
    ]
    figure = corner.corner(
        np.column_stack([*dust.values(), fractions]),
        labels=[*labels, *bin_labels],
        quantiles=[0.16, 0.50, 0.84],
        title_quantiles=[0.16, 0.50, 0.84],
        show_titles=True,
        levels=(0.68, 0.95),
        **CORNER_STYLE,
    )
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=72, bbox_inches="tight")
    width, height = figure.get_size_inches() * figure.dpi
    description = f"<Figure size {width:g}x{height:g} with {len(figure.axes)} Axes>"
    plt.close(figure)

    lines = []
    for label, column in zip(labels, dust.values()):
        for bin_index, bin_label in enumerate(bin_labels):
            rho = spearmanr(column, fractions[:, bin_index]).statistic
            lines.append(f"Spearman {label} vs {bin_label}: {rho:+.2f}\n")
    return [
        {
            "data": {
                "image/png": base64.b64encode(buffer.getvalue()).decode("ascii"),
                "text/plain": [description],
            },
            "metadata": {},
            "output_type": "display_data",
        },
        {"name": "stdout", "output_type": "stream", "text": lines},
    ]


def add_cell(notebook_path, outputs):
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    cells = [
        cell
        for cell in notebook["cells"]
        if CELL_TAG not in cell.get("metadata", {}).get("tags", [])
    ]
    corner_cells = [
        index
        for index, cell in enumerate(cells)
        if cell["cell_type"] == "code" and "corner.corner(" in "".join(cell["source"])
    ]
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": [CELL_TAG]},
        "outputs": outputs,
        "source": CELL_SOURCE,
    }
    if (notebook.get("nbformat"), notebook.get("nbformat_minor", 0)) >= (4, 5):
        new_cell["id"] = uuid.uuid4().hex[:8]
    position = corner_cells[-1] + 1 if corner_cells else len(cells)
    cells.insert(position, new_cell)
    notebook["cells"] = cells
    notebook_path.write_text(
        json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--seed", type=int, help="notebook SEED when no derived outputs exist")
    parser.add_argument("--redshift", type=float, help="catalogue z when no derived outputs exist")
    parser.add_argument("--posterior-count", type=int, default=2000)
    parser.add_argument("--selected-count", type=int, default=400)
    parser.add_argument("--png", type=Path, help="also write the figure here; notebook untouched")
    arguments = parser.parse_args()

    notebooks = []
    for path in arguments.paths:
        notebooks += sorted(path.rglob("*executed*.ipynb")) if path.is_dir() else [path]
    universe_age = None if arguments.redshift is None else float(age_gyr(arguments.redshift))

    failures = 0
    for notebook_path in notebooks:
        try:
            dust, fractions, edges, checked = notebook_draws(
                notebook_path.parent,
                arguments.seed,
                universe_age,
                arguments.posterior_count,
                arguments.selected_count,
            )
            if not dust:
                raise ValueError("no dust parameter in the saved samples")
            outputs = cell_outputs(dust, fractions, edges)
            if arguments.png:
                arguments.png.write_bytes(base64.b64decode(outputs[0]["data"]["image/png"]))
            else:
                add_cell(notebook_path, outputs)
            check = "draws match the notebook" if checked else "no saved draws to check"
            print(f"ok   {notebook_path}  {len(dust)} dust x {fractions.shape[1]} bins  {check}")
        except Exception as error:  # report and continue with the next notebook
            failures += 1
            print(f"FAIL {notebook_path}  {type(error).__name__}: {error}")
    print(f"{len(notebooks) - failures} done, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
