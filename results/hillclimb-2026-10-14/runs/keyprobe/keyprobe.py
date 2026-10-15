"""GPU and CPU topology fingerprints (hashed into every JAX compile-cache key) and host details on 9 L40S containers."""
import subprocess
import modal

IMAGE = 'ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34'
app = modal.App('hillclimb-keyprobe3')
CODE = r'''
import numpy as np, jax
from jax._src.lib import xla_client
out = []
for platform in ('cuda', 'cpu'):
    d = jax.devices(platform)[:1]
    t = xla_client.get_topology_for_devices(d)
    dev = d[0]
    attrs = {k: getattr(dev, k) for k in dir(dev) if not k.startswith('_') and isinstance(getattr(dev, k, None), (int, str, float))}
    out.append(f"{platform} fp={t.fingerprint()}")
print(' || '.join(out))
'''

@app.function(image=modal.Image.from_registry(IMAGE), gpu='L40S', cpu=2, memory=4096, timeout=600)
def probe(i):
    smi = subprocess.run(['nvidia-smi', '--query-gpu=driver_version,memory.total,clocks.max.sm,clocks.max.mem,pcie.link.gen.max,pcie.link.width.max,power.limit,ecc.mode.current',
                          '--format=csv,noheader'], capture_output=True, text=True).stdout.strip()
    info = open('/proc/cpuinfo').read(); flags = next((l for l in info.splitlines() if l.startswith('flags')), ''); cpu = f"vendor={next((l.split(':')[1].strip() for l in info.splitlines() if l.startswith('vendor_id')), '?')} nflags={len(flags.split())} avx512f={'avx512f' in flags} amx={'amx_tile' in flags} nproc={info.count('processor')}"
    out = subprocess.run(['/opt/ceridwen/bin/python', '-c', CODE], capture_output=True, text=True,
                         env={'JAX_ENABLE_X64': '1', 'PATH': '/usr/bin:/bin'})
    return f'{i} | {smi} | {cpu} | {out.stdout.strip()} {out.stderr.strip()[-300:] if out.returncode else ""}'

@app.local_entrypoint()
def main():
    for line in probe.map(range(9)):
        print(line)
