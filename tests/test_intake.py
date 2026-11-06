"""Re-running a completed quarantine batch refreshes evidence instead of duplicating downloads."""

from asset_library import intake
from asset_library.files import write_json


def test_existing_candidate_is_reinspected_without_refetching(tmp_path, monkeypatch):
    monkeypatch.setattr(intake, "ROOT", tmp_path)
    directory = tmp_path / "quarantine" / "test-batch" / "test-asset"
    directory.mkdir(parents=True)
    write_json(
        directory / "asset.json",
        {"id": "test-asset", "review": {"status": "awaiting-visual-review", "approved": False}},
    )
    calls = []
    monkeypatch.setattr(intake, "reinspect", lambda path: calls.append(path))

    def fail_fetch(*args):
        raise AssertionError("Existing candidates must not be downloaded again")

    monkeypatch.setattr(intake, "fetch", fail_fetch)
    result = intake.candidate({"id": "test-asset", "source": "polyhaven"}, "test-batch")
    assert calls == [directory]
    assert result["reinspected"] is True
    assert result["status"] == "awaiting-visual-review"
