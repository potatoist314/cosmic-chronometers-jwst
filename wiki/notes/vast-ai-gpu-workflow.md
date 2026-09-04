---
title: Vast.ai GPU workflow
date: 2026-08-30
section: Guides
tags: [gpu, vast-ai, ceridwen]
job: t_2fc31190
old: _old/guides/vast-ai-gpu-workflow.html
---

Operational guide

The spectrum notebook fits spectra. The joint notebook fits photometry with native spectra or stellar indices. Use local CPUs for checks. Use Vast.ai GPUs for full fits. The DR2 production run assigns one deterministic target shard to each one-GPU instance.

### Choose an instance

- Use a Linux image with Jupyter, SSH, and CUDA 12. Prefer `vastai/base-image:cuda-12.6.3-auto`. It avoids the unused PyTorch stack. The bootstrap installs CUDA JAX.
- Require at least 8 GB GPU memory and 12 GB disk.
- Require host reliability above 99.5 per cent.
- Reject upload or download prices above $0.01 per GB.
- Use the cheapest qualifying RTX 5060 offer.

Vast host `148498` in Croatia provided a tested-good A100 SXM4 40 GB allocation. Instance `48652928` completed the quick and full fits on 25 August 2026. This result applies to that allocation only.

The bootstrap stops if Linux, NVIDIA access, or 8 GB of GPU memory is unavailable. It never uses the CPU as an unreported substitute.

`scripts/bootstrap_vast_ai.sh:22-34 · GPU preflight`

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

**Documented contract:** The script sets the default minimum to 8,000 MiB at `scripts/bootstrap_vast_ai.sh:12`.

**Why it matters:** The preflight stops before setup when the instance cannot run a Ceridwen GPU fit.

### Clone the project

Open the instance terminal. Clone the project into the persistent workspace. Include the submodules because Ceridwen is a submodule of this repository.

```
cd /workspace
git clone --recurse-submodules \
  https://github.com/potatoist314/cosmic-chronometers-jwst.git
cd cosmic-chronometers-jwst`
```

### Transfer private data

Run this command on the local computer. Replace `<INSTANCE_ID>` with the instance identifier. Git does not contain the LEGA-C spectra or matched photometry.

```
vastai copy "local:$PWD/data/raw" \
  "C.<INSTANCE_ID>:/workspace/cosmic-chronometers-jwst/data/"`
```

The required remote paths are:

- `data/raw/legac_dr2/legaCdr2.fits.gz`
- `data/raw/legac_dr2/sp/`
- `data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits`

The bootstrap uses the Ceridwen registry to download the published high-resolution SSP grid. The registry fixes the expected checksum.

### Bootstrap and verify

Run the maintained setup script from the remote project root:

```
bash scripts/bootstrap_vast_ai.sh`
```

The script removes the Vast system CUDA library path. JAX then uses the compatible CUDA libraries from its Python environment.

`scripts/bootstrap_vast_ai.sh:13-14`

```
# Use the CUDA libraries installed with JAX, not Vast's system CUDA libraries.
unset LD_LIBRARY_PATH`
```

The script creates an isolated Python 3.11 environment. It installs CUDA JAX, Ceridwen from the `ceridwen` submodule, and sedpy_jax from the `external/sedpy_jax` submodule. That sedpy_jax fork accepts the grid's wavelength-dependent resolution array and builds filters in NumPy, which keeps per-fit setup near 27 s. Both submodules install from the tree, so the bootstrap never fetches them from GitHub; a driver that provisions an instance copies both directories with the scripts. The script checks GPU float64 execution, runs the Ceridwen check, and registers the notebook kernel.

`scripts/bootstrap_vast_ai.sh:52-99`

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

The script checks 1,988 spectra. It also checks the catalogue and photometry row counts. It fetches the published schema-2.1 grid and loads it in strict mode. It checks shape `(5, 13, 107, 10992)`.

### Run the fixed benchmark

Run the benchmark after the bootstrap finishes. Replace the example Vast price, host, and instance values:

```
.venv-ceridwen-gpu/bin/python \
  scripts/benchmark_ceridwen_vast.py run \
  --price-usd-per-hour 0.670 \
  --vast-host 148498 \
  --vast-instance 48652928`
```

The workload uses M1_210210, 11 photometric bands, and 3,523 spectral pixels. It compiles one warm-up step. It then times five steps with 1,000 likelihood calls each.

The runner disables JAX's 75% memory reservation before it imports JAX. The Vast sweep therefore accepts 8 GB GPUs for this benchmark.

The runner saves JSON, CSV, and text results. It records input checksums, code versions, GPU metadata, memory use, throughput, and cost. The short run measures performance. It does not estimate a posterior.

The comparison fingerprint includes the workload, inputs, Ceridwen version, and software versions. Allocator settings and the script checksum remain provenance fields. They do not split otherwise equal runs. The summary command also accepts verified schema-v1 results.

Copy each result directory to the local project before you stop the instance. The summary command rejects files with different comparison fingerprints.

### Run the notebooks

1. Open JupyterLab on the Vast.ai instance.
2. Select `Ceridwen (Vast.ai GPU)` as the kernel.
3. Run `notebooks/ceridwen_test_spectra.ipynb` for spectra only.
4. Run `notebooks/ceridwen_integrated_photometry_spectra.ipynb` for the selectable combined fit.

The local CPU kernel and remote GPU kernel share the `ceridwen` identifier. Their visible names identify the active computer and backend.

The remote kernel requires CUDA and float64 for every notebook session. It also prevents the system CUDA path from replacing the installed JAX libraries.

#### Run the two DR2 shards

The runner selects 194 eligible spectra. It keeps the highest-S/N spectrum for each repeated object. This produces 187 targets. It sorts targets by decreasing S/N and alternates them between two shards.

Generate one shared manifest before the remote launch:

```
.venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --write-targets-file /workspace/ceridwen-dr2-targets.json`
```

