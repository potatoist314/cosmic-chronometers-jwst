#!/usr/bin/env python3
"""Refit stored DR2 targets under the static-smoothing change, same seeds.

Importance reweighting can only re-balance samples the old chain already
visited.  This runs the sampler afresh under the new likelihood, with each
target's original seed, so the comparison against the stored posterior is a real
one.

The instance is stopped, never destroyed: it holds the production results.
"""
from __future__ import annotations
import argparse, json, shlex, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
import sweep_ceridwen_vast_gpus as S  # noqa: E402

REMOTE = "/workspace/cosmic-chronometers-jwst"
OUT_SUBDIR = "results/refit-static-smoothing"


def _log(m): print(datetime.now(timezone.utc).strftime("%H:%M:%S"), m, flush=True)


def _wait_running(iid, limit=40):
    for _ in range(limit):
        if S._instance_state(iid).get("actual_status") == "running":
            return
        time.sleep(15)
    raise S.SweepError("instance did not reach running")


def _install(iid, target, port):
    """Install the ceridwen tree this checkout carries, then prove it is imported.

    The bootstrap installs ceridwen NON-editable, so the source tree on the
    instance is not what a fit imports.  Sync the package, reinstall through the
    bootstrap, and stop if the combined static smoother is still absent.
    """
    for rel in ("ceridwen/ceridwen/", "ceridwen/pyproject.toml"):
        S._rsync(port, str(PROJECT / rel), f"{target}:{REMOTE}/{rel}", timeout=600.0)
    S._bootstrap(iid, _log)
    probe = S._ssh(iid, f"cd {shlex.quote(REMOTE)} && LD_LIBRARY_PATH= JAX_PLATFORMS=cpu "
        ".venv-ceridwen-gpu/bin/python -c \""
        "from ceridwen.observation._smoothing import make_static_smoother; print('SMOOTHER_LIVE')\"",
        timeout=600.0).stdout
    if "SMOOTHER_LIVE" not in probe:
        raise S.SweepError("the installed ceridwen lacks the combined static smoother")
    _log("combined static smoother installed")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--instance", type=int, required=True)
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    iid = args.instance
    targets = json.loads(args.targets.read_text())
    if args.limit: targets = targets[:args.limit]

    st = S._instance_state(iid)
    _log(f"instance {iid} ({st.get('gpu_name')}) ${float(st['dph_total']):.4f}/hr, "
         f"{len(targets)} targets")
    started = time.time()
    report = {"schema_version": 1, "vast_instance": iid, "gpu_name": st.get("gpu_name"),
              "price_usd_per_hour": float(st["dph_total"]),
              "ceridwen_commit": subprocess.run(
                  ["git", "-C", str(PROJECT / "ceridwen"), "rev-parse", "--short", "HEAD"],
                  capture_output=True, text=True, check=True).stdout.strip(),
              "started_at_utc": datetime.now(timezone.utc).isoformat(), "fits": []}
    try:
        if st.get("actual_status") != "running":
            S._vastai(["start", "instance", str(iid)]); _wait_running(iid)
        S._attach_ssh_key(iid); S._wait_for_ssh(iid, _log)
        target_host, port = S._ssh_target(iid)
        _install(iid, target_host, port)

        # A previous driver may have been killed while a remote fit kept
        # running: the fit is launched over ssh but is not a child of the
        # driver, so it survives.  Wait for it rather than starting a second
        # fit on the same GPU.
        for _ in range(90):
            # The bracket stops pgrep matching the ssh wrapper that carries this
            # very pattern on its own command line.
            busy = S._ssh(iid, "pgrep -f '[r]un_ceridwen_vast_multi_gpu' >/dev/null "
                               "&& echo BUSY || echo FREE", timeout=120.0).stdout
            if "FREE" in busy: break
            _log("a fit from an earlier driver is still running; waiting")
            time.sleep(60)

        for k, t in enumerate(targets, 1):
            gid = t["spect_id"]
            rdir = f"{REMOTE}/{OUT_SUBDIR}/{t['object_id']}-{gid}"
            done = S._ssh(iid, f"test -f {shlex.quote(rdir)}/ceridwen_result.h5 "
                               "&& echo yes || echo no", timeout=120.0).stdout.strip()
            if done.endswith("yes"):
                _log(f"[{k}/{len(targets)}] {gid} already complete, skipping")
                report["fits"].append(dict(spect_id=gid, seed=t["seed"],
                                           status="complete", wall_seconds=None,
                                           result_dir=rdir, resumed=True))
                continue
            env = " ".join([
                "LD_LIBRARY_PATH=", "JAX_PLATFORMS=cuda", "JAX_ENABLE_X64=1",
                "CUDA_DEVICE_ORDER=PCI_BUS_ID", "CUDA_VISIBLE_DEVICES=0",
                "CERIDWEN_EXPECT_SINGLE_GPU=1", "CERIDWEN_FIT_MODE=full_spectrum",
                "CERIDWEN_NOTEBOOK_QUICK=0", f"CERIDWEN_PROJECT_ROOT={REMOTE}",
                f"CERIDWEN_RANDOM_SEED={t['seed']}", f"CERIDWEN_RESULT_DIR={rdir}",
                f"CERIDWEN_TARGET_ID={gid}", f"CERIDWEN_OBJECT_ID={t['object_id']}",
                f"CERIDWEN_MANIFEST_INDEX={t['manifest_index']}",
            ])
            t0 = time.time()
            _log(f"[{k}/{len(targets)}] fitting {gid} (seed {t['seed']})")
            try:
                S._ssh(iid, f"mkdir -p {shlex.quote(rdir)} && cd {shlex.quote(REMOTE)} && "
                            f"{env} .venv-ceridwen-gpu/bin/python "
                            f"scripts/run_ceridwen_vast_multi_gpu.py --worker-output "
                            f"{shlex.quote(rdir)}/{gid}_executed.ipynb "
                            f"> {shlex.quote(rdir)}/execution.log 2>&1",
                       timeout=5400.0)
                ok = S._ssh(iid, f"test -f {shlex.quote(rdir)}/ceridwen_result.h5 "
                                 "&& echo yes || echo no", timeout=120.0).stdout.strip()
                status = "complete" if ok.endswith("yes") else "missing_result"
            except Exception as e:  # noqa: BLE001
                status = f"failed: {type(e).__name__}"
            dt = time.time() - t0
            report["fits"].append(dict(spect_id=gid, seed=t["seed"], status=status,
                                       wall_seconds=dt, result_dir=rdir))
            _log(f"[{k}/{len(targets)}] {gid} {status} in {dt/60:.1f} min")
            # Pull immediately: an interrupted driver must not cost completed work.
            if status == "complete":
                local = PROJECT / OUT_SUBDIR
                local.mkdir(parents=True, exist_ok=True)
                try:
                    S._rsync(port, f"{target_host}:{rdir}", f"{local}/", timeout=1800.0)
                except Exception as e:  # noqa: BLE001
                    _log(f"download of {gid} failed, will retry at the end: {e}")

        done = [f for f in report["fits"] if f["status"] == "complete"]
        _log(f"downloading {len(done)} results")
        local = PROJECT / OUT_SUBDIR
        local.mkdir(parents=True, exist_ok=True)
        S._rsync(port, f"{target_host}:{REMOTE}/{OUT_SUBDIR}/", f"{local}/", timeout=3600.0)
    finally:
        report["elapsed_seconds"] = time.time() - started
        report["cost_usd"] = report["elapsed_seconds"]/3600.0*float(st["dph_total"])
        out = PROJECT / "benchmarks/ceridwen/runs"
        out.mkdir(parents=True, exist_ok=True)
        p = out / ("refit_static_smoothing_"
                   + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".json")
        p.write_text(json.dumps(report, indent=2, default=str))
        _log(f"report: {p}")
        _log(f"elapsed {report['elapsed_seconds']/60:.1f} min, cost ${report['cost_usd']:.3f}")
        _log(f"stopping instance {iid}")
        S._vastai(["stop", "instance", str(iid)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
