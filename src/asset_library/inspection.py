"""Run technical checks and Blender renders without marking a candidate approved."""

import json
import os
import shutil
import subprocess
from pathlib import Path

from .config import ROOT
from .contact_sheet import build
from .files import inventory, write_checksums, write_json
from .gltf import extract_textures, validate_local


def run(command: list[str], log: Path, timeout: int = 900) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run(
            command,
            cwd=ROOT,
            stdout=stream,
            stderr=subprocess.STDOUT,
            env=environment,
            timeout=timeout,
            check=False,
        )
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}); see {log.relative_to(ROOT)}")


def inspect(directory: Path, candidate: dict, manifest: dict) -> dict:
    model = directory / manifest["model"]
    manifest["gltf"] = validate_local(model)
    manifest["textures"] = extract_textures(model, directory / "textures")
    blender = shutil.which("blender")
    if not blender:
        raise RuntimeError("Blender is required; run intake through the pinned CI renderer")
    run(
        [
            blender,
            "--background",
            "--factory-startup",
            "--python-exit-code",
            "1",
            "--python",
            str(ROOT / "rendering" / "inspect_asset.py"),
            "--",
            str(model.resolve()),
            str((directory / "previews").resolve()),
        ],
        directory / "logs" / "blender.log",
    )
    build(directory / "previews", candidate["title"])
    validator = ROOT / "scripts" / "validate-gltf.js"
    if not (ROOT / "node_modules" / "gltf-validator" / "index.js").exists():
        raise RuntimeError("Run npm ci before inspecting assets")
    run(
        [
            "node",
            str(validator),
            str(model.resolve()),
            str((directory / "provenance" / "gltf-validator.json").resolve()),
        ],
        directory / "logs" / "validator.log",
    )
    report = json.loads((directory / "provenance" / "gltf-validator.json").read_text())
    errors = report.get("issues", {}).get("numErrors", 0)
    if errors:
        raise ValueError(f"Khronos validator reported {errors} errors")
    manifest["geometry"] = json.loads((directory / "previews" / "geometry.json").read_text())
    manifest["validation"] = {
        "gltf_errors": errors,
        "gltf_warnings": report.get("issues", {}).get("numWarnings", 0),
        "blender_import": "passed",
        "inspection_views": 12,
    }
    manifest["files"] = inventory(directory)
    write_checksums(directory, manifest["files"])
    write_json(directory / "asset.json", manifest)
    return manifest
