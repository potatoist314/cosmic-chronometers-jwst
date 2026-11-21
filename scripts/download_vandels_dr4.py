#!/usr/bin/env python3
"""Download VANDELS final-release (DR4) 1D spectra and photometry of passive galaxies,
and count the passive galaxies per redshift bin.

Survey: VLT/VIMOS, MR grism, R ~ 650, 4800-9800 A, 1 arcsec slits (Garilli et al. 2021,
A&A 647, A150, arXiv:2101.07645, Sect. 3).

Catalogue: ESO table safcat.VANDELS_SPECTRO_V4, "measured redshifts for all the 2165
observed galaxies" (ESO TAP, https://archive.eso.org/tap_cat). Photometry in uJy
(Garilli+2021 Table 3, 4); the TAP unit label "mJy" is wrong: F160W = 1.13 at H_AB = 23.77.

Selection
- Passive sample, the target definition of Garilli+2021 Sect. 2.2: H_AB <= 22.5 and
  1.0 <= z_phot <= 2.5. Secure redshift: zflg 2, 3, 4 or 9 (Sect. 4.2, 5; flags 1x are
  broad-line AGN, 2x serendipitous objects). This gives the 275 secure passive redshifts
  of Table 1 (CDFS 122, UDS 153).
- uvj: still inside the Williams et al. (2009) box of Sect. 2.1, U-V > 0.88 (V-J) + 0.49,
  U-V > 1.2, V-J < 1.6, with the release BAGPIPES colours UV_50, VJ_50 (Sect. 7, Table 5).
- Pilot spectra: uvj; HST region (H_FILTER = HST_F160W), whose photometry is the CANDELS
  total flux (McLure et al. 2018 Sect. 4.1; Guo et al. 2013; Galametz et al. 2013), not the
  2 arcsec apertures of the ground regions; z small enough that REST_RANGE, the rest_range
  of the SDSS pilot settings (results/sdss-pilot-2026-11-20/experiment.json), lies inside
  4800-9800 A air. The --n spectra with the highest archive SNR header value.

Galactic E(B-V): SFD98 value at each position from the IRSA DUST service
(https://irsa.ipac.caltech.edu/applications/DUST/, refPixelValueSFD), through curl: the
Python CA bundle does not verify the IRSA certificate chain.

Output in data/raw/vandels_dr4/: catalogue.csv (the full TAP table), counts.csv,
candidates.csv (pilot candidates with SNR), targets.csv (selected rows with E(B-V)) and
spectra/<id>.fits (ESO 1D spectra, by FILENAME_ARCFILE from the ESO data portal).

Running this twice downloads nothing the second time.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from astropy import units as u
from astropy.io import fits
from download_sdss_dr17 import fetch, write_csv
from specutils.utils.wcs_utils import air_to_vac

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data/raw/vandels_dr4"
TAP = "https://archive.eso.org/tap_cat/sync"
PORTAL = "https://dataportal.eso.org/dataportal_new/file"
DUST = "https://irsa.ipac.caltech.edu/cgi-bin/DUST/nph-dust"
Z_EDGES = (0.0, 1.0, 1.1, 1.2, 1.3, 1.45, 2.0, 2.5, 7.0)
SECURE = (2, 3, 4, 9)
VIMOS_AIR = (4800.0, 9800.0)
REST_RANGE = (4074.5, 4666.1)


def number(row: dict, key: str) -> float:
    return float(row[key]) if row[key] else float("nan")


def passive(row: dict) -> bool:
    return (number(row, "H_AB") <= 22.5 and 1.0 <= number(row, "zphot") <= 2.5
            and number(row, "zflg") in SECURE)


def uvj(row: dict) -> bool:
    uv, vj = number(row, "UV_50"), number(row, "VJ_50")
    return uv > 0.88 * vj + 0.49 and uv > 1.2 and vj < 1.6


def ebv_sfd(ra: float, dec: float) -> float:
    query = urllib.parse.urlencode({"locstr": f"{ra} {dec} equ j2000", "regSize": "2.0"})
    text = subprocess.run(["curl", "-sf", f"{DUST}?{query}"], capture_output=True, text=True, check=True).stdout
    return float(re.search(r"<refPixelValueSFD>\s*([0-9.]+)", text).group(1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--n", type=int, default=10, help="pilot spectra")
    args = parser.parse_args()

    catalogue_path = RAW / "catalogue.csv"
    fetch(f"{TAP}?" + urllib.parse.urlencode({"QUERY": "SELECT * FROM safcat.VANDELS_SPECTRO_V4",
                                              "LANG": "ADQL", "FORMAT": "csv"}), catalogue_path)
    rows = list(csv.DictReader(io.StringIO(catalogue_path.read_text())))
    sample = [row for row in rows if passive(row)]
    print(f"secure passive: {len(sample)}, CDFS {sum('CDFS' in r['id'] for r in sample)}, "
          f"UDS {sum('UDS' in r['id'] for r in sample)}", flush=True)

    z_max = float(air_to_vac(VIMOS_AIR[1] * u.AA).to_value(u.AA)) / REST_RANGE[1] - 1.0
    counts = []
    for low, high in zip(Z_EDGES[:-1], Z_EDGES[1:]):
        in_bin = [r for r in sample if low <= number(r, "zspec") < high]
        counts.append({"z_low": low, "z_high": high, "passive": len(in_bin),
                       "uvj": sum(map(uvj, in_bin)),
                       "uvj_hst": sum(uvj(r) and r["H_FILTER"] == "HST_F160W" for r in in_bin)})
        print(counts[-1], flush=True)
    counts.append({"z_low": 0.0, "z_high": 1.45, "passive": sum(number(r, "zspec") < 1.45 for r in sample),
                   "uvj": sum(uvj(r) and number(r, "zspec") < 1.45 for r in sample),
                   "uvj_hst": sum(uvj(r) and r["H_FILTER"] == "HST_F160W" and number(r, "zspec") < 1.45
                                  for r in sample)})
    counts.append({"z_low": 0.0, "z_high": round(z_max, 4),
                   "passive": sum(number(r, "zspec") <= z_max for r in sample),
                   "uvj": sum(uvj(r) and number(r, "zspec") <= z_max for r in sample),
                   "uvj_hst": sum(uvj(r) and r["H_FILTER"] == "HST_F160W" and number(r, "zspec") <= z_max
                                  for r in sample)})
    print(counts[-2], counts[-1], flush=True)
    write_csv(counts, RAW / "counts.csv")

    candidates = [r for r in sample if uvj(r) and r["H_FILTER"] == "HST_F160W" and number(r, "zspec") <= z_max]
    for row in candidates:
        path = RAW / "spectra" / row["FILENAME"]
        fetch(f"{PORTAL}/{row['FILENAME_ARCFILE']}", path)
        row["SNR"] = float(fits.getheader(path, 0)["SNR"])
    candidates.sort(key=lambda r: -r["SNR"])
    write_csv(candidates, RAW / "candidates.csv")
    targets = candidates[: args.n]
    for row in targets:
        row["ebv_sfd"] = ebv_sfd(row["alpha"], row["delta"])
        print(f"{row['id']} z={number(row, 'zspec'):.4f} SNR={row['SNR']:.1f} E(B-V)={row['ebv_sfd']:.4f}", flush=True)
    write_csv(targets, RAW / "targets.csv")


if __name__ == "__main__":
    main()
