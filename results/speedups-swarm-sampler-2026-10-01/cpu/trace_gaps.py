"""GPU stream events of a perfetto trace: kernels vs memcpy, and idle gaps by size."""
import collections, gzip, json, sys
ev = json.load(gzip.open(sys.argv[1]))["traceEvents"]
proc = {e["pid"]: e["args"]["name"] for e in ev if e.get("ph") == "M" and e.get("name") == "process_name"}
thr = {(e["pid"], e["tid"]): e["args"]["name"] for e in ev if e.get("ph") == "M" and e.get("name") == "thread_name"}
gpu = sorted((e for e in ev if e.get("ph") == "X" and "GPU" in proc.get(e["pid"], "")
              and "Stream" in thr.get((e["pid"], e["tid"]), "")), key=lambda e: e["ts"])
kinds = collections.Counter()
for e in gpu:
    n = e["name"].lower()
    kinds["memcpy" if "memcpy" in n else "memset" if "memset" in n else "kernel"] += 1
span = gpu[-1]["ts"] + gpu[-1]["dur"] - gpu[0]["ts"]
busy = sum(e["dur"] for e in gpu)
gaps, end = [], gpu[0]["ts"]
for e in gpu:
    if e["ts"] > end:
        gaps.append(e["ts"] - end)
    end = max(end, e["ts"] + e["dur"])
bins = [(0, 5), (5, 20), (20, 50), (50, 200), (200, 1e12)]
print(f"span {span/1e3:.1f} ms busy {busy/1e3:.1f} ms idle {sum(gaps)/1e3:.1f} ms; events {dict(kinds)}")
for lo, hi in bins:
    g = [x for x in gaps if lo <= x < hi]
    print(f"  gaps {lo}-{hi} us: {len(g)} totalling {sum(g)/1e3:.1f} ms")
big = collections.Counter()
for e in gpu:
    if e["dur"] > 100: big[e["name"][:60]] += e["dur"]
print("kernels >100us:", {k: round(v/1e3, 1) for k, v in big.most_common(6)})
