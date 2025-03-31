import json
import requests
from blog.render import render_template


def get(token):
    username = "vinyl.enjoyer"
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases?sort=artist"

    headers = {
        "User-Agent": "Samiser/0.1 +https://samiser.xyz/#vinyl",
        "Authorization": f"Discogs token={token}"
    }

    r = requests.get(url, headers=headers)
    return r.json()['releases']


def get_html(templates_dir, token):
    releases = get(token)

    html = render_template(
        templates_dir,
        "discogs.html",
        { "releases": releases },
    )

    return html


def main():
    print(get_html())


if __name__ == "__main__":
    main()
