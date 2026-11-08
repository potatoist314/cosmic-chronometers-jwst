#!/usr/bin/env python3
"""Download MaNGA DR17 cubes, DAP maps, NSA and WISE photometry for red galaxies
whose whole NSA elliptical Petrosian aperture lies inside the IFU.

Selection from drpall-v3_1_1 (the DR17 MaNGA summary file):
- MANGA_TARGET1 bit 10 or 11: Primary or Secondary v1_2_0 sample (DR17 targeting
  bits, https://www.sdss4.org/dr17/manga/manga-target-selection/targeting-catalog/).
- DRP3QUAL == 0: no cube quality flag (sdssMaskbits.par, MANGA_DRP3QUAL).
- All seven NSA elliptical Petrosian bands (FNugriz) with flux > 0 and ivar > 0.
- Rest-frame NUV - r > 5: redder than the green valley 4 < NUV - r < 5 (Salim 2014,
  SerAJ 189, 1).
- The NSA aperture is an ellipse of major-axis radius 2 r_P with the NSA b/a and
  position angle (Wake et al. 2017, AJ 154, 86). r_P is ELPETRO_THETA, which the
  drpall file does not carry; it comes from the DR17 CAS table nsatlas.
- Pre-screen: 2 r_P plus the object-to-IFU-centre offset <= 0.85 of the nominal IFU
  radius (diameters 12, 17, 22, 27 and 32 arcsec for 19 to 127 fibres; Bundy et al.
  2015, ApJ 798, 7, Table 1). The hexagon's inscribed radius is 0.866 of its circumradius. scripts/manga_aperture_spectra.py
  rejects any aperture that contains an uncovered spaxel.
- 2 r_P >= 3 RFWHM (drpall reconstructed r-band PSF FWHM), so that the cube PSF moves
  little light across the aperture edge.
- No spaxel inside the aperture carries the DRP3PIXMASK FORESTAR bit (foreground star;
  sdssMaskbits.par). The star's light is in the cube r-band image that
  scripts/manga_aperture_spectra.py uses to rescale masked pixels. Checked on the
  downloaded cube; rejected cubes stay in cubes/.
- Sorted by NSA elliptical Petrosian stellar mass, most massive first; the first
  --count galaxies are downloaded.

WISE W1 and W2 come from the DR17 CAS table wiseForcedTarget (Lang, Hogg & Schlegel
2016, AJ 151, 36), joined on the nearest SDSS primary object, with its r-band cModel
flux for the aperture correction in scripts/manga_aperture_spectra.py.

Running this twice downloads nothing the second time.
"""

from __future__ import annotations

import argparse
import csv
import io
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from manga_aperture_spectra import aperture_weights

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data/raw/manga_dr17"
SAS = "https://data.sdss.org/sas/dr17/manga/spectro"
DRPALL_URL = f"{SAS}/redux/v3_1_1/drpall-v3_1_1.fits"
DAPTYPE = "HYB10-MILESHC-MASTARSSP"
CAS = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
FORESTAR = 1 << 3
IFU_DIAMETER_ARCSEC = {19: 12.0, 37: 17.0, 61: 22.0, 91: 27.0, 127: 32.0}
NSA_COLUMNS = (
    ["nsaid", "elpetro_theta", "elpetro_ba", "elpetro_phi"]
    + [f"elpetro_{kind}_{band}" for kind in ("flux", "flux_ivar", "nmgy") for band in "fnugriz"]
)
PHOTO_WISE_COLUMNS = (
    "p.objID, p.ra, p.dec, p.type, p.cModelFlux_r, w.has_wise_phot, w.treated_as_pointsource, "
    "w.w1_nanomaggies, w.w1_nanomaggies_ivar, w.w1_profracflux, "
    "w.w2_nanomaggies, w.w2_nanomaggies_ivar, w.w2_profracflux"
)


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
    text = urllib.request.urlopen(url, timeout=300).read().decode()
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def colour_candidates(drpall) -> np.ndarray:
    target = drpall["mngtarg1"]
    main_sample = ((target & (1 << 10)) > 0) | ((target & (1 << 11)) > 0)
    photometry = np.all((drpall["nsa_elpetro_flux"] > 0) & (drpall["nsa_elpetro_flux_ivar"] > 0), axis=1)
    absmag = drpall["nsa_elpetro_absmag"]
    return main_sample & (drpall["drp3qual"] == 0) & photometry & (absmag[:, 1] - absmag[:, 4] > 5.0)


