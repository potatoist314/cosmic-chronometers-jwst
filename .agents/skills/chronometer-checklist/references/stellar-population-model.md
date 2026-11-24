Copied without change on 2026-11-24 from Part A of `~/.claude/scripts/hermes-bridge/results/t_3de1c8a9-detail.md`. A file name such as `t_0c96cd9b-detail.md` refers to a file in `~/.claude/scripts/hermes-bridge/results/`.

## Stellar population model: what it contains and its limits

Sources, with the short names used below:

- **P25**: Park, Conroy, Johnson, Leja, Dotter, Cargile 2025, "α-MC", ApJ 994:165. Read as arXiv:2410.21375v1, the local PDF in `papers/spectral fitting/`. Section and figure numbers are those of v1.
- **D26**: Dotter et al. 2026, "MIST II", arXiv:2602.22012v1. This is the isochrone paper that P25 cites as "in prep".
- **C14**: Conroy, Graves & van Dokkum 2014, ApJ 780:33 (local PDF). Stacked SDSS early-type spectra, σ = 90 to 300 km/s.
- **B23**: Beverage et al. 2023, arXiv:2303.03412 (local PDF). 135 LEGA-C quiescent galaxies at z ~ 0.7.
- **grid**: attributes and axes of `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5`.

"Not stated" means that the source text does not give the item.

### 1. What the models are

| Item | Value | Source |
|---|---|---|
| Isochrones | MIST, computed with MESA. Masses 0.1 to 300 M_sun. Each track ends at the end of the AGB (M < 8 M_sun) or at the end of carbon burning (M ≥ 8 M_sun). | P25 §2.1 |
| Isochrone version | The paper says "MIST v2.3". The grid file says "MIST v2.5 (aMIST, alpha-variable)". | P25 §2.1; grid `isoc_type` |
| Stellar spectra | C3K v2.3. ATLAS12 atmospheres and SYNTHE spectra. 1D, plane-parallel, LTE. Microturbulence 1 km/s for all stars. | P25 §2.2, §2.4 |
| Line list | Tuned to the Sun and Arcturus for 4728 Å to 1 µm only. | P25 §2.2, Fig. 1 |
| Stellar grid | T_eff 2500 to 50,000 K. log g −1.0 to 5.5 in steps of 0.5. | P25 §2.2 |
| IMF | Kroupa (2001), lower mass limit 0.1 M_sun. One IMF only. | P25 §2.3; grid `imf_name` |
| Enhanced elements | O, Ne, Mg, Si, S, Ar, Ca, Ti. All change by the same [α/Fe] ("in lockstep"). | P25 §2.1, §2.4; D26 §2.1 |
| C and N | Solar-scaled in all evolutionary phases. | P25 §2.4 |
| Solar mixture | GS98, Z/X = 0.023. Isochrones and spectra use the same mixture. | P25 §2.1, §4 |
| Solar initial composition | X = 0.7080, Y = 0.2735, Z = 0.0185. | D26 Table 1 |
| Helium | ΔY/ΔZ ≈ 1.32 with Y_p = 0.249. Helium is not a free quantity. | D26 Eq. 1 |
| [Fe/H] | −2.5 to +0.5, step 0.25, 13 nodes. | P25 abstract; grid `ssp_lgmet` |
| [α/Fe] | −0.2, 0.0, +0.2, +0.4, +0.6. | P25 abstract; grid `ssp_afe` |
| Age | log(age/yr) 5.0 to 10.3, step 0.05, 107 nodes. | P25 §2.3; grid `ssp_lg_age_gyr` |
| Wavelength | 100 Å to 30 µm. High resolution only for 0.1 to 2.5 µm. | P25 §2.3, §4 |
| Resolution, paper | R = 3000 for 0.3 to 1.0 µm. R = 500 for 0.1 to 0.3 µm and 1.0 to 2.5 µm. R = 200 below 0.1 µm. R = 50 above 2.5 µm. | P25 Fig. 1 |
| Resolution, our grid | λ/Δλ = 6000 per pixel from 3001 to 9997 Å. Two-pixel limit σ_v = 42.44 km/s. | grid `ssp_resolution`; `ceridwen/docs/afe.md:48-50` |

How Ceridwen reads the grid:

