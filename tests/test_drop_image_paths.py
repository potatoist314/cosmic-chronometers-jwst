"""Only layers that hold nothing but the given directories are left out."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/containers"))
import drop_image_layers as drop  # noqa: E402

NCCL, NVSHMEM = "venv/nvidia/nccl/lib", "venv/nvidia/nvshmem/lib"
REST = [("venv", b"5", ""), ("venv/nvidia/nccl", b"5", ""), ("venv/nvidia/nccl/__init__.py", b"0", "")]
NCCL_LAYER = [(NCCL, b"5", ""), (f"{NCCL}/libnccl.so.2", b"0", "")]
NVSHMEM_LAYER = [(NVSHMEM, b"5", ""), (f"{NVSHMEM}/libnvshmem_host.so.3", b"0", "")]


def test_layers_of_only_the_directories_are_dropped():
    assert drop.droppable([REST, NCCL_LAYER, [("venv/x.so", b"0", "")], NVSHMEM_LAYER], [NCCL, NVSHMEM]) == [1, 3]


def test_a_directory_split_over_two_layers_is_refused():
    with pytest.raises(SystemExit, match="depends on"):
        drop.droppable([REST + [(f"{NCCL}/extra.so", b"0", "")], NCCL_LAYER], [NCCL])


def test_a_hard_link_into_a_dropped_directory_is_refused():
    with pytest.raises(SystemExit, match="depends on"):
        drop.droppable([REST + [("venv/nccl.so", b"1", f"{NCCL}/libnccl.so.2")], NCCL_LAYER], [NCCL])


def test_a_directory_without_its_own_layer_is_refused():
    with pytest.raises(SystemExit, match="not exactly one layer"):
        drop.droppable([REST + NCCL_LAYER], [NCCL])
