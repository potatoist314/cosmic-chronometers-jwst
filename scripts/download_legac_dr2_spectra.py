#!/usr/bin/env python3
"""Download the LEGA-C DR2 1D spectra listed in the DR2 catalogue.

The catalogue's ``Filename`` column names one FITS file per spectrum. VizieR
mirrors those files for catalogue J/ApJS/239/27 in its ``sp/`` subdirectory,
which its ReadMe records as the 1988 reduced 1D spectra taken from
http://www.mpia.de/home/legac/.

Running this twice downloads nothing the second time, so it is safe to resume
after an interruption.
"""

from __future__ import annotations

import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from astropy.io import fits
from astropy.table import Table


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGAC_INPUT = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
OUTPUT_DIR = PROJECT_ROOT / "data/raw/legac_dr2/sp"

BASE_URL = "https://cdsarc.cds.unistra.fr/ftp/J/ApJS/239/27/sp/"

EXPECTED_SPECTRA = 1988
FILENAME_PATTERN = re.compile(r"^legac_M\d+_\d+_v2\.0\.fits$")

# Each spectrum is ~100 kB, so a short timeout is generous; CDS occasionally
# drops a connection over a run of ~2000 requests, hence the retries.
TIMEOUT_SECONDS = 60
MAX_ATTEMPTS = 3
RETRY_PAUSE_SECONDS = 5.0

# The four columns of the sole binary-table extension, per the ESO DR2 release
# description: wavelength in angstroms, flux and its error in
# 1e-19 erg s-1 cm-2 angstrom-1, and an integer quality flag.
EXPECTED_COLUMNS = ["WAVE", "FLUX", "ERR", "QUAL"]


def spectrum_filenames(path: Path) -> list[str]:
    catalogue = Table.read(path)
    if "Filename" not in catalogue.colnames:
        raise ValueError(f"{path} has no Filename column")

    names = sorted({str(value).strip() for value in catalogue["Filename"]})
    if len(names) != EXPECTED_SPECTRA:
        raise ValueError(
            f"Expected {EXPECTED_SPECTRA} unique spectrum filenames, found {len(names)}"
        )

    unexpected = [name for name in names if not FILENAME_PATTERN.match(name)]
    if unexpected:
        raise ValueError(f"Unexpected spectrum filenames: {unexpected[:5]}")
    return names


def check_spectrum(path: Path) -> None:
    """Raise unless the file is a readable Phase 3 single-row spectrum table."""
    with fits.open(path) as hdulist:
        if len(hdulist) < 2:
            raise ValueError(f"{path.name} has no binary-table extension")
        table = hdulist[1]
        if table.columns.names != EXPECTED_COLUMNS:
            raise ValueError(
                f"{path.name} has columns {table.columns.names}, "
                f"expected {EXPECTED_COLUMNS}"
            )
        if len(table.data) != 1:
            raise ValueError(
                f"{path.name} has {len(table.data)} table rows, expected 1 "
                "(each cell holds the whole spectrum)"
            )


def download(name: str, destination: Path) -> int:
    """Fetch one spectrum, returning its size in bytes.

    The file is written to a ``.part`` temporary and moved into place only after
    it has been validated, so an interrupted run never leaves a truncated FITS
    file that a later run would mistake for a complete download.
    """
    partial = destination.with_suffix(destination.suffix + ".part")
    last_error: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(
                BASE_URL + name, timeout=TIMEOUT_SECONDS
            ) as response:
                payload = response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_PAUSE_SECONDS)
            continue

        partial.write_bytes(payload)
        check_spectrum(partial)
        os.replace(partial, destination)
        return len(payload)

    partial.unlink(missing_ok=True)
    raise RuntimeError(f"Failed to download {name} after {MAX_ATTEMPTS} attempts: {last_error}")


def main() -> None:
    names = spectrum_filenames(LEGAC_INPUT)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    downloaded_bytes = 0

    for index, name in enumerate(names, start=1):
        destination = OUTPUT_DIR / name
        if destination.exists() and destination.stat().st_size > 0:
            skipped += 1
            continue
        downloaded_bytes += download(name, destination)
        downloaded += 1
        if downloaded % 100 == 0:
            print(f"  {index}/{len(names)} checked, {downloaded} downloaded")

    present = sorted(path.name for path in OUTPUT_DIR.glob("legac_M*_v2.0.fits"))
    if present != names:
        raise ValueError(
            f"{OUTPUT_DIR.relative_to(PROJECT_ROOT)} holds {len(present)} spectra, "
            f"expected {len(names)}"
        )
    total_bytes = sum((OUTPUT_DIR / name).stat().st_size for name in names)

    print(
        f"{len(names)} spectra in {OUTPUT_DIR.relative_to(PROJECT_ROOT)} "
        f"({total_bytes / 1e6:.1f} MB total)"
    )
    print(
        f"Downloaded {downloaded} ({downloaded_bytes / 1e6:.1f} MB), "
        f"already present {skipped}"
    )


if __name__ == "__main__":
    main()
