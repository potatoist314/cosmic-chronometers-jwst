---
title: Modal GPU workflow
date: 2026-08-28
section: Guides
tags: [gpu, modal, ceridwen]
job: 
old: _old/guides/modal-gpu-workflow.html
---

Operational guide

Use batch mode for automatic execution. Use trace mode for GPU timing. Use Jupyter mode for interactive cells.

### Mental model

- **A100 GPU**Numerical execution
- **Mounted Volumes**Inputs and results
- **JupyterLab**Optional browser interface

<figure>
<figcaption>The browser shows JupyterLab, but Python and JAX run inside the Sandbox.</figcaption>
</figure>

A Sandbox is one active container. JupyterLab is one program in that container. The browser displays JupyterLab. Python and JAX run in the container.

Batch mode starts the same container type without Jupyter. It runs every notebook cell and saves the executed notebook. Modal then releases the GPU.

**Batch mode**

Run all cells, save the notebook, commit results, and release the GPU.

**Jupyter mode**

Keep the Sandbox active until Jupyter or the local command stops.

<figure>
<figcaption>Both modes use the same image, GPU, and mounted Volumes.</figcaption>
</figure>

### Configure Modal

Run the authentication command once from the local project directory:

```
uvx --from modal==1.5.4 modal setup`
```

The adapter uses Python 3.11 and CUDA JAX. It includes the local Ceridwen source, the two active notebooks, and the sedpy_jax fork from the `external/sedpy_jax` submodule, which accepts wavelength-dependent input resolution and builds filters in NumPy. By default, it requests one `A100-40GB`.

`scripts/modal_ceridwen.py:60-62`

```
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")`
```

### Upload inputs

Upload the raw catalogues, 1,988 spectra, and matched photometry:

```
uvx --from modal==1.5.4 modal run \
  scripts/modal_ceridwen.py::upload`
```

The adapter checks the local raw inputs and spectrum count. It then stores the published schema-2.1 grid in the input Volume. The adapter checks all row counts, the grid shape, and the fixed checksum.

The batch and Jupyter containers mount the input Volume as read-only. The notebooks cannot change the raw data.

`scripts/modal_ceridwen.py:357-362`

```
with input_volume.batch_upload(force=True) as batch:
    batch.put_directory(raw_root, "/raw")
_fetch_grid.remote()
print(_validate_inputs.remote())`
```

### Run a batch job

A batch job runs one notebook automatically. Quick mode is the default:

```
uvx --from modal==1.5.4 modal run \
  scripts/modal_ceridwen.py::batch \
  --notebook spectra --profile quick \
  --spectrum-mode full`
```

Use `--notebook joint` for the integrated fit. Use `--profile full` only for a production BlackJAX nested-sampling run.

For the joint notebook, select native pixels with `--fit-mode full_spectrum`. Select published absorption indices with `--fit-mode stellar_indices`.

For the spectra notebook, use `--spectrum-mode full` to fit all 3,523 valid pixels. Use `--spectrum-mode features` to fit 1,924 pixels from the LEGA-C feature bandpasses. Both modes compact the observation before model projection.

The local command stays connected to the remote job. Modal saves the source notebook and executed notebook in one timestamped results path.

Add `--detach` before the function name for a long run. Modal then continues the batch job if the local terminal disconnects:

```
uvx --from modal==1.5.4 modal run --detach \
  scripts/modal_ceridwen.py::batch \
  --notebook spectra --profile full \
  --spectrum-mode features`
```

The batch entry point creates a spawned Modal function call and then waits for its result. The spawned GPU call remains independent if the local entry point is canceled.

The notebook reads raw inputs from the mounted data Volume. It receives `CERIDWEN_PROJECT_ROOT=/workspace` so the physical Volume path cannot change data resolution. It locates the published grid through `CERIDWEN_GRID_DIR`. It writes checkpoints, both HDF5 output files, and execution timing to the results Volume.

`scripts/modal_ceridwen.py:315-331 · _execute_notebook`

```
finally:
    execution_completed_at = datetime.now(UTC)
    execution_timing = {
        "notebook": notebook,
        "profile": profile,
        "spectrum_mode": spectrum_mode,
        "fit_mode": fit_mode,
        "status": execution_status,
        "started_at_utc": execution_started_at.isoformat(),
        "completed_at_utc": execution_completed_at.isoformat(),
        "wall_time_s": time.perf_counter() - execution_start_time,
    }
    nbformat.write(document, output_path)
    (REMOTE_NOTEBOOK_ROOT / "modal_execution_timing.json").write_text(
        json.dumps(execution_timing, indent=2) + "\n"
    )
    results_volume.commit()`
```

**Documented contract:** The batch entry point documents complete notebook execution on one Modal GPU (`scripts/modal_ceridwen.py:346-354`). It creates the detached function call at `scripts/modal_ceridwen.py:365-375`.

**Why it matters:** The `finally` block commits outputs and timing after success or error. The persistent Volume outlives the GPU container.

### Validated quick run

