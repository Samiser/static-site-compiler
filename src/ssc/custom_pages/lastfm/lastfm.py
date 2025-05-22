import json
import requests
from ssc.render import render_template
from .types import MyTopAlbums, TopAlbums
from ssc.secrets.types import Secrets
from ssc.config.types import Config
from ssc.parsers.types import Page
from pathlib import Path


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


def get_albums(api_key: str) -> MyTopAlbums:
    year = get_albums_from_period(api_key, "12month")
    month = get_albums_from_period(api_key, "1month")
    week = get_albums_from_period(api_key, "7day")

    return {
        "albums": {
            "week": week,
            "month": month,
            "year": year,
        }
    }


def create(secrets: Secrets, _config: Config) -> Page:

    api_key = secrets["lastfm"]["api_key"]
    my_top_albums = get_albums(api_key)

    html = render_template(
        Path(__file__).parent / "templates",
        "lastfm.html",
        my_top_albums,
    )

    return Page(
        {"title": "listening", "content": html, "navbar": False, "type": "single-page"}
    )
