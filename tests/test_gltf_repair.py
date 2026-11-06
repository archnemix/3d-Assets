"""Skin-weight repair is deterministic, bounded and checksum-recorded."""

import json
import struct

import pytest

from asset_library.gltf_repair import normalize_skin_weights


def write_glb(path, weights):
    binary = bytearray()
    for vertex in weights:
        binary += struct.pack("<4f", *vertex)
    document = {
        "asset": {"version": "2.0"},
        "buffers": [{"byteLength": len(binary)}],
        "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": len(binary)}],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(weights), "type": "VEC4"}
        ],
        "meshes": [{"primitives": [{"attributes": {"WEIGHTS_0": 0}}]}],
    }
    json_chunk = json.dumps(document).encode()
    json_chunk += b" " * (-len(json_chunk) % 4)
    binary += b"\x00" * (-len(binary) % 4)
    size = 12 + 8 + len(json_chunk) + 8 + len(binary)
    data = struct.pack("<4sII", b"glTF", 2, size)
    data += struct.pack("<I4s", len(json_chunk), b"JSON") + json_chunk
    data += struct.pack("<I4s", len(binary), b"BIN\x00") + binary
    path.write_bytes(data)


def read_weights(path):
    data = path.read_bytes()
    offset = 12
    binary = None
    while offset < len(data):
        size, kind = struct.unpack_from("<I4s", data, offset)
        offset += 8
        if kind == b"BIN\x00":
            binary = data[offset : offset + size]
        offset += size
    return [struct.unpack_from("<4f", binary, i * 16) for i in range(2)]


def test_normalizes_drifting_weights_and_records_checksums(tmp_path):
    path = tmp_path / "rigged.glb"
    write_glb(path, [(0.5, 0.5, 0.0, 0.0), (1.0, 1.0, 0.0, 0.0)])
    report = normalize_skin_weights(path)
    assert report["checked_vertices"] == 2
    assert report["normalized_vertices"] == 1
    assert report["original_sha256"] != report["repaired_sha256"]
    first, second = read_weights(path)
    assert first == (0.5, 0.5, 0.0, 0.0)
    assert second == (0.5, 0.5, 0.0, 0.0)


def test_already_normalized_weights_are_not_rewritten(tmp_path):
    path = tmp_path / "rigged.glb"
    write_glb(path, [(0.25, 0.25, 0.25, 0.25), (1.0, 0.0, 0.0, 0.0)])
    before = path.read_bytes()
    report = normalize_skin_weights(path)
    assert report["normalized_vertices"] == 0
    assert path.read_bytes() == before


def test_rejects_non_positive_weight_sum(tmp_path):
    path = tmp_path / "rigged.glb"
    write_glb(path, [(0.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0)])
    with pytest.raises(ValueError, match="Non-positive"):
        normalize_skin_weights(path)
