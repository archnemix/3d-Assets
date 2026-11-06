"""Fetch immutable GitHub revisions and preserve external glTF dependencies."""

from pathlib import Path, PurePosixPath
from urllib.parse import quote

from asset_library.files import destination, safe_relative_path, write_json
from asset_library.gltf import dependencies
from asset_library.http import download, text

HOSTS = {"raw.githubusercontent.com", "github.com", "objects.githubusercontent.com"}


def raw_url(source: dict, path: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{source['repository']}/{source['commit']}/{quote(path)}"
    )


def fetch_github(source: dict, candidate: dict, directory: Path) -> dict:
    license_text = text(raw_url(source, source["license_path"]), HOSTS)
    if "Creative Commons Zero" not in license_text and "CC0 1.0 Universal" not in license_text:
        raise ValueError("Pinned upstream license is not explicitly CC0")
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    if source.get("terms_path"):
        terms_path = safe_relative_path(source["terms_path"]).as_posix()
        terms_text = text(raw_url(source, terms_path), HOSTS)
        if "CC0" not in terms_text:
            raise ValueError("Pinned upstream terms do not confirm CC0")
        evidence = directory / "provenance" / "upstream-terms.md"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(terms_text, encoding="utf-8")
    upstream = safe_relative_path(candidate["path"]).as_posix()
    if PurePosixPath(upstream).suffix.lower() not in {".glb", ".gltf"}:
        raise ValueError("GitHub model must be GLB or glTF")
    model = directory / "model" / Path(upstream).name
    records = [download(raw_url(source, upstream), model, HOSTS)]
    parent = PurePosixPath(upstream).parent
    if model.suffix == ".gltf":
        import json

        document = json.loads(model.read_text(encoding="utf-8"))
        for dependency in sorted(dependencies(document)):
            relative = safe_relative_path(dependency)
            remote = (parent / relative).as_posix()
            records.append(
                download(raw_url(source, remote), destination(model.parent, relative), HOSTS)
            )
    write_json(
        directory / "provenance" / "github-source.json",
        {
            "repository": source["repository"],
            "commit": source["commit"],
            "path": upstream,
            "license_path": source["license_path"],
            "terms_path": source.get("terms_path"),
            "original_creator": source["creator"],
            "original_page": source["page"],
            "mirror_notice": source.get("mirror_notice"),
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": source["creator"],
        "license": "CC0-1.0",
        "license_evidence": raw_url(source, source["license_path"]),
        "source_url": f"https://github.com/{source['repository']}/blob/{source['commit']}/{quote(upstream)}",
        "source_id": upstream,
        "revision": source["commit"],
        "downloads": records,
    }