def nsa_rows(nsaids) -> dict[int, dict]:
    rows = {}
    for start in range(0, len(nsaids), 100):
        chunk = ",".join(str(int(i)) for i in nsaids[start:start + 100])
        for row in cas(f"SELECT {', '.join(NSA_COLUMNS)} FROM nsatlas WHERE nsaid IN ({chunk})"):
            rows[int(row["nsaid"])] = row
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--count", type=int, default=8, help="galaxies to download")
    args = parser.parse_args()

    fetch(DRPALL_URL, RAW / "drpall-v3_1_1.fits")
    drpall = fits.getdata(RAW / "drpall-v3_1_1.fits", "MANGA")
    candidates = np.flatnonzero(colour_candidates(drpall))
    nsa = nsa_rows(np.unique(drpall["nsa_nsaid"][candidates]))
    for index in candidates:  # the CAS nsatlas and the drpall NSA columns are one catalogue
        row = nsa[int(drpall["nsa_nsaid"][index])]
        if not np.isclose(float(row["elpetro_flux_r"]), drpall["nsa_elpetro_flux"][index, 4], rtol=1e-5):
            raise ValueError(f"nsatlas and drpall disagree for {drpall['plateifu'][index]}")
    write_csv([nsa[key] for key in sorted(nsa)], RAW / "nsa_candidates.csv")

    aperture = np.array([2.0 * float(nsa[int(drpall["nsa_nsaid"][i])]["elpetro_theta"]) for i in candidates])
    ifu_radius = np.array([IFU_DIAMETER_ARCSEC[int(drpall["ifudesignsize"][i])] / 2 for i in candidates])
    offset = SkyCoord(drpall["objra"][candidates] * u.deg, drpall["objdec"][candidates] * u.deg).separation(
        SkyCoord(drpall["ifura"][candidates] * u.deg, drpall["ifudec"][candidates] * u.deg)).arcsec
    inside = (aperture + offset <= 0.85 * ifu_radius) & (aperture >= 3.0 * drpall["rfwhm"][candidates])
    ranked = candidates[inside][np.argsort(-drpall["nsa_elpetro_mass"][candidates[inside]])]

    targets, photo_wise = [], []
    for index in ranked:
        if len(targets) == args.count:
            break
        plate, ifu = str(drpall["plateifu"][index]).split("-")
        ra, dec = float(drpall["objra"][index]), float(drpall["objdec"][index])
        major = float(aperture[candidates == index][0])
        cube_path = RAW / "cubes" / f"manga-{plate}-{ifu}-LOGCUBE.fits.gz"
        fetch(f"{SAS}/redux/v3_1_1/{plate}/stack/manga-{plate}-{ifu}-LOGCUBE.fits.gz", cube_path)
        nsa_row = nsa[int(drpall["nsa_nsaid"][index])]
        with fits.open(cube_path) as cube:
            weights = aperture_weights(cube["FLUX"].header, cube["FLUX"].data.shape[1:], ra, dec, major,
                                       float(nsa_row["elpetro_ba"]), float(nsa_row["elpetro_phi"]))
            star = np.any(cube["MASK"].data[:, weights > 0] & FORESTAR)
        if star:
            print(f"{plate}-{ifu} rejected: FORESTAR spaxel inside the aperture", flush=True)
            continue
        match = cas(
            f"SELECT {PHOTO_WISE_COLUMNS} FROM PhotoPrimary p JOIN wiseForcedTarget w ON w.objID = p.objID "
            f"WHERE p.objID = dbo.fGetNearestObjIdEq({ra}, {dec}, 0.05)"
        )
        if len(match) != 1:
            raise ValueError(f"no SDSS primary object with WISE photometry within 3 arcsec of {plate}-{ifu}")
        photo_wise.append({"plateifu": f"{plate}-{ifu}", **match[0]})
        targets.append({"plateifu": f"{plate}-{ifu}", "nsaid": int(drpall["nsa_nsaid"][index]),
                        "aperture_major_arcsec": major})
        fetch(f"{SAS}/analysis/v3_1_1/3.1.0/{DAPTYPE}/{plate}/{ifu}/manga-{plate}-{ifu}-MAPS-{DAPTYPE}.fits.gz",
              RAW / "maps" / f"manga-{plate}-{ifu}-MAPS-{DAPTYPE}.fits.gz")
        print(f"{plate}-{ifu} downloaded", flush=True)
    write_csv(targets, RAW / "targets.csv")
    write_csv(photo_wise, RAW / "sdss_wise.csv")


if __name__ == "__main__":
    main()
