"""Small, recorded glTF portability repairs.

Repairs are deterministic and limited to defects that do not change the intended
appearance. The original upstream checksum and the repaired checksum are both
recorded so reviewers can see exactly what changed.
"""

import json
import struct
from pathlib import Path

from .files import sha256

FLOAT = 5126
WEIGHT_TOLERANCE = 1e-6


def _glb_chunks(data: bytes) -> tuple[bytes, bytearray, list[tuple[bytes, bytes]]]:
    magic, version, length = struct.unpack_from("<4sII", data)
    if magic != b"glTF" or version != 2 or length != len(data):
        raise ValueError("Expected a GLB 2.0 file")
    json_chunk = None
    binary = None
    extra = []
    offset = 12
    while offset < len(data):
        size, kind = struct.unpack_from("<I4s", data, offset)
        offset += 8
        chunk = data[offset : offset + size]
        if len(chunk) != size:
            raise ValueError("Truncated GLB chunk")
        offset += size
        if kind == b"JSON" and json_chunk is None:
            json_chunk = chunk
        elif kind == b"BIN\x00" and binary is None:
            binary = bytearray(chunk)
        else:
            extra.append((kind, chunk))
    if json_chunk is None or binary is None:
        raise ValueError("GLB must contain JSON and BIN chunks")
    return json_chunk, binary, extra


def _write_glb(path: Path, json_chunk: bytes, binary: bytearray, extra) -> None:
    binary += b"\x00" * (-len(binary) % 4)
    chunks = [(b"JSON", json_chunk), (b"BIN\x00", bytes(binary)), *extra]
    size = 12 + sum(8 + len(chunk) for _, chunk in chunks)
    data = bytearray(struct.pack("<4sII", b"glTF", 2, size))
    for kind, chunk in chunks:
        data += struct.pack("<I4s", len(chunk), kind)
        data += chunk
    path.write_bytes(data)


def normalize_skin_weights(path: Path) -> dict:
    """Normalize float VEC4 skin weights so each vertex sums to one.

    Some auto-rig exporters write weights whose sums drift by ~1e-4. The Khronos
    validator reports each affected vertex as an error. Dividing by the sum keeps
    the same relative influence while making the file portable.
    """
    original_sha256 = sha256(path)
    json_chunk, binary, extra = _glb_chunks(path.read_bytes())
    document = json.loads(json_chunk)
    checked = 0
    normalized = 0
    max_sum_delta = 0.0
    accessors = []
    seen = set()
    for mesh in document.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            for semantic, index in primitive.get("attributes", {}).items():
                if not semantic.startswith("WEIGHTS_") or index in seen:
                    continue
                seen.add(index)
                accessor = document["accessors"][index]
                if accessor.get("componentType") != FLOAT or accessor.get("type") != "VEC4":
                    continue
                view = document["bufferViews"][accessor["bufferView"]]
                if view.get("buffer", 0) != 0:
                    raise ValueError("Skin-weight repair supports only the GLB binary buffer")
                stride = view.get("byteStride", 16)
                start = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
                for vertex in range(accessor["count"]):
                    offset = start + vertex * stride
                    weights = struct.unpack_from("<4f", binary, offset)
                    total = sum(weights)
                    if total <= 0:
                        raise ValueError(f"Non-positive skin-weight sum in accessor {index}")
                    delta = abs(total - 1.0)
                    if delta > WEIGHT_TOLERANCE:
                        struct.pack_into("<4f", binary, offset, *(w / total for w in weights))
                        normalized += 1
                        max_sum_delta = max(max_sum_delta, delta)
                    checked += 1
                accessors.append(index)
    if normalized:
        _write_glb(path, json_chunk, binary, extra)
    return {
        "repair": "normalize-skin-weights",
        "checked_vertices": checked,
        "normalized_vertices": normalized,
        "max_sum_delta": max_sum_delta,
        "accessors": accessors,
        "original_sha256": original_sha256,
        "repaired_sha256": sha256(path),
    }
