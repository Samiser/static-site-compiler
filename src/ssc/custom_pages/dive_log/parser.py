import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from .types import Dive


namespaces = {"uddf": "http://www.streit.cc/uddf/3.2/"}


def _get_text(el: ET.Element, path: str) -> str | None:
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


def _parse_divesites(root: ET.Element) -> dict[str, str]:
    sites: dict[str, str] = {}
    for site_el in root.findall(".//uddf:divesite/uddf:site", namespaces):
        site_id = site_el.get("id")
        name = _get_text(site_el, "./uddf:name")
        if site_id and name:
            sites[site_id] = name
    return sites


def parse_uddf(uddf_path: Path) -> dict[int, Dive]:
    tree = ET.parse(str(uddf_path))
    root = tree.getroot()

    divesites = _parse_divesites(root)

    dives: dict[int, Dive] = {}
    for dive_el in root.findall(
        ".//uddf:profiledata/uddf:repetitiongroup/uddf:dive", namespaces
    ):
        divenumber = _get_text(dive_el, "./uddf:informationbeforedive/uddf:divenumber")
        if divenumber != None:
            dt_s = _get_text(dive_el, "./uddf:informationbeforedive/uddf:datetime")
            dt = datetime.fromisoformat(dt_s) if dt_s else None

            location = None
            for link_el in dive_el.findall(
                "./uddf:informationbeforedive/uddf:link[@ref]", namespaces
            ):
                site_ref = link_el.get("ref")
                if site_ref and site_ref in divesites:
                    location = divesites[site_ref]
                    break

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
                "location": location,
                "rating": rating,
                "visibility": visibility,
                "greatestdepth": greatestdepth,
                "diveduration": diveduration,
                "notes": notes,
            }

            dives[int(divenumber)] = dive

    return dives
