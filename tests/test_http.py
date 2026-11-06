import pytest
import requests

from asset_library import http
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


class FakeResponse:
    def __init__(self, status):
        self.status_code = status
        self.closed = False

    def close(self):
        self.closed = True

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


def _session_returning(monkeypatch, statuses):
    """Patch Session.get to walk a fixed sequence of status codes."""
    calls = []
    sleeps = []

    class FakeSession:
        headers = {}

        def get(self, url, **kwargs):
            calls.append(url)
            return FakeResponse(statuses[len(calls) - 1])

    monkeypatch.setattr(http.requests, "Session", FakeSession)
    monkeypatch.setattr(http.time, "sleep", sleeps.append)
    return calls, sleeps


def test_transient_server_error_is_retried_then_succeeds(monkeypatch):
    calls, sleeps = _session_returning(monkeypatch, [500, 500, 200])
    response = http.request("https://dl.polyhaven.org/a.jpg", {"dl.polyhaven.org"})
    assert response.status_code == 200
    assert len(calls) == 3
    assert sleeps == [2, 4]


def test_retries_are_bounded_and_reraise(monkeypatch):
    calls, sleeps = _session_returning(monkeypatch, [500] * http.MAX_ATTEMPTS)
    with pytest.raises(requests.HTTPError):
        http.request("https://dl.polyhaven.org/a.jpg", {"dl.polyhaven.org"})
    assert len(calls) == http.MAX_ATTEMPTS
    assert sleeps == [2, 4, 8]


def test_client_errors_are_not_retried(monkeypatch):
    calls, sleeps = _session_returning(monkeypatch, [404])
    with pytest.raises(requests.HTTPError):
        http.request("https://dl.polyhaven.org/a.jpg", {"dl.polyhaven.org"})
    assert len(calls) == 1
    assert sleeps == []
