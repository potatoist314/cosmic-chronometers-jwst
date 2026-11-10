#!/usr/bin/env python3
"""Download immutable Kroupa abundance-response spectra from a pinned alf revision.

Source: https://github.com/cconroy20/alf (Conroy & van Dokkum 2012;
Conroy et al. 2018). File columns and steps are defined by their headers and
src/setup.f90, src/getmodel.f90. Raw spectra stay unchanged, including the
supersolar files that alf itself replaces with solar responses during setup.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request


REVISION = "cda32111c721efe586945d7dfcb9f605a9f6a105"
API = f"https://api.github.com/repos/cconroy20/alf/git/trees/{REVISION}?recursive=1"
RAW = f"https://raw.githubusercontent.com/cconroy20/alf/{REVISION}/"
DESTINATION = Path(__file__).resolve().parents[1] / "data/raw/alf" / REVISION


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def download(entry: dict, destination: Path) -> str:
    path = destination / Path(entry["path"]).name
    if path.exists():
        if blob_sha(path.read_bytes()) != entry["sha"]:
            raise ValueError(f"Existing raw file differs from pinned source: {path}")
        return f"verified {path.name}"
    data = urllib.request.urlopen(RAW + entry["path"], timeout=120).read()
    if blob_sha(data) != entry["sha"]:
        raise ValueError(f"Download differs from pinned source: {entry['path']}")
    with path.open("xb") as output:
        output.write(data)
    return f"downloaded {path.name}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--output", type=Path, default=DESTINATION)
    args = parser.parse_args()
    tree = json.load(urllib.request.urlopen(API, timeout=120))["tree"]
    entries = [entry for entry in tree
               if entry["path"].startswith("infiles/atlas_ssp_")
               and entry["path"].endswith(".abund.krpa.s100")]
    args.output.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(lambda entry: download(entry, args.output), entries):
            print(result, flush=True)


if __name__ == "__main__":
    main()
