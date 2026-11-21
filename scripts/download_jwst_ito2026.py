#!/usr/bin/env python3
"""Download the JWST NIRSpec quiescent-galaxy sample of Ito et al. (2026, arXiv:2506.22642):
combined spectra and photometry of the 136 quiescent galaxies, Zenodo concept DOI
10.5281/zenodo.18508154 (record 19354838).

Files (Zenodo record description):
- Archive_SEPphot.tar.gz: 108 quiescent galaxies of the DJA archival search, DJA photometry.
- DeepDive_SEPphot.tar.gz: 10 DeepDive targets (JWST PID 3567) and 18 archival secondary
  targets, DJA photometry.
The PSF-matched DeepDive set (17 secondary targets) and the contaminant set are not downloaded.

Galactic E(B-V): SFD98 (Schlegel, Finkbeiner & Davis 1998) value at each galaxy position, from
the IRSA DUST service (refPixelValueSFD; https://irsa.ipac.caltech.edu/applications/DUST/).
The DJA photometry is not corrected for it: Valentino et al. (2023, ApJ 947, 20, Sect. 2.3)
apply the Milky Way correction to the eazy-py templates instead.

Output in data/raw/jwst_ito2026/: the archives, their extracted folders and irsa_sfd_ebv.csv.
Running this twice downloads nothing the second time.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import tarfile
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data/raw/jwst_ito2026"
RECORD = "https://zenodo.org/api/records/19354838"
ARCHIVES = ("Archive_SEPphot.tar.gz", "DeepDive_SEPphot.tar.gz")
IRSA_DUST = "https://irsa.ipac.caltech.edu/cgi-bin/DUST/nph-dust?locstr={ra}+{dec}+equ+j2000"


def fetch(url: str, path: Path, md5: str) -> None:
    if path.is_file():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    digest = hashlib.md5()
    with urllib.request.urlopen(url, timeout=600) as response, partial.open("wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)
            digest.update(chunk)
    if digest.hexdigest() != md5:
        raise RuntimeError(f"{path.name}: md5 {digest.hexdigest()} != Zenodo {md5}")
    partial.rename(path)


def main() -> None:
    record = json.load(urllib.request.urlopen(RECORD, timeout=60))
    files = {f["key"]: f for f in record["files"]}
    for name in ARCHIVES:
        path = RAW / name
        fetch(files[name]["links"]["self"], path, files[name]["checksum"].removeprefix("md5:"))
        folder = RAW / name.removesuffix(".tar.gz")
        if not folder.is_dir():
            with tarfile.open(path) as archive:
                archive.extractall(RAW, filter="data")
        print(f"{name}: {path.stat().st_size} bytes", flush=True)

    ebv_path = RAW / "irsa_sfd_ebv.csv"
    if ebv_path.is_file():
        return
    rows = []
    for sample in ("Archive", "DeepDive"):
        with (RAW / f"{sample}_SEPphot" / f"{sample}_QG_master.csv").open() as stream:
            for galaxy in csv.DictReader(stream):
                with urllib.request.urlopen(IRSA_DUST.format(ra=galaxy["ra"], dec=galaxy["dec"]), timeout=120) as reply:
                    xml = reply.read().decode()
                ebv = float(re.search(r"<refPixelValueSFD>\s*([0-9.]+)", xml).group(1))
                rows.append({"sample": sample, "id": galaxy["id"], "ra": galaxy["ra"], "dec": galaxy["dec"], "ebv_sfd": ebv})
    with ebv_path.open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{ebv_path.name}: {len(rows)} positions", flush=True)


if __name__ == "__main__":
    main()
