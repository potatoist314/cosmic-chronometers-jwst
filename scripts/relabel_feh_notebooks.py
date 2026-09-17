#!/usr/bin/env python3
"""Relabel executed per-target notebooks to display [Fe/H] instead of grid Z.

For every ``*_executed.ipynb`` under the given roots this patches the source of
the corner/summary cell exactly as in the production notebook
(``notebooks/ceridwen_integrated_photometry_spectra.ipynb``), rebuilds the
physical corner figure from the saved ``ceridwen_result.h5`` and
``ceridwen_derived_outputs.h5`` (the same 400 equal-weight posterior draws,
metallicity shifted by ``FEH_OFFSET``), rewrites the ``Z`` row of the displayed
summary table as ``[Fe/H]``, and leaves every other output untouched. Nothing
is re-executed and the HDF5 files are not modified.

    ceridwen/.venv/bin/python scripts/relabel_feh_notebooks.py results archive/results
"""

from __future__ import annotations

import argparse
import base64
import io
import re
import sys
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")

import corner
import matplotlib.pyplot as plt
import nbformat
import numpy as np
from scipy.special import softmax

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from build_dr2_quiescent_summary import FEH_OFFSET  # noqa: E402

CORNER_ANCHOR = "physical_corner = np.column_stack"
SOURCE_EDITS = [
    (
        'direct_draws = {\n    name: scalar_draws(selected_posterior, name)\n'
        '    for name in ["logmass", "Z", "afe", "diffuse_tau_kc"]\n}\n',
        "# Grid Z is log10 of the iron abundance relative to Z_sun = 0.0185\n"
        "# (ceridwen/scripts_afe/build_afe_hr_grid.py), so [Fe/H] = Z + FEH_OFFSET.\n"
        f"FEH_OFFSET = {FEH_OFFSET}\n"
        'direct_draws = {\n    name: scalar_draws(selected_posterior, name)\n'
        '    for name in ["logmass", "Z", "afe", "diffuse_tau_kc"]\n}\n',
    ),
    (
        'physical_columns = [\n    direct_draws["logmass"],\n    direct_draws["Z"],\n',
        'physical_columns = [\n    direct_draws["logmass"],\n    direct_draws["Z"] + FEH_OFFSET,\n',
    ),
    ('    r"$\\log_{10} Z$",\n', '    r"$[\\mathrm{Fe}/\\mathrm{H}]$",\n'),
    (
        'physical_ranges = [\n    joint_bounds["logmass"],\n    joint_bounds["Z"],\n',
        'physical_ranges = [\n    joint_bounds["logmass"],\n    tuple(np.asarray(joint_bounds["Z"]) + FEH_OFFSET),\n',
    ),
    (
        '    "Z": "log10 absolute metallicity",\n',
        f'    "Z": "log10 iron abundance; [Fe/H] = Z + {FEH_OFFSET}",\n',
    ),
    (
        "display(summary)\n",
        'summary_display = summary.copy()\nz_row = summary_display["parameter"] == "Z"\n'
        'summary_display.loc[z_row, ["q16", "q50", "q84"]] += FEH_OFFSET\n'
        'summary_display.loc[z_row, ["parameter", "unit"]] = ["[Fe/H]", "dex"]\n'
        "display(summary_display)\n",
    ),
]
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
C_KMS = 299792.458
HTML_ROW = re.compile(
    r"<td>Z</td>\n(\s*)<td>(-?\d+\.\d+)</td>\n\s*<td>(-?\d+\.\d+)</td>\n\s*<td>(-?\d+\.\d+)</td>\n\s*<td>log10 abso\.\.\.</td>"
)
PLAIN_ROW = re.compile(
    r"^(\d+)(\s+Z)(\s+-?\d+\.\d+)(\s+-?\d+\.\d+)(\s+-?\d+\.\d+)(\s+log10 abso\.\.\.)$", re.MULTILINE
)


class Skip(Exception):
    pass


def posterior_draws(result_path: Path, derived_path: Path):
    """The notebook's 400 evenly spaced rows of the seeded equal-weight posterior."""
    columns, labels = [], []
    with h5py.File(result_path, "r") as result, h5py.File(derived_path, "r") as derived:
        attrs = result["model"].attrs
        weights = softmax(np.asarray(result["samples/log_weights"]))
        rng = np.random.default_rng(int(attrs["random_seed"]) + 1)
        rows = rng.choice(len(weights), size=2000, replace=True, p=weights)
        rows = rows[np.linspace(0, 1999, 400, dtype=int)]

        def draws(name):
            return np.asarray(result["samples"][name]).reshape(len(weights), -1)[rows, 0]

        columns += [draws("logmass"), draws("Z") + FEH_OFFSET, draws("afe"), draws("diffuse_tau_kc")]
        labels += [r"$\log_{10}(M_\star/M_\odot)$", r"$[\mathrm{Fe}/\mathrm{H}]$",
                   r"$[\alpha/\mathrm{Fe}]$", r"$\tau_{\mathrm{diffuse}}$"]
        if str(attrs["fit_mode"]) == "full_spectrum":
            columns += [100.0 * np.exp(draws("log_f_calib")), draws("spectrum_scaling")]
            labels += [r"$f_{\mathrm{calib}}\,[\%]$", r"$s_{\mathrm{spectrum}}$"]
        if float(attrs.get("free_zred_kms", 0.0)) > 0:
            z_catalog = float(derived.attrs["redshift"])
            columns.append(C_KMS * (draws("zred") - z_catalog) / (1.0 + z_catalog))
            labels.append(r"$\Delta v_z\,[\mathrm{km\,s^{-1}}]$")
        if bool(attrs.get("free_sigma", False)) or float(attrs.get("free_sigma_frac", 0.0)) > 0:
            columns.append(draws("sigma_smooth"))
            labels.append(r"$\sigma_\star\,[\mathrm{km\,s^{-1}}]$")
        columns.append(np.asarray(derived["sfh/mass_weighted_age_gyr"]))
        labels.append(r"$t_{\mathrm{MW}}\,[\mathrm{Gyr}]$")
        names = [n.decode() if isinstance(n, bytes) else str(n) for n in derived["summary/parameter"][:]]
        stored = {n: (float(derived["summary/q16"][i]), float(derived["summary/q50"][i]),
                      float(derived["summary/q84"][i])) for i, n in enumerate(names)}
    # The stored summary quantiles come from the same draws: check the reproduction.
    checks = {"logmass": columns[0], "Z": columns[1] - FEH_OFFSET, "afe": columns[2],
              "diffuse_tau_kc": columns[3], "mass-weighted age [Gyr]": columns[-1]}
    for name, values in checks.items():
        if not np.allclose(np.percentile(values, [16, 50, 84]), stored[name], rtol=0, atol=1e-9):
            raise Skip(f"draws do not reproduce the stored summary for {name}")
    return np.column_stack(columns), labels, stored["Z"]


