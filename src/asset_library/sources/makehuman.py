"""Build reproducible human candidates from the pinned CC0 MakeHuman system pack.

MPFB2 is a GPL build tool, not an asset dependency. The exported candidate contains
only CC0 base mesh, targets, clothes and textures from the official system pack.
"""

import shutil
from pathlib import Path

from jsonschema import validate

from asset_library.config import ROOT, read_json, require_slug
from asset_library.files import destination, extract_zip, safe_relative_path, sha256, write_json
from asset_library.http import download
from asset_library.inspection import run

HOSTS = {
    "files2.makehumancommunity.org",
    "files.makehumancommunity.org",
    "codeload.github.com",
    "github.com",
    "raw.githubusercontent.com",
}


def pinned_archive(
    url: str, expected_sha256: str, expected_bytes: int | None = None
) -> tuple[Path, dict]:
    cache = ROOT / ".work" / "cache" / "makehuman"
    path = cache / url.rsplit("/", 1)[-1]
    if path.exists() and sha256(path) == expected_sha256:
        record = {
            "url": url,
            "bytes": path.stat().st_size,
            "sha256": expected_sha256,
            "cached": True,
        }
    else:
        record = download(url, path, HOSTS)
        if record["sha256"] != expected_sha256:
            raise ValueError(f"Pinned archive checksum mismatch: {url}")
    if expected_bytes is not None and record["bytes"] != expected_bytes:
        raise ValueError(f"Pinned archive size mismatch: {url}")
    return path, record


def extracted(archive: Path, digest: str, name: str) -> Path:
    target = ROOT / ".work" / "cache" / "makehuman" / f"{name}-{digest[:12]}"
    marker = target / ".extracted.json"
    if marker.exists() and read_json(marker).get("sha256") == digest:
        return target
    if target.exists():
        shutil.rmtree(target)
    result = extract_zip(archive, target)
    write_json(marker, {"sha256": digest, **result})
    return target


def recipe_path(candidate: dict) -> Path:
    name = require_slug(candidate["recipe"])
    path = ROOT / "config" / "human-recipes" / f"{name}.json"
    recipe = read_json(path)
    validate(recipe, read_json(ROOT / "schemas" / "human-recipe.schema.json"))
    if recipe["id"] != name:
        raise ValueError(f"Recipe id does not match filename: {path}")
    return path


def selected_paths(recipe: dict) -> list[str]:
    values = [recipe["skin"], *recipe["clothes"], *recipe["bodyparts"].values()]
    return sorted(set(values))


def preserve_descriptors(pack: Path, recipe: dict, directory: Path) -> list[dict]:
    records = []
    for value in selected_paths(recipe):
        relative = safe_relative_path(value)
        source = destination(pack, relative)
        if not source.is_file():
            raise ValueError(f"Recipe references a missing pack asset: {value}")
        targets = [source]
        if source.suffix == ".mhclo":
            targets.extend(sorted(source.parent.glob("*.mhmat")))
        for item in targets:
            output = directory / "provenance" / "makehuman" / item.relative_to(pack)
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, output)
        records.append({"path": relative.as_posix(), "sha256": sha256(source)})
    return records


def fetch_makehuman(source: dict, candidate: dict, directory: Path) -> dict:
    recipe_file = recipe_path(candidate)
    recipe = read_json(recipe_file)
    pack_archive, pack_record = pinned_archive(
        source["pack_url"], source["pack_sha256"], source.get("pack_bytes")
    )
    mpfb_archive, mpfb_record = pinned_archive(source["mpfb_url"], source["mpfb_sha256"])
    pack = extracted(pack_archive, source["pack_sha256"], "system-pack")
    mpfb = extracted(mpfb_archive, source["mpfb_sha256"], "mpfb2")
    mpfb_src = mpfb / f"mpfb2-{source['mpfb_commit']}" / "src"
    if not (mpfb_src / "mpfb" / "__init__.py").is_file():
        raise ValueError("Pinned MPFB archive does not contain src/mpfb")

    evidence = read_json(ROOT / "research" / "makehuman-system-pack.json")
    if evidence["archive"]["sha256"] != source["pack_sha256"]:
        raise ValueError("Committed pack research does not match the configured digest")
    (directory / "LICENSE.txt").write_text(evidence["license_text"], encoding="utf-8")
    descriptors = preserve_descriptors(pack, recipe, directory)
    write_json(directory / "provenance" / "recipe.json", recipe)
    write_json(
        directory / "provenance" / "pack.json",
        {key: evidence["archive"][key] for key in ("url", "bytes", "sha256")}
        | {"license_url": source["license_url"], "descriptors": descriptors},
    )

    model = directory / "model" / f"{candidate['id']}.glb"
    run(
        [
            "blender",
            "--background",
            "--factory-startup",
            "--python-exit-code",
            "1",
            "--python",
            str(ROOT / "rendering" / "build_makehuman.py"),
            "--",
            str(recipe_file.resolve()),
            str(pack.resolve()),
            str(mpfb_src.resolve()),
            str(model.resolve()),
        ],
        directory / "logs" / "makehuman-build.log",
        timeout=1200,
    )
    build = read_json(directory / "provenance" / "build-report.json")
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": source["creator"],
        "license": "CC0-1.0",
        "license_evidence": source["license_url"],
        "source_url": source["page"],
        "source_id": recipe["id"],
        "revision": source["pack_sha256"],
        "generation": {
            "tool": "MPFB2",
            "tool_revision": source["mpfb_commit"],
            "tool_license": source["tool_license"],
            "recipe": recipe["id"],
            "blender_version": build["blender_version"],
        },
        "downloads": [pack_record, mpfb_record],
    }
