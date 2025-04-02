from . import discogs, lastfm

from blog.site.types import Pages
from blog.config.types import Secrets
from blog.parsers.types import Page
from collections.abc import Callable
from typing import TypeAlias

CustomPageCreators: TypeAlias = dict[str, Callable[[], str]]


def custom_page(title: str, content: str, navbar: bool) -> Page:
    return Page(
        {
            "content": content,
            "title": title,
            "navbar": navbar,
        }
    )


def generate(secrets: Secrets) -> Pages:
    pages: CustomPageCreators = {
        "listening": lambda: lastfm.create(secrets["lastfm"]["api_key"]),
        "vinyl": lambda: discogs.create(secrets["discogs"]["token"]),
    }

    return {
        name: custom_page(name.title(), creator(), False)
        for name, creator in pages.items()
    }
