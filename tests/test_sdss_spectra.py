import csv
import sys
from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits
from astropy.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sdss_spectra as sdss  # noqa: E402

TARGET = "0309-51994-0145"


@pytest.fixture(scope="module")
def row():
    with (sdss.RAW / "targets_sigma250.csv").open() as table:
        return next(r for r in csv.DictReader(table)
                    if f"{int(r['plate']):04d}-{r['mjd']}-{int(r['fiberID']):04d}" == TARGET)


def processed(row, photometry, directory, monkeypatch):
    monkeypatch.setitem(sdss.PROCESSED, photometry, directory)
    record = sdss.process(row, photometry)
    path = directory / f"{TARGET}.fits"
    return record, fits.getheader(path), Table.read(path, "SPECTRUM"), Table.read(path, "PHOTOMETRY")


def test_model_photometry_and_spectrum_scale(row, tmp_path, monkeypatch):
    record, header, spectrum, photometry = processed(row, "model", tmp_path / "model", monkeypatch)
    _, _, cmodel_spectrum, cmodel_photometry = processed(row, "cmodel", tmp_path / "cmodel", monkeypatch)
    assert record["photometry"] == header["PHOTSRC"] == "sdss_model_wise"

    # ugriz: dereddened AB maggies of modelFlux (nanomaggies), so the colours are the model colours.
    maggies = dict(zip(photometry["BAND"], photometry["FLUX_MAGGIES"]))
    errors = dict(zip(photometry["BAND"], photometry["ERROR_MAGGIES"]))
    for band in "ugriz":
        scale = 10.0 ** (0.4 * (float(row[f"extinction_{band}"]) - sdss.AB_OFFSET[band])) * 1e-9
        assert maggies[band] == pytest.approx(float(row[f"modelFlux_{band}"]) * scale)
        assert errors[band] == pytest.approx(float(row[f"modelFluxIvar_{band}"]) ** -0.5 * scale)
    # r is the model r flux with no scale to the cModel r flux.
    assert maggies["r"] == pytest.approx(float(row["modelFlux_r"]) * 10.0 ** (0.4 * float(row["extinction_r"])) * 1e-9)
    # WISE does not change.
    wise = np.array([band not in "ugriz" for band in photometry["BAND"]])
    assert wise.sum() == 2
    assert np.array_equal(photometry["FLUX_MAGGIES"][wise], cmodel_photometry["FLUX_MAGGIES"][wise])

    # The spectrum scale follows the r flux: synthetic r of the scaled spectrum = model r.
    # FITS columns are big-endian; the filter code needs native floats.
    wave, flux = (np.asarray(spectrum[name], dtype=float) for name in ("WAVE", "FLUX"))
    synthetic_r = sdss.synthetic_maggies(wave, flux * 1e-17, np.asarray(spectrum["VALID"], dtype=bool),
                                         sdss.load_filters(["sdss_r0"]))[0]
    assert synthetic_r == pytest.approx(maggies["r"])
    ratio = float(row["modelFlux_r"]) / float(row["cModelFlux_r"])
    assert header["APERSCL"] == pytest.approx(ratio * fits.getheader(tmp_path / "cmodel" / f"{TARGET}.fits")["APERSCL"])
    good = np.asarray(spectrum["VALID"])
    assert np.asarray(spectrum["FLUX"])[good] == pytest.approx(ratio * np.asarray(cmodel_spectrum["FLUX"])[good])


def test_cmodel_reproduces_the_stored_file(row, tmp_path, monkeypatch):
    record, header, spectrum, photometry = processed(row, "cmodel", tmp_path, monkeypatch)
    stored = sdss.PROJECT_ROOT / "data/processed/sdss_dr17" / f"{TARGET}.fits"
    assert record["photometry"] == header["PHOTSRC"] == "sdss_cmodel_wise"
    for name in ("FLUX_MAGGIES", "ERROR_MAGGIES"):
        assert np.array_equal(photometry[name], Table.read(stored, "PHOTOMETRY")[name])
    for name in ("WAVE", "FLUX", "ERROR", "VALID", "LSF_SIGMA"):
        assert np.array_equal(spectrum[name], Table.read(stored, "SPECTRUM")[name])
    assert header["APERSCL"] == fits.getheader(stored)["APERSCL"]
