from ssc.render import render_template
from ssc.filesystem import write_index_html, copy_files
from ssc.parsers import parse_pages

from pathlib import Path
from ssc.config.types import Config
from .types import Pages


def _generate_index_html(pages: Pages):
    return render_template(
        Path(__file__).parent / "templates", "main.html", {"pages": pages}
    )


def build(config: Config, custom_pages: Pages | None, out_dir: Path):
    md_pages = parse_pages(config["pages"])

    pages = md_pages if custom_pages is None else custom_pages + md_pages

    output = _generate_index_html(pages)

    write_index_html(out_dir, output)

    images = config["blogs"] / "images"
    if images.exists():
        copy_files(config["blogs"] / "images", out_dir / "images")

    copy_files(config["static"], out_dir)
    copy_files(Path(__file__).parent.parent / "style", out_dir)
