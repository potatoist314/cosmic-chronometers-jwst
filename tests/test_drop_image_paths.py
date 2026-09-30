"""Removed paths leave the image; every other tar member is copied byte for byte."""
import gzip
import hashlib
import io
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/containers"))
import drop_image_paths as drop  # noqa: E402

NCCL, NVSHMEM, CUDNN = "venv/nvidia/nccl/lib", "venv/nvidia/nvshmem/lib", "venv/nvidia/cudnn/lib"
REST = [("venv", b"5", ""), ("venv/nvidia/nccl", b"5", ""), ("venv/nvidia/nccl/__init__.py", b"0", "")]
NCCL_LAYER = [(NCCL, b"5", ""), (f"{NCCL}/libnccl.so.2", b"0", "")]
NVSHMEM_LAYER = [(NVSHMEM, b"5", ""), (f"{NVSHMEM}/libnvshmem_host.so.3", b"0", "")]
CUDNN_LAYER = [(CUDNN, b"5", ""), (f"{CUDNN}/libcudnn.so.9", b"0", ""), (f"{CUDNN}/libcudnn_ops.so.9", b"0", "")]


def test_layers_are_kept_dropped_or_rewritten():
    paths = [NCCL, NVSHMEM, f"{CUDNN}/libcudnn_ops.so.9"]
    assert drop.plan([REST, NCCL_LAYER, CUDNN_LAYER, NVSHMEM_LAYER], paths) == ["keep", "drop", "rewrite", "drop"]


def test_a_hard_link_to_a_removed_path_is_refused():
    with pytest.raises(SystemExit, match="hard-links"):
        drop.plan([REST + [("venv/nccl.so", b"1", f"{NCCL}/libnccl.so.2")], NCCL_LAYER], [NCCL])


def test_paths_that_match_nothing_are_refused():
    with pytest.raises(SystemExit, match="no member"):
        drop.plan([REST], ["venv/nvidia/cufft/lib"])


def test_rewritten_layer_keeps_other_members_byte_for_byte(tmp_path):
    def layer(names):
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for name in names:
                data = name.encode() * 300
                info = tarfile.TarInfo(name)
                info.size, info.mtime, info.pax_headers = len(data), 1_700_000_000, {"comment": "x" * 40}
                tar.addfile(info, io.BytesIO(data))
        return buffer.getvalue()

    long_name = f"{CUDNN}/" + "d" * 120 + "/libcudnn_graph.so.9"  # needs a pax path record
    kept, removed = [f"{CUDNN}/libcudnn.so.9", long_name], f"{CUDNN}/libcudnn_ops.so.9"
    source = tmp_path / "source.tar.gz"
    source.write_bytes(gzip.compress(layer([kept[0], removed, kept[1]])))
    rewritten = drop.rewrite(source, [removed], str(tmp_path), 0)
    unpacked = gzip.decompress(Path(rewritten.path).read_bytes())
    with gzip.open(source) as stream:
        source_members = [(path, raw) for path, _, _, raw in drop.members(stream)]
    assert [path for path, _ in source_members] == [kept[0], removed, kept[1]]
    assert unpacked == b"".join(raw for path, raw in source_members if path != removed) + bytes(1024)
    with tarfile.open(fileobj=io.BytesIO(unpacked)) as tar:
        assert [(m.name, tar.extractfile(m).read()) for m in tar] == [(n, n.encode() * 300) for n in kept]
    assert rewritten.diff_id.hexdigest() == hashlib.sha256(unpacked).hexdigest()
    assert rewritten.digest.hexdigest() == hashlib.sha256(Path(rewritten.path).read_bytes()).hexdigest()
