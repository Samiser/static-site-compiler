from ssc.render import render_template
from pathlib import Path
from .types import Dive
from .parser import parse_uddf
from ssc.secrets.types import Secrets
from ssc.config.types import Config
from ssc.parsers.types import Page


def create(_secrets: Secrets | None, config: Config) -> Page:
    log_path = config.get("dive_log")
    assert log_path is not None

    dives: dict[int, Dive] = parse_uddf(log_path)

    html = render_template(
        Path(__file__).parent / "templates",
        "dive_log.html",
        {"dives": dives},
    )

    return Page(
        {"title": "dives", "content": html, "navbar": False, "type": "single-page"}
    )
