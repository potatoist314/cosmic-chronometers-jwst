# Three wiki notes cut back to figures

Job t_44a42fb9 · 2026-09-06 · branch `absorption-mask` · screenshots in `reports/astro-notes-rewrite-2026-09-06/`

## What happened

The three notes explained the idea back to you. They now show the work instead. Each one opens with the title, then a short block of the settings the fits actually ran with, then the figures. Under each figure is one short clause. Everything that was argument, table, run log or reproduction step is either behind a collapsed "Details" block at the foot of the page, or in the report that already held it.

The originals are kept, unchanged, in `wiki/_old/`.

## The three pages

| Page | What is on it |
| --- | --- |
| `wiki/notes/calibration-polynomial-dr2.md` | Model settings, the explainer diagram, the calibration curves, the before/after parameters, a four-sentence paragraph on what the polynomial absorbs, the equation once, then Details |
| `wiki/notes/per-galaxy-fit-diagnostics.md` | Model settings, then the photometric χ², spectral χ² and t10/t20/t50 figures of M1_210210, then Details |
| `wiki/notes/per-galaxy-diagnostics-gallery.md` | Model settings once, then 187 sections, each labelled with its target, redshift and S/N, each carrying the same three figures in the same order |

The tilted mock and the six per-galaxy χ² figures are gone from the calibration page. The two sample-wide summary figures are gone from the diagnostics page. All of them are deleted from the pages, not moved into Details. The figure files stay where they were, and the numbers they carried are still in `reports/astro-calibration-2026-09-06.md` and `reports/astro-chisq-sf-plots-2026-09-06.md`.

The gallery is written by `scripts/per_galaxy_diagnostics.py gallery`, so its shape had to go into the generator, not only into the file. That is the one code change: a new `model_settings_block()` reads the settings out of the result files, and `write_gallery_note()` emits the settings block, the per-galaxy labels and the captions.

## Where the Model settings block comes from

Nothing in it is typed by hand. `model_settings_block(target_dir)` opens that fit's own files:

| Field | Source |
| --- | --- |
| Free parameters, priors, redshift, calibration order, prior width, photometry anchor, band count | `ceridwen_result.h5`, `model` attributes and the `priors` and `theta_init` groups |
| Star-formation history bin edges | `ceridwen_derived_outputs.h5`, `sfh/lookback_time_gyr` |
| Library, isochrones, IMF, grid axes, dust law, birth-cloud and dust-emission switches, nebular emission, IGM | `diagnostics/model_parameters.txt`, which the diagnostics run generates from the live model objects |

The calibration note covers three arms, so its block carries an extra `Arms` row and states the production default. Its numbers were read the same way, from `results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/` and that run's `execution.log`.

## The 50-word budget

Visible prose is the paragraph plus the captions. The Model settings block is a list, so it does not count.

| Page | Paragraph and headings | Captions | Total |
| --- | --- | --- | --- |
| calibration-polynomial-dr2 | 30 | 18 | 48 |
| per-galaxy-fit-diagnostics | 4 | 22 | 26 |

The gallery is the exception, and it cannot meet the same figure. It carries 561 captions, so any per-caption length sums past 50 words. Each caption is one sentence of 25 words or fewer. They cannot be cut to a bare clause either: `html_text_lint.py` treats every gallery figure as scientific, because the run directory name contains the word "spectrum", and it then requires the caption to state the quantity, the sample, the uncertainty, the comparison and the caveat. The figures on the other two pages are not flagged that way, so their captions are clauses.

## A gate landed while this ran

Another card (t_55e4f1c9) was rewriting `wiki/build.py` at the same time. Its build refuses to publish a note whose visible body runs past 50 words, and refuses any figure caption longer than one sentence. The notes were written to pass it. `wiki/build.py` is left uncommitted and untouched, because that card owns it. The three notes need its collapsed-block support to render, so it must land before the pages are correct on the server.

## Checks

| Check | Verdict |
| --- | --- |
| `python3 wiki/build.py` | built 28 notes, no faults |
| `python3 wiki/tests/run_tests.py` | all tests passed, 39 checks |
| `html_text_lint.py` on the three pages | 0 issues each |
| Same lint on the front, by-date and by-topic pages | 0 issues |
| Screenshots at 1400 px wide from `http://127.0.0.1:8765/wiki/` | three PNGs beside this report |

## Open item

The gallery keeps a per-galaxy table's worth of numbers only inside its captions. The full table stays at `results/per-galaxy-diagnostics.csv`.
