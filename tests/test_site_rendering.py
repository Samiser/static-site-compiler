import pytest
from pytest import TempPathFactory
from expecttest import assert_expected_inline
from pathlib import Path

from ssc.site import build
from ssc.config.types import Config, Secrets
from ssc.custom_pages import blog


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("site")


@pytest.fixture(scope="module")
def built_site(site_dir: Path) -> Path:
    """Builds the site once and returns the output directory."""
    test_data_path = Path(__file__).parent / "test_data"

    secrets: Secrets = {
        "lastfm": {"api_key": "boop", "shared_secret": "boop"},
        "discogs": {"token": "boop"},
        "letterboxd": {"username": "boop", "password": "boop"},
    }

    config: Config = {
        "templates": Path("templates"),
        "blogs": test_data_path / "blogs",
        "static": test_data_path / "static",
        "pages": test_data_path / "pages",
    }

    build(config, [blog.create(secrets, config)], site_dir)
    return site_dir


def test_static_files(built_site: Path):
    static_file = built_site / "static_file"
    assert static_file.exists()


def test_style_file(built_site: Path):
    style_file = built_site / "style.css"
    assert style_file.exists()


def test_main_rendering(built_site: Path):
    rendered_index = (built_site / "index.html").read_text()
    assert_expected_inline(
        rendered_index,
        """\
<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width,initial-scale=1" name="viewport"/>
  <title>
   Samiser
  </title>
  <meta content="Samiser's space on the internet" name="description"/>
  <!-- twitter card -->
  <meta content="Samiser" property="og:title"/>
  <meta content="my space on the internet" property="og:description"/>
  <meta content="https://images.samiser.xyz/location.png" property="og:image"/>
  <meta content="summary_large_image" name="twitter:card"/>
  <link href="style.css" rel="stylesheet"/>
 </head>
 <body>
  <header>
   <h1>
    <a href="#home">
     Samiser
    </a>
   </h1>
   <nav>
    <a href="#test">
     Test
    </a>
    <a href="#blog">
     blog
    </a>
   </nav>
  </header>
  <main>
   <section id="test">
    <h1>
     Test
    </h1>
    <hr/>
    <p>
     test page
    </p>
    <p>
     with a
     <a href="#blog">
      link!
     </a>
    </p>
   </section>
   <section id="blog">
    <h1>
     blog
    </h1>
    <hr/>
    <p>
     occasionally i like writing about things here
    </p>
    <h2>
     2000
    </h2>
    <ul>
     <li>
      <a href="#2000-01-01-test-page">
       <em>
        2000-01-01
       </em>
       - Test page
      </a>
     </li>
    </ul>
   </section>
   <section id="2000-01-01-test-page">
    <h1>
     Test page
    </h1>
    <p>
     <em>
      2000-01-01
     </em>
    </p>
    <p>
     <em>
      0 minute read
     </em>
    </p>
    <hr/>
    <p>
     This is a test!
    </p>
    <pre class="codehilite"><code class="language-python">print("test")
</code></pre>
    <hr/>
    <a href="#blog">
     Back
    </a>
   </section>
  </main>
 </body>
</html>
""",
    )
