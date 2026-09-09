#!/usr/bin/env python3
"""Add the HST ACS F814W cutout cell to already-executed fit notebooks.

The production notebook gained a cell that shows the fitted galaxy and the
COSMOS2015 three-arcsecond aperture. Re-running the 187 finished fits to pick
it up would cost about 16 GPU hours, so this script inserts the cell instead.

It executes the cell on its own, in a kernel that holds only the four names the
cell reads (``PROJECT_ROOT``, ``TARGET_ID``, ``galaxy`` and ``z_catalog``), and
writes the cell and its real outputs into each executed notebook at the same
position it has in the production notebook. Nothing else in those notebooks
changes, and no fit is repeated.

Running this twice changes nothing the second time.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from astropy.table import Table
from nbclient import NotebookClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
LEGAC_PATH = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
DEFAULT_RESULTS_ROOT = PROJECT_ROOT / "results/dr2-quiescent-new-defaults"
CELL_MARKER = "hst_f814w"
READ_MARKER = "READ-MARKER"

PREAMBLE_SOURCE = """\
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.table import Table

PROJECT_ROOT = Path({root!r})
_legac = Table.read(PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz").to_pandas()
_legac["SPECT_ID"] = _legac["SPECT_ID"].map(
    lambda value: value.decode() if isinstance(value, bytes) else value
)
"""

TARGET_SOURCE = """\
TARGET_ID = {target!r}
_rows = _legac[_legac["SPECT_ID"] == TARGET_ID]
assert len(_rows) == 1
galaxy = _rows.iloc[0]
z_catalog = float(galaxy["z"])
"""


def _single_index(cells, marker: str) -> int:
    found = [index for index, cell in enumerate(cells) if marker in "".join(cell.source)]
    if len(found) != 1:
        raise RuntimeError(f"Expected one cell containing {marker!r}, found {found}")
    return found[0]


def _executed_notebooks(results_root: Path) -> list[Path]:
    return sorted(results_root.glob("*/*_executed.ipynb"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", type=Path, default=DEFAULT_RESULTS_ROOT)
    parser.add_argument("--kernel", default="python3")
    arguments = parser.parse_args()

    production = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cell_source = production.cells[_single_index(production.cells, CELL_MARKER)].source
    offset = _single_index(production.cells, CELL_MARKER) - _single_index(
        production.cells, READ_MARKER
    )

    notebooks = _executed_notebooks(arguments.results_root)
    if not notebooks:
        raise SystemExit(f"No executed notebooks under {arguments.results_root}")
    # Read the catalogue once here as well, so a target missing from it stops the
    # run before any kernel starts.
    catalogue = Table.read(LEGAC_PATH).to_pandas()
    known = {
        value.decode() if isinstance(value, bytes) else value
        for value in catalogue["SPECT_ID"]
    }

    inserted = 0
    skipped = 0
    failures: list[str] = []

    scratch = nbformat.v4.new_notebook()
    client = NotebookClient(
        scratch,
        kernel_name=arguments.kernel,
        timeout=600,
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    with client.setup_kernel():
        preamble = nbformat.v4.new_code_cell(
            source=PREAMBLE_SOURCE.format(root=str(PROJECT_ROOT))
        )
        client.nb.cells = [preamble]
        client.execute_cell(preamble, 0)

        for path in notebooks:
            target = path.name.removesuffix("_executed.ipynb")
            notebook = nbformat.read(path, as_version=4)
            if any(CELL_MARKER in "".join(cell.source) for cell in notebook.cells):
                skipped += 1
                continue
            if target not in known:
                failures.append(f"{target}: not in {LEGAC_PATH.name}")
                continue
            setup = nbformat.v4.new_code_cell(source=TARGET_SOURCE.format(target=target))
            cell = nbformat.v4.new_code_cell(source=cell_source)
            client.nb.cells = [preamble, setup, cell]
            client.execute_cell(setup, 1)
            client.execute_cell(cell, 2)
            errors = [output for output in cell.outputs if output.output_type == "error"]
            if errors:
                failures.append(f"{target}: {errors[0].ename}: {errors[0].evalue}")
                continue
            cell.execution_count = None
            notebook.cells.insert(_single_index(notebook.cells, READ_MARKER) + offset, cell)
            nbformat.write(notebook, path)
            inserted += 1
            if inserted % 25 == 0:
                print(f"  {inserted} notebooks updated")

    print(
        f"{len(notebooks)} executed notebooks: {inserted} updated, "
        f"{skipped} already had the cell, {len(failures)} failed"
    )
    for failure in failures:
        print(f"  fail {failure}")


if __name__ == "__main__":
    main()
