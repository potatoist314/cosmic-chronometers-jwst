# Galaxy images and the photometric aperture in the production fit notebooks

Card t_c268de16. Written 2026-09-09 on branch `absorption-mask`.

Every production fit now shows the galaxy it fits. The notebook draws an HST
ACS F814W cutout of the target and marks the aperture that the photometry came
from. The 187 fits that already ran carry the same picture, and none of them
was refitted.

## What the picture is for

The joint fit compares two measurements of one galaxy. The LEGA-C spectrum
comes through a 1-arcsecond slit. The COSMOS2015 photometry comes from a
circular aperture of 3 arcseconds in diameter, which the pipeline then rescales
to a total flux. Neither aperture is drawn in any other figure, so the sizes
stayed abstract.

At z = 0.6 to 1.0 one arcsecond is about 7 to 8 kiloparsecs. A quiescent galaxy
of that mass has a half-light radius of a few kiloparsecs. The 3-arcsecond
circle therefore holds most of the light of the target, and it often holds a
neighbour as well. The image makes both facts visible in one look. It shows
whether the target is a clean isolated ellipsoid, whether a companion sits
inside the aperture, and whether the galaxy is large enough for the slit to
have missed a colour gradient.

That matters for the calibration polynomial. The polynomial absorbs a smooth
mismatch between the slit flux and the aperture flux. A blended neighbour and a
strong colour gradient both produce such a mismatch, and the image is the
fastest way to see which galaxies are at risk.

## The image source

The cutouts come from the COSMOS HST/ACS F814W mosaic of Koekemoer et al.
(2007). IRSA serves it as the `acs_mosaic_2.0` cutout table. The mosaic is
drizzled to 0.03 arcseconds per pixel and is oriented north up with no
rotation, so a cutout needs no reprojection before it is drawn.

`scripts/download_hst_cutouts.py` reads the production manifest
(`results/dr2-quiescent-new-defaults/targets.json`), takes each target's
catalogue position from `data/raw/legac_dr2/legaCdr2.fits.gz`, and asks IRSA
for a 10-arcsecond box. Each answer is a 335 by 335 pixel image, about 0.9 MB.
The script writes it to `data/raw/hst_f814w/<spect_id>.fits` through a `.part`
temporary, so an interrupted run leaves no truncated file. It skips a target
that already has a file, and it prints one `miss` line for a target that IRSA
cannot serve.

All 187 manifest targets returned a cutout. The run downloaded 184 files and
167.5 MB, after 3 test files from the same script. There were no misses. The
whole COSMOS quiescent sample lies inside the ACS footprint, which is the
expected result for a sample selected from COSMOS2015 photometry.

The directory is 170 MB, so `.gitignore` excludes it and names the script that
restores it. That follows the rule already used for the LEGA-C spectra.

## The notebook cell

`notebooks/ceridwen_integrated_photometry_spectra.ipynb` gained one code cell,
at index 10, immediately after the read marker and before the photometry
section. It runs after the target is selected, so it reads the same `galaxy`
row, `TARGET_ID` and `z_catalog` that the fit uses.

The cell draws the cutout with an asinh stretch over the central 99.5 percent
of the pixel values. It labels both axes in arcseconds of offset from the
catalogue position, with north up and east to the left. It draws an orange
circle of 1.5-arcsecond radius at the catalogue position and names it
"COSMOS2015 3 arcsec aperture". The title carries the spectrum identifier and
the catalogue redshift. When the file is absent the cell prints the expected
path and the command that fetches it, and it draws nothing.

Two details in the cell are worth knowing.

- IRSA aligns each cutout to the mosaic pixel grid. The catalogue position
  therefore lands within one pixel of the centre, not exactly on it. The cell
  converts the catalogue position through the WCS and centres the axes on the
  result, so the circle sits on the galaxy and not on the array centre.
- The axes use `extent` rather than a WCS projection. That is only correct
  because this mosaic has a diagonal CD matrix. A rotated image would need
  `WCSAxes`.

Adding a cell at index 10 moved every later cell by one.
`tests/test_ceridwen_dr2_production.py` pins the cells that mark absorption
features by index, so its two index lists moved from (13, 23, 25, 27) and
(23, 25, 27) to (14, 24, 26, 28) and (24, 26, 28). That file now passes its 20
tests.

## The backfill

Re-running the 187 finished fits would cost about 16 GPU hours and would change
every posterior file for one figure. `scripts/backfill_hst_cutout_cell.py`
inserts the cell instead.

1. It reads the cell source from the production notebook, so there is one copy
   of the code.
2. It starts one kernel and gives it only the four names the cell reads:
   `PROJECT_ROOT`, `TARGET_ID`, `galaxy` and `z_catalog`.
3. It executes the cell for each target and writes the cell and its real output
   into that target's executed notebook, at the same position the cell holds in
   the production notebook.

The script skips a notebook that already carries the cell, so a second run
changes nothing. The inserted cell keeps `execution_count: null`, because it did
not run as part of that notebook's original execution. Nothing else in those
notebooks changed. A cell-by-cell comparison of one backfilled notebook against
its original found every other cell identical.

All 187 notebooks under `results/dr2-quiescent-new-defaults/` were updated and
none failed. Each now holds 32 cells, carries exactly one cutout cell at index
10 with source identical to the production notebook, and embeds 9 figures where
it held 8.

## Verification

Three galaxies were checked: M5_172669 (the highest signal-to-noise target),
M12_101089 and M1_210210.

The circle radius was measured through the WCS, not asserted from the code. The
check takes 16 points on the drawn circle in axis coordinates, converts them
back to pixels through the same scale the cell uses, and converts those pixels
to sky positions. Their separations from the plotted centre are 1.49993 to
1.49998 arcseconds, so the drawn radius is 1.5 arcseconds to within 7e-5
arcseconds. The residual is the tangent-plane scale change 0.4 degrees from the
mosaic reference point. The same check confirms the orientation: the +y axis
lies within 0.01 degrees of north and the +x axis within 0.01 degrees of east.

`_validate_result()` from `scripts/run_ceridwen_vast_multi_gpu.py` passes on all
three result directories. It reads the posterior file, checks the seven physical
parameter groups, checks that the log weights and the evidence are finite,
checks the five derived-output groups and the diagnostics flag, and counts the
embedded figures. The figure count rose from 8 to 9, and the floor is 5.

`tests/test_ceridwen_dr2_production.py` passes, 20 tests.

## Open items

The circle centre uses the LEGA-C catalogue position as written, in ICRS. The
ACS header declares FK5 with equinox J2000. The two frames differ by 28.6
milliarcseconds at this position, which is one mosaic pixel and 2 percent of the
circle radius. Converting the frame was not done, because the offset is far
below the seeing of the ground-based photometry the circle describes. Convert
it if the image is ever used for astrometry.

The production photometry source is `cosmos_total`, not `cosmos_ap3`. The
circle still shows the aperture the fluxes were measured in, because
`cosmos_total` is the same 3-arcsecond aperture photometry rescaled by a
per-object offset. The label says "aperture" and not "photometry" for that
reason.

Fifteen tests in `tests/test_ceridwen_results_board.py` and two in
`tests/test_plot_ceridwen_checkpoint_evolution.py` fail on this branch for an
unrelated reason. They look for `wiki/analyses/*.html` pages that the
notes-based wiki no longer builds. That failure predates this card.

## Reproduce

```
ceridwen/.venv/bin/python scripts/download_hst_cutouts.py
ceridwen/.venv/bin/python scripts/backfill_hst_cutout_cell.py
ceridwen/.venv/bin/python -m pytest tests/test_ceridwen_dr2_production.py -q
```
