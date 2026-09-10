---
title: Vast.ai GPU workflow
date: 2026-08-30
section: Guides
theme: Compute
tags: [gpu, vast-ai, ceridwen]
job: t_2fc31190
old: _old/guides/vast-ai-gpu-workflow.html
---

Operational guide

<details>
<summary>Details</summary>

The spectrum notebook fits spectra. The joint notebook fits photometry with native spectra or stellar indices. Use local CPUs for checks. Use Vast.ai GPUs for full fits. The DR2 production run assigns one deterministic target shard to each one-GPU instance.

</details>

<details>
<summary>Choose an instance</summary>

- Use a Linux image with Jupyter, SSH, and CUDA 12. Prefer `vastai/base-image:cuda-12.6.3-auto`. It avoids the unused PyTorch stack. The bootstrap installs CUDA JAX.
- Require at least 8 GB GPU memory and 12 GB disk.
- Require host reliability above 99.5 per cent.
- Reject upload or download prices above $0.01 per GB.
- Use the cheapest qualifying RTX 5060 offer.

Vast host `148498` in Croatia provided a tested-good A100 SXM4 40 GB allocation. Instance `48652928` completed the quick and full fits on 25 August 2026. This result applies to that allocation only.

The bootstrap stops if Linux, NVIDIA access, or 8 GB of GPU memory is unavailable. It never uses the CPU as an unreported substitute.

`scripts/bootstrap_vast_ai.sh:22-34 · GPU preflight`

</details>

```
if ! command -v nvidia-smi >/dev/null 2>&1; then
    echo "nvidia-smi is unavailable; launch a Vast.ai NVIDIA GPU instance." >&2
    exit 1
fi

GPU_MEMORY_MIB="$(
    nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits \
        | head -n 1 \
        | tr -d ' '
)"
if (( GPU_MEMORY_MIB < MINIMUM_GPU_MEMORY_MIB )); then
    echo "GPU has ${GPU_MEMORY_MIB} MiB; this run requires at least ${MINIMUM_GPU_MEMORY_MIB} MiB." >&2
    exit 1
fi`
```

<details>
<summary>Details</summary>

**Documented contract:** The script sets the default minimum to 8,000 MiB at `scripts/bootstrap_vast_ai.sh:12`.

**Why it matters:** The preflight stops before setup when the instance cannot run a Ceridwen GPU fit.

</details>

<details>
<summary>Clone the project</summary>

Open the instance terminal. Clone the project into the persistent workspace. Include the submodules because Ceridwen is a submodule of this repository.

</details>

```
cd /workspace
git clone --recurse-submodules \
  https://github.com/potatoist314/cosmic-chronometers-jwst.git
cd cosmic-chronometers-jwst`
```

<details>
<summary>Transfer private data</summary>

Run this command on the local computer. Replace `<INSTANCE_ID>` with the instance identifier. Git does not contain the LEGA-C spectra or matched photometry.

</details>

```
vastai copy "local:$PWD/data/raw" \
  "C.<INSTANCE_ID>:/workspace/cosmic-chronometers-jwst/data/"`
```

<details>
<summary>Details</summary>

The required remote paths are:

- `data/raw/legac_dr2/legaCdr2.fits.gz`
- `data/raw/legac_dr2/sp/`
- `data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits`

The bootstrap uses the Ceridwen registry to download the published high-resolution SSP grid. The registry fixes the expected checksum.

</details>

<details>
<summary>Bootstrap and verify</summary>

Run the maintained setup script from the remote project root:

</details>

```
bash scripts/bootstrap_vast_ai.sh`
```

<details>
<summary>Details</summary>

The script removes the Vast system CUDA library path. JAX then uses the compatible CUDA libraries from its Python environment.

`scripts/bootstrap_vast_ai.sh:13-14`

</details>

```
# Use the CUDA libraries installed with JAX, not Vast's system CUDA libraries.
unset LD_LIBRARY_PATH`
```

<details>
<summary>Details</summary>

The script creates an isolated Python 3.11 environment. It installs CUDA JAX, Ceridwen from the `ceridwen` submodule, and sedpy_jax from the `external/sedpy_jax` submodule. That sedpy_jax fork accepts the grid's wavelength-dependent resolution array and builds filters in NumPy, which keeps per-fit setup near 27 s. Both submodules install from the tree, so the bootstrap never fetches them from GitHub; a driver that provisions an instance copies both directories with the scripts. The script checks GPU float64 execution, runs the Ceridwen check, and registers the notebook kernel.

`scripts/bootstrap_vast_ai.sh:52-99`

</details>

```
JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "${PYTHON_BIN}" - <<'PY'
import jax
import jax.numpy as jnp

devices = jax.devices()
if not devices or any(device.platform != "gpu" for device in devices):
    raise SystemExit(f"Expected CUDA GPU devices, found {devices}")
value = jnp.ones(1, dtype=jnp.float64).block_until_ready()
PY

