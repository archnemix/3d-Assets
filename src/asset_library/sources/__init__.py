"""Source adapters return files plus evidence; they do not approve quality."""

from .github import fetch_github
from .polyhaven import fetch_polyhaven


def fetch(source: dict, candidate: dict, directory) -> dict:
    if source["kind"] == "polyhaven":
        return fetch_polyhaven(source, candidate, directory)
    if source["kind"] == "github":
        return fetch_github(source, candidate, directory)
    raise ValueError(f"Unsupported source kind: {source['kind']}")