def render_corner(data, labels) -> tuple[bytes, str]:
    figure = corner.corner(
        data,
        labels=labels,
        range=None,
        quantiles=[0.16, 0.50, 0.84],
        title_quantiles=[0.16, 0.50, 0.84],
        show_titles=True,
        levels=(0.68, 0.95),
        **CORNER_STYLE,
    )
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi="figure", bbox_inches="tight",
                   facecolor=figure.get_facecolor(), edgecolor=figure.get_edgecolor())
    text = repr(figure)
    plt.close(figure)
    return buffer.getvalue(), text


def relabel_table(output, stored_z) -> None:
    feh = ["%.6f" % (q + FEH_OFFSET) for q in stored_z]
    html = output["data"]["text/html"]
    match = HTML_ROW.search(html)
    if match is None:
        raise Skip("summary HTML has no Z row")
    for old, new in zip(match.groups()[1:], feh):
        if abs(float(old) - (float(new) - FEH_OFFSET)) > 1e-6:
            raise Skip("summary HTML Z row does not match the stored quantiles")
    pad = match.group(1)
    output["data"]["text/html"] = html[: match.start()] + (
        f"<td>[Fe/H]</td>\n{pad}<td>{feh[0]}</td>\n{pad}<td>{feh[1]}</td>\n{pad}<td>{feh[2]}</td>\n{pad}<td>dex</td>"
    ) + html[match.end():]
    plain = output["data"]["text/plain"]
    match = PLAIN_ROW.search(plain)
    if match is None:
        raise Skip("summary text has no Z row")
    index, name, *numbers, unit = match.groups()
    line = index + "[Fe/H]".rjust(len(name)) + "".join(
        value.rjust(len(segment)) for segment, value in zip(numbers, feh)
    ) + "dex".rjust(len(unit))
    output["data"]["text/plain"] = plain[: match.start()] + line + plain[match.end():]


def relabel_notebook(path: Path) -> str:
    notebook = nbformat.read(path, as_version=4)
    cells = [c for c in notebook.cells if c.cell_type == "code" and CORNER_ANCHOR in c.source]
    if not cells:
        raise Skip("no corner cell")
    cell = cells[0]
    if "FEH_OFFSET" in cell.source:
        return "already relabelled"
    source = cell.source
    for old, new in SOURCE_EDITS:
        if source.count(old) != 1:
            raise Skip(f"corner cell source lacks {old.splitlines()[0]!r}")
        source = source.replace(old, new)
    figures = [o for o in cell.outputs if o.output_type == "display_data" and "image/png" in o["data"]]
    tables = [o for o in cell.outputs if o.output_type == "display_data" and "text/html" in o["data"]]
    if not cell.outputs:  # the run stopped before this cell: source only
        cell.source = source
        nbformat.write(notebook, path)
        return "relabelled"
    if not figures or not tables:
        raise Skip("corner cell has no figure or table output")
    data, labels, stored_z = posterior_draws(path.parent / "ceridwen_result.h5",
                                             path.parent / "ceridwen_derived_outputs.h5")
    png, text = render_corner(data, labels)
    if figures[0]["data"]["text/plain"].strip() != text:
        raise Skip(f"corner figure text differs: {figures[0]['data']['text/plain'].strip()!r} vs {text!r}")
    relabel_table(tables[0], stored_z)
    figures[0]["data"]["image/png"] = base64.b64encode(png).decode("ascii")
    cell.source = source
    nbformat.write(notebook, path)
    return "relabelled"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--limit", type=int, default=None, help="stop after this many notebooks")
    parser.add_argument("--pattern", default="*_executed.ipynb", help="notebook file name glob")
    args = parser.parse_args(argv)
    paths = sorted(p for root in args.roots for p in root.rglob(args.pattern))
    if args.limit:
        paths = paths[: args.limit]
    counts = {"relabelled": 0, "already relabelled": 0, "skipped": 0}
    for path in paths:
        try:
            status = relabel_notebook(path)
        except Skip as reason:
            status = "skipped"
            print(f"SKIP {path}: {reason}", flush=True)
        counts[status] += 1
        if status == "relabelled":
            print(f"ok   {path}", flush=True)
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
