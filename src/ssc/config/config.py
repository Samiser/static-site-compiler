from pathlib import Path
from .types import Config


def create_config(
    pages: Path,
    blogs: Path | None = None,
    dive_log: Path | None = None,
) -> Config:
    config = Config({"pages": pages})
    if blogs is not None:
        config["blogs"] = blogs
    if dive_log is not None:
        config["dive_log"] = dive_log
    return config
