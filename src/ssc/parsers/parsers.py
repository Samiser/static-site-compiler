import markdown
import frontmatter
from collections.abc import Callable
from typing import TypeVar
from pathlib import Path

from .types import Page


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
        "type": "single-page",
    }

    return parsed


def get_files(dir: Path):
    return [x for x in dir.iterdir() if x.is_dir()]


def parse_files(
    dir: Path,
    exclude: list[str] | None,
    parse_function: Callable[[frontmatter.Post], T],
) -> list[T]:
    out: list[T] = []

    if exclude is None:
        exclude = []

    for file in dir.glob("**/*.md"):
        name = file.stem
        if name not in exclude:
            with open(file, mode="r", encoding="utf-8") as infile:
                raw_md: frontmatter.Post = frontmatter.loads(infile.read())

            if "publish" in raw_md and not raw_md["publish"]:
                continue

            out.append(parse_function(raw_md))

    return out


def parse_pages(dir: Path, exclude: list[str] | None = None) -> list[Page]:
    return parse_files(dir, exclude, parse_page)