- `logzsol` is [Fe/H], not total metallicity. The native axis is log10 Z = [Fe/H] + log10(0.0185). Source: `ceridwen/docs/afe.md:47-51`, `ceridwen/GOTCHAS.md:34-37`, grid `fsps_kwargs_json`.
- Total metallicity: [Z/H] = [Fe/H] + log10(1 − x + x 10^[α/Fe]), x = 0.68749. This gives +0.15, +0.31 and +0.48 dex at [α/Fe] = +0.2, +0.4 and +0.6. Source: `ceridwen/ceridwen/ssps/grid_metadata.py:44-60`.
- `afe` is interpolated linearly between the five planes. Source: `ceridwen/docs/afe.md:55`.
- `CSPBasis_afe` has no nebular model. Source: `ceridwen/docs/afe.md:60`.

Where each range ends:

- **Metal-rich corner.** Opacity tables are missing for the most metal-rich compositions. For seven grid points the 0.1 to 0.5 M_sun part of the isochrone is a copy from the nearest metallicity. For [Fe/H] = +0.5, [α/Fe] = +0.6 the full isochrone is a copy of the [α/Fe] = +0.4 one (P25 §2.1). D26 §2.1 drops that composition. Ceridwen refuses a prior that includes both `logzsol` > +0.25 and [α/Fe] > +0.4 (`ceridwen/docs/afe.md:66-68`, `grid_metadata.py:82-88`).
- **Blue of 4728 Å.** The paper states line-list tuning for 4728 Å to 1 µm only. It does not give the accuracy at shorter wavelengths. The window 4074.5 to 4666.1 Å is fully below 4728 Å.
- **Outside 0.3 to 1.0 µm.** The resolution falls to R = 500 or lower (P25 Fig. 1).
- **Stars outside the spectral grid.** Not stated.
- **Grid edges in a fit.** The forward model clamps at the grid edge and gives no warning (`ceridwen/GOTCHAS.md:52`).

### 2. Limits the authors state, and the validations they show

Limits stated by the authors:

1. [Fe/H] and [α/Fe] are the initial composition. The atmospheres do not include changes of surface abundance from diffusion or dredge-up (P25 §2.4).
2. One [α/Fe] sets all α elements (P25 §2.4).
3. C and N do not vary (P25 §2.4, §3.2.3).
4. The spectra are 1D, plane-parallel and LTE, with a constant microturbulence (P25 §2.4).
5. Post-AGB stars and white dwarfs are not in the new isochrones. FUV − V differs from MIST v1.2 at log(age/yr) > 9.0 (P25 §3.1, Fig. 3; D26 §2.7).
6. C2 4668 is much weaker than in models made from observed stars (P25 §3.3.2, Fig. 18). The authors give two possible causes: surface C and N evolution, or the line list.
7. Opacity tables are missing at the metal-rich end (P25 §2.1; D26 §2.1).
8. The paper has no comparison with observed data: "Applications to observed data will be presented in a subsequent paper" (P25 §1, §4).
9. The isochrones have one value of RGB mass loss. They "will not describe a full zero-age horizontal branch sequence" (D26 §3.4).

Validations shown:

| Test | Compared with | Size given | Source |
|---|---|---|---|
| SSP spectra and colours, solar-scaled | MIST v1.2 | "Good agreement". FUV − V differs at log age > 9.0. | P25 §3.1, Figs. 2-3 |
| Continuum shape, old ages | Coelho et al. 2007; Knowles et al. 2023 (sMILES) | Agree. No number. | P25 §3.3.2, Fig. 16 |
| g − r | same two models | Agree. α minus solar ≈ 0.1 mag at log age ≈ 9. | P25 §3.3.2, Fig. 17 |
| V − I | same | α-enhanced ≈ 0.1 mag redder. | P25 §3.3.2, Fig. 17 |
| Lick index trends with [α/Fe] | same | Consistent, except C2 4668. | P25 §3.3.2, Fig. 18 |
| C2 4668 | sMILES | "Large discrepancy". No number. | P25 §3.3.2, Fig. 18 |
| Isochrones | BaSTI at 0.1, 1 and 10 Gyr | "The overall agreement is reassuring". No number. | D26 §3.3, Fig. 6 |
| Colour-magnitude diagrams | M 92, M 3, 47 Tuc, NGC 6397, NGC 6752 | Isochrones of 10 to 13 Gyr drawn on the data. No fit. No number. "Not meant to be a detailed analysis". | D26 §3.4, Figs. 7-8, Table 2 |
| RGB bump | Nataf et al. 2013 clusters | Envelope overshoot calibrated on it. The earlier MIST was ~0.5 mag off for the most metal-poor clusters. | D26 §2.5, Fig. 1 |
| Observed galaxy spectra or indices | none | None shown. | P25 §1 |

