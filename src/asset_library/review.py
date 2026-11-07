"""Apply explicit visual decisions; never infer approval from a successful download."""

import shutil
from pathlib import Path

from jsonschema import FormatChecker, validate

from .config import ROOT, asset_directory, read_json
from .files import inventory, sha256, write_checksums, write_json
from .inspection import validate_inventory

CRITERIA = {"silhouette", "materials", "topology", "completeness", "style_fit"}


def check_decision(decision: dict) -> None:
    scores = decision["scores"]
    if set(scores) != CRITERIA:
        raise ValueError(f"{decision['id']}: all five quality criteria must be scored")
    if decision["decision"] == "approved":
        if min(scores.values()) < 4 or sum(scores.values()) / len(scores) < 4.6:
            raise ValueError(f"{decision['id']}: does not meet the high-quality approval threshold")
    elif len(decision["notes"]) < 30:
        raise ValueError(f"{decision['id']}: a rejection needs a substantive reason")


def asset_readme(manifest: dict) -> str:
    geometry = manifest["geometry"]
    return f"""# {manifest["title"]}

- Creator: {manifest["source"]["creator"]}
- Source: {manifest["source"]["source_url"]}
- License: CC0-1.0; no attribution required; commercial use and redistribution allowed.
- Category: `{manifest["category"]}`
- Intended style: {manifest["style"]}
- Import: `{manifest["model"]}`
- Triangles: {geometry["triangles"]:,}; mesh objects: {geometry["mesh_objects"]}
- Rig: {bool(geometry["armatures"])}; animation clips: {len(manifest["gltf"]["animations"])}
- Texture images: {len(manifest["textures"])}

Keep the entire folder together when importing. See `asset.json` for texture paths,
source evidence and technical measurements. See `review.json` for the visual decision.
`previews/` contains eight orbit views, top, bottom, clay and triangle-wireframe images.
These are inspection renders, not a guarantee of identical shading in every engine.

## Review limitations

{chr(10).join("- " + note for note in manifest["review"]["limitations"]) or "- No additional limitations recorded."}

Texture handling is recorded per image in `asset.json`. GLB files retain embedded
textures; where present, sidecar copies are byte-for-byte extracts for inspection and
DCC workflows, not additional dependencies. Embedded-only image records identify the
GLB and image index; extract them losslessly for DCC workflows when needed. External
glTF maps remain at their referenced paths.
If `textures` is empty, the source uses flat-color or vertex-color materials rather
than image maps; no texture files were omitted.
"""


def apply(path: Path) -> None:
    document = read_json(path)
    validate(
        document,
        read_json(ROOT / "schemas" / "review.schema.json"),
        format_checker=FormatChecker(),
    )
    seen = set()
    targets = set()
    evidence_paths = set()
    prepared = []
    for decision in document["decisions"]:
        check_decision(decision)
        if decision["id"] in seen:
            raise ValueError(f"Duplicate review: {decision['id']}")
        seen.add(decision["id"])
        source = ROOT / "quarantine" / document["batch"] / decision["id"]
        manifest = read_json(source / "asset.json")
        if manifest["id"] != decision["id"] or manifest["batch"] != document["batch"]:
            raise ValueError(f"{decision['id']}: candidate identity does not match its batch/path")
        if manifest["review"]["status"] != "awaiting-visual-review":
            raise ValueError(f"{decision['id']}: candidate has not passed technical intake")
        if sha256(source / "previews" / "contact-sheet.jpg") != decision["contact_sheet_sha256"]:
            raise ValueError(f"{decision['id']}: reviewed image does not match this candidate")
        validate_inventory(source, manifest)
        if manifest["license"]["spdx"] != "CC0-1.0" or manifest["validation"]["gltf_errors"]:
            raise ValueError(f"{decision['id']}: license/format gate failed")
        if decision["decision"] == "approved":
            target = asset_directory(ROOT / "assets", manifest["category"], manifest["id"])
            if target.exists() or target in targets:
                raise ValueError(f"Refusing to overwrite published asset: {target}")
            targets.add(target)
        else:
            evidence = ROOT / "reports" / "rejected" / document["batch"] / manifest["id"]
            if evidence.exists():
                raise ValueError(f"Refusing to overwrite rejection evidence: {evidence}")
            evidence_paths.add(evidence)
        record = {
            **decision,
            "reviewer": document["reviewer"],
            "reviewed_at": document["reviewed_at"],
            "views_inspected": 12,
            "method": "Visual inspection of local-model renders and technical reports",
        }
        prepared.append((source, manifest, record))
    for source, manifest, record in prepared:
        approve = record["decision"] == "approved"
        manifest["review"] = {**record, "status": record["decision"], "approved": approve}
        write_json(source / "review.json", record)
        if approve:
            target = asset_directory(ROOT / "assets", manifest["category"], manifest["id"])
            if target.exists():
                raise ValueError(f"Refusing to overwrite published asset: {target}")
            (source / "README.md").write_text(asset_readme(manifest), encoding="utf-8")
            manifest["files"] = inventory(source)
            write_checksums(source, manifest["files"])
            write_json(source / "asset.json", manifest)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
        else:
            evidence = ROOT / "reports" / "rejected" / document["batch"] / manifest["id"]
            evidence.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / "previews" / "contact-sheet.jpg", evidence / "contact-sheet.jpg")
            write_json(evidence / "review.json", manifest["review"])
            shutil.rmtree(source)
        print(f"{record['decision']}: {manifest['id']}")
