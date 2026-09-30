"""The split layers unpack to the same members, byte for byte, as the layer they replace."""
import collections
import gzip
import hashlib
import io
import tarfile
from pathlib import Path

import pytest

from scripts.containers import split_image_layer as split


def add(archive, name, data=b"", kind=tarfile.REGTYPE, link="", pax=None):
    member = tarfile.TarInfo(name)
    member.type, member.linkname, member.mtime, member.size = kind, link, 1234567, len(data)
    member.mode = 0o755 if kind == tarfile.DIRTYPE else 0o644
    member.pax_headers = pax or {}
    archive.addfile(member, io.BytesIO(data) if data else None)


def members(paths):
    found = collections.Counter()
    for path in paths:
        with tarfile.open(path) as archive:
            for m in archive:
                data = archive.extractfile(m).read() if m.isfile() else b""
                found[(m.name, m.type, m.mode, m.mtime, m.linkname, tuple(sorted(m.pax_headers.items())),
                       hashlib.sha256(data).hexdigest())] += 1
    return found


@pytest.fixture
def layer(tmp_path):
    gnu, pax = io.BytesIO(), io.BytesIO()
    with tarfile.open(fileobj=gnu, mode="w", format=tarfile.GNU_FORMAT) as archive:
        for directory in ("opt", "opt/v", "opt/v/big", "opt/v/big/sub", "opt/v/small"):
            add(archive, directory, kind=tarfile.DIRTYPE)
        add(archive, "opt/v/big/a.so", bytes(range(256)) * 8)
        add(archive, "opt/v/big/sub/b.so", bytes(2500))
        add(archive, "opt/v/big/" + "x" * 150, b"long name")
        add(archive, "opt/v/big/hard", kind=tarfile.LNKTYPE, link="opt/v/big/a.so")
        add(archive, "opt/v/small/c.py", b"print(1)\n")
        add(archive, "opt/v/small/soft", kind=tarfile.SYMTYPE, link="c.py")
        add(archive, "opt/v/small/" + "y" * 120, kind=tarfile.DIRTYPE)
    with tarfile.open(fileobj=pax, mode="w", format=tarfile.PAX_FORMAT) as archive:
        add(archive, "opt/v/small/ünï" + "z" * 110, b"abc", pax={"SCHILY.xattr.user.k": "v"})
    body = gnu.getvalue()
    end = len(body)
    while body[end - 512:end] == bytes(512):
        end -= 512
    path = tmp_path / "source.tar.gz"
    path.write_bytes(gzip.compress(body[:end] + pax.getvalue()))
    return path


def test_split_layers_hold_the_same_members_and_record_their_digests(layer, tmp_path, monkeypatch):
    monkeypatch.setattr(split, "SPLIT_BYTES", 3000)
    chosen = split.groups(layer)
    assert chosen == ["opt/v/big/sub", "opt/v/small"]
    layers = split.split(layer, chosen, tmp_path)
    assert members([layer]) == members([part.path for part in layers])
    for part in layers:
        packed = Path(part.path).read_bytes()
        assert (len(packed), hashlib.sha256(packed).hexdigest()) == (part.size, part.digest.hexdigest())
        assert hashlib.sha256(gzip.decompress(packed)).hexdigest() == part.diff_id.hexdigest()


def test_hard_link_across_layers_is_refused(layer, tmp_path):
    with pytest.raises(SystemExit, match="hard link"):
        split.split(layer, ["opt/v/big/sub", "opt/v/big/hard"], tmp_path)
