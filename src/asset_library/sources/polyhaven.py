"""Resolve the official Poly Haven file API, including every glTF dependency."""

from pathlib import Path

from asset_library.files import destination, safe_relative_path, write_json
from asset_library.http import download, json, text

HOSTS = {
    "api.polyhaven.com",
    "dl.polyhaven.org",
    "polyhaven.com",
    "creativecommons.org",
    "raw.githubusercontent.com",
}
LICENSE_REVISION = "2fd1796dc3506dfa8269439aac8e6f5c65876bd1"


def fetch_polyhaven(source: dict, candidate: dict, directory: Path) -> dict:
    upstream = candidate["upstream_id"]
    resolution = candidate.get("resolution", "2k")
    headers = {"User-Agent": source["user_agent"], "Referer": source["user_agent"]}
    info = json(f"{source['api']}/info/{upstream}", HOSTS, headers)
    files = json(f"{source['api']}/files/{upstream}", HOSTS, headers)
    # The website is a JavaScript application. Check the official, immutable API terms instead.
    terms_url = f"https://raw.githubusercontent.com/Poly-Haven/Public-API/{LICENSE_REVISION}/ToS.md"
    license_document = text(terms_url, HOSTS)
    if "CC0 assets carry no attribution requirement whatsoever" not in license_document:
        raise ValueError("Poly Haven's license statement changed; manual review required")
    try:
        package = files["gltf"][resolution]["gltf"]
    except KeyError as error:
        raise ValueError(f"No glTF package at {resolution} for {upstream}") from error
    model = directory / "model" / Path(package["url"]).name
    records = [download(package["url"], model, HOSTS, package.get("md5"), headers)]
    for relative, entry in package.get("include", {}).items():
        path = destination(directory / "model", safe_relative_path(relative))
        records.append(download(entry["url"], path, HOSTS, entry.get("md5"), headers))
    write_json(directory / "provenance" / "api-info.json", info)
    write_json(directory / "provenance" / "selected-package.json", package)
    license_text = text("https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt", HOSTS)
    (directory / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    return {
        "model": model.relative_to(directory).as_posix(),
        "creator": ", ".join(info.get("authors", {})),
        "license": "CC0-1.0",
        "license_evidence": terms_url,
        "license_page": source["license_page"],
        "source_url": source["page"] + upstream,
        "source_id": upstream,
        "resolution": resolution,
        "downloads": records,
        "api_credit": "Powered by Poly Haven. This credits the discovery API, not a condition on asset use.",
    }
