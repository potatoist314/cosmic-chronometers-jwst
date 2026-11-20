#!/usr/bin/env python3
"""Download GAMA DR4 AAOmega spectra, gkv FUV-W2 photometry and stellar velocity dispersions
of clean passive galaxies, and count the galaxies that pass the same cuts.

Selection, GAMA DR4 SQL (https://www.gama-survey.org/dr4/query/; column definitions from the
DR4 table pages):
- SpecAllv27 with SURVEY = 'GAMA': AAT/AAOmega, 2 arcsec fibres, 3750-8850 A, R = 1000 at the
  blue end to 1600 at the red end (Hopkins et al. 2013, arXiv:1301.7127, Sect. 2). NQ >= 3
  ("use nQ > 2 for science") and IS_BEST = 1 (spectrum with the best redshift of the object).
- 0.02 <= z < 0.30, the redshift bins of scripts/download_sdss_dr17.py.
- VelocityDispersionsv02 of the same spectrum (Driver et al. 2022, arXiv:2203.08539, Sect. 3.7;
  Dogruel et al. 2024, arXiv:2405.10866): SIG_STARCORR > 100 km/s, the SDSS pilot limit, and the
  recommended cuts of the DMU: SIG_STARCORR < 450 km/s, SIGERR_STAR < 0.2 SIG_STARCORR + 25 km/s,
  |V_STAR| < 1000 km/s.
- GaussFitSimplev05 of the same spectrum (DMU SpecLineSFR): SN > 10, the median S/N per pixel
  in rest 6383-6536 A. Passive, with the emission cuts of the SDSS pilot: [O II] 3726+3729 EW
  (OIIB_EW + OIIR_EW) < 5 A and no 3 sigma [O II], [O III] 5007 (OIIIR) or H-alpha line.
  Emission EWs are positive here ("a small negative value is allowed for emission-only lines",
  DMU SpecLineSFR notes), the opposite of the MPA-JHU sign. Catalogue EW errors as given.
- gkvInputCatv02 row of the CATAID (Bellstedt et al. 2020, arXiv:2005.11215): duplicate = 0,
  mask = 0 (inside the GAMA regions), starmask = 0, uberclass = 1 (galaxy); W1 and W2 at
  S/N > 5, as in the SDSS pilot.
- Per redshift bin (Z_EDGES), the --per-bin spectra with the highest SN.

Filter curves: the KiDS u, g, r, i images are from VST/OmegaCAM (Driver et al. 2022, Sect. 2),
whose curves ceridwen's filter library does not hold. The u_SDSS, g_SDSS, r_SDSS, i_SDSS
filter x CCD curves of the SVO Filter Profile Service (Paranal/OmegaCAM, profile reference
http://www.eso.org/sci/facilities/paranal/instruments/omegacam/tools/) are written as
filters/omegacam_<band>.par (wavelength in A, transmission).

Output in data/raw/gama_dr4/: counts.csv (galaxies passing the cuts per bin), targets.csv
(SQL rows of the selected spectra), spectra/<SPECID>.fit (SpecAllv27 URL) and filters/.

Running this twice downloads nothing the second time.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data/raw/gama_dr4"
QUERY = "https://www.gama-survey.org/dr4/query/index.php"
SVO = "https://svo2.cab.inta-csic.es/theory/fps/getdata.php"
Z_EDGES = (0.02, 0.10, 0.15, 0.20, 0.25, 0.30)
GKV_BANDS = ("FUV", "NUV", "u", "g", "r", "i", "Z", "Y", "J", "H", "K", "W1", "W2")
OMEGACAM = ("u", "g", "r", "i")
COLUMNS = ", ".join([
    "s.SPECID", "s.CATAID", "s.Z", "s.NQ", "s.WMIN", "s.WMAX", "s.URL",
    "v.SIG_STARCORR", "v.SIGERR_STARCORR", "v.SNR_OBSR",
    "g.SN", "g.OIIB_EW", "g.OIIR_EW", "g.OIIIR_EW", "g.OIIIR_EW_ERR", "g.HA_EW", "g.HA_EW_ERR",
    "k.uberID", "k.RAcen", "k.Deccen", "k.EBV",
    *(f"k.flux_{b}t, k.flux_err_{b}t" for b in GKV_BANDS),
])
FROM_WHERE = """
FROM SpecAllv27 s
JOIN VelocityDispersionsv02 v ON v.SPECID = s.SPECID
JOIN GaussFitSimplev05 g ON g.SPECID = s.SPECID
JOIN gkvInputCatv02 k ON k.CATAID = s.CATAID
WHERE s.SURVEY = 'GAMA' AND s.NQ >= 3 AND s.IS_BEST = 1
  AND v.SIG_STARCORR > 100 AND v.SIG_STARCORR < 450
  AND v.SIGERR_STAR < 0.2 * v.SIG_STARCORR + 25 AND v.V_STAR > -1000 AND v.V_STAR < 1000
  AND g.SN > 10
  AND g.OIIB_EW + g.OIIR_EW < 5
  AND ABS(g.OIIB_EW + g.OIIR_EW) < 3 * SQRT(POW(g.OIIB_EW_ERR, 2) + POW(g.OIIR_EW_ERR, 2))
  AND ABS(g.OIIIR_EW) < 3 * g.OIIIR_EW_ERR
  AND ABS(g.HA_EW) < 3 * g.HA_EW_ERR
  AND k.duplicate = 0 AND k.mask = 0 AND k.starmask = 0 AND k.uberclass = 1
  AND k.flux_W1t > 5 * k.flux_err_W1t AND k.flux_W2t > 5 * k.flux_err_W2t
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


