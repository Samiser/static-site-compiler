import requests
from ssc.render import render_template
from .types import Releases
from pathlib import Path
from ssc.config.types import Secrets, Config
from ssc.parsers.types import Page


def get(token: str):
    username = "vinyl.enjoyer"
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases?sort=artist"

    headers = {
        "User-Agent": "Samiser/0.1 +https://samiser.xyz/#vinyl",
        "Authorization": f"Discogs token={token}",
    }

    r = requests.get(url, headers=headers)

    releases: Releases = {"releases": r.json()["releases"]}
    return releases


def create(secrets: Secrets, _config: Config) -> Page:

    token = secrets["discogs"]["token"]
    releases = get(token)

    html = render_template(
        Path(__file__).parent / "templates",
        "discogs.html",
        releases,
    )

    return Page(
        {"title": "vinyl", "content": html, "navbar": False, "type": "single-page"}
    )
