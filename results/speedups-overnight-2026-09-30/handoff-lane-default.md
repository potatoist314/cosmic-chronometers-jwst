# Hand-off: lane kernel as the default slice kernel

Task (Liu Hao, 2026-09-30): "okay yeah turn this on as default." Then moved to the
`speedups` integration branch.

## Done

- Ceridwen fork: `8161d3d` merges `lane-kernel` (`16c7a90`) with `--no-ff`.
  `BlackJAXNestedSamplerAdapter` defaults to `slice_kernel='lanes'`; `'carry'` and
  `'stock'` remain options.
- `8161d3d` is on `potatoist314/ceridwen` branch `speedups` (new) and also on `main`.
  `main` was pushed before the change of plan; it is not reverted.
- This repo, branch `speedups` (from `absorption-mask` `01f196d`): submodule pin
  `0a3bd51` -> `8161d3d`; `wiki/notes/ceridwen-likelihood-sampling.md` kernel
  paragraph, `lane_update` excerpt (nested.py:209-220) and `_logical_likelihood_calls`
  locator (673-683); `wiki/log.md` entry.
- Nothing is committed to `absorption-mask`. Its pin stays `0a3bd51`.
- No GPU rented. Spend: $0.

## Measured (CPU, `ceridwen/.venv`, `JAX_PLATFORMS=cpu`)

- Full ceridwen suite at `8161d3d`: 270 passed, 6 skipped, 7 failed, 10 errors.
- The same 7 failures and 10 errors occur at `0a3bd51` (detached worktree):
  `tests/csp/test_lookback_flip_invariant.py` (6), `tests/test_ssp_provenance.py`
  (FSPS import), `tests/regression/test_regression.py` (10 errors, ImportError).
- `tests/test_nss_diagnostics.py` and `tests/test_ns_checkpoint.py`: 14 passed,
  including lanes bitwise equal to stock `blackjax.nss`.
- Wiki in the shared tree with these edits: `wiki/build.py` builds;
  `wiki/tests/run_tests.py` fails one check, "resumable note carries the question box".
  Not compared with a baseline: a fresh worktree cannot build the wiki
  (3170 validation faults from untracked files).

## Open

- Merge of `speedups` into `absorption-mask` (pin and wiki): Liu Hao's call.
- Other `nested.py` locators on `wiki/notes/ceridwen-likelihood-sampling.md`
  (156-190, 144-172, 577-587, 88-142, 502-529) do not match `8161d3d`.
  Not changed.
- bd `astro-qn7` stays in progress.