def gama_sql(query: str) -> list[dict]:
    """Rows of a DR4 SQL query: the form writes the CSV to tmp/ and links it from the page."""
    form = urllib.parse.urlencode({"query": query, "format": "csv", "nshow": 1, "ndownload": 2000,
                                   "nsov": 1000}).encode()
    page = urllib.request.urlopen(QUERY, data=form, timeout=600).read().decode(errors="replace")
    link = re.search(r"tmp/GAMA_\w+\.csv", page)
    if link is None:
        raise RuntimeError(re.sub(r"<[^>]+>", " ", page)[-2000:])
    text = urllib.request.urlopen(QUERY.rsplit("/", 2)[0] + "/" + link.group(0), timeout=600).read().decode()
    return list(csv.DictReader(io.StringIO(text)))


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--per-bin", type=int, default=2, help="spectra per redshift bin")
    args = parser.parse_args()

    for band in OMEGACAM:
        fetch(f"{SVO}?format=ascii&id=Paranal/OmegaCAM.{band}_SDSS", RAW / "filters" / f"omegacam_{band}.par")
    counts, targets = [], []
    for low, high in zip(Z_EDGES[:-1], Z_EDGES[1:]):
        z_cut = f"AND s.Z >= {low} AND s.Z < {high}"
        counts.append({"z_low": low, "z_high": high,
                       "galaxies": int(gama_sql(f"SELECT COUNT(*) AS n {FROM_WHERE} {z_cut}")[0]["n"])})
        targets += gama_sql(f"SELECT {COLUMNS} {FROM_WHERE} {z_cut} ORDER BY g.SN DESC LIMIT {args.per_bin}")
        print(counts[-1], flush=True)
    write_csv(counts, RAW / "counts.csv")
    write_csv(targets, RAW / "targets.csv")
    for row in targets:
        name = f"{row['SPECID']}.fit"
        fetch(row["URL"].replace("http://", "https://"), RAW / "spectra" / name)
        print(f"{name} CATAID={row['CATAID']} z={float(row['Z']):.3f} SN={float(row['SN']):.1f}", flush=True)


if __name__ == "__main__":
    main()
