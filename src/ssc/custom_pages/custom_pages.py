from ssc.custom_pages import lastfm, discogs, blog, dive_log

from ssc.site.types import Pages
from ssc.secrets.types import Secrets
from ssc.config.types import Config
from ssc.parsers.types import Page
from collections.abc import Callable


def custom_page(
    create: Callable[[Secrets, Config], Page], secrets: Secrets, config: Config
) -> Page:
    return create(secrets, config)


def generate(config: Config, secrets: Secrets) -> Pages:

    creators = map(
        lambda x: x.create,
        [blog, lastfm, discogs, dive_log],
    )

    return [custom_page(creator, secrets, config) for creator in creators]
