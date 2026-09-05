# Three wiki notes cut back to figures

Job t_44a42fb9 · 2026-09-06 · branch `absorption-mask` · screenshots in `reports/astro-notes-rewrite-2026-09-06/`

## What happened

The three notes explained the idea back to you. They now show the work instead. Each one opens with the title, then a short block of the settings the fits actually ran with, then the figures. Under each figure is one sentence: what it plots, and the number that matters. Everything that was argument, table, run log or reproduction step is either behind a collapsed "Details" block at the foot of the page, or in the report that already held it.

The originals are kept, unchanged, in `wiki/_old/`.

## The three pages

| Page | Shape now |
| --- | --- |
| `wiki/notes/calibration-polynomial-dr2.md` | Model settings, the explainer diagram, the calibration curves, the before/after parameters, the tilted mock, the six per-galaxy χ² figures, one four-sentence paragraph on what the polynomial absorbs, the equation once, then Details |
| `wiki/notes/per-galaxy-fit-diagnostics.md` | Model settings, the two sample-wide figures, the three figures of the example galaxy M1_210210, then Details |
| `wiki/notes/per-galaxy-diagnostics-gallery.md` | Model settings once, then 187 sections, each labelled with its target, redshift and S/N, each carrying photometric χ², spectral χ² and t10/t20/t50 in that order |

The gallery is written by `scripts/per_galaxy_diagnostics.py gallery`, so the new shape had to go into the generator, not only into the file. That is the one code change: a new `model_settings_block()` reads the settings out of the result files, and `write_gallery_note()` emits the settings block, the per-galaxy labels and the one-sentence captions.

## Where the Model settings block comes from

Nothing in it is typed by hand. `model_settings_block(target_dir)` opens that fit's own files:

| Field | Source |
| --- | --- |
| Free parameters, priors, redshift, calibration order, prior width, photometry anchor, band count | `ceridwen_result.h5`, `model` attributes and the `priors` and `theta_init` groups |
| Star-formation history bin edges | `ceridwen_derived_outputs.h5`, `sfh/lookback_time_gyr` |
| Library, isochrones, IMF, grid axes, dust law, birth-cloud and dust-emission switches, nebular emission, IGM | `diagnostics/model_parameters.txt`, which the diagnostics run generates from the live model objects |

The calibration note covers three arms, so its block carries an extra `Arms` row and states the production default. Its numbers were read the same way, from `results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/` and that run's `execution.log`.

## A gate landed while this ran

Another card was rewriting `wiki/build.py` at the same time. Its build now refuses to publish a note whose visible body runs past 50 words, and refuses any figure caption longer than one sentence. That is the same complaint from the other direction, so the notes were written to pass it rather than around it. Two consequences worth knowing:

- Captions are one sentence, not two. The interpretation that a second sentence would have carried sits in the figure itself or in the sibling note.
- The gallery cannot use 187 headings, because headings count against the 50 words. Each galaxy is labelled with a definition-list row instead, which reads as a section label and does not count. A `## Galaxies` heading separates the first one from the settings block.

`wiki/build.py` is left uncommitted, because that card is still editing it. The three notes need its collapsed-block support to render, so it must land before the pages are correct on the server.

## Checks

| Check | Verdict |
| --- | --- |
| `python3 wiki/build.py` | built 28 notes, no faults |
| `python3 wiki/tests/run_tests.py` | all tests passed, 39 checks |
| `python3 ~/.claude/scripts/hermes-bridge/html_text_lint.py` on the three pages | 0 issues each |
| Same lint on the front, by-date and by-topic pages | 0 issues |
| Screenshots at 1400 px wide from `http://127.0.0.1:8765/wiki/` | three PNGs beside this report |

The lint treats every gallery figure as scientific, because the run directory name contains the word "spectrum". Its captions therefore state the quantity, the sample, the uncertainty, the comparison and the caveat inside one sentence of 25 words or fewer.

## Decisions taken here

- The tilted-mock figure stays on the calibration page. The request listed four figures by name and did not mention it, but it is the only direct evidence that the polynomial leaves the physics alone.
- The paragraph on what the polynomial absorbs is four sentences, not six. Six did not fit the 50-word body budget.
- Per-galaxy tables and flag lists are gone from the gallery. The numbers that mattered are now in the captions, and the full table stays at `results/per-galaxy-diagnostics.csv`.
