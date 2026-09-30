"""Push a copy of an image whose largest layer is split into one layer per large directory.

Docker downloads up to three layers at a time, and ghcr serves one stream at about
14-18 MB/s from a cold cache, so the image's single 3.5 GB venv layer took about 6 min
to download on a Vast host. Each tar member of that layer, with its extended headers,
is copied byte for byte into one of the new layers; the other layers are reused.
The unpacked filesystem is therefore the same.

Usage: split_image_layer.py <repository> <image digest> <tag>
Env: REGISTRY_USER, REGISTRY_TOKEN (push access to ghcr.io/<repository>).
Prints the new manifest digest.
"""
import base64
import collections
import gzip
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

REGISTRY = "https://ghcr.io"
# A directory of at least this many bytes with no subdirectory this large gets its own layer.
SPLIT_BYTES = 200_000_000
CHUNK = 64 << 20
INDEX = ("application/vnd.oci.image.index.v1+json", "application/vnd.docker.distribution.manifest.list.v2+json")
MANIFEST = "application/vnd.oci.image.manifest.v1+json"
LAYER = "application/vnd.oci.image.layer.v1.tar+gzip"


def token(repository):
    auth = base64.b64encode(f"{os.environ['REGISTRY_USER']}:{os.environ['REGISTRY_TOKEN']}".encode()).decode()
    request = urllib.request.Request(f"{REGISTRY}/token?scope=repository:{repository}:pull,push",
                                     headers={"Authorization": f"Basic {auth}"})
    return json.load(urllib.request.urlopen(request))["token"]


def call(repository, method, path, body=None, headers=None):
    url = path if path.startswith("http") else f"{REGISTRY}/v2/{repository}/{path}"
    request = urllib.request.Request(url, data=body, method=method,
                                     headers={"Authorization": f"Bearer {token(repository)}", **(headers or {})})
    return urllib.request.urlopen(request)


def manifest(repository, digest):
    response = call(repository, "GET", f"manifests/{digest}", headers={"Accept": ",".join((*INDEX, MANIFEST))})
    document = json.load(response)
    if document.get("mediaType") in INDEX:
        entry = next(m for m in document["manifests"]
                     if m.get("platform", {}).get("architecture") == "amd64" and m["platform"].get("os") == "linux")
        return manifest(repository, entry["digest"])
    return document


def download(repository, digest, path):
    sha = hashlib.sha256()
    with call(repository, "GET", f"blobs/{digest}") as response, open(path, "wb") as out:
        while chunk := response.read(CHUNK):
            sha.update(chunk)
            out.write(chunk)
    if f"sha256:{sha.hexdigest()}" != digest:
        raise SystemExit(f"{digest}: downloaded blob does not match its digest")


def octal(field):
    if field[0] & 0x80:  # GNU base-256 number
        return int.from_bytes(field[1:], "big")
    return int(field.rstrip(b"\0 ") or b"0", 8)


