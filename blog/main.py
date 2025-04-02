#!/usr/bin/env python

from blog import lastfm
from blog import discogs

from blog.args import get_args
from blog.config import load_configuration
from blog.site import build

from blog.site_types import Pages
from blog.parsers import custom_page
from collections.abc import Callable
from typing import TypeAlias

CustomPageCreators: TypeAlias = dict[str, Callable[[], str]]


def generate_custom_pages(creators: CustomPageCreators) -> Pages:
    return {
        name: custom_page(name.title(), creator(), False)
        for name, creator in creators.items()
    }


def main():
    args = get_args()

    config, secrets = load_configuration(args["config"], args["secrets"])

    custom_pages = generate_custom_pages(
        {
            "listening": lambda: lastfm.create(secrets["lastfm"]["api_key"]),
            "vinyl": lambda: discogs.create(secrets["discogs"]["token"]),
        }
    )

    build(config, custom_pages, args["out"])


if __name__ == "__main__":
    main()
