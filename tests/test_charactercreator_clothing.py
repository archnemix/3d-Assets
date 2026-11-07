"""Pin provenance to explicitly CC0 output files, not GPL source code."""

import pytest

from asset_library.sources.charactercreator_clothing import verify_metadata, verify_terms


def test_metadata_rejects_ambiguous_or_non_cc0_sources():
    item = {
        "id": "shirt",
        "file": "clothing_shirt.glb",
        "license": "CC0",
        "bytes": 123,
        "source": "MakeHuman",
    }
    verify_metadata(item, "shirt", 123)
    for change in ({"license": "CC-BY"}, {"file": "other.glb"}, {"bytes": 124}, {"source": ""}):
        with pytest.raises(ValueError):
            verify_metadata({**item, **change}, "shirt", 123)


def test_terms_explicitly_separate_output_licenses():
    notes = "Garment GLBs (`output/clothing_*.glb`) CC0-1.0 (all sources CC0 or our own authored data) A generated file derived from a **CC-BY** asset"
    verify_terms(notes)
    with pytest.raises(ValueError):
        verify_terms(notes.replace("CC0-1.0 (all sources CC0 or our own authored data)", "unknown"))


def test_neutralize_morph_weights_preserves_binary_and_rejects_drift(tmp_path):
    import json
    import struct

    from asset_library.gltf import read_model
    from asset_library.sources.charactercreator_clothing import reset_default_morph_weights

    doc = {
        "asset": {"version": "2.0"},
        "meshes": [
            {
                "weights": [1, 1],
                "extras": {"targetNames": ["a", "b"]},
                "primitives": [{"targets": [{}, {}]}],
            }
        ],
        "nodes": [{"mesh": 0}],
    }
    js = json.dumps(doc).encode()
    js += b" " * (-len(js) % 4)
    binary = b"abcd"
    data = struct.pack("<4sII", b"glTF", 2, 28 + len(js) + len(binary))
    data += struct.pack("<I4s", len(js), b"JSON") + js
    data += struct.pack("<I4s", len(binary), b"BIN\0") + binary
    path = tmp_path / "test.glb"
    path.write_bytes(data)
    result = reset_default_morph_weights(path)
    actual, actual_binary = read_model(path)
    assert actual["meshes"][0]["weights"] == [0, 0]
    assert actual_binary == binary
    assert result["target_count"] == 2
    with pytest.raises(ValueError):
        reset_default_morph_weights(path)
