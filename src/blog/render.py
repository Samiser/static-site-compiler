import jinja2
from bs4 import BeautifulSoup

from pathlib import Path
from blog.custom_pages.lastfm.types import MyTopAlbums as LastFMTopAlbums
from blog.custom_pages.discogs.types import Releases as DiscogsReleases
from blog.parsers.types import PostsAndPages


def render_template(
    template_file: str,
    template_vars: LastFMTopAlbums | DiscogsReleases | PostsAndPages,
) -> str:
    template_dir = Path(__file__).parent / "templates"
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template(template_file)

    rendered = template.render(template_vars)

    soup = BeautifulSoup(rendered, "html.parser")
    return soup.prettify()
