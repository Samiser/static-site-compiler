from typing import TypedDict
from collections import OrderedDict, defaultdict


class Metadata(TypedDict):
    tags: list[str]
    title: str
    summary: str
    date: object
    publish: bool
    time_to_read: int


class Post(TypedDict):
    content: str
    meta: Metadata


class Page(TypedDict):
    title: str
    content: str
    navbar: bool


class PostsAndPages(TypedDict):
    blogs: OrderedDict[str, Post]
    blogs_by_year: defaultdict[int, list[str]]
    pages: dict[str, Page]
