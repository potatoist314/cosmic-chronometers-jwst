"""Push a copy of an image without the given files and directories.

split_image_layer.py puts each large venv directory in its own layer. A layer that holds
only removed paths (NCCL, NVSHMEM) is left out; a layer that also holds kept files (the
cuDNN libraries XLA never loads) is rewritten with its other tar members copied byte for
byte. Every other layer is reused unchanged.

Usage: drop_image_paths.py <repository> <image digest> <tag> <path>...
Env: REGISTRY_USER, REGISTRY_TOKEN (push access to ghcr.io/<repository>).
Prints the new manifest digest.
"""
import gzip
import hashlib
import json
import os
import sys
import tempfile

from split_image_layer import LAYER, MANIFEST, Layer, call, download, manifest, members, upload


def inside(path, paths):
    return any(path == p or path.startswith(p + "/") for p in paths)


def plan(layers, paths):
    """What happens to each layer, given its (path, type flag, link target) members:
    'keep' (nothing removed), 'drop' (everything removed) or 'rewrite'."""
    actions = []
    for entries in layers:
        removed = sum(inside(path, paths) for path, _, _ in entries)
        actions.append("keep" if not removed else "drop" if removed == len(entries) else "rewrite")
    for entries in layers:
        for path, kind, link in entries:
            if kind == b"1" and not inside(path, paths) and inside(link.rstrip("/"), paths):
                raise SystemExit(f"{path} hard-links to {link}, which is removed")
    if "drop" not in actions and "rewrite" not in actions:
        raise SystemExit("no member matches the given paths")
    return actions


def rewrite(source, paths, directory, index):
    """The layer file ``source`` without the members inside ``paths``; the others byte for byte."""
    layer = Layer(directory, index)
    with gzip.open(source) as stream:
        for path, _, _, raw in members(stream):
            if not inside(path, paths):
                layer.add(raw)
    layer.close()
    return layer


def main():
    repository, digest, tag, *paths = sys.argv[1:]
    source = manifest(repository, digest)
    config = json.load(call(repository, "GET", f"blobs/{source['config']['digest']}"))
    with tempfile.TemporaryDirectory() as directory:
        files, listings = [], []
        for index, layer in enumerate(source["layers"]):
            files.append(os.path.join(directory, f"source{index}.tar.gz"))
            download(repository, layer["digest"], files[-1])
            with gzip.open(files[-1]) as stream:
                listings.append([(path, kind, link) for path, kind, link, _ in members(stream)])
        actions = plan(listings, paths)
        layers, diff_ids = [], []
        for index, (action, layer, diff_id) in enumerate(zip(actions, source["layers"], config["rootfs"]["diff_ids"])):
            if action == "keep":
                layers.append(layer)
                diff_ids.append(diff_id)
            elif action == "rewrite":
                rewritten = rewrite(files[index], paths, directory, index)
                new_digest = f"sha256:{rewritten.digest.hexdigest()}"
                upload(repository, rewritten.path, new_digest, rewritten.size)
                layers.append({"mediaType": LAYER, "digest": new_digest, "size": rewritten.size})
                diff_ids.append(f"sha256:{rewritten.diff_id.hexdigest()}")
            print(f"layer {index}: {action}", file=sys.stderr)
    # History entries that are not empty layers pair with the layers in order.
    history, seen = [], 0
    for entry in config["history"]:
        if entry.get("empty_layer") or actions[seen] != "drop":
            history.append(entry)
        seen += not entry.get("empty_layer")
    config = {**config, "history": history, "rootfs": {**config["rootfs"], "diff_ids": diff_ids}}
    body = json.dumps(config, separators=(",", ":")).encode()
    config_digest = f"sha256:{hashlib.sha256(body).hexdigest()}"
    with tempfile.NamedTemporaryFile() as stream:
        stream.write(body)
        stream.flush()
        upload(repository, stream.name, config_digest, len(body))
    document = {"schemaVersion": 2, "mediaType": MANIFEST,
                "config": {"mediaType": source["config"]["mediaType"], "digest": config_digest, "size": len(body)},
                "layers": layers}
    response = call(repository, "PUT", f"manifests/{tag}", json.dumps(document).encode(), {"Content-Type": MANIFEST})
    print(response.headers["Docker-Content-Digest"])


if __name__ == "__main__":
    main()
