#!/usr/bin/env python3
"""Download SDSS DR17 single-fibre spectra, ugriz cModel and WISE forced photometry of
clean passive galaxies, and count the galaxies that pass the same cuts.

Selection, DR17 CAS (column definitions from the CAS table DBColumns):
- SpecObj (science-primary spectra) with SURVEY = 'sdss': the SDSS-I/II spectrographs,
  3 arcsec fibres, 3800-9200 A, R = 1500 at 3800 A to 2500 at 9000 A
  (https://www.sdss4.org/dr17/spectro/spectro_basics/).
- CLASS = 'GALAXY' and ZWARNING = 0 ("0 means all is well").
- 0.02 <= z < 0.30: [O II] 3727 inside the 3800 A blue limit.
- velDisp > 100 km/s and velDispErr > 0: smaller dispersions are below the resolution
  limit, and a negative error marks a fit at the edge of the template grid
  (https://www.sdss4.org/dr17/algorithms/redshifts/).
- MPA-JHU galSpecInfo RELIABLE = 1 (https://www.sdss4.org/dr17/spectro/galaxy_mpajhu/).
- Passive, with the emission cuts of the LEGA-C production selection
  (scripts/run_ceridwen_vast_multi_gpu.py): [O II] 3726+3729 EW > -5 A and no 3 sigma
  [O II] or [O III] 5007 line; MPA-JHU galSpecLine EWs, emission negative. No 3 sigma
  H-alpha line replaces the LEGA-C rest-frame NUV-r, r-J colour cut, which the CAS
  does not carry for every galaxy.
- PhotoObj CLEAN = 1 for the bestObjID photometric match; wiseForcedTarget
  HAS_WISE_PHOT = 1 with W1 and W2 detected at S/N > 5.
- Per redshift bin (Z_EDGES), the --per-bin spectra with the highest median r-band
  S/N per pixel (snMedian_r).
- --sigma250, a second selection with the same cuts and velDisp >= 250 km/s (the trial
  widths of the velocity-dispersion fit are 100 to 850 km/s, same page), in bins of 0.05
  from z = 0.05, without the spectra of targets.csv.

Output in data/raw/sdss_dr17/: counts.csv (galaxies passing the cuts per bin),
targets.csv (CAS rows of the selected spectra) and spectra/spec-PLATE-MJD-FIBER.fits
(spec-lite files, https://dr17.sdss.org/sas/dr17/sdss/spectro/redux/<run2d>/spectra/lite/).
--sigma250 writes counts_sigma250.csv and targets_sigma250.csv.

Running this twice downloads nothing the second time.
"""

from __future__ import annotations

import argparse
import csv
import io
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data/raw/sdss_dr17"
SAS = "https://dr17.sdss.org/sas/dr17/sdss/spectro/redux"
CAS = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
Z_EDGES = (0.02, 0.10, 0.15, 0.20, 0.25, 0.30)
COLUMNS = ", ".join([
    "s.specObjID", "s.bestObjID", "s.plate", "s.mjd", "s.fiberID", "s.run2d", "s.ra", "s.dec",
    "s.z", "s.zErr", "s.velDisp", "s.velDispErr", "s.snMedian_r",
    *(f"p.cModelFlux_{b}, p.cModelFluxIvar_{b}, p.extinction_{b}" for b in "ugriz"),
    "w.w1_nanomaggies", "w.w1_nanomaggies_ivar", "w.w2_nanomaggies", "w.w2_nanomaggies_ivar",
    "w.treated_as_pointsource",
    "l.oii_3726_eqw", "l.oii_3729_eqw", "l.oiii_5007_eqw", "l.oiii_5007_eqw_err",
    "l.h_alpha_eqw", "l.h_alpha_eqw_err",
])
FROM_WHERE = """
FROM SpecObj s
JOIN PhotoObj p ON p.objID = s.bestObjID
JOIN wiseForcedTarget w ON w.objID = s.bestObjID
JOIN galSpecInfo g ON g.specObjID = s.specObjID
JOIN galSpecLine l ON l.specObjID = s.specObjID
WHERE s.survey = 'sdss' AND s.class = 'GALAXY' AND s.zWarning = 0
  AND s.velDisp > 100 AND s.velDispErr > 0
  AND g.reliable = 1 AND p.clean = 1 AND w.has_wise_phot = 1
  AND w.w1_nanomaggies * SQRT(w.w1_nanomaggies_ivar) > 5
  AND w.w2_nanomaggies * SQRT(w.w2_nanomaggies_ivar) > 5
  AND l.oii_3726_eqw + l.oii_3729_eqw > -5
  AND ABS(l.oii_3726_eqw + l.oii_3729_eqw) < 3 * SQRT(SQUARE(l.oii_3726_eqw_err) + SQUARE(l.oii_3729_eqw_err))
  AND ABS(l.oiii_5007_eqw) < 3 * l.oiii_5007_eqw_err
  AND ABS(l.h_alpha_eqw) < 3 * l.h_alpha_eqw_err
"""


def fetch(url: str, path: Path) -> None:
    if path.is_file():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    with urllib.request.urlopen(url, timeout=600) as response, partial.open("wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)
    partial.rename(path)


def cas(query: str) -> list[dict]:
    url = CAS + "?" + urllib.parse.urlencode({"cmd": query, "format": "csv"})
    text = urllib.request.urlopen(url, timeout=600).read().decode()
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--per-bin", type=int, default=2, help="spectra per redshift bin")
    parser.add_argument("--sigma250", action="store_true",
                        help="velDisp >= 250 km/s, z from 0.05, without the spectra of targets.csv")
    args = parser.parse_args()

    edges, cut, suffix = Z_EDGES, "", ""
    if args.sigma250:
        with (RAW / "targets.csv").open() as first:
            selected = ", ".join(row["specObjID"] for row in csv.DictReader(first))
        edges, suffix = (0.05, *Z_EDGES[1:]), "_sigma250"
        cut = f"AND s.velDisp >= 250 AND s.specObjID NOT IN ({selected}) "
    counts, targets = [], []
    for low, high in zip(edges[:-1], edges[1:]):
        z_cut = f"{cut}AND s.z >= {low} AND s.z < {high}"
        counts.append({"z_low": low, "z_high": high,
                       "galaxies": int(cas(f"SELECT COUNT(*) AS n {FROM_WHERE} {z_cut}")[0]["n"])})
        targets += cas(f"SELECT TOP {args.per_bin} {COLUMNS} {FROM_WHERE} {z_cut} ORDER BY s.snMedian_r DESC")
        print(counts[-1], flush=True)
    write_csv(counts, RAW / f"counts{suffix}.csv")
    write_csv(targets, RAW / f"targets{suffix}.csv")
    for row in targets:
        plate, mjd, fiber = int(row["plate"]), int(row["mjd"]), int(row["fiberID"])
        name = f"spec-{plate:04d}-{mjd}-{fiber:04d}.fits"
        fetch(f"{SAS}/{row['run2d']}/spectra/lite/{plate:04d}/{name}", RAW / "spectra" / name)
        print(f"{name} z={float(row['z']):.3f} S/N_r={float(row['snMedian_r']):.1f}", flush=True)


if __name__ == "__main__":
    main()
