"""Bounded, retrying HTTP requests with an explicit host allowlist."""

import hashlib
import time
from pathlib import Path

import requests

MAX_FILE_BYTES = 400 * 1024 * 1024
USER_AGENT = "3d-Assets-Curator/0.1 (https://github.com/archnemix/3d-Assets)"


class DownloadError(RuntimeError):
    pass


def check_url(url: str, allowed_hosts: set[str]) -> None:
    parsed = requests.utils.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
        raise DownloadError(f"URL is outside the source allowlist: {url}")
    if parsed.username or parsed.password:
        raise DownloadError("Credentials in download URLs are forbidden")


def request(url: str, allowed_hosts: set[str], headers: dict | None = None) -> requests.Response:
    check_url(url, allowed_hosts)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, **(headers or {})})
    for attempt in range(3):
        try:
            response = session.get(url, timeout=(15, 120), stream=True)
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 2:
                response.close()
                time.sleep(2 ** (attempt + 1))
                continue
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 ** (attempt + 1))
    raise DownloadError(f"Could not fetch {url}")


def json(url: str, allowed_hosts: set[str], headers: dict | None = None) -> dict:
    with request(url, allowed_hosts, headers) as response:
        return response.json()


def text(url: str, allowed_hosts: set[str]) -> str:
    with request(url, allowed_hosts) as response:
        return response.content[: 1024 * 1024].decode("utf-8")


def download(
    url: str,
    path: Path,
    allowed_hosts: set[str],
    md5: str | None = None,
    headers: dict | None = None,
) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    digest = hashlib.sha256()
    md5_digest = hashlib.md5(usedforsecurity=False)
    size = 0
    try:
        with request(url, allowed_hosts, headers) as response, temporary.open("wb") as stream:
            for block in response.iter_content(1024 * 1024):
                size += len(block)
                if size > MAX_FILE_BYTES:
                    raise DownloadError(f"File exceeds {MAX_FILE_BYTES} bytes: {url}")
                stream.write(block)
                digest.update(block)
                md5_digest.update(block)
        if md5 and md5_digest.hexdigest() != md5:
            raise DownloadError(f"Upstream MD5 mismatch: {url}")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return {"url": url, "bytes": size, "sha256": digest.hexdigest()}
