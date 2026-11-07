"""Pin provenance to explicitly CC0 output files, not GPL source code."""

import pytest

from asset_library.sources.charactercreator_clothing import verify_metadata, verify_terms


def test_metadata_rejects_ambiguous_or_non_cc0_sources():
    item = {
        "id": "shirt",
        "file": "clothing_shirt.glb",
        "license": "CC0",
        "bytes": 123,
        "source": "MakeHuman",
    }
    verify_metadata(item, "shirt", 123)
    for change in ({"license": "CC-BY"}, {"file": "other.glb"}, {"bytes": 124}, {"source": ""}):
        with pytest.raises(ValueError):
            verify_metadata({**item, **change}, "shirt", 123)


def test_terms_explicitly_separate_output_licenses():
    notes = "Garment GLBs (`output/clothing_*.glb`) CC0-1.0 (all sources CC0 or our own authored data) A generated file derived from a **CC-BY** asset"
    verify_terms(notes)
    with pytest.raises(ValueError):
        verify_terms(notes.replace("CC0-1.0 (all sources CC0 or our own authored data)", "unknown"))
