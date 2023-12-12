#!/usr/bin/env python

import os
import markdown
import jinja2
import json
import frontmatter

import lastfm
import discogs

from render import render_template
from collections import OrderedDict, defaultdict


def get_files(dir_string):
    return os.listdir(os.fsencode(dir_string))


def parse_markdown(raw_md):
    parser = markdown.Markdown(extensions=["codehilite"])

    # parse markdown into HTML and use a bad
    # hack to ensure all images are lazy loaded
    parsed = {
        "content": parser.convert(raw_md.content).replace(
            "<img alt", '<img loading="lazy" alt'
        ),
        "meta": raw_md.metadata,
    }

    parsed["meta"]["time_to_read"] = round(len(raw_md.content.strip().split(" ")) / 300)

    return parsed


def parse_dir(dir_string, exclude=[], sort_output=False):
    out = {}

    for file in get_files(dir_string):
        name = os.fsdecode(file)
        if name.endswith(".md") and name not in exclude:
            infile = open(os.path.join(dir_string, name), mode="r", encoding="utf-8")
            raw_md = frontmatter.loads(infile.read())

            if "publish" in raw_md and not raw_md["publish"]:
                continue

            out[name[:-3]] = parse_markdown(raw_md)

    if sort_output:
        return OrderedDict(
            sorted(out.items(), key=lambda x: x[1]["meta"]["date"], reverse=True)
        )
    else:
        return OrderedDict(
            sorted(out.items(), key=lambda x: x[1]["meta"]["navbar_position"])
        )


def main():

    with open("config.json", "r") as raw:
        config = json.load(raw)

    blogs = parse_dir(config["blogs"], exclude=["README.md"], sort_output=True)
    pages = parse_dir(config["pages"])

    #pages["listening"] = {
    #    "content": lastfm.get_html(),
    #    "meta": {"title": "Listening", "navbar": False, "time_to_read": 0},
    #}

    #pages["vinyl"] = {
    #    "content": discogs.get_html(),
    #    "meta": {"title": "Vinyl", "navbar": False, "time_to_read": 0},
    #}

    blogs_by_year = defaultdict(list)
    for blog in blogs:
        blogs_by_year[blogs[blog]["meta"]["date"].year].append(blog)

    output = render_template(
        config["templates"],
        "main.html",
        {"blogs": blogs, "blogs_by_year": blogs_by_year, "pages": pages},
    )

    outfile = open(f"index.html", mode="w")

    outfile.write(output)


if __name__ == "__main__":
    main()
