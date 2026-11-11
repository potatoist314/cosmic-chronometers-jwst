#!/usr/bin/env python3
"""Download the LEGA-C DR3 catalogue and 1D spectra from the ESO archive.

DR3 is the ESO Phase 3 release of collection LEGA-C with release description
185 (van der Wel et al. 2021, ApJS 256, 44): one catalogue, ``legac_DR3.fits``,
and 4081 1D spectra. The ESO ObsCore TAP service lists each file; the ESO data
portal serves it by its archive identifier.

Running this twice downloads nothing the second time, so it is safe to resume
after an interruption.
"""

from __future__ import annotations

import csv
import io
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from astropy.io import fits
from astropy.table import Table


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data/raw/legac_dr3"
SPECTRA_DIR = OUTPUT_DIR / "sp"
CATALOGUE_NAME = "legac_DR3.fits"
RELEASE_DESCRIPTION_URL = "https://www.eso.org/rm/api/v1/public/releaseDescriptions/185"
RELEASE_DESCRIPTION_NAME = "ESO_DR3_release_description.pdf"

TAP_URL = "https://archive.eso.org/tap_obs/sync"
FILE_URL = "https://dataportal.eso.org/dataPortal/file/"
QUERY = (
    "SELECT dp_id, obs_creator_did, dataproduct_type FROM ivoa.ObsCore "
    "WHERE obs_collection = 'LEGA-C' "
    f"AND release_description = '{RELEASE_DESCRIPTION_URL}'"
)

EXPECTED_SPECTRA = 4081
EXPECTED_COLUMNS = ["WAVE", "FLUX", "ERR", "QUAL"]
TIMEOUT_SECONDS = 120
MAX_ATTEMPTS = 3
RETRY_PAUSE_SECONDS = 5.0
WORKERS = 6


def archive_files() -> tuple[dict, dict]:
    """Return ({catalogue name: dp_id}, {spectrum name: dp_id}) of the release."""
    payload = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": QUERY}
    ).encode()
    with urllib.request.urlopen(TAP_URL, data=payload, timeout=TIMEOUT_SECONDS) as response:
        rows = list(csv.DictReader(io.StringIO(response.read().decode())))
    catalogues, spectra = {}, {}
    for row in rows:
        name = row["obs_creator_did"].removeprefix("ivo://eso.org/origfile?")
        (spectra if row["dataproduct_type"] == "spectrum" else catalogues)[name] = row["dp_id"]
    if list(catalogues) != [CATALOGUE_NAME]:
        raise ValueError(f"Expected one catalogue {CATALOGUE_NAME}, found {sorted(catalogues)}")
    if len(spectra) != EXPECTED_SPECTRA:
        raise ValueError(f"Expected {EXPECTED_SPECTRA} spectra, found {len(spectra)}")
    return catalogues, spectra


def check_spectrum(path: Path) -> None:
    """Raise unless the file is a readable Phase 3 single-row spectrum table."""
    with fits.open(path) as hdulist:
        table = hdulist[1]
        if table.columns.names != EXPECTED_COLUMNS:
            raise ValueError(f"{path.name} has columns {table.columns.names}, expected {EXPECTED_COLUMNS}")
        if len(table.data) != 1:
            raise ValueError(f"{path.name} has {len(table.data)} table rows, expected 1")


def check_catalogue(path: Path) -> None:
    if len(Table.read(path, hdu=1)) != EXPECTED_SPECTRA:
        raise ValueError(f"{path.name} does not have {EXPECTED_SPECTRA} rows")


def download(url: str, destination: Path, check) -> int:
    """Fetch one file through a validated ``.part`` temporary; return its size in bytes."""
    if destination.exists() and destination.stat().st_size > 0:
        return 0
    partial = destination.with_suffix(destination.suffix + ".part")
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
                payload = response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_PAUSE_SECONDS)
            continue
        partial.write_bytes(payload)
        if check is not None:
            check(partial)
        os.replace(partial, destination)
        return len(payload)
    partial.unlink(missing_ok=True)
    raise RuntimeError(f"Failed to download {url} after {MAX_ATTEMPTS} attempts: {last_error}")


def main() -> None:
    catalogues, spectra = archive_files()
    SPECTRA_DIR.mkdir(parents=True, exist_ok=True)

    download(RELEASE_DESCRIPTION_URL, OUTPUT_DIR / RELEASE_DESCRIPTION_NAME, None)
    catalogue_path = OUTPUT_DIR / CATALOGUE_NAME
    download(FILE_URL + catalogues[CATALOGUE_NAME], catalogue_path, check_catalogue)

    listed = sorted(str(name).strip() for name in Table.read(catalogue_path, hdu=1)["Filename"])
    if listed != sorted(spectra):
        raise ValueError("Catalogue Filename column and archive spectra differ")

    with ThreadPoolExecutor(WORKERS) as pool:
        sizes = list(pool.map(
            lambda name: download(FILE_URL + spectra[name], SPECTRA_DIR / name, check_spectrum),
            sorted(spectra),
        ))
    present = sorted(path.name for path in SPECTRA_DIR.glob("legac_M*_v3.0.fits"))
    if present != sorted(spectra):
        raise ValueError(f"{SPECTRA_DIR.relative_to(PROJECT_ROOT)} holds {len(present)} spectra, expected {len(spectra)}")
    total = sum((SPECTRA_DIR / name).stat().st_size for name in present)
    print(f"{len(present)} spectra in {SPECTRA_DIR.relative_to(PROJECT_ROOT)} ({total / 1e6:.1f} MB total)")
    print(f"Downloaded {sum(size > 0 for size in sizes)} ({sum(sizes) / 1e6:.1f} MB), already present {sum(size == 0 for size in sizes)}")


if __name__ == "__main__":
    main()
