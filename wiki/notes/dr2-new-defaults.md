---
title: DR2 quiescent refit with the new production defaults
date: 2026-09-07
section: Analyses
theme: Single-fit accuracy
tags: [dr2-quiescent-sample, ceridwen, fit-accuracy-knobs]
figures: [old-vs-new-parameters.png, dust-index-posteriors.png, headline-age-redshift-old-vs-new.png, headline-age-redshift-oldest30.png, example-fits.png, example-sfh.png, example-corner.png]
---

Sample
: 187 LEGA-C DR2 quiescent galaxies, the same manifest and seeds as the first run
Old run
: `results/rtx-5060-dr2-quiescent-full-spectrum` · `results/dr2-quiescent-summary.csv`
New run
: `results/dr2-quiescent-new-defaults` · `results/dr2-quiescent-new-defaults-summary.csv`
Changed
: order-0 to order-3 calibration; aperture to `cosmos_total` photometry; free Kriek & Conroy dust index Uniform(-1.0, 0.4); StudentT(0, 0.3, df 2) on `logsfr_ratios`
Unchanged
: `diffuse_tau_kc` Uniform(0, 2), BlackJAX NSS gpu-full profile
Sampled parameters
: 14
Diagnostics
: 187/187 passed
Median ln Z shift
: +254, higher in 187/187
Cost
: 12.5 h on two RTX 5060 Ti, $4.05
Commit
: `998b6e1` · `origin/absorption-mask`

## Per-galaxy shifts

| parameter | median shift | NMAD | median half-width | moved > 1 half-width |
| --- | --- | --- | --- | --- |
| age [Gyr] | +1.23 | 1.15 | 0.17 | 169/187 |
| log Z | -0.17 | 0.21 | 0.036 | 173/187 |
| [α/Fe] | -0.056 | 0.059 | 0.018 | 148/187 |
| τ_diffuse | +0.17 | 0.15 | 0.023 | 171/187 |
| log M | +0.19 | 0.12 | 0.018 | 182/187 |

<figure>
<img src="figures/dr2-new-defaults/old-vs-new-parameters.png" alt="Five old-versus-new scatter panels and a histogram of the ln Z shift">
<figcaption><code>old-vs-new-parameters.png</code> · <code>results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb</code></figcaption>
</figure>

<details>
<summary>Seed noise</summary>

Seed repeats cover two galaxies. Maximum parameter shifts use posterior
half-width units: old model [1.20, 0.49, 0.96, 0.32, 0.49], new model
[0.34, 0.54, 0.23, 0.07, 0.29], for age, log Z, [α/Fe], τ_dust and log M.
[Seed comparisons](/wiki/e/e-seed-repeatability/).

The maximum seed-to-seed ln Z spread is 2.0 for the old model and 3.1 for the
new model. The old and new population runs use different photometry.

</details>

## Dust index

<figure>
<img src="figures/dr2-new-defaults/dust-index-posteriors.png" alt="Histogram of median dust index and its lack of correlation with the age shift">
<figcaption><code>dust-index-posteriors.png</code> · weighted quantiles from <code>samples/diffuse_dust_index</code></figcaption>
</figure>

Bimodal: 99 of 187 rail at -1.0.

<details>
<summary>Railing and the age shift</summary>

Railing counts a galaxy whose 16th percentile falls below -0.98. A second group
sits between 0.0 and 0.4, medians span -0.997 to 0.390, and 66 medians lie
above the old fixed -0.7. The `dust_wide` arm has posteriors near its -2.0 bound.

The median age shift is 1.34 Gyr for railed galaxies and 1.16 Gyr for the rest.

</details>

## Age against redshift

<figure>
<img src="figures/dr2-new-defaults/headline-age-redshift-old-vs-new.png" alt="Mass-weighted age against redshift for both runs, with Borghi+22 binned medians">
<figcaption><code>headline-age-redshift-old-vs-new.png</code> · σ split 215 km/s · four fixed z bins 0.6-0.9</figcaption>
</figure>

Mean offset from Borghi+22 grows from +0.21 to +1.89 Gyr.

<details>
<summary>Headline</summary>
<div id="what-the-headline-shows"></div>

The offset is the mean over binned medians for the 68-galaxy Borghi+22 overlap.
Both runs have a nearly flat age–redshift relation over 0.6 < z < 0.9.
Ceridwen ages are mass-weighted; Borghi ages are SSP-equivalent.

</details>

## Oldest 30% per bin

<figure>
<img src="figures/dr2-new-defaults/headline-age-redshift-oldest30.png" alt="Mass-weighted age against redshift for the oldest 30 percent of each sigma-z bin, both runs, with Borghi+22 treated the same way">
<figcaption><code>headline-age-redshift-oldest30.png</code> · oldest 30% of each σ-z bin · Borghi+22 cut the same way</figcaption>
</figure>

<details>
<summary>Chronometer cut</summary>
<div id="what-the-chronometer-cut-shows"></div>

The cut keeps the oldest 30% of each bin. New-default ages stay near 5–6 Gyr
over 0.6 < z < 0.9, about 1–2 Gyr above Borghi+22 with the same cut.
High-σ bins contain 3–4 galaxies, so their oldest 30% is one galaxy.
Table: `results/dr2-quiescent-new-defaults/age_redshift_oldest30.csv`.

</details>

## Example galaxies

<figure>
<img src="figures/dr2-new-defaults/example-fits.png" alt="Observed and posterior spectra for four galaxies spanning the age shift">
<figcaption><code>example-fits.png</code> · 139662, 120540, 237437, 104877</figcaption>
</figure>

<figure>
<img src="figures/dr2-new-defaults/example-sfh.png" alt="Star-formation histories for the same four galaxies">
<figcaption><code>example-sfh.png</code></figcaption>
</figure>

<figure>
<img src="figures/dr2-new-defaults/example-corner.png" alt="Corner plot over log M, Z, alpha/Fe, tau and dust index">
<figcaption><code>example-corner.png</code></figcaption>
</figure>

<details>
<summary>Run details</summary>

Two RTX 5060 Ti instances ran two deterministic shards, shard index equal to
manifest index modulo 2, seed 20260830 plus manifest index. Account credit fell
$4.05 over the run. Another session held an instance for part of that window,
so these two boxes cost no more than that. The shard driver logs stayed on the
rented boxes and were not pulled; each fit folder keeps its own
`execution.log`.

The derived-outputs summary table does not carry `diffuse_dust_index`, so the
dust numbers come from `samples/diffuse_dust_index` in `ceridwen_result.h5`,
weighted by `samples/log_weights`.

</details>

```
ceridwen/.venv/bin/python scripts/run_ceridwen_vast_multi_gpu.py \
  --targets-file results/dr2-quiescent-new-defaults/targets.json \
  --shard-index N --num-shards 2 --base-seed 20260830 \
  --output-root results/dr2-quiescent-new-defaults
ceridwen/.venv/bin/python scripts/build_dr2_quiescent_summary.py \
  --result-root results/dr2-quiescent-new-defaults \
  --out-path results/dr2-quiescent-new-defaults-summary.csv
```