"${PYTHON_BIN}" -m ipykernel install --user \
    --name ceridwen \
    --display-name "Ceridwen (Vast.ai GPU)"`
```

<details>
<summary>Details</summary>

The script checks 1,988 spectra. It also checks the catalogue and photometry row counts. It fetches the published schema-2.1 grid and loads it in strict mode. It checks shape `(5, 13, 107, 10992)`.

</details>

<details>
<summary>Run the notebooks</summary>

1. Open JupyterLab on the Vast.ai instance.
2. Select `Ceridwen (Vast.ai GPU)` as the kernel.
3. Run `notebooks/ceridwen_test_spectra.ipynb` for spectra only.
4. Run `notebooks/ceridwen_integrated_photometry_spectra.ipynb` for the selectable combined fit.

The local CPU kernel and remote GPU kernel share the `ceridwen` identifier. Their visible names identify the active computer and backend.

The remote kernel requires CUDA and float64 for every notebook session. It also prevents the system CUDA path from replacing the installed JAX libraries.

</details>

<details>
<summary>Run the two DR2 shards</summary>

The runner selects 194 eligible spectra. It keeps the highest-S/N spectrum for each repeated object. This produces 187 targets. It sorts targets by decreasing S/N and alternates them between two shards.

Generate one shared manifest before the remote launch:

</details>

```
.venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --write-targets-file /workspace/ceridwen-dr2-targets.json`
```

<details>
<summary>Details</summary>

Run M1_210210 first with the complete production settings:

</details>

```
.venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --targets-file /workspace/ceridwen-dr2-targets.json --shard-index 0 --only-target M1_210210`
```

<details>
<summary>Details</summary>

After that result passes validation, run shard zero on the first instance and shard one on the second instance. The runner skips a valid completed target:

</details>

```
.venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --targets-file /workspace/ceridwen-dr2-targets.json --shard-index 0`
```

<details>
<summary>Details</summary>

The other instance uses `--shard-index 1`. The full profile uses 500 live points, 65 slice steps, 100 deletions, and `logZ_tol=-5`. Seed `20260830 + manifest_index` identifies each target.

A shard runs one target at a time by default. `--fits-per-gpu N` runs N targets at once, each worker with `XLA_CLIENT_MEM_FRACTION = 0.85/N`, and the shard manifest records `fits_per_gpu`.

Each target writes one executed notebook, two HDF5 files, and one execution log. Figures remain embedded in the notebook. The runner retries a failed target once with the same seed.

A periodic BlackJAX NSS checkpoint is a usable partial posterior. It cannot resume the sampler from the same point.

The local `--monitor` mode polls both shard manifests, downloads only completed four-file target products, validates them on the local computer, enforces the recorded credit cap, and destroys both production instances only after all 187 results pass.

`scripts/run_ceridwen_vast_multi_gpu.py:108-126 · build_target_manifest`

</details>

```
selected = (
    usable.sort_values(["SN", "SPECT_ID"], ascending=[False, True])
    .drop_duplicates("OBJECT", keep="first")
    .sort_values(["SN", "SPECT_ID"], ascending=[False, True])
)
if len(selected) != 187:
    raise RuntimeError(f"Expected 187 unique objects, found {len(selected)}")

targets = []
for index, row in enumerate(selected.itertuples(index=False)):
    targets.append(
        {
            "manifest_index": index,
            "object_id": int(row.OBJECT),
            "spect_id": str(row.SPECT_ID),
            "sn": float(row.SN),
            "shard_index": index % num_shards,
            "seed": base_seed + index,
        }`
```

<details>
<summary>Details</summary>

**Documented contract:** The function docstring selects one highest-S/N spectrum for each eligible object.

**Why it matters:** Repeat spectra cannot make one galaxy contribute more than one production fit.

</details>

<details>
<summary>Preserve results and finish</summary>

1. Download each completed four-file target result with `rsync -aP`.
2. Load both HDF5 files on the local computer.
3. Open the executed notebook and check its embedded figures.
4. Stop or destroy the paid instance after you secure the files.

Do not use the rented computer as the permanent copy of a scientific result.

</details>

<details>
<summary>Evidence</summary>

- `README.md:18-49` describes the instance, clone, transfer, bootstrap, and kernel workflow.
- `scripts/bootstrap_vast_ai.sh:8-14` fixes the requirements and isolates the CUDA libraries.
- `scripts/bootstrap_vast_ai.sh:52-94` installs and checks wavelength-dependent resolution support.
- `scripts/bootstrap_vast_ai.sh:97-119` configures the kernel and results root.
- `scripts/bootstrap_vast_ai.sh:122-168` checks the raw data and published grid.
- `scripts/run_ceridwen_vast_multi_gpu.py:37-137` selects and shards the 187 unique objects.
- `scripts/run_ceridwen_vast_multi_gpu.py:457-561` runs up to `fits_per_gpu` targets at once and records completion.
- `.gitignore:23-24` keeps the LEGA-C spectra out of Git.

</details>
