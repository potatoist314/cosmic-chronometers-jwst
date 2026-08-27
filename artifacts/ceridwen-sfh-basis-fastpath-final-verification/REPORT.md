# Ceridwen SFH-basis fast-path final verification

Generated at 2026-08-27T21:55:46Z.

## Scope and immutable state

- This bridge task is `task_aITNOSz5SdVtDx7a`.
- This task did not resume or steer `task_gYnS22H3R2XblM6O`.
- The target branch is `experiment/ceridwen-sfh-basis-fastpath`.
- The target branch resolves to parent commit `1e0b7e95eb72ef315d9ef4f53bbfdc3cf13b70e3`.
- The parent tree is `2364505d49bb53488576d4d2c220312ad7b94143`.
- The parent tree records Ceridwen gitlink `80ca35dd1f3adcca716efd82b9d91240c8e76c9e`.
- The task used that parent and that Ceridwen checkout without code changes.
- This task did not create a nested-repository worker.
- This task did not clean, stash, push, merge, or land changes to `main`.
- This task did not write to the main checkout.

The first local submodule command could not read the isolated submodule tree.
One retry produced the same result. The task then used verified local Git objects.
The checkout reached the recorded gitlink without a fetch or a code change.

## Supplied smoke artifact

The task checked the source SHA-256 before it copied the source.

| Item | Result |
|---|---|
| Required SHA-256 | `346d9eea45d7f485d8d72bc578807bda7b2aeaf966c767d935076d432e539977` |
| Source SHA-256 | Match |
| Copied SHA-256 | Match |
| Byte comparison | Match |
| Source bytes | 13,270 |
| Copied bytes | 13,270 |

## Verification results

| Check | Outcome |
|---|---|
| Harness readiness | 11 passed |
| Parent regression tests | 61 passed |
| Ceridwen focused regression tests | 19 passed |
| Parent Ruff check | Passed |
| Ceridwen Ruff check | Passed |
| Live CPU numerical-equivalence harness | Passed |
| Live StableHLO check | Passed |
| Preserved smoke-artifact assertions | Passed |

The live harness and the supplied artifact have the same numerical maxima.
They also have the same StableHLO counts and StableHLO hashes.

| Measurement | Verified value |
|---|---|
| Maximum prediction relative delta | `2.2081381700900238e-07` |
| Maximum log-likelihood relative delta | `3.2281766627231943e-07` |
| Baseline forbidden expansion count | 15 |
| Variant A forbidden expansion count | 0 |
| Variant B forbidden expansion count | 0 |
| Preserved baseline CPU rate | 220.78812894155755 calls/s, rounded to 221 |
| Preserved variant A CPU rate | 618.5087519474804 calls/s, rounded to 619 |
| Preserved variant B CPU rate | 531.3318275105612 calls/s, rounded to 531 |
| Live baseline CPU rate | 170.07224763689842 calls/s |
| Live variant A CPU rate | 686.3613599423037 calls/s |
| Live variant B CPU rate | 537.5743111869909 calls/s |

The live smoke timing uses only two timed calls for each implementation.
It verifies function and output identity. It is not a stable performance estimate.

The first direct harness invocation failed before it imported the harness.
The direct file entry point did not put the repository root on `sys.path`.
The module entry point then ran the same immutable harness successfully.
No code changed to obtain this result.

## Input identity

| Input | Identity |
|---|---|
| Target | `M1_210210` |
| Redshift | `0.65420001745224` |
| Velocity dispersion | `259.5 km/s` |
| Photometric bands | 11 |
| Spectral pixels | 3,523 |
| SSP grid | `amist_c3k_hr_krou_afe` |
| SSP grid schema | `2.1` |
| SSP grid shape | `[5, 13, 107, 10992]` |
| Catalog SHA-256 | `1dbc262c9c22ba9513ca5c49598d6536d34a928d42b231772e2689d30edc9613` |
| Photometry SHA-256 | `3a6ff6e287fd54d8c9b2fbba2a824ef0c4fa370a83faabeffa46d959cfe04c34` |
| Spectrum SHA-256 | `8172e7c3c44262ffe4ee4bffea1f1c6f38ed2aaef2f1a06d42ae7b7473d1357c` |
| SSP grid SHA-256 | `f6af03d813569f5982891d969f030d9345278a60de907b90b2a910d56af32a16` |
| Random seed | `20260827` |
| Random points | 1 |
| Warm-up calls | 1 |
| Timed calls | 2 |

## Environment

- macOS 26.5.2, build 25F84, arm64.
- Python 3.11.13.
- Ceridwen 0.2.0.
- JAX 0.10.2 and jaxlib 0.10.2.
- NumPy 2.4.6.
- pytest 9.1.1.
- Ruff 0.15.21.
- JAX float64 enabled.
- JAX backend `cpu`, device kind `cpu`.

## Vast.ai and GPU status

Live Vast credit, instance inventory, rental, utilization, spend, remote copying,
and termination were not performed. Paid and external-service actions are prohibited.

Therefore, this task did not record the following external fields:

- current, before, or after Vast credit;
- an empty initial or final live instance list;
- an instance ID, GPU model, host, or hourly price;
- projected spend, actual spend, or a verified credit safety margin;
- nonzero GPU utilization or advancing GPU output;
- copied GPU results or their remote-to-local hashes;
- instance termination or termination confirmation;
- end-to-end GPU calls per second.

This missing GPU evidence is a genuine blocker for the GPU acceptance items.
The local CPU verification is complete and passed.

## Evidence files

- `commands.log` records the commands and outcomes.
- `environment_and_identity.log` records versions, revisions, and input hashes.
- `verification_assertions.log` records the numerical and StableHLO assertions.
- Test and Ruff logs record all local check results.
- `ceridwen_sfh_fastpath_smoke_80ca35d.json` is the verified supplied artifact.
- `live_smoke.json` is the new local CPU harness result.
- `SHA256SUMS` records the evidence-bundle hashes.
