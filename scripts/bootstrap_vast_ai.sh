#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
ENV_DIR="${PROJECT_ROOT}/.venv-ceridwen-gpu"
PYTHON_BIN="${ENV_DIR}/bin/python"
PYTHON_VERSION="3.11.16"
JAX_VERSION="0.10.2"
TFP_NIGHTLY_VERSION="0.26.0.dev20260810"
SEDPY_JAX_COMMIT="0291d58bd86fc0e401b2cdd8beae25d994d1ba0e"
MINIMUM_GPU_MEMORY_MIB="${CERIDWEN_MIN_GPU_MEMORY_MIB:-12000}"

# Use the CUDA libraries installed with JAX, not Vast's system CUDA libraries.
unset LD_LIBRARY_PATH

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "This bootstrap is for Linux Vast.ai instances." >&2
    exit 1
fi

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
fi

if [[ ! -f "${PROJECT_ROOT}/ceridwen/pyproject.toml" ]]; then
    git -C "${PROJECT_ROOT}" submodule update --init --recursive
fi

if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
else
    python3 -m pip install --user --upgrade uv
    UV_BIN="$(python3 -m site --user-base)/bin/uv"
fi

"${UV_BIN}" python install "${PYTHON_VERSION}"
if [[ ! -x "${PYTHON_BIN}" ]]; then
    "${UV_BIN}" venv "${ENV_DIR}" --python "${PYTHON_VERSION}"
fi

"${UV_BIN}" pip install --python "${PYTHON_BIN}" \
    "jax[cuda12]==${JAX_VERSION}" \
    "jaxlib==${JAX_VERSION}" \
    "${PROJECT_ROOT}/ceridwen" \
    "astroquery>=0.4.11,<0.5" \
    "corner>=2.3,<3" \
    "ipykernel>=7.3,<8" \
    "jupyterlab>=4.6,<5" \
    "nbclient>=0.10,<0.11" \
    "nbconvert>=7.17,<8" \
    "pandas>=3,<4" \
    "specutils>=2.2,<3"
"${UV_BIN}" pip install --python "${PYTHON_BIN}" --reinstall --no-deps \
    "tfp-nightly==${TFP_NIGHTLY_VERSION}"
"${UV_BIN}" pip install --python "${PYTHON_BIN}" --reinstall --no-deps \
    "sedpy-jax @ git+https://github.com/Espe13/sedpy_jax.git@${SEDPY_JAX_COMMIT}"
"${UV_BIN}" pip check --python "${PYTHON_BIN}"

JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "${PYTHON_BIN}" - <<'PY'
import jax
import jax.numpy as jnp

devices = jax.devices()
if not devices or any(device.platform != "gpu" for device in devices):
    raise SystemExit(f"Expected CUDA GPU devices, found {devices}")
value = jnp.ones(1, dtype=jnp.float64).block_until_ready()
if value.dtype != jnp.float64:
    raise SystemExit(f"JAX float64 is disabled: {value.dtype}")
print(f"JAX {jax.__version__}: {devices}; float64 verified")
PY

(
    cd /tmp
    JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "${PYTHON_BIN}" -m ceridwen.check
)

"${PYTHON_BIN}" - <<'PY'
import numpy as np
from sedpy_jax.smoothing import make_lsf_smoother

wave = np.linspace(4000.0, 5000.0, 128)
sigma = np.full(wave.shape, 2.0)
inres = np.full(wave.shape, 1.0)
make_lsf_smoother(wave, sigma, wave[::2], inres=inres)
print("sedpy_jax wavelength-dependent input resolution verified")
PY

"${PYTHON_BIN}" -m ipykernel install --user \
    --name ceridwen \
    --display-name "Ceridwen (Vast.ai GPU)"
KERNEL_JSON="$(
    "${PYTHON_BIN}" -c \
        'from jupyter_core.paths import jupyter_data_dir; from pathlib import Path; print(Path(jupyter_data_dir()) / "kernels" / "ceridwen" / "kernel.json")'
)"
"${PYTHON_BIN}" - "${KERNEL_JSON}" "${PROJECT_ROOT}" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
project_root = Path(sys.argv[2])
kernel = json.loads(path.read_text())
kernel["env"] = {
    **kernel.get("env", {}),
    "CERIDWEN_RESULTS_ROOT": str(project_root / "results"),
    "JAX_ENABLE_X64": "1",
    "JAX_PLATFORMS": "cuda",
    "LD_LIBRARY_PATH": "",
}
path.write_text(json.dumps(kernel, indent=2) + "\n")
PY

CATALOG_PATH="${PROJECT_ROOT}/data/raw/legac_dr2/legaCdr2.fits.gz"
PHOTOMETRY_PATH="${PROJECT_ROOT}/data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits"
SPECTRA_DIR="${PROJECT_ROOT}/data/raw/legac_dr2/sp"

missing=0
for path in "${CATALOG_PATH}" "${PHOTOMETRY_PATH}"; do
    if [[ ! -f "${path}" ]]; then
        echo "Missing required data: ${path#"${PROJECT_ROOT}/"}" >&2
        missing=1
    fi
done

SPECTRA_COUNT=0
if [[ -d "${SPECTRA_DIR}" ]]; then
    SPECTRA_COUNT="$(find "${SPECTRA_DIR}" -maxdepth 1 -type f -name 'legac_M*_v2.0.fits' | wc -l | tr -d ' ')"
fi
if [[ "${SPECTRA_COUNT}" != "1988" ]]; then
    echo "Expected 1988 LEGA-C spectra, found ${SPECTRA_COUNT}." >&2
    missing=1
fi

if (( missing != 0 )); then
    echo "Upload data/raw, then rerun this script." >&2
    exit 1
fi

"${PYTHON_BIN}" - "${CATALOG_PATH}" "${PHOTOMETRY_PATH}" <<'PY'
import sys

from astropy.table import Table
from ceridwen.ssps import SSPDataAfe, fetch_grid

catalog_path, photometry_path = sys.argv[1:]
catalog = Table.read(catalog_path)
photometry = Table.read(photometry_path)
grid_path = fetch_grid("amist_c3k_hr_krou_afe")
ssp = SSPDataAfe.load(grid_path)

if len(catalog) != 1988:
    raise SystemExit(f"Expected 1988 catalogue rows, found {len(catalog)}")
if len(photometry) != 1982:
    raise SystemExit(f"Expected 1982 photometry rows, found {len(photometry)}")
if ssp.ssp_flux.shape != (5, 13, 107, 10992):
    raise SystemExit(f"Unexpected SSP grid shape: {ssp.ssp_flux.shape}")
if ssp.schema_version != "2.1":
    raise SystemExit(f"Unexpected SSP grid schema: {ssp.schema_version}")
print(f"LEGA-C inputs and schema-2.1 HR SSP grid verified: {grid_path}")
PY

echo "Select the 'Ceridwen (Vast.ai GPU)' kernel in JupyterLab."
