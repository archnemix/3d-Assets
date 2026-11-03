"""Inspect the official MakeHuman pack without redistributing its 267 MB payload.

This is a source-research utility, not an asset approval step. It records the
archive checksum and small, CC0 asset descriptors so generation can be pinned.
"""

import zipfile
from pathlib import Path

from asset_library.files import sha256, write_json
from asset_library.http import download, text

PACK_URL = "https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
LICENSE_URL = "https://raw.githubusercontent.com/makehumancommunity/makehuman/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/LICENSE.ASSETS.md"


def main() -> None:
    archive = Path("/tmp/makehuman_system_assets_cc0.zip")
    record = download(PACK_URL, archive, {"files2.makehumancommunity.org"})
    license_text = text(LICENSE_URL, {"raw.githubusercontent.com"})
    if "CC0" not in license_text:
        raise ValueError("MakeHuman asset license needs manual review")
    descriptors = {}
    with zipfile.ZipFile(archive) as package:
        entries = [{"path": info.filename, "bytes": info.file_size} for info in package.infolist() if not info.is_dir()]
        for entry in entries:
            name = entry["path"]
            if name.lower().endswith((".mhclo", ".mhmat")) or Path(name).name.lower().startswith(("license", "pack")):
                if entry["bytes"] > 100_000:
                    continue
                payload = package.read(name)
                try:
                    descriptors[name] = payload.decode("utf-8")
                except UnicodeDecodeError:
                    continue
    output = Path("research/makehuman-system-pack.json")
    write_json(output, {"archive": {**record, "sha256": sha256(archive)},
                        "license_url": LICENSE_URL, "license_text": license_text,
                        "entries": entries, "descriptors": descriptors})
    print(f"Inspected {len(entries)} pack entries; SHA-256 {record['sha256']}", flush=True)


if __name__ == "__main__":
    main()
