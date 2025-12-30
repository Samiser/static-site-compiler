from typing import TypedDict
from datetime import datetime


class Dive(TypedDict):
    # before dive
    divenumber: int
    datetime: datetime | None
    location: str | None
    # after dive
    rating: int | None
    visibility: int | None
    greatestdepth: float | None
    diveduration: int | None
    notes: str | None
