"""Author mechanical animation clips for already-approved assets.

Approved assets are never re-downloaded and their original model file is never
modified. For each candidate we write a self-contained animated GLB beside the
original, render three verification frames per clip, and record the clips in the
asset manifest. The visual review record is left intact because the contact
sheet does not change; the new motion is recorded separately and must be
confirmed from the verification frames.
"""

import shutil

from .config import ROOT, read_json
from .files import inventory, write_checksums, write_json
from .inspection import author_animations


def targets(request: dict) -> list:
    """Approved assets without authored motion, or all of them when re-authoring.

    ``force`` re-runs assets that already carry an animated model so a corrected
    rule can replace a bad clip. The original model file is still never touched.
    """
    wanted = request.get("ids")
    found = []
    for path in sorted((ROOT / "assets").glob("*/*/*/asset.json")):
        manifest = read_json(path)
        if wanted is not None and manifest["id"] not in wanted:
            continue
        if manifest.get("animated_model") and not request.get("force"):
            continue
        found.append(path)
    return found


def describe(request: dict) -> None:
    found = targets(request)
    print(f"{request['batch']}: {len(found)} approved assets eligible for animation")


def shards(request: dict) -> dict:
    found = targets(request)
    return {"shard": list(range(min(5, max(1, len(found)))))}


def run_shard(request: dict, shard: int) -> int:
    found = targets(request)
    assigned = [path for index, path in enumerate(found) if index % 5 == shard]
    blender = shutil.which("blender")
    if not blender:
        raise RuntimeError("Blender is required; run through the pinned CI renderer")
    results = []
    for path in assigned:
        directory = path.parent
        manifest = read_json(path)
        identifier = manifest["id"]
        try:
            data = author_animations(directory, directory / manifest["model"], blender)
            clips = data.get("authored", [])
            if clips:
                manifest["authored_animations"] = clips
                manifest["animated_model"] = f"model/{data['animated_model']}"
            # The authoring pass always leaves an animations.json and a log behind,
            # even when it finds nothing to animate, so the inventory has to be
            # refreshed either way or the catalog gate fails on untracked files.
            manifest["files"] = inventory(directory)
            write_checksums(directory, manifest["files"])
            write_json(path, manifest)
            results.append({"id": identifier, "clips": [c["name"] for c in clips]})
            print(f"{identifier}: {len(clips)} clips {[c['name'] for c in clips]}", flush=True)
        except Exception as error:  # noqa: BLE001 - record and continue the shard
            results.append({"id": identifier, "error": str(error)})
            print(f"{identifier}: FAILED {error}", flush=True)
    report = ROOT / "reports" / "animations" / request["batch"] / f"shard-{shard}.json"
    write_json(report, {"batch": request["batch"], "shard": shard, "results": results})
    return 0
