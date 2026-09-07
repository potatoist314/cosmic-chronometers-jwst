---
title: DR2 quiescent refit with the new production defaults
date: 2026-09-07
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, fit-accuracy-knobs]
figures: [old-vs-new-parameters.png, dust-index-posteriors.png, headline-age-redshift-old-vs-new.png, example-fits.png, example-sfh.png, example-corner.png]
---

Sample
: 187 LEGA-C DR2 quiescent galaxies, the same manifest and seeds as the first run
Old run
: `results/rtx-5060-dr2-quiescent-full-spectrum` · `results/dr2-quiescent-summary.csv`
New run
: `results/dr2-quiescent-new-defaults` · `results/dr2-quiescent-new-defaults-summary.csv`
Changed
: free Kriek & Conroy dust index Uniform(-1.0, 0.4); StudentT(0, 0.3, df 2) continuity prior on `logsfr_ratios`
Unchanged
: order-3 marginalised calibration polynomial, `cosmos_total` 12-band photometry, `diffuse_tau_kc` Uniform(0, 2), BlackJAX NSS gpu-full profile
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

| parameter | median shift | NMAD | median half-width | moved > 1 half-width | median vs seed noise |
| --- | --- | --- | --- | --- | --- |
| age [Gyr] | +1.23 | 1.15 | 0.17 | 169/187 | 13.5 |
| log Z | -0.17 | 0.21 | 0.036 | 173/187 | 3.1 |
| [α/Fe] | -0.056 | 0.059 | 0.018 | 148/187 | 0.8 |
| τ_diffuse | +0.17 | 0.15 | 0.023 | 171/187 | 7.1 |
| log M | +0.19 | 0.12 | 0.018 | 182/187 | 4.6 |

<figure>
<img src="figures/dr2-new-defaults/old-vs-new-parameters.png" alt="Five old-versus-new scatter panels and a histogram of the ln Z shift">
<figcaption><code>old-vs-new-parameters.png</code> · <code>results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb</code></figcaption>
</figure>

<details>
<summary>Seed noise</summary>

Posterior half-widths are far smaller than the seed floors measured in
[fit-accuracy knobs](fit-accuracy-knobs.html). The old model floors are age
1.20 Gyr, log Z 0.49, [α/Fe] 0.96, τ_dust 0.32, log M 0.49. The new model
floors are 0.34, 0.54, 0.23, 0.07, 0.29. A shift between the two runs carries
both, added in quadrature: age 1.25, log Z 0.73, [α/Fe] 0.99, τ_dust 0.33,
log M 0.57. One galaxy's shift is therefore not resolved against sampler noise,
and the "moved > 1 half-width" column overstates significance for that reason.
The sample median is resolved, because noise on a median of 187 galaxies falls
by sqrt(187). The last column is the median shift over that noise. [α/Fe] at
0.8 is the one parameter that does not move.

Old ages pile up near 3 Gyr. New ages spread over 3 to 6 Gyr.

The seed-to-seed ln Z spread is 2.0 for the old model and 3.1 for the new one,
3.7 combined, against a median shift of 254. ln Z is the prior-weighted
marginal likelihood, so it compares the two prior choices directly.

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
above the old fixed -0.7. Few galaxies sit near -0.7, so the old fixed value
falls in the least-favoured part of the posterior. The prior floor at -1.0 is
doing real work, and a wider prior would change the railing fraction. The
`dust_wide` arm already showed galaxies following the wall out to -2.0.

The age shift does not track the dust index. Railed galaxies move by a median
1.34 Gyr and the rest by 1.16 Gyr, so the freed index is not what drives the
ages up.

</details>

## Age against redshift

<figure>
<img src="figures/dr2-new-defaults/headline-age-redshift-old-vs-new.png" alt="Mass-weighted age against redshift for both runs, with Borghi+22 binned medians">
<figcaption><code>headline-age-redshift-old-vs-new.png</code> · σ split 215 km/s · four fixed z bins 0.6-0.9</figcaption>
</figure>

Mean offset from Borghi+22 grows from +0.21 to +1.89 Gyr.

<details>
<summary>What the headline shows</summary>

The offset is the mean over the binned medians for the 68 galaxies that
overlap Borghi+22. The old defaults sat on Borghi+22. The new defaults sit
about 1.8 Gyr above. Both runs give a flat age-redshift relation across
0.6 < z < 0.9, so neither recovers the decline a cosmic chronometer needs. The
new defaults win decisively on evidence and move away from the published ages.

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
