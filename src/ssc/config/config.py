from pathlib import Path
from .types import Config


def create_config(blogs: Path, pages: Path) -> Config:
    return Config(
        {
            "blogs": blogs,
            "pages": pages,
        }
    )