Run M1_210210 first with the complete production settings:

```
.venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --targets-file /workspace/ceridwen-dr2-targets.json --shard-index 0 --only-target M1_210210`
```

After that result passes validation, run shard zero on the first instance and shard one on the second instance. The runner skips a valid completed target:

```
.venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --targets-file /workspace/ceridwen-dr2-targets.json --shard-index 0`
```

The other instance uses `--shard-index 1`. The full profile uses 500 live points, 65 slice steps, 100 deletions, and `logZ_tol=-5`. Seed `20260830 + manifest_index` identifies each target.

A shard runs one target at a time by default. `--fits-per-gpu N` runs N targets at once, each worker with `XLA_CLIENT_MEM_FRACTION = 0.85/N`, and the shard manifest records `fits_per_gpu`. Concurrent fits share the GPU by time-slicing. With the production sampler settings one fit already keeps the GPU busy: on an 8 GB RTX 4060 Ti three concurrent production fits each ran 3.1 times slower than the same fit alone, on an 8 GB RTX 3070 two and three concurrent fits summed to 0.96 to 0.97 of the single-fit throughput, and on Blackwell (RTX 5060 8 GB, RTX 5070 12 GB, RTX 5060 Ti 16 GB) they summed to 0.99 to 1.03 with no memory pressure. Leave the default unless a same-boot measurement with production settings shows headroom.

GPU memory does not set this limit. One production fit holds 0.8 to 1.0 GiB of JAX device memory; the default JAX preallocation reserves 75 percent of the card, which is what `nvidia-smi` reports. `XLA_CLIENT_MEM_FRACTION=0.14` (a 1,098 MiB pool on 8 GB) and `XLA_PYTHON_CLIENT_PREALLOCATE=false` both run a production fit at full speed; a 0.10 fraction fails in GEMM autotuning at compile time. A smaller pool changes the autotuned kernels and can shift a fit by one outer sampler iteration with the same ln Z within one sigma, so keep the allocator setting fixed inside one comparison.

Each target writes one executed notebook, two HDF5 files, and one execution log. Figures remain embedded in the notebook. The runner retries a failed target once with the same seed.

A periodic BlackJAX NSS checkpoint is a usable partial posterior. It cannot resume the sampler from the same point.

The local `--monitor` mode polls both shard manifests, downloads only completed four-file target products, validates them on the local computer, enforces the recorded credit cap, and destroys both production instances only after all 187 results pass.

`scripts/run_ceridwen_vast_multi_gpu.py:108-126 · build_target_manifest`

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

**Documented contract:** The function docstring selects one highest-S/N spectrum for each eligible object.

**Why it matters:** Repeat spectra cannot make one galaxy contribute more than one production fit.

### Preserve results and finish

1. Download each completed four-file target result with `rsync -aP`.
2. Load both HDF5 files on the local computer.
3. Open the executed notebook and check its embedded figures.
4. Stop or destroy the paid instance after you secure the files.

Do not use the rented computer as the permanent copy of a scientific result.

### Evidence

- `README.md:18-49` describes the instance, clone, transfer, bootstrap, and kernel workflow.
- `scripts/bootstrap_vast_ai.sh:8-14` fixes the requirements and isolates the CUDA libraries.
- `scripts/bootstrap_vast_ai.sh:52-94` installs and checks wavelength-dependent resolution support.
- `scripts/bootstrap_vast_ai.sh:97-119` configures the kernel and results root.
- `scripts/bootstrap_vast_ai.sh:122-168` checks the raw data and published grid.
- `scripts/run_ceridwen_vast_multi_gpu.py:37-137` selects and shards the 187 unique objects.
- `scripts/run_ceridwen_vast_multi_gpu.py:457-561` runs up to `fits_per_gpu` targets at once and records completion.
- `scripts/benchmark_ceridwen_vast.py:23-39` fixes the workload and sampler sizes.
- `scripts/benchmark_ceridwen_vast.py:662-713` excludes one warm-up step and measures five later steps.
- `scripts/benchmark_ceridwen_vast.py:770-775` disables JAX preallocation before JAX initializes CUDA.
- `scripts/benchmark_ceridwen_vast.py:154-216` defines schema-v2 and legacy comparison fingerprints.
- `.gitignore:23-24` keeps the LEGA-C spectra out of Git.
