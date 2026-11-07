"""Run technical checks and Blender renders without marking a candidate approved."""

import json
import os
import shutil
import subprocess
from pathlib import Path

from .config import ROOT, read_json
from .contact_sheet import build
from .files import inventory, write_checksums, write_json
from .gltf import compact_embedded_textures, extract_textures, validate_local


def validate_inventory(directory: Path, manifest: dict) -> None:
    actual = {item["path"]: item for item in inventory(directory)}
    expected = {item["path"]: item for item in manifest["files"]}
    if actual != expected:
        changed = sorted(
            path for path in actual.keys() & expected.keys() if actual[path] != expected[path]
        )
        missing = sorted(expected.keys() - actual.keys())
        added = sorted(actual.keys() - expected.keys())
        raise ValueError(f"Inventory mismatch: changed={changed}, missing={missing}, added={added}")


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


def author_animations(directory: Path, model: Path, blender: str) -> dict:
    """Add mechanical clips where the moving parts are already separate nodes.

    Non-destructive: the downloaded model is never modified. An animated GLB is
    written beside it and three verification frames per clip are rendered so the
    motion can be reviewed before approval. A failure here is not fatal to intake
    -- the static asset is still valid -- but it is recorded.
    """
    output = directory / "provenance"
    try:
        run(
            [
                blender,
                "--background",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "--python",
                str(ROOT / "rendering" / "author_animations.py"),
                "--",
                str(model.resolve()),
                str(output.resolve()),
            ],
            directory / "logs" / "animations.log",
        )
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        return {"authored": [], "error": str(error)}
    report = output / "animations.json"
    if not report.exists():
        return {"authored": []}
    data = json.loads(report.read_text())
    for strip in data.get("verification", []):
        for name in strip["frames"]:
            source = output / name
            if source.exists():
                shutil.move(str(source), str(directory / "previews" / name))
    return data


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
    authored = (
        {"authored": []}
        if manifest.get("skip_authored_animation", False)
        else author_animations(directory, model, blender)
    )
    if authored.get("authored"):
        manifest["authored_animations"] = authored["authored"]
        manifest["animated_model"] = f"model/{authored['animated_model']}"
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
    # Garment GLBs are self-contained; preserve lossless image indices rather
    # than committing large redundant extracted copies for every candidate.
    if manifest.get("source", {}).get("provider") == "makehuman-clothing":
        compact_embedded_textures(directory, manifest)
    manifest["files"] = inventory(directory)
    write_checksums(directory, manifest["files"])
    write_json(directory / "asset.json", manifest)
    return manifest


def reinspect(directory: Path) -> dict:
    """Replace stale renders and clear earlier approvals of those renders."""
    manifest = read_json(directory / "asset.json")
    status = manifest["review"]["status"]
    if status not in {"awaiting-visual-review", "intake-failed"}:
        raise ValueError("Only quarantine candidates can be reinspected")
    if status == "awaiting-visual-review":
        validate_inventory(directory, manifest)
    print(f"Reinspecting {manifest['id']}", flush=True)
    inspect(directory, {"title": manifest["title"]}, manifest)
    manifest["review"] = {"status": "awaiting-visual-review", "approved": False}
    manifest.pop("error", None)
    write_json(directory / "asset.json", manifest)
    print(f"awaiting-visual-review: {manifest['id']}", flush=True)
    return manifest
