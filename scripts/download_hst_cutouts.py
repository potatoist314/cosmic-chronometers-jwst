#!/usr/bin/env python3
"""Download HST ACS F814W cutouts for the production DR2 quiescent targets.

Each fit notebook shows the galaxy it fits. The image comes from the COSMOS
HST/ACS F814W mosaic of Koekemoer et al. (2007), drizzled to 0.03 arcsec per
pixel and oriented north up, which IRSA serves as the ``acs_mosaic_2.0``
cutout table.

IRSA answers a cutout request with an XML summary that names a temporary
workspace file, so each target needs two requests: one for the summary and one
for the FITS file itself. A target outside the ACS footprint returns a summary
with no cutout; the run records it as a miss and continues.

Running this twice downloads nothing the second time, so it is safe to resume
after an interruption.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ElementTree
from pathlib import Path

from astropy.io import fits
from astropy.table import Table

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGAC_PATH = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
DEFAULT_MANIFEST = PROJECT_ROOT / "results/dr2-quiescent-new-defaults/targets.json"
OUTPUT_DIR = PROJECT_ROOT / "data/raw/hst_f814w"

CUTOUT_URL = "https://irsa.ipac.caltech.edu/cgi-bin/Cutouts/nph-cutouts"
CUTOUT_TABLE = "acs_mosaic_2.0"
DEFAULT_SIZE_ARCSEC = 10.0

# One cutout is ~0.9 MB and IRSA builds a temporary workspace for every
# request, so the run is deliberately serial with a short pause between
# targets.
TIMEOUT_SECONDS = 120
MAX_ATTEMPTS = 3
RETRY_PAUSE_SECONDS = 10.0
REQUEST_PAUSE_SECONDS = 1.0


def manifest_spect_ids(path: Path) -> list[str]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return [str(target["spect_id"]) for target in manifest["targets"]]


def catalogue_positions(path: Path) -> dict[str, tuple[float, float]]:
    """Map each LEGA-C SPECT_ID to its catalogue (RA, Dec) in degrees."""
    catalogue = Table.read(path)
    positions = {}
    for spect_id, ra, dec in zip(
        catalogue["SPECT_ID"], catalogue["RAJ2000"], catalogue["DECJ2000"], strict=True
    ):
        name = spect_id.decode() if isinstance(spect_id, bytes) else str(spect_id)
        positions[name.strip()] = (float(ra), float(dec))
    return positions


def _fetch(url: str) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_PAUSE_SECONDS)
    raise RuntimeError(f"Failed after {MAX_ATTEMPTS} attempts: {url}: {last_error}")


def cutout_fits_url(ra: float, dec: float, size_arcsec: float) -> str | None:
    """Ask IRSA for one cutout and return its FITS URL, or None if there is none."""
    query = urllib.parse.urlencode(
        {
            "mission": "COSMOS",
            "locstr": f"{ra:.7f} {dec:.7f}",
            "units": "arcsec",
            "sizeX": f"{size_arcsec:g}",
            "min_size": "1",
            "max_size": "180",
            "ntable_cutouts": "1",
            "cutouttbl1": CUTOUT_TABLE,
            "mode": "PI",
        }
    )
    summary = ElementTree.fromstring(_fetch(f"{CUTOUT_URL}?{query}"))
    if summary.get("status") != "ok":
        raise RuntimeError(f"IRSA returned status {summary.get('status')}")
    element = summary.find("./images/cutouts/fits")
    if element is None or not (element.text or "").strip():
        return None
    return element.text.strip()


def check_cutout(path: Path, ra: float, dec: float) -> None:
    """Raise unless the file is an F814W image whose WCS contains the target."""
    from astropy.wcs import WCS

    with fits.open(path) as hdulist:
        header = hdulist[0].header
        data = hdulist[0].data
        if data is None or data.ndim != 2 or min(data.shape) < 2:
            raise ValueError(f"{path.name} holds no two-dimensional image")
        if header.get("FILTER2", "").strip() != "F814W":
            raise ValueError(f"{path.name} is not F814W: FILTER2={header.get('FILTER2')!r}")
        column, row = WCS(header).all_world2pix(ra, dec, 0)
    if not (0 <= column < data.shape[1] and 0 <= row < data.shape[0]):
        raise ValueError(f"{path.name} does not cover its catalogue position")


def download(spect_id: str, ra: float, dec: float, size_arcsec: float) -> int | None:
    """Fetch one cutout, returning its size in bytes, or None if IRSA has none.

    The file is written to a ``.part`` temporary and moved into place only after
    it has been validated, so an interrupted run never leaves a truncated FITS
    file that a later run would mistake for a complete download.
    """
    url = cutout_fits_url(ra, dec, size_arcsec)
    if url is None:
        return None
    payload = _fetch(url)
    destination = OUTPUT_DIR / f"{spect_id}.fits"
    partial = destination.with_suffix(destination.suffix + ".part")
    partial.write_bytes(payload)
    try:
        check_cutout(partial, ra, dec)
    except (OSError, ValueError):
        partial.unlink(missing_ok=True)
        raise
    os.replace(partial, destination)
    return len(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--size-arcsec", type=float, default=DEFAULT_SIZE_ARCSEC)
    arguments = parser.parse_args()

    spect_ids = manifest_spect_ids(arguments.manifest)
    positions = catalogue_positions(LEGAC_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    downloaded_bytes = 0
    misses: list[str] = []

    for index, spect_id in enumerate(spect_ids, start=1):
        destination = OUTPUT_DIR / f"{spect_id}.fits"
        if destination.exists() and destination.stat().st_size > 0:
            skipped += 1
            continue
        if spect_id not in positions:
            misses.append(f"{spect_id}: not in {LEGAC_PATH.name}")
            continue
        ra, dec = positions[spect_id]
        size = download(spect_id, ra, dec, arguments.size_arcsec)
        if size is None:
            misses.append(f"{spect_id}: no {CUTOUT_TABLE} coverage at {ra:.6f} {dec:.6f}")
            continue
        downloaded += 1
        downloaded_bytes += size
        if downloaded % 25 == 0:
            print(f"  {index}/{len(spect_ids)} checked, {downloaded} downloaded")
        time.sleep(REQUEST_PAUSE_SECONDS)

    present = sum((OUTPUT_DIR / f"{name}.fits").exists() for name in spect_ids)
    print(
        f"{present}/{len(spect_ids)} manifest targets in "
        f"{OUTPUT_DIR.relative_to(PROJECT_ROOT)}"
    )
    print(
        f"Downloaded {downloaded} ({downloaded_bytes / 1e6:.1f} MB), "
        f"already present {skipped}, missing {len(misses)}"
    )
    for miss in misses:
        print(f"  miss {miss}")


if __name__ == "__main__":
    main()
