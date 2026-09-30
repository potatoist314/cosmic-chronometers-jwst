"""GPU kernel time by kernel name from a jax.profiler perfetto trace.

Usage: python3 trace_summary.py <perfetto_trace.json.gz> [top]
Prints the wall span, the summed kernel time on the GPU streams, the idle
fraction and the kernels with the largest summed time.
"""
import collections
import gzip
import json
import sys

events = json.load(gzip.open(sys.argv[1]))["traceEvents"]
top = int(sys.argv[2]) if len(sys.argv) > 2 else 25
process = {e["pid"]: e["args"]["name"] for e in events if e.get("ph") == "M" and e.get("name") == "process_name"}
thread = {(e["pid"], e["tid"]): e["args"]["name"] for e in events if e.get("ph") == "M" and e.get("name") == "thread_name"}
kernels = [e for e in events if e.get("ph") == "X" and "GPU" in process.get(e["pid"], "")
           and "Stream" in thread.get((e["pid"], e["tid"]), "")]
if not kernels:
    raise SystemExit(f"no GPU stream events; processes: {sorted(set(process.values()))}")
start = min(e["ts"] for e in kernels)
end = max(e["ts"] + e["dur"] for e in kernels)
busy = sum(e["dur"] for e in kernels)
by_name = collections.defaultdict(lambda: [0.0, 0])
for e in kernels:
    by_name[e["name"]][0] += e["dur"]
    by_name[e["name"]][1] += 1
print(f"span {1e-3 * (end - start):.2f} ms, kernel time {1e-3 * busy:.2f} ms "
      f"({100 * busy / (end - start):.0f}% busy), {len(kernels)} kernels, "
      f"mean {busy / len(kernels):.1f} us")
for name, (dur, count) in sorted(by_name.items(), key=lambda kv: -kv[1][0])[:top]:
    print(f"{1e-3 * dur:9.2f} ms {100 * dur / busy:5.1f}% {count:7d}x {dur / count:8.1f} us  {name[:110]}")
