# Ceridwen Stellar-Population Fits for Cosmic Chronometers

Research code for Ceridwen fits of massive quiescent galaxies. The current
workflow fits LEGA-C spectra and photometry with BlackJAX nested sampling. The
longer-term goal is age-based cosmology with JWST samples.

Ceridwen is the primary implementation focus. Earlier Prospector, MilesPy, and
Lick-index branches remain only for provenance and reproducibility.

## Repository layout

- `ceridwen/` — primary stellar-population model and inference submodule.
- `notebooks/` — active Ceridwen analyses.
- `src/` — reusable support code from earlier project stages.
- `scripts/` — production run, Vast drivers, figures, data download; see `scripts/README.md`.
- `data/` — raw and processed research data.
- `papers/` — local reference literature.
- `external/` — retained external reference implementations.
- `archive/` — inactive scripts, notebooks, plans and results; see `archive/README.md`.

## Ceridwen on Vast.ai

Use a Linux Jupyter+SSH instance with a CUDA 12-compatible image, at least
12 GB GPU memory, and at least 30 GB disk. Prefer
`vastai/base-image:cuda-12.6.3-auto`: it avoids the unused PyTorch stack, and
the bootstrap installs its own CUDA JAX. Prefer a consumer RTX card when
minimizing fit cost. Compare current Vast prices with the measured likelihood
calls per second because listing prices vary.

Clone the repository into Vast's workspace:

```bash
cd /workspace
git clone --recurse-submodules \
  https://github.com/potatoist314/cosmic-chronometers-jwst.git
cd cosmic-chronometers-jwst
```

From the local project directory, upload the untracked LEGA-C data:

```bash
vastai copy "local:$PWD/data/raw" \
  "C.<INSTANCE_ID>:/workspace/cosmic-chronometers-jwst/data/"
```

Then configure and verify the remote GPU environment:

```bash
bash scripts/bootstrap_vast_ai.sh
```

The script downloads and verifies Ceridwen's published schema-2.1
high-resolution SSP grid. Open `notebooks/ceridwen_test_spectra.ipynb` or
`notebooks/ceridwen_integrated_photometry_spectra.ipynb` and select
`Ceridwen (Vast.ai GPU)`. The kernel requires CUDA and enables JAX float64, so
a broken GPU setup cannot silently use CPU. Each run writes checkpoints and a
reloadable HDF5 posterior under `results/`.
