"""Exercise the actual Node validator boundary, including its report-file contract."""

import base64
import json
import shutil
import struct
import subprocess

import pytest

from asset_library.config import ROOT


@pytest.mark.skipif(
    not shutil.which("node") or not (ROOT / "node_modules/gltf-validator").exists(),
    reason="Run npm ci to enable the Node integration test",
)
def test_validator_writes_report_and_accepts_valid_triangle(tmp_path):
    positions = struct.pack("<9f", 0, 0, 0, 1, 0, 0, 0, 1, 0)
    indices = struct.pack("<3H", 0, 1, 2)
    binary = positions + indices
    document = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1}]}],
        "buffers": [
            {
                "uri": "data:application/octet-stream;base64," + base64.b64encode(binary).decode(),
                "byteLength": len(binary),
            }
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": 36},
            {"buffer": 0, "byteOffset": 36, "byteLength": 6},
        ],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": 3,
                "type": "VEC3",
                "min": [0, 0, 0],
                "max": [1, 1, 0],
            },
            {"bufferView": 1, "componentType": 5123, "count": 3, "type": "SCALAR"},
        ],
    }
    model = tmp_path / "triangle.gltf"
    model.write_text(json.dumps(document))
    report = tmp_path / "report.json"
    result = subprocess.run(
        ["node", str(ROOT / "scripts/validate-gltf.js"), str(model), str(report)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(report.read_text())["issues"]["numErrors"] == 0
