from pathlib import Path
from .types import Config


def create_config(blogs: Path, pages: Path, dive_log: Path) -> Config:
    return Config(
        {
            "blogs": blogs,
            "pages": pages,
            "dive_log": dive_log,
        }
    )
