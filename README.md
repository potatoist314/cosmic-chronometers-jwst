# Stellar Ages and Cosmic Chronometers with JWST

Research code and notes for testing age-based cosmological measurements with
massive quiescent galaxies.

## Repository layout

- `src/` — reusable scientific code.
- `notebooks/` — exploratory analyses and reproductions.
- `scripts/` — reproducible data-processing utilities.
- `data/` — raw and processed research data.
- `papers/` — local reference literature.
- `external/` — external reference implementations.
- `session_plans/` — dated work plans, plus a rough project roadmap. The
  roadmap is a working draft rather than a committed schedule: its stages are
  placeholders until explicitly agreed.

## Ceridwen on Vast.ai

Use a Linux Jupyter+SSH instance with a CUDA 12-compatible image, at least
12 GB GPU memory, and at least 30 GB disk. A 24 GB RTX 3090 or 4090 leaves
comfortable memory headroom for notebooks 07 and 08.

Clone the repository into Vast's workspace:

```bash
cd /workspace
git clone --recurse-submodules \
  https://github.com/potatoist314/cosmic-chronometers-jwst.git
cd cosmic-chronometers-jwst
```

From the local project directory, upload the untracked scientific data:

```bash
vastai copy "local:$PWD/data/raw" \
  "C.<INSTANCE_ID>:/workspace/cosmic-chronometers-jwst/data/"
vastai copy "local:$PWD/ceridwen/amist_c3k_hr_krou_afe.h5" \
  "C.<INSTANCE_ID>:/workspace/cosmic-chronometers-jwst/ceridwen/"
```

Then configure and verify the remote GPU environment:

```bash
bash scripts/bootstrap_vast_ai.sh
```

Open `ceridwen_test_spectra.ipynb` or
`ceridwen_integrated_photometry_spectra.ipynb` and select
`Ceridwen (Vast.ai GPU)`. The kernel requires CUDA and enables JAX float64, so
a broken GPU setup cannot silently use CPU.
