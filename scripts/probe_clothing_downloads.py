"""Check whether public garment sources serve files without signing in.

A successful HTTP response is not a license or quality approval. No source files
are retained and signed URL query strings are intentionally not recorded.
"""

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

URLS = {
    "blendswap-cloth-library": "https://blendswap.com/blend/19332/download",
    "blendswap-character-kit": "https://blendswap.com/blend/28676/download",
    "blendswap-mindys-wardrobe": "https://blendswap.com/blend/22938/download",
}


def main():
    result = {}
    for name, url in URLS.items():
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "3d-Assets-Curator/0.1"})
            with urllib.request.urlopen(request, timeout=40) as response:
                target = urllib.parse.urlsplit(response.url)
                sample = response.read(64)
                result[name] = {
                    "source": url,
                    "status": response.status,
                    "final_url_without_query": urllib.parse.urlunsplit(
                        (target.scheme, target.netloc, target.path, "", "")
                    ),
                    "content_type": response.headers.get("Content-Type"),
                    "content_length": response.headers.get("Content-Length"),
                    "signature_hex": sample[:16].hex(),
                }
        except (urllib.error.URLError, TimeoutError) as error:
            result[name] = {"source": url, "error": str(error)}
        print(name, result[name], flush=True)
    path = Path("reports/research/clothing-download-access.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
