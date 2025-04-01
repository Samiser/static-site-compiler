from typing import TypedDict


class FormatData(TypedDict):
    name: str
    qty: str
    text: str
    descriptions: list[str]


class ArtistData(TypedDict):
    name: str
    anv: str
    join: str
    role: str
    tracks: str
    id: int
    resource_url: str


class LabelData(TypedDict):
    name: str
    catno: str
    entity_type: str
    entity_type_name: str
    id: int
    resource_url: str


class BasicInformation(TypedDict):
    id: int
    master_id: int
    master_url: str
    resource_url: str
    thumb: str
    cover_image: str
    title: str
    year: int
    formats: list[FormatData]
    artists: list[ArtistData]
    labels: list[LabelData]
    genres: list[str]
    styles: list[str]


class ReleaseData(TypedDict):
    id: int
    instance_id: int
    date_added: str
    rating: int
    basic_information: BasicInformation


class PaginationData(TypedDict):
    page: int
    pages: int
    per_page: int
    items: int
    urls: dict[str, str]


class Releases(TypedDict):
    releases: list[ReleaseData]


class DiscogsResponse(TypedDict):
    pagination: PaginationData
    releases: list[ReleaseData]
