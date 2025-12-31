import re
import markdown
import frontmatter
from collections.abc import Callable
from typing import TypeVar, cast
from pathlib import Path

from .types import Page


T = TypeVar("T")


def _add_lazy_loading(html: str) -> str:
    """Add loading="lazy" to img tags that don't already have it."""
    return re.sub(r"<img(?![^>]*loading=)", '<img loading="lazy"', html)


def parse_content(content: str):
    parser = markdown.Markdown(extensions=["codehilite", "fenced_code"])
    return _add_lazy_loading(parser.convert(content))


def parse_page(raw_md: frontmatter.Post):
    title = str(raw_md.metadata["title"])
    navbar = bool(raw_md.metadata.get("navbar", False))
    order = cast(int, raw_md.metadata.get("order", 99))
    content = parse_content(raw_md.content)

    parsed: Page = {
        "title": title,
        "content": content,
        "navbar": navbar,
        "type": "single-page",
        "order": order,
    }

    return parsed


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
