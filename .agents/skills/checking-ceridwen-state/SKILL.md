---
name: checking-ceridwen-state
description: Use before you discuss, propose or run a Ceridwen experiment or model feature. One command prints each fit setting, prior and model option with its state, the commits that built it, the records that tested it with their findings, the open questions, the work that is not merged, and the experiments that are planned, running or recent.
---

# Check the Ceridwen state

Liu Hao, 2026-09-30: "marginalisation is already implemented to some extent. you
should be aware of that. hm. there should be a skill that tracks the running
progress/state of the experiment and settings".

Liu Hao, 2026-09-30: "like track a record of what work has been done and what
implementations have been tested (E.g. the worker should know emission line
marginalisation has been somehwat implemented, where it is, progresse etc)".

Before you discuss, propose or run a Ceridwen experiment or a model feature, run this
command from the project root. It rents nothing.

```bash
python3 scripts/ceridwen_state.py                                # all entries
python3 scripts/ceridwen_state.py emission_line_marginalisation  # the entries with this text
```

The command reads the committed HEAD, the pinned submodules, the research records,
`results/` and `bd`. Do not copy its output into a file. Run it again.

## One entry

This is from the run of 2026-09-30. Long lines are cut at `...`.

```
emission_line_marginalisation = False  [off; built 2026-09-22; tested]
    what: True: FSPS lines get free fluxes >= 0 in the calibration solve, shared with the photometry; z fixed; lines leave the mask
    used: notebook cells 6, 10
    built: c0adc0a 2026-09-22 Emission-line marginalisation option (default off): FSPS lines as flat-prior columns of the calibration solve
    code: ceridwen 6fc7539 2026-09-22 Emission lines as free-flux columns of the calibration solve (ceridwen/likelihood/__init__.py, ...)
    code: ceridwen 1fae781 2026-09-23 Emission lines: exclude FSPS's phantom [O II] 3867 (zero Cloudy flux; no NIST line) (ceridwen/likelihood/emission_lines.py)
    changed: 99e3091 2026-09-23 Emission lines: [O III] and [Ne III] doublets tied; z fixed and fluxes shared with photometry when on (Liu Hao, 2026-09-23)
    tested: e-emission-line-marginalisation [results-ready 2026-09-23] M1_210210, on minus off: mass-weighted age -0.408 Gyr; ...
    ran: results/m1-210210-nebular-2026-09-30 neb_eline=true
    open: q-emission-lines Should the fits model, mask or ignore emission lines, and on what physical grounds?
```

| Part | Source |
| --- | --- |
| Value, `what` | `SETTINGS` or `PRIORS` in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, and the comment there |
| `off`, `production default` | The value. `False` and `None` are `off`. |
| `built`, `changed` | The notebook commits that added the entry or changed its value or comment |
| `code` | The Ceridwen commits that those notebook commits pinned, and later commits to the files they created |
| `tested`, `planned`, `running`, `stopped` | A record in `wiki/research/experiments/` with the entry in `features`. The text is its `finding`. The state word is its `status`. |
| `ran` | An `experiment.json` in `results/` that changed the entry: record or directory, arm, value |
| `open` | The question of each such record, if the question is not `answered` |

## The blocks of the output

1. `SETTINGS` and `PRIORS`: one entry for each key.
2. `MODEL OPTIONS`: each option of `CSPBasis_afe`, and each option that only `CSPBasis`
   has. On 2026-09-30, `add_neb` was `[not in CSPBasis_afe; CSPBasis has it, default True]`.
3. `FEATURES THAT ARE NOT A CURRENT NOTEBOOK KEY OR CLASS OPTION`: a name in `features`
   that is not in blocks 1 and 2, with the commit that removed it from the notebook.
4. `WORK THAT IS NOT MERGED`: each branch that HEAD or the pinned Ceridwen does not
   contain, and each other worktree with changes that are not committed.
5. `OPEN ISSUES`: the `bd` issues that are open or in progress.
6. `EXPERIMENT RECORDS`: planned, running, or with results from the last 14 days.
   `--days 3` changes the 14. With a text, all records are candidates.
7. `RUN DIRECTORIES IN NO RECORD`: each `results/` directory with an `experiment.json`
   and a run manifest that no record lists in `result_groups`. A quick fit is here.
8. With a text only: the newest commits and the `wiki/research` files that contain it.

## Keep the records current

When you write or change an experiment record, set these two lines in its front matter.
The command shows a record under a feature only through them.

```yaml
features: emission_line_marginalisation
finding: M1_210210, on minus off: mass-weighted age -0.408 Gyr; RMS pull within 300 km/s of Hbeta 0.568 off, 0.484 on; ln Z not comparable with masked fits
```

- `features`: the names that the run used, with commas between them.
- `finding`: one line. Copy each number from the section Results of the record.

## Limits of the output

- A `finding` is a short copy. Read the section Results of the record before you speak
  about the result.
- A record without `features` is not under a feature. Find it with the text:
  `python3 scripts/ceridwen_state.py <text>`.
- `$ invoiced` is the sum of the `charges.json` files that `scripts/experiment.py`
  saved. A directory without `charges.json` shows no amount. Its record gives the cost.
- The command does not print `abandoned`. A record that stopped shows `stopped`. A
  branch shows the date of its last commit.

## Related rules

- For priorities and direction, read `AGENTS.md`, section "Research priorities".
- To run a fit, use the `running-ceridwen-experiments` skill.
- For the fields of a record, read `wiki/research/README.md`.
