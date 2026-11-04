"""Fetch Grab3D's directly published CC0 GLB packages.

Grab3D ships a per-package manifest and CC0 dedication beside each download. The
manifest is treated as the upstream file inventory; the adapter verifies the
license before downloading and preserves the package's AI-origin disclosure.
"""

from pathlib import Path

from asset_library.files import write_json
from asset_library.gltf_repair import normalize_skin_weights
from asset_library.http import download, json, text

HOSTS = {"grab3d.com"}


def package_base(source: dict, slug: str) -> str:
    return f"{source['download_base'].rstrip('/')}/{slug}"


def page_url(source: dict, slug: str) -> str:
    page_slug = slug.removesuffix("-rigged").removesuffix("-light")
    return f"{source['page'].rstrip('/')}/{page_slug}/"


def verify_cc0(manifest: dict, license_text: str) -> None:
    if manifest.get("extras", {}).get("license") != "CC0-1.0":
        raise ValueError("Grab3D manifest does not declare CC0-1.0")
    if "CC0 1.0 Universal" not in license_text:
        raise ValueError("Grab3D package license is not explicitly CC0")


def fetch_grab3d(source: dict, candidate: dict, directory: Path) -> dict:
    slug = candidate["upstream_id"]
    base = package_base(source, slug)
    manifest_url = f"{base}/manifest.json"
    license_url = f"{base}/LICENSE.txt"
    manifest = json(manifest_url, HOSTS)
    if manifest.get("slug") != slug:
        raise ValueError(f"Grab3D manifest slug mismatch: expected {slug}")
    license_text = text(license_url, HOSTS)
    verify_cc0(manifest, license_text)
    try:
        glb = manifest["files"]["glb"]
    except KeyError as error:
        raise ValueError(f"Grab3D package has no GLB download: {slug}") from error
    model = directory / "model" / Path(glb["name"]).name
    model_url = f"{base}/{glb['name']}"
    record = download(model_url, model, HOSTS)
    if record["bytes"] != glb["bytes"]:
        raise ValueError(f"Grab3D package size changed while downloading: {slug}")
    repair = normalize_skin_weights(model)
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    write_json(directory / "provenance" / "grab3d-manifest.json", manifest)
    write_json(directory / "provenance" / "grab3d-repair.json", repair)
    write_json(
        directory / "provenance" / "grab3d-package.json",
        {
            "slug": slug,
            "page_url": page_url(source, slug),
            "manifest_url": manifest_url,
            "license_url": license_url,
            "model_url": model_url,
            "download": record,
        },
    )
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": source["creator"],
        "license": "CC0-1.0",
        "license_evidence": license_url,
        "license_page": source["license_page"],
        "source_url": page_url(source, slug),
        "source_id": slug,
        "revision": repair["repaired_sha256"],
        "downloads": [record],
        "repairs": [repair] if repair["normalized_vertices"] else [],
        "origin": manifest.get("origin", {}),
    }
