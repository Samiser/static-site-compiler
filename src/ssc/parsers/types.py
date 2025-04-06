from typing import TypedDict, Literal, TypeAlias

PageType: TypeAlias = Literal["multi-page", "single-page"]


class Page(TypedDict):
    title: str
    content: str
    navbar: bool
    type: PageType
