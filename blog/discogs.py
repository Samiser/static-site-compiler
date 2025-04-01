import requests
from blog.render import render_template
from blog.discogs_types import Releases
from pathlib import Path


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


def create(templates_dir: Path, token: str):
    releases = get(token)

    html = render_template(
        templates_dir,
        "discogs.html",
        releases,
    )

    return html
