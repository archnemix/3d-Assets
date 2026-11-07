"""Inspect the two small, hash-pinned clothing archives without publishing them."""

import json
import subprocess
import tempfile
from pathlib import Path

from asset_library.config import ROOT, read_json
from asset_library.files import extract_zip
from asset_library.http import download

records = read_json(ROOT / "reports/research/oga-clothing-archives.json")
results = {}
with tempfile.TemporaryDirectory(prefix="oga-clothing-probe-") as temp:
    base = Path(temp)
    for name, evidence in records.items():
        archive = base / name
        result = download(evidence["url"], archive, {"opengameart.org"})
        if result["sha256"] != evidence["sha256"] or result["bytes"] != evidence["bytes"]:
            raise ValueError(f"Archive changed: {name}")
        folder = base / name[:-4]
        extract_zip(archive, folder, max_total_bytes=50 * 1024**2)
        files = list(folder.glob("*.blend"))
        if len(files) != 1:
            raise ValueError(f"Unexpected Blender files: {name}")
        report = base / (name + ".json")
        command = [
            "blender",
            "--background",
            "--factory-startup",
            "--disable-autoexec",
            str(files[0]),
            "--python-exit-code",
            "1",
            "--python",
            str(ROOT / "rendering/probe_clothing_blend.py"),
            "--",
            str(report),
        ]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=300, check=False)
        results[name] = {
            "exit_code": proc.returncode,
            "log_tail": (proc.stdout + proc.stderr)[-5000:],
            "inspection": json.loads(report.read_text()) if report.exists() else None,
        }
output = ROOT / "reports/research/oga-clothing-blend-probe.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
