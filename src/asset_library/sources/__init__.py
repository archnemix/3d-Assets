"""Source adapters return files plus evidence; they do not approve quality."""

from .github import fetch_github
from .github_release import fetch_github_release
from .grab3d import fetch_grab3d
from .innerscene import fetch_innerscene
from .makehuman import fetch_makehuman
from .oga_locomotive import fetch_oga_locomotive
from .polyhaven import fetch_polyhaven
from .three_d_assets import fetch_three_d_assets


def fetch(source: dict, candidate: dict, directory) -> dict:
    adapters = {
        "polyhaven": fetch_polyhaven,
        "github": fetch_github,
        "github-release": fetch_github_release,
        "makehuman": fetch_makehuman,
        "grab3d": fetch_grab3d,
        "innerscene": fetch_innerscene,
        "oga-locomotive": fetch_oga_locomotive,
        "three-d-assets": fetch_three_d_assets,
    }
    try:
        adapter = adapters[source["kind"]]
    except KeyError as error:
        raise ValueError(f"Unsupported source kind: {source['kind']}") from error
    return adapter(source, candidate, directory)
