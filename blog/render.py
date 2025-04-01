import jinja2
from blog.lastfm_types import MyTopAlbums as LastFMTopAlbums
from blog.discogs_types import Releases as DiscogsReleases
from pathlib import Path
from blog.parser_types import PostsAndPages


def render_template(
    template_dir: Path,
    template_file: str,
    template_vars: LastFMTopAlbums | DiscogsReleases | PostsAndPages,
):
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template(template_file)

    return template.render(template_vars)
