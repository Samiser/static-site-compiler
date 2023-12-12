import json
import requests
from render import render_template


def get():
    with open("../secrets.json", "r") as f:
        secrets = json.loads(f.read())
        token = secrets["discogs"]["token"]

    username = "vinyl.enjoyer"
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases?sort=artist"

    headers = {
        "User-Agent": "Samiser/0.1 +https://samiser.xyz/#vinyl",
        "Authorization": f"Discogs token={token}"
    }

    r = requests.get(url, headers=headers)
    return r.json()['releases']


def get_html():
    with open("config.json", "r") as raw:
        config = json.load(raw)

    releases = get()

    html = render_template(
        config["templates"],
        "discogs.html",
        { "releases": releases },
    )

    return html


def main():
    print(get_html())


if __name__ == "__main__":
    main()
