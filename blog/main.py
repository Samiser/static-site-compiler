#!/usr/bin/env python

import os
import markdown
import jinja2
import json
import frontmatter
import shutil

from blog import lastfm
from blog import discogs
from blog.render import render_template
from blog.args import get_args

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
        return out

def copy_files(source_dir, dest_dir):
    try:
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        print(f"Copied files from {source_dir} to {dest_dir}")
    except FileNotFoundError:
        print(f"Source directory {source_dir} does not exist.")
    except Exception as e:
        print(f"Error copying files: {e}")

def load_file(path):
    with open(path, "r") as f:
        try:
            config = json.load(f)
            print(f"Loaded file {path}")
            return config
        except FileNotFoundError:
            print(f"Failed to load {path}, file not found")


def main():

    args = get_args()

    config = load_file(args.config)
    secrets = load_file(args.secrets)

    blogs = parse_dir(config["blogs"], exclude=["README.md"], sort_output=True)
    pages = parse_dir(config["pages"])

    pages["listening"] = {
        "content": lastfm.get_html(config["templates"], secrets["lastfm"]["API-Key"]),
        "meta": {"title": "Listening", "navbar": False, "time_to_read": 0},
    }

    pages["vinyl"] = {
        "content": discogs.get_html(config["templates"], secrets["discogs"]["token"]),
        "meta": {"title": "Vinyl", "navbar": False, "time_to_read": 0},
    }

    blogs_by_year = defaultdict(list)
    for blog in blogs:
        blogs_by_year[blogs[blog]["meta"]["date"].year].append(blog)

    output = render_template(
        config["templates"],
        "main.html",
        {"blogs": blogs, "blogs_by_year": blogs_by_year, "pages": pages},
    )

    outfile = f"{args.out}/index.html"

    with open(f"{args.out}/index.html", mode="w") as f:
        f.write(output)
        print(f"Blog compiled and writted to {outfile}")

    copy_files(os.path.join(config["blogs"], "images"), os.path.join(args.out, "images"))
    copy_files(config["static"], args.out)

if __name__ == "__main__":
    main()
