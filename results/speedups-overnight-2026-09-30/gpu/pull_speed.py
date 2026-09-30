"""Download rate of the GPU image's 3.5 GB venv layer from ghcr on the box: one stream vs parallel ranges.

Env: SPEEDUP_OUT. Each trial reads for PULL_SECONDS (default 40) and discards the bytes.
"""
import json
import os
import threading
import time
import urllib.request
from pathlib import Path

REPO = "potatoist314/ceridwen-gpu"
BLOB = "sha256:b2449364bbe73278a9c4ff823b55c63b6bb105ed0ab3fd713f887502c433f55e"
SIZE = 3_536_400_000
SECONDS = float(os.environ.get("PULL_SECONDS", "40"))
token = json.load(urllib.request.urlopen(f"https://ghcr.io/token?scope=repository:{REPO}:pull"))["token"]


def stream(offset, counts, index, stop):
    request = urllib.request.Request(f"https://ghcr.io/v2/{REPO}/blobs/{BLOB}",
                                     headers={"Authorization": f"Bearer {token}", "Range": f"bytes={offset}-"})
    with urllib.request.urlopen(request) as response:
        while not stop.is_set():
            chunk = response.read(1 << 20)
            if not chunk:
                return
            counts[index] += len(chunk)


results = {}
for streams in (1, 3, 8, 1):
    counts, stop = [0] * streams, threading.Event()
    threads = [threading.Thread(target=stream, args=(k * SIZE // streams, counts, k, stop)) for k in range(streams)]
    start = time.perf_counter()
    for thread in threads:
        thread.start()
    time.sleep(SECONDS)
    stop.set()
    elapsed = time.perf_counter() - start
    for thread in threads:
        thread.join()
    rate = sum(counts) / elapsed / 1e6
    results.setdefault(str(streams), []).append(round(rate, 1))
    print(f"{streams} streams: {rate:.1f} MB/s", flush=True)
Path(os.environ["SPEEDUP_OUT"], "pull_speed.json").write_text(json.dumps(results))