def members(stream):
    """(path, type flag, link target, raw bytes) of each tar member, extended headers included."""
    pending, path, link = b"", None, None
    while True:
        header = stream.read(512)
        if len(header) < 512 or header == bytes(512):
            return
        size = octal(header[124:136])
        data = stream.read((size + 511) // 512 * 512)
        kind = header[156:157]
        if kind in (b"x", b"L", b"K"):
            pending += header + data
            if kind == b"L":
                path = data[:size].rstrip(b"\0").decode()
            elif kind == b"K":
                link = data[:size].rstrip(b"\0").decode()
            else:
                records = data[:size]
                while records:
                    length, _, rest = records.partition(b" ")
                    key, _, value = rest[:int(length) - len(length) - 1].partition(b"=")
                    if key == b"path":
                        path = value[:-1].decode()
                    elif key == b"linkpath":
                        link = value[:-1].decode()
                    records = records[int(length):]
            continue
        if kind == b"g":
            raise SystemExit("global pax headers are not supported")
        if path is None:
            name, prefix = header[:100].rstrip(b"\0").decode(), header[345:500].rstrip(b"\0").decode()
            path = f"{prefix}/{name}" if prefix else name
        if link is None:
            link = header[157:257].rstrip(b"\0").decode()
        yield path.rstrip("/"), kind, link, pending + header + data
        pending, path, link = b"", None, None


def groups(layer_path):
    """Directories that become their own layer: at least SPLIT_BYTES, with no such subdirectory."""
    sizes = collections.Counter()
    with gzip.open(layer_path) as stream:
        for path, kind, _, raw in members(stream):
            parts = path.split("/")
            for depth in range(1, len(parts)):
                sizes["/".join(parts[:depth])] += len(raw)
    large = [d for d, size in sizes.items() if size >= SPLIT_BYTES]
    return sorted(d for d in large if not any(other.startswith(d + "/") for other in large))


def group_of(path, chosen):
    return next((k + 1 for k, d in enumerate(chosen) if path == d or path.startswith(d + "/")), 0)


class Layer:
    """One gzip tar layer written to disk, with its digest and diff_id."""

    def __init__(self, directory, index):
        self.path = os.path.join(directory, f"layer{index}.tar.gz")
        self.file = open(self.path, "wb")
        self.digest, self.diff_id, self.size = hashlib.sha256(), hashlib.sha256(), 0
        self.gzip = gzip.GzipFile(fileobj=self, mode="wb", compresslevel=6, mtime=0)

    def write(self, data):  # called by GzipFile with compressed bytes
        self.digest.update(data)
        self.size += len(data)
        return self.file.write(data)

    def flush(self):
        self.file.flush()

    def add(self, raw):
        self.diff_id.update(raw)
        self.gzip.write(raw)

    def close(self):
        self.add(bytes(1024))
        self.gzip.close()
        self.file.close()


def split(layer_path, chosen, directory):
    layers = [Layer(directory, k) for k in range(len(chosen) + 1)]
    placed = {}
    with gzip.open(layer_path) as stream:
        for path, kind, link, raw in members(stream):
            index = group_of(path, chosen)
            if kind == b"1" and placed.get(link.rstrip("/")) != index:
                raise SystemExit(f"hard link {path} -> {link} would cross layers")
            placed[path] = index
            layers[index].add(raw)
    for layer in layers:
        layer.close()
    return layers


def upload(repository, path, digest, size):
    try:
        call(repository, "HEAD", f"blobs/{digest}")
        return
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
    location = call(repository, "POST", "blobs/uploads/").headers["Location"]
    with open(path, "rb") as stream:
        location = call(repository, "PATCH", urllib.parse.urljoin(REGISTRY, location), stream, {
            "Content-Type": "application/octet-stream", "Content-Length": str(size)}).headers["Location"]
    target = urllib.parse.urljoin(REGISTRY, location)
    target += ("&" if "?" in target else "?") + urllib.parse.urlencode({"digest": digest})
    call(repository, "PUT", target, b"", {"Content-Type": "application/octet-stream"})


def main():
    repository, digest, tag = sys.argv[1:4]
    source = manifest(repository, digest)
    config = json.load(call(repository, "GET", f"blobs/{source['config']['digest']}"))
    largest = max(range(len(source["layers"])), key=lambda k: source["layers"][k]["size"])
    with tempfile.TemporaryDirectory() as directory:
        layer_path = os.path.join(directory, "source.tar.gz")
        download(repository, source["layers"][largest]["digest"], layer_path)
        chosen = groups(layer_path)
        print(f"layer {largest}: {len(chosen) + 1} layers; own layers for {chosen}", file=sys.stderr)
        layers = split(layer_path, chosen, directory)
        for layer in layers:
            upload(repository, layer.path, f"sha256:{layer.digest.hexdigest()}", layer.size)
    # History entries that are not empty layers pair with the layers in order.
    history, seen = [], 0
    for entry in config["history"]:
        if not entry.get("empty_layer") and seen == largest:
            history += [{**entry, "comment": f"split {k + 1} of {len(layers)}"} for k in range(len(layers))]
        else:
            history.append(entry)
        seen += not entry.get("empty_layer")
    diff_ids = config["rootfs"]["diff_ids"]
    config = {**config, "history": history, "rootfs": {**config["rootfs"], "diff_ids": [
        *diff_ids[:largest], *(f"sha256:{layer.diff_id.hexdigest()}" for layer in layers), *diff_ids[largest + 1:]]}}
    body = json.dumps(config, separators=(",", ":")).encode()
    config_digest = f"sha256:{hashlib.sha256(body).hexdigest()}"
    with tempfile.NamedTemporaryFile() as stream:
        stream.write(body)
        stream.flush()
        upload(repository, stream.name, config_digest, len(body))
    new_layers = [{"mediaType": LAYER, "digest": f"sha256:{layer.digest.hexdigest()}", "size": layer.size}
                  for layer in layers]
    document = {"schemaVersion": 2, "mediaType": MANIFEST,
                "config": {"mediaType": source["config"]["mediaType"], "digest": config_digest, "size": len(body)},
                "layers": [*source["layers"][:largest], *new_layers, *source["layers"][largest + 1:]]}
    response = call(repository, "PUT", f"manifests/{tag}", json.dumps(document).encode(), {"Content-Type": MANIFEST})
    print(response.headers["Docker-Content-Digest"])


if __name__ == "__main__":
    main()
