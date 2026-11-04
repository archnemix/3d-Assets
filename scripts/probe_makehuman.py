"""Record the official MakeHuman pack's digest and asset metadata, not its 267 MB payload."""

import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

URL = "https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
OUTPUT = Path("reports/research/makehuman-pack")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    archive = Path(".work/makehuman-system.zip")
    archive.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(URL, headers={"User-Agent": "3d-Assets-Curator/0.1"})
    digest = hashlib.sha256()
    with urllib.request.urlopen(request, timeout=120) as response, archive.open("wb") as stream:
        while block := response.read(1024 * 1024):
            digest.update(block)
            stream.write(block)
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        records = [{"path": name, "bytes": package.getinfo(name).file_size} for name in names]
        metadata = {}
        for name in names:
            if name.endswith((".mhmat", ".mhclo", ".mhpack")) or "license" in name.lower():
                if package.getinfo(name).file_size < 100_000:
                    metadata[name] = package.read(name).decode("utf-8", errors="replace")
    report = {"url": URL, "sha256": digest.hexdigest(), "bytes": archive.stat().st_size,
              "files": records}
    (OUTPUT / "archive.json").write_text(json.dumps(report, indent=2) + "\n")
    (OUTPUT / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Verified download: {report['bytes']} bytes; SHA-256 {digest.hexdigest()}")
    print(f"Archive entries: {len(names)}; metadata documents: {len(metadata)}")


if __name__ == "__main__":
    main()
