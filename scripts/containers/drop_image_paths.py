"""Push a copy of an image without the layers that hold only the given directories.

split_image_layer.py puts each large venv directory in its own layer, so a library the
fits never load (NCCL and NVSHMEM on one GPU) is one layer that can be left out. Every
other layer, and its bytes, is reused unchanged.

Usage: drop_image_layers.py <repository> <image digest> <tag> <directory>...
Env: REGISTRY_USER, REGISTRY_TOKEN (push access to ghcr.io/<repository>).
Prints the new manifest digest.
"""
import gzip
import hashlib
import json
import os
import sys
import tempfile

from split_image_layer import MANIFEST, call, download, manifest, members, upload


def inside(path, directory):
    return path == directory or path.startswith(directory + "/")


def droppable(layers, directories):
    """Indices of the layers whose members all lie in one of the directories.

    layers: one list of (path, type flag, link target) per layer. Each directory must be
    exactly one such layer: no other layer may hold, or hard-link into, any path in it."""
    chosen = {}
    for index, entries in enumerate(layers):
        owners = {d for d in directories for path, _, _ in entries if inside(path, d)}
        if len(owners) == 1 and all(inside(path, next(iter(owners))) for path, _, _ in entries):
            chosen.setdefault(owners.pop(), []).append(index)
    for directory in directories:
        if len(chosen.get(directory, [])) != 1:
            raise SystemExit(f"{directory} is not exactly one layer of its own")
    drop = {i for indices in chosen.values() for i in indices}
    for index, entries in enumerate(layers):
        if index in drop:
            continue
        for path, kind, link in entries:
            for directory in directories:
                if inside(path, directory) or (kind == b"1" and inside(link.rstrip("/"), directory)):
                    raise SystemExit(f"layer {index} holds {path}, which depends on {directory}")
    return sorted(drop)


def main():
    repository, digest, tag, *directories = sys.argv[1:]
    source = manifest(repository, digest)
    config = json.load(call(repository, "GET", f"blobs/{source['config']['digest']}"))
    layers = []
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "layer.tar.gz")
        for layer in source["layers"]:
            download(repository, layer["digest"], path)
            with gzip.open(path) as stream:
                layers.append([(p, kind, link) for p, kind, link, _ in members(stream)])
    drop = droppable(layers, directories)
    print(f"leaving out layers {drop}: {sum(source['layers'][i]['size'] for i in drop):,} bytes", file=sys.stderr)
    # History entries that are not empty layers pair with the layers in order.
    history, seen = [], 0
    for entry in config["history"]:
        if entry.get("empty_layer") or seen not in drop:
            history.append(entry)
        seen += not entry.get("empty_layer")
    diff_ids = [d for i, d in enumerate(config["rootfs"]["diff_ids"]) if i not in drop]
    config = {**config, "history": history, "rootfs": {**config["rootfs"], "diff_ids": diff_ids}}
    body = json.dumps(config, separators=(",", ":")).encode()
    config_digest = f"sha256:{hashlib.sha256(body).hexdigest()}"
    with tempfile.NamedTemporaryFile() as stream:
        stream.write(body)
        stream.flush()
        upload(repository, stream.name, config_digest, len(body))
    document = {"schemaVersion": 2, "mediaType": MANIFEST,
                "config": {"mediaType": source["config"]["mediaType"], "digest": config_digest, "size": len(body)},
                "layers": [layer for i, layer in enumerate(source["layers"]) if i not in drop]}
    response = call(repository, "PUT", f"manifests/{tag}", json.dumps(document).encode(), {"Content-Type": MANIFEST})
    print(response.headers["Docker-Content-Digest"])


if __name__ == "__main__":
    main()
