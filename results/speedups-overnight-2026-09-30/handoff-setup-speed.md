# Setup speed: hand-off (2026-09-30)

## Done

- Setup-time breakdown from saved run records (below).
- No code change. Nothing committed to `absorption-mask`. No GPU rented.

## Measured

Run `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30`, host 146008, times BST.
Its driver stdout was not saved; stages come from `run/manifest.json`, `run/charges.json` and file times.

| Stage | Time | Source |
|---|---|---|
| Offer search, 4 rentals refused (`vastai returned no JSON`) | 18:01:59–18:04:09, 2.2 min | manifest `attempts[0..4].started` |
| Instance loading (image pull) | 18:04:09–~18:09:55, ~5.8 min | charges: disk 0.483 h from creation, GPU 0.386 h from running |
| SSH ready + upload (source, inputs, 612 MB grid) + bootstrap | ~18:09:55–18:21:00, ~11 min | `run/53558252-bootstrap.log` mtime |
| Fit | 18:21:10–~18:32:20, ~11 min | `fit-0.log`, result file time |

Same host, next run (`results/m1-210210-neb-eline-ca-noo-2026-09-30/driver.log`, 17:38 UTC):
rent to running 28 s (image cached), upload 3 min 10 s, bootstrap 13 s; setup 4 min.
Upload rate from this Mac there: ~3.2 MB/s. The ~11 min window above is not split into SSH wait and upload.

## Open

- Premise: no grid is fetched on the box today. `Run.upload` (`scripts/benchmark.py`) rsyncs every grid from the Mac,
  the standard `amist_c3k_hr_krou_afe` too; `vast._bootstrap` does the same. `fetch_grid` runs on the box only when
  `CERIDWEN_GRID_PATH` is unset.
- Grid download on the box (not built): host both grids on potatoist314 storage, `curl` on the box, check the manifest
  `grid_sha256` (nebular `6fe00c55a177…`), rsync from the Mac only on failure. Saves ~3 min per rental at 3.2 MB/s; more
  when several drivers upload at once.
- Image pull on a host without the image: 5.8 min here; the 17:17 and 17:29 UTC attempts of the `noo` run loaded for
  6–10 min and were replaced. Hosts with the image cached reach running in ~30 s.
- `vastai returned no JSON` refuses 2–5 rentals at the start of every run in these logs (1–2 min per run).