Size of the α effect inside the model, [α/Fe] = +0.4 against solar, ages > 1 Gyr:

| Quantity | Fixed [Fe/H] = 0 | Fixed [Z/H] = +0.26 | Source |
|---|---|---|---|
| Continuum level | ~20 % lower | ~10 % lower above 0.45 µm | P25 §3.2.1, §3.2.4, §4 |
| G − K | ~0.2 mag redder | ~0.05 mag redder | P25 §3.2.2, §3.2.4 |
| u − g | small | ~0.2 mag bluer at 10 Gyr | P25 §3.2.4 |
| Mg b, Fe5270 on our grid, one node | +2.3 Å, −0.11 Å | | `grid_metadata.py:175-181` |

### 3. What is not varied

| Quantity | State in the model | What the sources say |
|---|---|---|
| O, Mg, Si, Ca, Ti separately | Not possible. One [α/Fe]. | P25 §2.4 |
| C, N | Fixed at solar-scaled. | P25 §2.4. "Future work is needed" (§3.2.3). |
| Na | Not in the list of enhanced elements. | P25 §2.1. [Na/Fe] itself: not stated. |
| IMF | Kroupa only. | P25 §2.3. One remark that TiO at young ages depends on the IMF slope (§3.2.3, citing Vazdekis et al. 2015). |
| Binaries | Not stated. | P25, D26 |
| Blue horizontal branch | No free quantity. | P25: not stated. D26 §3.4: one RGB mass-loss value, no full horizontal branch. |
| AGB and TP-AGB | Included to the end of the TP-AGB. No free quantity. | P25 §2.1, §3.2.2; D26 §2.7 |
| Post-AGB, white dwarfs | Not included. | P25 §3.1; D26 §2.7 |
| Rotation | D26 has two model sets, with and without rotation (Ω = 0.4 Ω_crit for M ≥ 1.8 M_sun). The set used for the SSPs: not stated. | D26 §2.4. P25: not stated. |
| Mass loss | "Essentially the same" as Choi et al. 2016. One RGB value. | D26 §2, §3.4. P25: not stated. |
| Surface abundance changes | Not in the atmospheres. | P25 §2.4 |
| Helium | Tied to Z. | D26 Eq. 1 |

Ceridwen adds one thing: `abundance_response` applies alf C and N responses with free `cfe` and `nfe` (`ceridwen/ceridwen/csp/csp_afe.py:66`, `:262-264`). The alf response covers 3501.0 to 24997.6 Å (`t_0c96cd9b-detail.md:107`). There is no free Na (`t_dcbba686-detail.md:125`).

### 4. Absorption features, rest 3600 to 7100 Å

Last column: the feature has a basis for a mask if (a) it depends on an abundance that the model cannot set and a cited paper measures that abundance away from the model value, or (b) a cited paper reports non-stellar absorption in the band. This test is the worker's, not from a paper.

Measured in massive early-type galaxies (C14 abstract, §5.2, §8): [Fe/H] changes by < 0.1 dex over the sample. Mg and O go from ≈ 0.0 at low σ to ≈ 0.25 at high σ. Si and Ti rise less. "Ca tracks Fe rather than O". [C/Fe] and [N/Fe] are above 0.2 at high σ. [Na/Fe] goes from −0.16 to +0.43. At z ~ 0.7 the patterns are "strikingly similar to those at z ~ 0" (B23 abstract).

