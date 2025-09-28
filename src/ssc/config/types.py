from typing import TypedDict
from pathlib import Path


class Config(TypedDict):
    blogs: Path
    pages: Path
    dive_log: Path
