from ssc.render import render_template
from ssc.filesystem import write_index_html, copy_files
from ssc.parsers import parse_pages

from pathlib import Path
from collections.abc import Generator
from ssc.config.types import Config
from .types import Pages


def _generate_index_html(pages: Pages):
    return render_template(
        Path(__file__).parent / "templates", "main.html", {"pages": pages}
    )


def _copy_images_and_static_files(config: Config, out_dir: Path):
    paths: Generator[Path] = (
        config[base] / dir
        for dir in ["images", "static"]
        for base in ["blogs", "pages"]
    )

    for path in paths:
        if path.exists():
            copy_files(path, out_dir / "images" if path.name == "images" else out_dir)


def build(config: Config, custom_pages: Pages | None, out_dir: Path):
    md_pages = parse_pages(config["pages"])

    pages = md_pages if custom_pages is None else md_pages + custom_pages

    output = _generate_index_html(pages)

    write_index_html(out_dir, output)

    _copy_images_and_static_files(config, out_dir)

    copy_files(Path(__file__).parent.parent / "static", out_dir)
