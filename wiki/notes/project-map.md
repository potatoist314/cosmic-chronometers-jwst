---
title: Project map
date: 2026-08-25
section: Codebase
tags: [repository]
job: 
old: _old/codebase/project-map.html
---

The repository now focuses on Ceridwen stellar-population fits. The longer-term goal is cosmic-chronometer work with massive quiescent galaxies. Active notebooks provide the scientific entry points (`README.md:1-21`).

**Active fit path**

`scripts/` prepares data. `notebooks/` configures Ceridwen. `results/` stores output.

**Project evidence**

`data/` stores inputs. `papers/` stores literature. `wiki/` explains the code.

**Retained or upstream**

`src/` retains earlier support code. `external/` and `ceridwen/` are submodule checkouts.

<figure>
<figcaption>The active fit crosses project-owned orchestration and the Ceridwen package.</figcaption>
</figure>

### Repository boundaries

- The `ceridwen/` directory contains the primary model and inference implementation.
- The `src/` directory retains project-owned support code from earlier stages.
- The `scripts/` directory downloads and transforms data reproducibly.
- The `notebooks/` directory contains the active Ceridwen analyses and practice material.
- The `data/raw/` directory contains immutable downloaded inputs.
- The `data/processed/` directory contains reproducible derived tables.
- The `papers/` directory contains immutable literature sources.
- The `external/CCcovariance/` directory is a covariance reference submodule.
- The `external/fsps/` directory contains the FSPS submodule and its data.
- The `wiki/` directory contains generated code-reading documentation.

`.gitmodules:1-9` declares the three submodule paths and remotes.

### Entry points

The repository has no single scientific `main()` function. `main.py:1-6` is a scaffold that prints a greeting. Scientific execution starts in a notebook or one of these functions:

- `scripts/build_borghi2022_legac_dr2_subset.py:176` builds the joined table.
- `scripts/download_legac_dr2_spectra.py:113` downloads the spectra.
- `scripts/download_cosmos2015_legac_dr2_photometry.py:116` matches the photometry.
- `ceridwen/ceridwen/fit.py:67` starts a high-level Ceridwen fit.
- `ceridwen/ceridwen/sampler/runner.py:275` selects and runs a sampler.

### Environments

The root project requires Python 3.14. It retains dependencies for earlier project stages (`pyproject.toml:1-33`). Ceridwen is an independent package. It requires Python 3.11 or newer, JAX, and BlackJAX (`ceridwen/pyproject.toml:5-82`). The active fits use the Ceridwen environment.

**Root environment**

Python 3.14 and retained project dependencies.

**Ceridwen environment**

Python 3.11 or newer, JAX, and BlackJAX.

<figure>
<figcaption>The active notebooks run inside the Ceridwen environment.</figcaption>
</figure>

### Ownership

These rules describe code ownership:

- An active notebook configures a Ceridwen fit.
- The `src/` directory contains retained project support code.
- The `ceridwen/ceridwen/` directory contains the external package code used by current fits.
- The `external/` directory contains reference or upstream code.

The inspected Ceridwen checkout is upstream release `v0.2.2` at commit `034381f`. The project records that exact submodule commit.

### `main.py`

`main.py:1-6 · main`

```
def main():
    print("Hello from astro-project!")

if __name__ == "__main__":
    main()`
```

**Documented contract:** The project README names the Ceridwen notebooks as the active scientific entry points (`README.md:1-21`).

**Why it matters:** The guard calls `main()` only when Python runs this file directly. `main()` only prints a greeting. Therefore, this file is a package scaffold, not a scientific entry point.
