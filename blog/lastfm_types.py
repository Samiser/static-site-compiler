from typing import TypedDict


class ImageData(TypedDict):
    size: str
    text: str


class ArtistData(TypedDict):
    url: str
    name: str
    mbid: str


class AlbumData(TypedDict):
    artist: ArtistData
    image: list[ImageData]


class TopAlbumsData(TypedDict):
    album: list[AlbumData]


class TopAlbums(TypedDict):
    topalbums: TopAlbumsData


class TopAlbumsByPeriod(TypedDict):
    week: list[AlbumData]
    month: list[AlbumData]
    year: list[AlbumData]


class MyTopAlbums(TypedDict):
    albums: TopAlbumsByPeriod