Run `batch-20260825T151156339684Z` completed on one A100-40GB. It used JAX 0.10.2, CUDA, and float64. All 14 code cells ran without notebook errors.

The BlackJAX NSS smoke fit used 16 live points, two inner steps, and eight deletions. It completed in 11.6 seconds after 128 likelihood calls.

This quick profile checks the Modal, data, GPU, and notebook path. Its posterior-weight ESS was 1.0. Therefore, this run is not a scientific fit.

`astro-ceridwen-results/batch-20260825T151156339684Z/ceridwen_test_spectra.executed.ipynb`

### Trace one sampler step

Run one fixed A100-40GB trace:

```
uvx --from modal==1.5.4 modal run \
  scripts/modal_ceridwen.py::trace`
```

The trace uses the matched M1_210210 workload. It initializes 300 live points and completes one warm-up step. It then records one BlackJAX NSS step with 1,000 likelihood calls.

JAX writes a compressed timeline and an XProf database to the results Volume. The command prints the download and rename commands.

Open a downloaded trace locally:

```
uvx --from xprof xprof \
  --logdir benchmarks/ceridwen/runs/ceridwen_modal_a100_kernel_trace_complete_2026-08-26/xprof`
```

The 26 August trace measured 127.5 calls/s. One reduction fusion used 93.8% of GPU event time. See the [kernel results](figures/ceridwen-gpu-benchmarks.html#kernel-trace).

`scripts/benchmark_ceridwen_vast.py:647-680 · run_traced_step`

`scripts/modal_ceridwen.py:328-351 · _execute_trace`

### Use interactive Jupyter

Start a Jupyter Sandbox with a one-hour limit:

```
uvx --from modal==1.5.4 modal run \
  scripts/modal_ceridwen.py::jupyter \
  --spectrum-mode full \
  --fit-mode stellar_indices`
```

The terminal prints a private JupyterLab link. Keep the local command active while you use Jupyter.

Restart the Sandbox with `--spectrum-mode features` to run the compact feature fit. The adapter passes the choice through `CERIDWEN_SPECTRUM_MODE`.

Use `--fit-mode full_spectrum` or `stellar_indices` for the integrated notebook. The adapter passes this choice through `CERIDWEN_FIT_MODE`.

- **Interrupt** stops the current cell. The kernel, variables, Sandbox, GPU, and billing remain active.
- **Restart Kernel** clears Python memory. Saved notebook cells and outputs remain in the results Volume.
- **Shut Down Kernel** stops only the kernel. JupyterLab and the GPU container remain active.
- **Shut Down JupyterLab** ends the server. The adapter then terminates the Sandbox and releases the GPU.
- **Ctrl-C in the local terminal** also terminates the Sandbox and releases the GPU.

The one-hour limit terminates the Sandbox if the local stop path does not run. Use `--hours` to select a limit of up to 24 hours.

`scripts/modal_ceridwen.py:490-499`

```
gpu=gpu,
cpu=4,
memory=16384,
timeout=int(hours * 3600),
volumes={
    REMOTE_DATA_ROOT: read_only_inputs,
    REMOTE_NOTEBOOK_ROOT: run_results,
},
encrypted_ports=[JUPYTER_PORT],
workdir=REMOTE_NOTEBOOK_ROOT.as_posix(),`
```

`scripts/modal_ceridwen.py:515-520 · jupyter`

```
try:
    sandbox.wait()
except KeyboardInterrupt:
    print("Stopping the Modal Sandbox")
finally:
    sandbox.terminate(wait=True)`
```

**Documented contract:** The entry-point docstring defines an attached JupyterLab Sandbox on one Modal GPU (`scripts/modal_ceridwen.py:443-450`).

**Why it matters:** Both normal interruption and errors reach `terminate`, which releases the paid GPU container.

### Keep results

Each command prints its run identifier and download command. Replace the final path with a local destination:

```
uvx --from modal==1.5.4 modal volume get \
  astro-ceridwen-results <run-id> <destination>`
```

The results Volume remains available after the batch container or Jupyter Sandbox stops. Each notebook also creates a UTC-stamped directory. Long runs write 20-minute checkpoints there. Every completed run writes a rescue snapshot and `ceridwen_result.h5`. The spectra notebook also writes `ceridwen_derived_outputs.h5`. The outer run directory contains `modal_execution_timing.json`.

### Evidence

- `scripts/modal_ceridwen.py:21-53` defines the Volume names, default GPU, versions, and notebook choices.
- `scripts/modal_ceridwen.py:137-192` checks the catalogues, photometry, spectra, grid shape, and checksum.
- `scripts/modal_ceridwen.py:232-262` fetches and checks the published grid on Modal.
- `scripts/modal_ceridwen.py:265-325` runs the bounded batch job and saves the notebook output.
- `scripts/modal_ceridwen.py:328-428` runs and saves the fixed A100 trace.
- `scripts/modal_ceridwen.py:431-524` controls the Jupyter Sandbox, tunnel, timeout, and termination.
- `astro-ceridwen-results/batch-20260825T151156339684Z/ceridwen_test_spectra.executed.ipynb` contains the quick-run output on Modal.
