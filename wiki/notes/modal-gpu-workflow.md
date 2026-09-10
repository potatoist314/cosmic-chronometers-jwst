---
title: Modal GPU workflow
date: 2026-08-28
section: Guides
theme: Compute
tags: [gpu, modal, ceridwen]
job: 
old: _old/guides/modal-gpu-workflow.html
status: obsolete
---

Operational guide

<details>
<summary>Details</summary>

Use batch mode for automatic execution. Use trace mode for GPU timing. Use Jupyter mode for interactive cells.

</details>

<details>
<summary>Mental model</summary>

- **A100 GPU**Numerical execution
- **Mounted Volumes**Inputs and results
- **JupyterLab**Optional browser interface

</details>

<figure>
<figcaption>The browser shows JupyterLab, but Python and JAX run inside the Sandbox.</figcaption>
</figure>

<details>
<summary>Details</summary>

A Sandbox is one active container. JupyterLab is one program in that container. The browser displays JupyterLab. Python and JAX run in the container.

Batch mode starts the same container type without Jupyter. It runs every notebook cell and saves the executed notebook. Modal then releases the GPU.

**Batch mode**

Run all cells, save the notebook, commit results, and release the GPU.

**Jupyter mode**

Keep the Sandbox active until Jupyter or the local command stops.

</details>

<figure>
<figcaption>Both modes use the same image, GPU, and mounted Volumes.</figcaption>
</figure>

<details>
<summary>Configure Modal</summary>

Run the authentication command once from the local project directory:

</details>

```
uvx --from modal==1.5.4 modal setup`
```

<details>
<summary>Details</summary>

The adapter uses Python 3.11 and CUDA JAX. It includes the local Ceridwen source, the two active notebooks, and the sedpy_jax fork from the `external/sedpy_jax` submodule, which accepts wavelength-dependent input resolution and builds filters in NumPy. By default, it requests one `A100-40GB`.

`archive/scripts/modal_ceridwen.py:60-62`

</details>

```
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")`
```

<details>
<summary>Upload inputs</summary>

Upload the raw catalogues, 1,988 spectra, and matched photometry:

</details>

```
uvx --from modal==1.5.4 modal run \
  archive/scripts/modal_ceridwen.py::upload`
```

<details>
<summary>Details</summary>

The adapter checks the local raw inputs and spectrum count. It then stores the published schema-2.1 grid in the input Volume. The adapter checks all row counts, the grid shape, and the fixed checksum.

The batch and Jupyter containers mount the input Volume as read-only. The notebooks cannot change the raw data.

`archive/scripts/modal_ceridwen.py:357-362`

</details>

```
with input_volume.batch_upload(force=True) as batch:
    batch.put_directory(raw_root, "/raw")
_fetch_grid.remote()
print(_validate_inputs.remote())`
```

<details>
<summary>Run a batch job</summary>

A batch job runs one notebook automatically. Quick mode is the default:

</details>

```
uvx --from modal==1.5.4 modal run \
  archive/scripts/modal_ceridwen.py::batch \
  --notebook spectra --profile quick \
  --spectrum-mode full`
```

<details>
<summary>Details</summary>

Use `--notebook joint` for the integrated fit. Use `--profile full` only for a production BlackJAX nested-sampling run.

For the joint notebook, select native pixels with `--fit-mode full_spectrum`. Select published absorption indices with `--fit-mode stellar_indices`.

For the spectra notebook, use `--spectrum-mode full` to fit all 3,523 valid pixels. Use `--spectrum-mode features` to fit 1,924 pixels from the LEGA-C feature bandpasses. Both modes compact the observation before model projection.

The local command stays connected to the remote job. Modal saves the source notebook and executed notebook in one timestamped results path.

Add `--detach` before the function name for a long run. Modal then continues the batch job if the local terminal disconnects:

</details>

```
uvx --from modal==1.5.4 modal run --detach \
  archive/scripts/modal_ceridwen.py::batch \
  --notebook spectra --profile full \
  --spectrum-mode features`
