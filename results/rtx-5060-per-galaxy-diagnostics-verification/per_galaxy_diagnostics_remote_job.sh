#!/usr/bin/env bash
set -u
cd /workspace/cosmic-chronometers-jwst
export JAX_ENABLE_X64=1 LD_LIBRARY_PATH=
OUT=results/rtx-5060-per-galaxy-diagnostics-verification
mkdir -p "$OUT"
echo "started $(date -u +%FT%TZ)" > "$OUT/REMOTE_STATUS"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader > "$OUT/gpu.txt" 2>&1
JAX_PLATFORMS=cpu .venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --targets-file "$OUT/targets.json" --shard-index 0 --only-target M1_210210 --output-root "$OUT" --max-attempts 1 > "$OUT/run_M1_210210.log" 2>&1
echo "refit M1_210210 exit $?" >> "$OUT/REMOTE_STATUS"
JAX_PLATFORMS=cpu .venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py --targets-file "$OUT/targets.json" --shard-index 1 --only-target M2_139662 --output-root "$OUT" --max-attempts 1 > "$OUT/run_M2_139662.log" 2>&1
echo "refit M2_139662 exit $?" >> "$OUT/REMOTE_STATUS"
: > "$OUT/gpu_lnl_check.log"
JAX_PLATFORMS=cuda .venv-ceridwen-gpu/bin/python scripts/per_galaxy_diagnostics.py check results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210 >> "$OUT/gpu_lnl_check.log" 2>&1
JAX_PLATFORMS=cuda .venv-ceridwen-gpu/bin/python scripts/per_galaxy_diagnostics.py check results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662 >> "$OUT/gpu_lnl_check.log" 2>&1
for d in "$OUT"/*/; do [ -f "$d/ceridwen_result.h5" ] && JAX_PLATFORMS=cuda .venv-ceridwen-gpu/bin/python scripts/per_galaxy_diagnostics.py check "$d" >> "$OUT/gpu_lnl_check.log" 2>&1; done
echo "finished $(date -u +%FT%TZ)" >> "$OUT/REMOTE_STATUS"
touch "$OUT/REMOTE_DONE"
