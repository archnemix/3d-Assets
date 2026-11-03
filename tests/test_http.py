import pytest

from asset_library.http import DownloadError, check_url


def test_download_host_allowlist():
    check_url("https://dl.polyhaven.org/file/model.glb", {"dl.polyhaven.org"})
    for url in [
        "http://dl.polyhaven.org/a",
        "https://evil.example/a",
        "https://user:pass@dl.polyhaven.org/a",
    ]:
        with pytest.raises(DownloadError):
            check_url(url, {"dl.polyhaven.org"})
