import json
import requests
from blog.render import render_template
from blog.lastfm_types import MyTopAlbums, TopAlbums


def get(api_key: str, method: str, period: str) -> TopAlbums:
    USER_AGENT = "Samiser"

    headers = {"user-agent": USER_AGENT}

    payload = {
        "api_key": api_key,
        "method": method,
        "format": "json",
        "period": period,
        "user": "Samiser",
        "limit": "5",
    }

    r = requests.get(
        "https://ws.audioscrobbler.com/2.0/", headers=headers, params=payload
    )

    response: TopAlbums = json.loads(r.text)

    return response


def get_albums_from_period(api_key: str, period: str):
    albums = get(api_key, "user.gettopalbums", period)

    return albums["topalbums"]["album"]


def get_albums(api_key: str):
    year = get_albums_from_period(api_key, "12month")
    month = get_albums_from_period(api_key, "1month")
    week = get_albums_from_period(api_key, "7day")

    return year, month, week


def create(api_key: str) -> str:
    year, month, week = get_albums(api_key)

    my_top_albums: MyTopAlbums = {
        "albums": {
            "week": week,
            "month": month,
            "year": year,
        }
    }

    html = render_template(
        "lastfm.html",
        my_top_albums,
    )

    return html
