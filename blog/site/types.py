from typing import TypeAlias
from collections import defaultdict, OrderedDict

from blog.parsers.types import Page, Post


Posts: TypeAlias = OrderedDict[str, Post]
Pages: TypeAlias = dict[str, Page]
PostTitlesByYear: TypeAlias = defaultdict[int, list[str]]