| Feature | Model behaviour when [α/Fe] rises at fixed [Fe/H] (P25 §3.2.3, Figs. 9-11) | Depends on | Evidence for massive ellipticals | Basis for a mask |
|---|---|---|---|---|
| H8 to H16, Hδ, Hγ | Produced. Hγ_A and Hδ_A get weaker. More sensitive than Hβ. | Age, [Fe/H], [α/Fe] | Not stated in the sources read. | None found |
| Hβ | Produced. At [Fe/H] = 0: no clear change above 1 Gyr. Weaker at log age 8.5 to 9. | Age, [Fe/H] | Not stated. | None found |
| Hα | Produced. P25 does not discuss it. | Not stated | Not stated. | None found |
| Ca II H and K | Deeper (P25 §3.2.1, Fig. 4). | Ca, tied to [α/Fe] | Ca follows Fe, not Mg (C14). | Yes, (a) |
| 4000 Å break | Produced (D4000, Bruzual 1983). Size of change: not stated in text. | Not stated | Not stated. | None found |
| CN1, CN2 | Weaker. | C, N, O | [C/Fe], [N/Fe] > 0.2 at high σ (C14 §5.2, Fig. 13). | Yes, (a), unless the C/N response is on |
| G4300 | Weaker. | C | Same as CN. | Yes, (a), unless the C/N response is on |
| Ca4227 | Much stronger. Also stronger at fixed [Z/H]. | Ca, tied to [α/Fe] | Ca follows Fe (C14). | Yes, (a) |
| Fe4383 | Weaker above 1 Gyr. Also carbon-sensitive. | Fe, C | [Fe/H] is free. C as for CN. | Fe: none. C: as CN |
| Fe4531 | Stronger. | Ti, tied to [α/Fe] | Ti rises less than Mg (C14 abstract). | Partly, (a) |
| Fe4668 (C2 4668) | "Dramatically decreases" above 1 Gyr. | C | Theoretical spectra are weaker than MILES stars (Knowles et al. 2019, cited in P25 §3.3.2). [C/Fe] > 0.2 (C14). | Yes, (a) |
| Fe5015 | Stronger. Weaker at fixed [Z/H]. | Ti, Fe | Ti rises less than Mg (C14). | Partly, (a) |
| Mg b | Most sensitive index to [α/Fe]. Stronger also at fixed [Z/H]. | Mg, tied to [α/Fe] | Mg ≈ O. Ca, Ti and Si do not follow Mg (C14). | Mg can be set. The other α elements then move with it. |
| Fe5270, Fe5335 | Weaker above 1 Gyr. | Fe | [Fe/H] is free. | None found |
| Na D | Weaker. "Behaves as Fe-sensitive lines". | Na, not free | [Na/Fe] −0.16 to +0.43. The 5895 Å line is "well-known to be affected by" the interstellar medium (C14 §5.2). | Yes, (a) and (b) |
| TiO1, TiO2 | Stronger. Isochrone and spectrum contribute about equally. Very sensitive to temperature. | Ti, O, T_eff of M stars | Ti rises less than Mg (C14). IMF dependence stated only for young ages (P25 §3.2.3). | Partly, (a) |

State of each feature in the current fits (`t_0c96cd9b-detail.md:111`, `:121`, `:227-272`): Ca II K, Ca II H, Hε and Ca4227 have no fitted pixel, because the `emission_lines` list masks 3934.77, 3966.6, 3973.3 and 4227.92 Å ± 1500 km/s. All other features above are fitted in the wide range. In the narrow window the fitted features are Hδ, CN, G4300, Hγ, Fe4383, Ca4455, Fe4531 and 0.36 of Fe4668.

### 5. Age

- **Age nodes.** 107 nodes, log(age/yr) 5.0 to 10.3, step 0.05 dex (P25 §2.3; grid). One step is 12.2 % in age.
- **Old nodes, in Gyr.** 7.94, 8.91, 10.00, 11.22, 12.59, 14.13, 15.85, 17.78, 19.95 (grid `ssp_lg_age_gyr`). The steps near 10 to 14 Gyr are 1.2 to 1.5 Gyr.
- **Above 13.8 Gyr.** Models exist. Four nodes are older than 13.8 Gyr. Their flux is finite and not zero (grid `ssp_flux`).
- **Isochrone age ceiling.** P25 gives 10^10.3 yr as the oldest SSP age. D26 shows isochrones up to 13 Gyr. A separate ceiling: not stated.
- **Ceiling in a Ceridwen fit.** `SedModel` refuses an SFH node more than 0.5 % older than the Universe at the galaxy redshift (`ceridwen/ceridwen/model/model.py:232`, `ceridwen/GOTCHAS.md:305-310`). The largest mass-weighted age is then 0.925 t_U (`t_0c96cd9b-detail.md:42`).
- **Absolute age scale.** P25: not stated. D26 calibrates the stellar models on the Sun (Table 1: α_MLT = 2.03) and the envelope overshoot on the RGB bump (§2.5).
- **Age uncertainty.** Not stated in P25 or D26.
- **Age and abundance.** At fixed [Fe/H], α-enhanced models have weaker Balmer lines. The ages at which this occurs change with [Fe/H]. "To accurately derive the ages of stellar populations, a detailed analysis with chemical abundances ([Fe/H], [α/Fe]) is required" (P25 §3.2.3, §4 item 4). The word "degeneracy" is not in P25.
- **[α/Fe] and metallicity.** "[α/Fe] ... is degenerate with total metallicity" (`ceridwen/docs/afe.md:5-6`). Ceridwen mock fits give a median [α/Fe] bias of +0.05, +0.02 and +0.01 dex at S/N 10, 25 and 50 (Ceridwen paper §6.5.2, p. 17).
- **Scaling Z in place of α.** A scaled-solar isochrone at the same total Z agrees with the α-enhanced one at [Fe/H] = −0.5. It does not agree at [Fe/H] = −0.25, [α/Fe] = +0.6 at old ages (D26 §3.2, Fig. 4).

