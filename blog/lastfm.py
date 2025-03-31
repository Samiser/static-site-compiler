import json
import requests
from blog.render import render_template


def get(api_key, method, payload):
    USER_AGENT = "Samiser"

    headers = {"user-agent": USER_AGENT}

    payload["api_key"] = (api_key,)
    payload["method"] = (method,)
    payload["format"] = "json"

    r = requests.get(
        "https://ws.audioscrobbler.com/2.0/", headers=headers, params=payload
    )
    return json.loads(r.text)


def get_albums_from_period(api_key, period):
    payload = {
        "period": period,
        "user": "Samiser",
        "limit": 5,
    }

    albums = get(api_key, "user.gettopalbums", payload)

    return albums["topalbums"]["album"]


def get_albums(api_key):
    year = get_albums_from_period(api_key, "12month")
    month = get_albums_from_period(api_key, "1month")
    week = get_albums_from_period(api_key, "7day")

    return year, month, week


def get_html(templates_dir, api_key):
    year, month, week = get_albums(api_key)

    html = render_template(
        templates_dir,
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
