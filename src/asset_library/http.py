"""Bounded, retrying HTTP requests with an explicit host allowlist."""

import hashlib
import time
from pathlib import Path

import requests

MAX_FILE_BYTES = 400 * 1024 * 1024
USER_AGENT = "3d-Assets-Curator/0.1 (https://github.com/archnemix/3d-Assets)"

# Poly Haven's CDN intermittently returns 500 for a single texture while the rest
# of the package serves fine. Retry those long enough to ride out a brief blip:
# four attempts with 2s, 4s and 8s waits span ~14s rather than ~6s.
MAX_ATTEMPTS = 4
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


class DownloadError(RuntimeError):
    pass


def check_url(url: str, allowed_hosts: set[str]) -> None:
    parsed = requests.utils.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
        raise DownloadError(f"URL is outside the source allowlist: {url}")
    if parsed.username or parsed.password:
        raise DownloadError("Credentials in download URLs are forbidden")


def request(url: str, allowed_hosts: set[str], headers: dict | None = None) -> requests.Response:
    """Fetch a URL, retrying only transient failures.

    Transport errors and the statuses in ``RETRY_STATUSES`` are worth another
    attempt. A permanent client error such as 404 or 403 is not: retrying it just
    delays the real error, so it propagates on the first attempt.
    """
    check_url(url, allowed_hosts)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, **(headers or {})})
    for attempt in range(MAX_ATTEMPTS):
        last = attempt == MAX_ATTEMPTS - 1
        try:
            response = session.get(url, timeout=(15, 120), stream=True)
        except requests.RequestException:
            if last:
                raise
            time.sleep(2 ** (attempt + 1))
            continue
        if response.status_code in RETRY_STATUSES and not last:
            response.close()
            time.sleep(2 ** (attempt + 1))
            continue
        response.raise_for_status()
        return response
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
