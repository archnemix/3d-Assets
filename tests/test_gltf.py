import json
import struct

import pytest
from PIL import Image

from asset_library.gltf import extract_textures, read_model, validate_local


def image_bytes(tmp_path):
    path = tmp_path / "source.png"
    Image.new("RGB", (4, 4), "red").save(path)
    return path.read_bytes()


def glb(document, binary):
    encoded = json.dumps(document).encode()
    encoded += b" " * (-len(encoded) % 4)
    binary += b"\0" * (-len(binary) % 4)
    chunks = struct.pack("<I4s", len(encoded), b"JSON") + encoded
    chunks += struct.pack("<I4s", len(binary), b"BIN\0") + binary
    return struct.pack("<4sII", b"glTF", 2, 12 + len(chunks)) + chunks


def test_extracts_embedded_png_without_reencoding(tmp_path):
    payload = image_bytes(tmp_path)
    document = {
        "asset": {"version": "2.0"},
        "meshes": [{}],
        "buffers": [{"byteLength": len(payload)}],
        "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": len(payload)}],
        "images": [{"name": "wood diff", "mimeType": "image/png", "bufferView": 0}],
    }
    model = tmp_path / "model.glb"
    model.write_bytes(glb(document, payload))
    assert read_model(model)[0]["meshes"] == [{}]
    assert validate_local(model)["images"] == 1
    textures = extract_textures(model, tmp_path / "textures")
    assert (tmp_path / textures[0]["path"]).read_bytes() == payload
    assert textures[0]["dimensions"] == [4, 4]
    assert textures[0]["embedded_in_glb"]


def test_missing_external_texture_is_rejected(tmp_path):
    model = tmp_path / "model.gltf"
    model.write_text(json.dumps({"meshes": [{}], "images": [{"uri": "missing.png"}]}))
    with pytest.raises(ValueError, match="Missing glTF dependencies"):
        validate_local(model)


def test_truncated_glb_is_rejected(tmp_path):
    model = tmp_path / "model.glb"
    model.write_bytes(glb({"buffers": [{"byteLength": 100}]}, b"short")[:40])
    with pytest.raises(ValueError):
        read_model(model)
