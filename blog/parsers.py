import markdown
import frontmatter
from collections import OrderedDict
from collections.abc import Callable
from typing import TypeVar
from pathlib import Path

from blog.parser_types import Page, Post, Metadata


T = TypeVar("T")


def parse_content(content: str):
    parser = markdown.Markdown(extensions=["codehilite"])

    # parse markdown into HTML and use a bad
    # hack to ensure all images are lazy loaded
    return parser.convert(content).replace("<img alt", '<img loading="lazy" alt')


def parse_page(raw_md: frontmatter.Post):
    title = str(raw_md.metadata["title"])
    navbar = bool(raw_md.metadata.get("navbar", False))
    content = parse_content(raw_md.content)

    parsed: Page = {
        "title": title,
        "content": content,
        "navbar": navbar,
    }

    return parsed


def parse_post(raw_md: frontmatter.Post):
    word_count = len(raw_md.content.strip().split(" "))
    time_to_read = round(word_count / 300)

    tags: list[str] = (
        raw_md.metadata["tags"] if isinstance(raw_md.metadata["tags"], list) else []
    )
    title = str(raw_md.metadata["title"])
    summary = str(raw_md.metadata["summary"])
    date = raw_md.metadata["date"]
    publish = bool(raw_md.metadata["publish"])
    content = parse_content(raw_md.content)

    meta: Metadata = {
        "tags": tags,
        "title": title,
        "summary": summary,
        "date": date,
        "publish": publish,
        "time_to_read": time_to_read,
    }

    parsed: Post = {
        "content": content,
        "meta": meta,
    }

    return parsed


def get_files(dir: Path):
    return [x for x in dir.iterdir() if x.is_dir()]


def parse_files(
    dir: Path,
    exclude: list[str] | None,
    parse_function: Callable[[frontmatter.Post], T],
) -> dict[str, T]:
    out: dict[str, T] = {}

    if exclude is None:
        exclude = []

    for file in dir.glob("**/*.md"):
        name = file.stem
        if name not in exclude:
            with open(file, mode="r", encoding="utf-8") as infile:
                raw_md: frontmatter.Post = frontmatter.loads(infile.read())

            if "publish" in raw_md and not raw_md["publish"]:
                continue

            out[name] = parse_function(raw_md)

    return out


def parse_pages(dir: Path, exclude: list[str] | None = None) -> dict[str, Page]:
    return parse_files(dir, exclude, parse_page)


def parse_posts(dir: Path, exclude: list[str] | None = None) -> OrderedDict[str, Post]:
    parsed = parse_files(dir, exclude, parse_post)
    return OrderedDict(
        sorted(
            parsed.items(),
            key=lambda x: str(x[1]["meta"].get("date", "")),
            reverse=True,
        )
    )


def custom_page(title: str, content: str, navbar: bool) -> Page:
    return Page(
        {
            "content": content,
            "title": title,
            "navbar": navbar,
        }
    )
