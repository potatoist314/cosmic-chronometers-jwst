"""Run the Ceridwen notebooks on Modal without changing the notebooks."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shlex
import shutil
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import modal

APP_NAME = "astro-ceridwen"
INPUT_VOLUME_NAME = "astro-ceridwen-inputs"
RESULTS_VOLUME_NAME = "astro-ceridwen-results"
DEFAULT_GPU = "A100-40GB"

JAX_VERSION = "0.10.2"
TFP_NIGHTLY_VERSION = "0.26.0.dev20260810"
GRID_NAME = "amist_c3k_hr_krou_afe.h5"
GRID_SHA256 = "f6af03d813569f5982891d969f030d9345278a60de907b90b2a910d56af32a16"
EXPECTED_SPECTRA = 1988
EXPECTED_CATALOG_ROWS = 1988
EXPECTED_PHOTOMETRY_ROWS = 1982
EXPECTED_GRID_SHAPE = (5, 13, 107, 10992)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REMOTE_NOTEBOOK_SOURCE = Path("/opt/astro/notebooks")
REMOTE_DATA_ROOT = Path("/workspace/data")
REMOTE_NOTEBOOK_ROOT = Path("/workspace/notebooks")
REMOTE_GRID_PATH = REMOTE_DATA_ROOT / "ceridwen" / GRID_NAME
JUPYTER_PORT = 8888

NOTEBOOKS = {
    "spectra": "ceridwen_test_spectra.ipynb",
    "joint": "ceridwen_integrated_photometry_spectra.ipynb",
}
PROFILES = {"quick", "full"}
SPECTRUM_MODES = {"full", "features"}
FIT_MODES = {"full_spectrum", "stellar_indices"}


def _ignore_python_cache(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}


image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")
    .add_local_dir(
        PROJECT_ROOT / "ceridwen" / "ceridwen",
        "/opt/ceridwen/ceridwen",
        copy=True,
        ignore=_ignore_python_cache,
    )
    .add_local_file(
        PROJECT_ROOT / "ceridwen" / "pyproject.toml",
        "/opt/ceridwen/pyproject.toml",
        copy=True,
    )
    .add_local_file(
        PROJECT_ROOT / "ceridwen" / "README.md",
        "/opt/ceridwen/README.md",
        copy=True,
    )
    .add_local_file(
        PROJECT_ROOT / "ceridwen" / "LICENSE",
        "/opt/ceridwen/LICENSE",
        copy=True,
    )
    # The sedpy_jax fork (NumPy filter construction) ships with the project as
    # a submodule; install it from the tree like ceridwen.
    .add_local_dir(
        PROJECT_ROOT / "external" / "sedpy_jax",
        "/opt/sedpy_jax",
        copy=True,
        ignore=_ignore_python_cache,
    )
    .uv_pip_install(
        f"jax[cuda12]=={JAX_VERSION}",
        f"jaxlib=={JAX_VERSION}",
        "/opt/ceridwen",
        "astroquery>=0.4.11,<0.5",
        "ipykernel>=7.3,<8",
        "jupyterlab>=4.6,<5",
        "nbclient>=0.10,<0.11",
        "pandas>=3,<4",
        "specutils>=2.2,<3",
    )
    .uv_pip_install(
        f"tfp-nightly=={TFP_NIGHTLY_VERSION}",
        extra_options="--reinstall --no-deps",
    )
    .uv_pip_install(
        "/opt/sedpy_jax",
        extra_options="--reinstall --no-deps",
    )
    .env(
        {
            "JAX_ENABLE_X64": "1",
            "JAX_PLATFORMS": "cuda",
            "CERIDWEN_GRID_DIR": str(REMOTE_GRID_PATH.parent),
            "CERIDWEN_PROJECT_ROOT": str(REMOTE_NOTEBOOK_ROOT.parent),
            "CERIDWEN_RESULTS_ROOT": str(REMOTE_NOTEBOOK_ROOT),
            "XLA_PYTHON_CLIENT_PREALLOCATE": "false",
        }
    )
    .run_commands("mkdir -p /opt/astro/notebooks /workspace")
    .add_local_file(
        PROJECT_ROOT / "notebooks" / NOTEBOOKS["spectra"],
        f"/opt/astro/notebooks/{NOTEBOOKS['spectra']}",
        copy=True,
    )
    .add_local_file(
        PROJECT_ROOT / "notebooks" / NOTEBOOKS["joint"],
        f"/opt/astro/notebooks/{NOTEBOOKS['joint']}",
        copy=True,
    )
)

app = modal.App(APP_NAME)
input_volume = modal.Volume.from_name(INPUT_VOLUME_NAME, create_if_missing=True)
results_volume = modal.Volume.from_name(RESULTS_VOLUME_NAME, create_if_missing=True)
read_only_inputs = input_volume.with_mount_options(read_only=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _local_input_paths() -> Path:
    raw_root = PROJECT_ROOT / "data" / "raw"
    required = (
        raw_root / "legac_dr2" / "legaCdr2.fits.gz",
        raw_root / "cosmos2015" / "cosmos2015_legac_dr2_photometry_1arcsec.fits",
    )
    missing = [path for path in required if not path.is_file()]
    if missing:
        names = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
        raise FileNotFoundError(f"Missing required input files: {names}")

    spectra = tuple((raw_root / "legac_dr2" / "sp").glob("legac_M*_v2.0.fits"))
    if len(spectra) != EXPECTED_SPECTRA:
        raise ValueError(f"Expected {EXPECTED_SPECTRA} spectra, found {len(spectra)}")
    return raw_root


def _validate_input_paths(raw_root: Path, grid_path: Path) -> None:
    import h5py
    from astropy.table import Table

    catalog = Table.read(raw_root / "legac_dr2" / "legaCdr2.fits.gz")
    photometry = Table.read(
        raw_root / "cosmos2015" / "cosmos2015_legac_dr2_photometry_1arcsec.fits"
    )
    spectra = tuple((raw_root / "legac_dr2" / "sp").glob("legac_M*_v2.0.fits"))
    with h5py.File(grid_path, "r") as grid:
        grid_shape = grid["ssp_flux"].shape
        grid_schema = str(grid.attrs.get("schema_version", ""))
        has_resolution = "ssp_resolution" in grid

    if len(catalog) != EXPECTED_CATALOG_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_CATALOG_ROWS} catalogue rows, found {len(catalog)}"
        )
    if len(photometry) != EXPECTED_PHOTOMETRY_ROWS:
        raise ValueError(
            "Expected "
            f"{EXPECTED_PHOTOMETRY_ROWS} photometry rows, found {len(photometry)}"
        )
    if len(spectra) != EXPECTED_SPECTRA:
        raise ValueError(f"Expected {EXPECTED_SPECTRA} spectra, found {len(spectra)}")
    if grid_shape != EXPECTED_GRID_SHAPE:
        raise ValueError(f"Unexpected SSP grid shape: {grid_shape}")
    if grid_schema != "2.1" or not has_resolution:
        raise ValueError("High-resolution SSP grid does not use schema 2.1")
    if _sha256(grid_path) != GRID_SHA256:
        raise ValueError("High-resolution SSP grid checksum mismatch")


def _validate_choice(value: str, choices: set[str] | dict[str, str], name: str) -> str:
    if value not in choices:
        valid = ", ".join(sorted(choices))
        raise ValueError(f"Unknown {name} {value!r}; choose {valid}")
    return value


def _run_id(mode: str) -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{mode}-{timestamp}"


def _profile_environment(
    profile: str,
    spectrum_mode: str,
    fit_mode: str,
) -> dict[str, str]:
    _validate_choice(profile, PROFILES, "profile")
    _validate_choice(spectrum_mode, SPECTRUM_MODES, "spectrum mode")
    _validate_choice(fit_mode, FIT_MODES, "fit mode")
    return {
        "CERIDWEN_GRID_DIR": str(REMOTE_GRID_PATH.parent),
        "CERIDWEN_FIT_MODE": fit_mode,
        "CERIDWEN_NOTEBOOK_QUICK": "1" if profile == "quick" else "0",
        "CERIDWEN_PROJECT_ROOT": str(REMOTE_NOTEBOOK_ROOT.parent),
        "CERIDWEN_RESULTS_ROOT": str(REMOTE_NOTEBOOK_ROOT),
        "CERIDWEN_SPECTRUM_MODE": spectrum_mode,
    }


def _verify_gpu() -> str:
    import jax
    import jax.numpy as jnp

    devices = jax.devices()
    if not devices or any(device.platform != "gpu" for device in devices):
        raise RuntimeError(f"Expected CUDA GPU devices, found {devices}")
    value = jnp.ones(1, dtype=jnp.float64).block_until_ready()
    if value.dtype != jnp.float64:
        raise RuntimeError(f"JAX float64 is disabled: {value.dtype}")
    return f"JAX {jax.__version__}: {devices}; float64 verified"


@app.function(
    image=image,
    cpu=2,
    memory=4096,
    volumes={REMOTE_DATA_ROOT: input_volume},
    max_containers=1,
    scaledown_window=2,
    timeout=1800,
)
def _fetch_grid() -> str:
    os.environ["JAX_PLATFORMS"] = "cpu"
    from ceridwen.ssps import fetch_grid

    force = REMOTE_GRID_PATH.is_file() and _sha256(REMOTE_GRID_PATH) != GRID_SHA256
    path = fetch_grid("amist_c3k_hr_krou_afe", force=force)
    input_volume.commit()
    return f"Published schema-2.1 HR SSP grid ready: {path}"


@app.function(
    image=image,
    cpu=2,
    memory=4096,
    volumes={REMOTE_DATA_ROOT: read_only_inputs},
    max_containers=1,
    scaledown_window=2,
    timeout=1800,
)
def _validate_inputs() -> str:
    _validate_input_paths(REMOTE_DATA_ROOT / "raw", REMOTE_GRID_PATH)
    return "LEGA-C catalogue, photometry, spectra, and HR SSP grid verified"


@app.function(
    image=image,
    cpu=4,
    memory=16384,
    max_containers=1,
    scaledown_window=2,
    timeout=86400,
)
def _execute_notebook(
    notebook: str,
    profile: str,
    spectrum_mode: str,
    fit_mode: str,
) -> str:
    import nbformat
    from nbclient import NotebookClient

    notebook = _validate_choice(notebook, NOTEBOOKS, "notebook")
    _validate_choice(profile, PROFILES, "profile")
    _validate_choice(spectrum_mode, SPECTRUM_MODES, "spectrum mode")
    _validate_choice(fit_mode, FIT_MODES, "fit mode")
    if notebook != "spectra" and spectrum_mode != "full":
        raise ValueError("features mode is available only for the spectra notebook")
    if notebook != "joint" and fit_mode != "full_spectrum":
        raise ValueError("stellar_indices mode is available only for the joint notebook")
    _validate_input_paths(REMOTE_DATA_ROOT / "raw", REMOTE_GRID_PATH)
    print(_verify_gpu())

    os.environ.update(_profile_environment(profile, spectrum_mode, fit_mode))
    source_name = NOTEBOOKS[notebook]
    source_path = REMOTE_NOTEBOOK_ROOT / source_name
    output_path = REMOTE_NOTEBOOK_ROOT / source_name.replace(
        ".ipynb", ".executed.ipynb"
    )
    shutil.copy2(REMOTE_NOTEBOOK_SOURCE / source_name, source_path)

    document = nbformat.read(source_path, as_version=4)
    client = NotebookClient(
        document,
        timeout=None,
        kernel_name="python3",
        resources={"metadata": {"path": str(REMOTE_NOTEBOOK_ROOT)}},
    )
    execution_started_at = datetime.now(UTC)
    execution_start_time = time.perf_counter()
    execution_status = "interrupted"
    try:
        client.execute()
        execution_status = "completed"
    except Exception as exc:
        execution_status = "failed"
        raise RuntimeError(f"Notebook execution failed: {exc}") from None
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
        results_volume.commit()
    return output_path.name


@app.local_entrypoint(name="upload")
def upload() -> None:
    """Upload immutable notebook inputs, then validate the remote copy."""
    raw_root = _local_input_paths()
    with input_volume.batch_upload(force=True) as batch:
        batch.put_directory(raw_root, "/raw")
    print(_fetch_grid.remote())
    print(_validate_inputs.remote())
    print(f"Inputs uploaded to Modal Volume {INPUT_VOLUME_NAME!r}")


@app.local_entrypoint(name="batch")
def batch(
    notebook: str = "spectra",
    profile: str = "quick",
    spectrum_mode: str = "full",
    fit_mode: str = "full_spectrum",
    gpu: str = DEFAULT_GPU,
) -> None:
    """Execute one notebook from start to finish on one Modal GPU."""
    _validate_choice(notebook, NOTEBOOKS, "notebook")
    _validate_choice(profile, PROFILES, "profile")
    _validate_choice(spectrum_mode, SPECTRUM_MODES, "spectrum mode")
    _validate_choice(fit_mode, FIT_MODES, "fit mode")
    if notebook != "spectra" and spectrum_mode != "full":
        raise ValueError("features mode is available only for the spectra notebook")
    if notebook != "joint" and fit_mode != "full_spectrum":
        raise ValueError("stellar_indices mode is available only for the joint notebook")
    print(_validate_inputs.remote())

    analysis_mode = fit_mode if notebook == "joint" else spectrum_mode
    run_id = _run_id(f"batch-{analysis_mode}")
    run_results = results_volume.with_mount_options(sub_path=run_id)
    print(f"Starting Modal run {run_id!r}")
    function_call = _execute_notebook.with_options(
        gpu=gpu,
        volumes={
            REMOTE_DATA_ROOT: read_only_inputs,
            REMOTE_NOTEBOOK_ROOT: run_results,
        },
    ).spawn(notebook, profile, spectrum_mode, fit_mode)
    print(f"Modal function call {function_call.object_id!r}")
    output_name = function_call.get()
    print(f"Completed Modal run {run_id!r}: {output_name}")
    print(
        "Download with: uvx modal volume get "
        f"{RESULTS_VOLUME_NAME} {run_id} <destination>"
    )


def _jupyter_is_ready(base_url: str, token: str) -> bool:
    status_url = f"{base_url.rstrip('/')}/api/status?token={token}"
    try:
        with urllib.request.urlopen(status_url, timeout=5) as response:
            if response.status != 200:
                return False
            status = json.loads(response.read().decode())
    except OSError:
        return False
    return bool(status.get("started"))


@app.local_entrypoint(name="jupyter")
def jupyter(
    profile: str = "quick",
    spectrum_mode: str = "full",
    fit_mode: str = "full_spectrum",
    gpu: str = DEFAULT_GPU,
    hours: float = 1.0,
) -> None:
    """Start an attached JupyterLab Sandbox on one Modal GPU."""
    _validate_choice(profile, PROFILES, "profile")
    _validate_choice(spectrum_mode, SPECTRUM_MODES, "spectrum mode")
    _validate_choice(fit_mode, FIT_MODES, "fit mode")
    if not 0 < hours <= 24:
        raise ValueError("hours must be greater than 0 and not greater than 24")
    print(_validate_inputs.remote())

    run_id = _run_id(f"jupyter-{spectrum_mode}-{fit_mode}")
    run_results = results_volume.with_mount_options(sub_path=run_id)
    token = secrets.token_urlsafe(24)
    token_secret = modal.Secret.from_dict({"JUPYTER_TOKEN": token})
    gpu_check = (
        "import jax; import jax.numpy as jnp; "
        "devices = jax.devices(); "
        "assert devices and all(device.platform == 'gpu' for device in devices), devices; "
        "value = jnp.ones(1, dtype=jnp.float64).block_until_ready(); "
        "assert value.dtype == jnp.float64, value.dtype; "
        "print(f'JAX {jax.__version__}: {devices}; float64 verified')"
    )
    command = (
        f"python -c {shlex.quote(gpu_check)} && "
        "python -m ceridwen.check && "
        "cp -n /opt/astro/notebooks/*.ipynb /workspace/notebooks/ && "
        "exec jupyter lab --no-browser --allow-root --ip=0.0.0.0 "
        f"--port={JUPYTER_PORT} --ServerApp.allow_origin='*' "
        "--ServerApp.allow_remote_access=True "
        '--IdentityProvider.token="$JUPYTER_TOKEN" '
        "--ServerApp.root_dir=/workspace/notebooks"
    )

    print(f"Starting Modal Jupyter run {run_id!r}")
    with modal.enable_output():
        sandbox = modal.Sandbox.create(
            "bash",
            "-lc",
            command,
            app=app,
            image=image,
            env=_profile_environment(profile, spectrum_mode, fit_mode),
            secrets=[token_secret],
            gpu=gpu,
            cpu=4,
            memory=16384,
            timeout=int(hours * 3600),
            volumes={
                REMOTE_DATA_ROOT: read_only_inputs,
                REMOTE_NOTEBOOK_ROOT: run_results,
            },
            encrypted_ports=[JUPYTER_PORT],
            workdir=REMOTE_NOTEBOOK_ROOT.as_posix(),
        )

    tunnel = sandbox.tunnels()[JUPYTER_PORT]
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if _jupyter_is_ready(tunnel.url, token):
            break
        time.sleep(1)
    else:
        sandbox.terminate(wait=True)
        raise RuntimeError("Jupyter did not become ready within 60 seconds")

    print(f"JupyterLab: {tunnel.url.rstrip('/')}/lab?token={token}")
    print("Use Jupyter to interrupt or restart the kernel.")
    print("Press Ctrl-C here to stop the Sandbox and release the GPU.")
    try:
        sandbox.wait()
    except KeyboardInterrupt:
        print("Stopping the Modal Sandbox")
    finally:
        sandbox.terminate(wait=True)
    print(
        "Download with: uvx modal volume get "
        f"{RESULTS_VOLUME_NAME} {run_id} <destination>"
    )