```

<details>
<summary>Details</summary>

The batch entry point creates a spawned Modal function call and then waits for its result. The spawned GPU call remains independent if the local entry point is canceled.

The notebook reads raw inputs from the mounted data Volume. It receives `CERIDWEN_PROJECT_ROOT=/workspace` so the physical Volume path cannot change data resolution. It locates the published grid through `CERIDWEN_GRID_DIR`. It writes checkpoints, both HDF5 output files, and execution timing to the results Volume.

`archive/scripts/modal_ceridwen.py:315-331 · _execute_notebook`

</details>

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

<details>
<summary>Details</summary>

**Documented contract:** The batch entry point documents complete notebook execution on one Modal GPU (`archive/scripts/modal_ceridwen.py:346-354`). It creates the detached function call at `archive/scripts/modal_ceridwen.py:365-375`.

**Why it matters:** The `finally` block commits outputs and timing after success or error. The persistent Volume outlives the GPU container.

</details>

<details>
<summary>Validated quick run</summary>

Run `batch-20260825T151156339684Z` completed on one A100-40GB. It used JAX 0.10.2, CUDA, and float64. All 14 code cells ran without notebook errors.

The BlackJAX NSS smoke fit used 16 live points, two inner steps, and eight deletions. It completed in 11.6 seconds after 128 likelihood calls.

This quick profile checks the Modal, data, GPU, and notebook path. Its posterior-weight ESS was 1.0. Therefore, this run is not a scientific fit.

`astro-ceridwen-results/batch-20260825T151156339684Z/ceridwen_test_spectra.executed.ipynb`

</details>

<details>
<summary>Use interactive Jupyter</summary>

Start a Jupyter Sandbox with a one-hour limit:

</details>

```
uvx --from modal==1.5.4 modal run \
  archive/scripts/modal_ceridwen.py::jupyter \
  --spectrum-mode full \
  --fit-mode stellar_indices`
```

<details>
<summary>Details</summary>

The terminal prints a private JupyterLab link. Keep the local command active while you use Jupyter.

Restart the Sandbox with `--spectrum-mode features` to run the compact feature fit. The adapter passes the choice through `CERIDWEN_SPECTRUM_MODE`.

Use `--fit-mode full_spectrum` or `stellar_indices` for the integrated notebook. The adapter passes this choice through `CERIDWEN_FIT_MODE`.

- **Interrupt** stops the current cell. The kernel, variables, Sandbox, GPU, and billing remain active.
- **Restart Kernel** clears Python memory. Saved notebook cells and outputs remain in the results Volume.
- **Shut Down Kernel** stops only the kernel. JupyterLab and the GPU container remain active.
- **Shut Down JupyterLab** ends the server. The adapter then terminates the Sandbox and releases the GPU.
- **Ctrl-C in the local terminal** also terminates the Sandbox and releases the GPU.

The one-hour limit terminates the Sandbox if the local stop path does not run. Use `--hours` to select a limit of up to 24 hours.

`archive/scripts/modal_ceridwen.py:490-499`

</details>

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

<details>
<summary>Details</summary>

`archive/scripts/modal_ceridwen.py:515-520 · jupyter`

</details>

```
try:
    sandbox.wait()
except KeyboardInterrupt:
    print("Stopping the Modal Sandbox")
finally:
    sandbox.terminate(wait=True)`
```

<details>
<summary>Details</summary>

**Documented contract:** The entry-point docstring defines an attached JupyterLab Sandbox on one Modal GPU (`archive/scripts/modal_ceridwen.py:443-450`).

**Why it matters:** Both normal interruption and errors reach `terminate`, which releases the paid GPU container.

</details>

<details>
<summary>Keep results</summary>

Each command prints its run identifier and download command. Replace the final path with a local destination:

</details>

```
uvx --from modal==1.5.4 modal volume get \
  astro-ceridwen-results <run-id> <destination>`
```

<details>
<summary>Details</summary>

The results Volume remains available after the batch container or Jupyter Sandbox stops. Each notebook also creates a UTC-stamped directory. Long runs write 20-minute checkpoints there. Every completed run writes a rescue snapshot and `ceridwen_result.h5`. The spectra notebook also writes `ceridwen_derived_outputs.h5`. The outer run directory contains `modal_execution_timing.json`.

</details>

<details>
<summary>Evidence</summary>

- `archive/scripts/modal_ceridwen.py:21-53` defines the Volume names, default GPU, versions, and notebook choices.
- `archive/scripts/modal_ceridwen.py:137-192` checks the catalogues, photometry, spectra, grid shape, and checksum.
- `archive/scripts/modal_ceridwen.py:232-262` fetches and checks the published grid on Modal.
- `archive/scripts/modal_ceridwen.py:265-325` runs the bounded batch job and saves the notebook output.
- `archive/scripts/modal_ceridwen.py:328-428` runs and saves the fixed A100 trace.
- `archive/scripts/modal_ceridwen.py:431-524` controls the Jupyter Sandbox, tunnel, timeout, and termination.
- `astro-ceridwen-results/batch-20260825T151156339684Z/ceridwen_test_spectra.executed.ipynb` contains the quick-run output on Modal.

</details>
