"""Record the official MakeHuman pack's digest and small CC0 asset descriptors.

The 267 MB archive stays in temporary CI storage. Only evidence needed to pin
and audit generation is committed. This is source research, not asset approval.
"""

import hashlib
import urllib.request
import zipfile
from pathlib import Path

from asset_library.files import write_json

PACK_URL = "https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
LICENSE_URL = "https://raw.githubusercontent.com/makehumancommunity/makehuman/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/LICENSE.ASSETS.md"


def main() -> None:
    archive = Path("/tmp/makehuman_system_assets_cc0.zip")
    digest = hashlib.sha256()
    request = urllib.request.Request(PACK_URL, headers={"User-Agent": "3d-Assets-Curator/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response, archive.open("wb") as stream:
        while block := response.read(1024 * 1024):
            digest.update(block)
            stream.write(block)
    with urllib.request.urlopen(LICENSE_URL, timeout=60) as response:
        license_text = response.read(100_000).decode("utf-8")
    if "CC0" not in license_text:
        raise ValueError("MakeHuman asset license needs manual review")
    descriptors = {}
    with zipfile.ZipFile(archive) as package:
        entries = [
            {"path": info.filename, "bytes": info.file_size}
            for info in package.infolist()
            if not info.is_dir()
        ]
        for entry in entries:
            name = entry["path"]
            if name.lower().endswith((".mhclo", ".mhmat")) or Path(name).name.lower().startswith(
                ("license", "pack")
            ):
                if entry["bytes"] > 100_000:
                    continue
                try:
                    descriptors[name] = package.read(name).decode("utf-8")
                except UnicodeDecodeError:
                    continue
    write_json(
        Path("research/makehuman-system-pack.json"),
        {
            "archive": {
                "url": PACK_URL,
                "bytes": archive.stat().st_size,
                "sha256": digest.hexdigest(),
            },
            "license_url": LICENSE_URL,
            "license_text": license_text,
            "entries": entries,
            "descriptors": descriptors,
        },
    )
    print(f"Inspected {len(entries)} pack entries; SHA-256 {digest.hexdigest()}", flush=True)


if __name__ == "__main__":
    main()
