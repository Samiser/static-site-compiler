import json
import requests
from render import render_template


def get(method, payload):
    with open("../secrets.json", "r") as f:
        secrets = json.loads(f.read())
        API_KEY = secrets["lastfm"]["API-Key"]
        USER_AGENT = "Samiser"

    headers = {"user-agent": USER_AGENT}

    payload["api_key"] = (API_KEY,)
    payload["method"] = (method,)
    payload["format"] = "json"

    r = requests.get(
        "https://ws.audioscrobbler.com/2.0/", headers=headers, params=payload
    )
    return json.loads(r.text)


def get_albums_from_period(period):
    payload = {
        "period": period,
        "user": "Samiser",
        "limit": 5,
    }

    albums = get("user.gettopalbums", payload)

    return albums["topalbums"]["album"]


def get_albums():
    year = get_albums_from_period("12month")
    month = get_albums_from_period("1month")
    week = get_albums_from_period("7day")

    return year, month, week


def get_html():
    with open("config.json", "r") as raw:
        config = json.load(raw)

    year, month, week = get_albums()

    html = render_template(
        config["templates"],
        "lastfm.html",
        {
            "albums": {
                "Week": week,
                "Month": month,
                "Year": year,
            }
        },
    )

    return html


def main():
    print(get_albums())


if __name__ == "__main__":
    main()
