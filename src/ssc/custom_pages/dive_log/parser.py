import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from .types import Dive


namespaces = {"uddf": "http://www.streit.cc/uddf/3.2/"}


def _get_text(el: ET.Element, path: str) -> str | None:
    """findtext with namespace + strip; returns None if missing/empty"""
    t = el.findtext(path, default=None, namespaces=namespaces)
    if t is None:
        return None
    t = t.strip()
    return t if t else None


def _to_int(s: str | None) -> int | None:
    if s is None:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _to_float(s: str | None) -> float | None:
    if s is None:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_uddf(uddf_path: Path) -> dict[int, Dive]:
    tree = ET.parse(str(uddf_path))
    root = tree.getroot()
    dives: dict[int, Dive] = {}
    for dive_el in root.findall(
        ".//uddf:profiledata/uddf:repetitiongroup/uddf:dive", namespaces
    ):
        divenumber = _get_text(dive_el, "./uddf:informationbeforedive/uddf:divenumber")
        if divenumber != None:
            dt_s = _get_text(dive_el, "./uddf:informationbeforedive/uddf:datetime")
            dt = datetime.fromisoformat(dt_s) if dt_s else None

            rating = _to_int(
                _get_text(
                    dive_el, "./uddf:informationafterdive/uddf:rating/uddf:ratingvalue"
                )
            )

            visibility = _to_int(
                _get_text(dive_el, "./uddf:informationafterdive/uddf:visibility")
            )

            greatestdepth = _to_float(
                _get_text(dive_el, "./uddf:informationafterdive/uddf:greatestdepth")
            )

            diveduration = _to_int(
                _get_text(dive_el, "./uddf:informationafterdive/uddf:diveduration")
            )

            notes = _get_text(
                dive_el, "./uddf:informationafterdive/uddf:notes/uddf:para"
            )

            dive: Dive = {
                "divenumber": int(divenumber),
                "datetime": dt,
                "rating": rating,
                "visibility": visibility,
                "greatestdepth": greatestdepth,
                "diveduration": diveduration,
                "notes": notes,
            }

            dives[int(divenumber)] = dive

    return dives
