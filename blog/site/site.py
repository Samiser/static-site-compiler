from collections import defaultdict
from datetime import date
from typing import cast

from blog.render import render_template
from blog.filesystem import write_index_html, copy_files
from blog.parsers import parse_posts, parse_pages

from pathlib import Path
from blog.config.types import Config
from .types import Posts, Pages, PostTitlesByYear


def _group_posts_by_year(posts: Posts) -> PostTitlesByYear:
    titles_by_year: PostTitlesByYear = defaultdict(list)

    for title in posts:
        post_date = cast(date, posts[title]["meta"]["date"])
        titles_by_year[post_date.year].append(title)

    return titles_by_year


def _generate_index_html(posts: Posts, pages: Pages):
    return render_template(
        "main.html",
        {
            "blogs": posts,
            "blogs_by_year": _group_posts_by_year(posts),
            "pages": pages,
        },
    )


def build(config: Config, custom_pages: Pages | None, out_dir: Path):
    posts = parse_posts(config["blogs"], exclude=["README.md"])
    md_pages = parse_pages(config["pages"])

    if custom_pages is None:
        pages = md_pages
    else:
        pages = {**custom_pages, **md_pages}

    output = _generate_index_html(posts, pages)

    write_index_html(out_dir, output)
    copy_files(config["blogs"] / "images", out_dir / "images")
    copy_files(config["static"], out_dir)
    copy_files(Path(__file__).parent.parent / "style", out_dir)
