from ssc.custom_pages import lastfm, discogs, blog, dive_log

from ssc.site.types import Pages
from ssc.secrets.types import Secrets
from ssc.config.types import Config


def generate(config: Config, secrets: Secrets | None) -> Pages:
    pages: Pages = []

    if "blogs" in config:
        pages.append(blog.create(secrets, config))

    if secrets is not None:
        pages.append(lastfm.create(secrets, config))
        pages.append(discogs.create(secrets, config))

    if "dive_log" in config:
        pages.append(dive_log.create(secrets, config))

    return pages
