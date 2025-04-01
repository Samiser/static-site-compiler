#!/usr/bin/env python

from collections import defaultdict, OrderedDict
from typing import TypeAlias

from blog import discogs
from blog import lastfm

from blog.args import get_args
from blog.config import load_configuration
from blog.filesystem import write_index_html, copy_files
from blog.parsers import custom_page
from blog.parsers import parse_posts, parse_pages
from blog.render import render_template

from blog.config_types import Config, Secrets
from blog.parser_types import PostsAndPages, Page, Post

Posts: TypeAlias = OrderedDict[str, Post]
PostTitlesByYear: TypeAlias = defaultdict[int, list[str]]


def generate_pages(config: Config, secrets: Secrets) -> dict[str, Page]:
    pages = parse_pages(config["pages"])

    custom_pages = {
        "listening": lastfm.create(config["templates"], secrets["lastfm"]["api_key"]),
        "vinyl": discogs.create(config["templates"], secrets["discogs"]["token"]),
    }

    for name in custom_pages:
        pages[name] = custom_page(name.title(), custom_pages[name], False)

    return pages


def group_blogs_by_year(blogs: Posts) -> PostTitlesByYear:
    titles_by_year: PostTitlesByYear = defaultdict(list)

    for title in blogs:
        titles_by_year[blogs[title]["meta"]["date"].year].append(title)

    return titles_by_year


def main():
    args = get_args()

    config, secrets = load_configuration(args["config"], args["secrets"])

    blogs = parse_posts(config["blogs"], exclude=["README.md"])
    pages = generate_pages(config, secrets)

    blogs_by_year = group_blogs_by_year(blogs)

    output = render_template(
        config["templates"],
        "main.html",
        PostsAndPages({"blogs": blogs, "blogs_by_year": blogs_by_year, "pages": pages}),
    )

    write_index_html(args["out"], output)
    copy_files(config["blogs"] / "images", args["out"] / "images")
    copy_files(config["static"], args["out"])


if __name__ == "__main__":
    main()
