#!/usr/bin/env python3
"""Download multi-aperture COSMOS2015 and total UltraVISTA photometry for LEGA-C DR2.

Two raw tables, one row per LEGA-C DR2 spectrum (``LEGAC_INDEX`` is the row
number in ``legaCdr2.fits.gz``), nearest match within one arcsecond:

``data/raw/cosmos2015/cosmos2015_legac_dr2_apertures_1arcsec.fits``
    Laigle et al. (2016): 2" and 3" aperture fluxes of the ten optical/NIR
    bands and of the five intermediate bands inside the LEGA-C wavelength
    range, the per-object aperture-to-total magnitude offset ``Offset``,
    ``E(B-V)``, the Ks AUTO magnitude and the total IRAC fluxes.
``data/raw/ultravista/ultravista_legac_dr2_1arcsec.fits``
    Muzzin et al. (2013): the total fluxes (zero point 25 AB) of the SED that
    LEGA-C DR2 used to flux-calibrate every spectrum.
"""

import time
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Column, Table, vstack
from astroquery.vizier import Vizier

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGAC_PATH = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
COSMOS_BANDS = ["Fu", "FB", "FV", "Fr", "Fip", "Fzpp", "FY", "FJ", "FH", "FKs",
                # intermediate bands inside the LEGA-C wavelength range
                "FIA679", "FIB709", "FIA738", "FIA767", "FIB827"]
CATALOGUES = {
    "J/ApJS/224/24/cosmos2015": (
        PROJECT_ROOT / "data/raw/cosmos2015/cosmos2015_legac_dr2_apertures_1arcsec.fits",
        ["_q", "RAJ2000", "DEJ2000", "Seq", "Offset", "E(B-V)", "Ksmag", "e_Ksmag",
         "Area", "Sat", "Cfl", "Deep", "Flag",
         *[f"{p}{b}ap{a}" for b in COSMOS_BANDS for a in (2, 3) for p in ("", "e_")],
         "F3.6um", "e_F3.6um", "F4.5um", "e_F4.5um"],
    ),
    "J/ApJS/206/8/catalog": (
        PROJECT_ROOT / "data/raw/ultravista/ultravista_legac_dr2_1arcsec.fits",
        ["_q", "RAJ2000", "DEJ2000", "Seq", "FKstot", "e_FKstot", "FKs", "e_FKs",
         "FH", "e_FH", "FJ", "e_FJ", "FY", "e_FY", "Fch2", "e_Fch2", "Fch1", "e_Fch1",
         "Fzp", "e_Fzp", "Fip", "e_Fip", "Frp", "e_Frp", "FV", "e_FV", "FB", "e_FB",
         "Fu", "e_Fu", "FIA679", "e_FIA679", "FIB709", "e_FIB709", "FIA738", "e_FIA738",
         "FIA767", "e_FIA767", "FIB827", "e_FIB827",
         "Kflag", "S/G", "KKron", "apcor", "Star", "Cont", "USE"],
    ),
}


def nearest_matches(legac: Table, catalog: str, columns: list[str],
                    batch_size: int = 100) -> Table:
    coords = SkyCoord(legac["RAJ2000"], legac["DECJ2000"], unit="deg")
    vizier = Vizier(columns=columns, row_limit=-1)
    batches = []
    for start in range(0, len(legac), batch_size):
        stop = min(start + batch_size, len(legac))
        for attempt in range(5):
            try:
                result = vizier.query_region(coords[start:stop], radius=1 * u.arcsec,
                                             catalog=catalog)
                break
            except Exception as error:  # noqa: BLE001 - VizieR drops connections
                if attempt == 4:
                    raise
                print(f"retry {attempt + 1} after {type(error).__name__}", flush=True)
                time.sleep(10 * (attempt + 1))
        if not result:
            continue
        candidates = result[0]
        index = np.asarray(candidates["_q"], dtype=int) - 1 + start
        separation = coords[index].separation(
            SkyCoord(candidates["RAJ2000"], candidates["DEJ2000"], unit="deg")).arcsec
        candidates["LEGAC_INDEX"] = Column(index)
        candidates["MATCH_SEP_ARCSEC"] = Column(separation)
        batches.append(candidates)
    matched = vstack(batches, metadata_conflicts="silent")
    matched.sort(["LEGAC_INDEX", "MATCH_SEP_ARCSEC"])
    _, first = np.unique(np.asarray(matched["LEGAC_INDEX"]), return_index=True)
    matched = matched[first]
    matched.remove_column("_q")
    for name in ("OBJECT", "SPECT_ID"):
        matched[name] = legac[name][np.asarray(matched["LEGAC_INDEX"])]
    for name in matched.colnames:
        # VizieR serves the Muzzin fluxes as 0.3631 uJy units (zero point 25 AB),
        # a scale FITS cannot store; write every flux in uJy.  FKstot and its
        # error arrive with no unit but share that zero point (catalogue note 1).
        unit = matched[name].unit
        if name in ("FKstot", "e_FKstot"):
            matched[name] = Column(np.asarray(matched[name], dtype=float) * 0.3631, unit=u.uJy)
        elif unit is not None and unit.is_equivalent(u.uJy) and unit != u.uJy:
            matched[name] = Column(matched[name].to(u.uJy))
    return matched


def main() -> None:
    legac = Table.read(LEGAC_PATH)
    for catalog, (path, columns) in CATALOGUES.items():
        matched = nearest_matches(legac, catalog, columns)
        path.parent.mkdir(parents=True, exist_ok=True)
        matched.write(path, overwrite=True)
        print(f"{catalog}: {len(matched)} of {len(legac)} spectra matched -> {path}")


if __name__ == "__main__":
    main()
