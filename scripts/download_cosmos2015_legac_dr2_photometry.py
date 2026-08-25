#!/usr/bin/env python3
"""Download COSMOS2015 photometry matched to the LEGA-C DR2 catalogue."""

from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Column, Table, vstack
from astroquery.vizier import Vizier


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGAC_PATH = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits"
)
COSMOS_CATALOG = "J/ApJS/224/24/cosmos2015"
COSMOS_COLUMNS = [
    "_q",
    "RAJ2000",
    "DEJ2000",
    "Seq",
    "Area",
    "Sat",
    "Cfl",
    "Deep",
    "Flag",
    "E(B-V)",
    "NUVMag",
    "RMag",
    "JMag",
    "Fuap3",
    "e_Fuap3",
    "FBap3",
    "e_FBap3",
    "FVap3",
    "e_FVap3",
    "Frap3",
    "e_Frap3",
    "Fipap3",
    "e_Fipap3",
    "Fzppap3",
    "e_Fzppap3",
    "FYap3",
    "e_FYap3",
    "FJap3",
    "e_FJap3",
    "FHap3",
    "e_FHap3",
    "FKsap3",
    "e_FKsap3",
    "F3.6um",
    "e_F3.6um",
    "F4.5um",
    "e_F4.5um",
]


def download_cosmos2015(legac: Table, batch_size: int = 200) -> Table:
    """Return each LEGA-C row's nearest COSMOS2015 match within one arcsecond."""
    coords = SkyCoord(legac["RAJ2000"], legac["DECJ2000"], unit="deg")
    vizier = Vizier(columns=COSMOS_COLUMNS, row_limit=-1)
    matched_batches = []

    for start in range(0, len(legac), batch_size):
        stop = min(start + batch_size, len(legac))
        result = vizier.query_region(
            coords[start:stop], radius=1 * u.arcsec, catalog=COSMOS_CATALOG
        )
        if not result:
            continue

        candidates = result[0]
        candidates["LEGAC_INDEX"] = (
            np.asarray(candidates["_q"], dtype=int) - 1 + start
        )
        indices = np.asarray(candidates["LEGAC_INDEX"], dtype=int)
        candidate_coords = SkyCoord(
            candidates["RAJ2000"], candidates["DEJ2000"], unit="deg"
        )
        candidates["MATCH_SEP_ARCSEC"] = coords[indices].separation(
            candidate_coords
        ).arcsec

        order = np.lexsort(
            (
                np.asarray(candidates["MATCH_SEP_ARCSEC"]),
                np.asarray(candidates["LEGAC_INDEX"]),
            )
        )
        candidates = candidates[order]
        _, nearest = np.unique(
            np.asarray(candidates["LEGAC_INDEX"]), return_index=True
        )
        matched_batches.append(candidates[np.sort(nearest)])

    photometry = vstack(matched_batches, metadata_conflicts="silent")
    indices = np.asarray(photometry["LEGAC_INDEX"], dtype=int)
    extra_columns = [
        ("OBJECT", np.asarray(legac["OBJECT"][indices])),
        ("SPECT_ID", np.asarray(legac["SPECT_ID"][indices]).astype(str)),
        ("LEGAC_RA_DEG", np.asarray(legac["RAJ2000"][indices])),
        ("LEGAC_DEC_DEG", np.asarray(legac["DECJ2000"][indices])),
    ]
    for position, (name, values) in enumerate(extra_columns, start=1):
        photometry.add_column(Column(values, name=name), index=position)

    photometry.meta["CATALOG"] = f"VizieR {COSMOS_CATALOG}"
    photometry.meta["MATCHRAD"] = "1 arcsec; nearest match retained"
    photometry.meta["FLUXUNIT"] = "COSMOS2015 3 arcsec aperture fluxes in uJy"
    return photometry


def main() -> None:
    if OUTPUT_PATH.exists():
        print(f"Already downloaded: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
        return

    legac = Table.read(LEGAC_PATH)
    photometry = download_cosmos2015(legac)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    photometry.write(OUTPUT_PATH)
    print(f"Wrote {len(photometry)} matches to {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