### 6. Our results against these limits

Na D, 50 SDSS galaxies, wide range (`~/.claude/scripts/hermes-bridge/results/t_dcbba686-detail.md`):

| Quantity | Na D fitted | Na D masked | Line |
|---|---|---|---|
| Data minus model in the band, fraction of model flux | −2.8 % [−4.0, −2.1], negative in 49 of 49 | −4.5 % [−6.1, −3.5] | 91-92 |
| Extra absorption, rest equivalent width | 0.89 Å [0.65, 1.21] | 1.43 Å [0.98, 1.98] | 95 |
| χ² per pixel in the band | 3.24 | 6.83 | 98 |
| Fits older than the Planck18 Universe age | 11 | 1 | 9, 38 |
| Fits with > 0.9 of the mass in the oldest step | 5 | 0 | 9, 40 |
| Median [Fe/H], [α/Fe] | +0.03, +0.19 | −0.04, +0.27 | 44-45 |
| Age slope, Gyr per unit z (Planck18 −11.38) | −11.9 ± 3.3 | −10.0 ± 2.9 | 8 |

Median age change per galaxy with the mask: −1.09 Gyr [−1.87, −0.63] (line 63).

Worst-fitted bands, same sample, χ² per pixel pooled over 50 galaxies (`t_0c96cd9b-detail.md:122`): Na D 3.28, Fe4668 1.90, Mg b 1.36, Mg_2 1.36. Median for all pixels: 1.14 wide, 0.99 narrow (line 11). Median [Fe/H]: −0.28 narrow, +0.05 wide (line 155).

C and N response and Mg b, 135 LEGA-C galaxies (`results/chronometer-135-2026-11-10/REPORT.md`):

| Quantity | (a) baseline | (b) C/N free | (d) carbon mask | Line |
|---|---|---|---|---|
| Median [α/Fe], all | −0.03 | +0.12 | +0.09 | 122, 125, 131 |
| Median [C/Fe], [N/Fe], all | – | −0.02, +0.30 | – | 125 |
| Median [C/Fe], [N/Fe], Mg b group (61) | – | +0.12, +0.12 | – | 126 |
| Median [C/Fe], [N/Fe], no-Mg b group (74) | – | −0.14, +0.45 | – | 127 |
| Mg b offset, Gyr | +0.27 | −0.86 | +0.11 | 152-155 |
| Mg b step, Gyr | −0.01 (−0.19 to +0.17) | −0.99 (−1.19 to −0.79) | −0.10 (−0.29 to +0.09) | 152-155 |
| Age slope, Gyr per unit z (Planck18 −5.17) | −1.55 | +0.97 | −2.72 | 68-74 |

Band pulls, negative means data below the model (`REPORT.md:616-637`):

| Feature | Arm | Own fit | Baseline (a), same galaxies |
|---|---|---|---|
| C4668 | (l), 96 galaxies | −2.58 (−3.76 to −0.79) | −3.82 (−6.64 to −2.02) |
| C4668 | (m), 46 galaxies | −4.72 (−7.32 to −2.68) | −5.39 (−8.11 to −3.37) |
| Mg b | (m) | −2.20 (−3.75 to −0.85) | −3.80 (−5.66 to −1.61) |
| Fe5015 | (m) | −0.05 (−2.24 to +1.72) | −0.65 (−3.21 to +1.41) |
| Hβ | (l) | +0.02 (−0.70 to +1.35) | +0.64 (−0.70 to +2.22) |
