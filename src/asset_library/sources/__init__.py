"""Source adapters return files plus evidence; they do not approve quality."""

from .github import fetch_github
from .makehuman import fetch_makehuman
from .polyhaven import fetch_polyhaven


def fetch(source: dict, candidate: dict, directory) -> dict:
    adapters = {
        "polyhaven": fetch_polyhaven,
        "github": fetch_github,
        "makehuman": fetch_makehuman,
    }
    try:
        adapter = adapters[source["kind"]]
    except KeyError as error:
        raise ValueError(f"Unsupported source kind: {source['kind']}") from error
    return adapter(source, candidate, directory)
