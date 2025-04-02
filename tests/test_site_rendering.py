import pytest
from pytest import TempPathFactory
import json
from expecttest import assert_expected_inline
from pathlib import Path

from blog.site import build
from blog.config import load_config


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("site")


@pytest.fixture(scope="module")
def config_file(tmp_path_factory: TempPathFactory) -> Path:
    config_data = {
        "templates": "templates",
        "blogs": "tests/test_data/blogs",
        "static": "tests/test_data/static",
        "pages": "tests/test_data/pages",
    }
    config_path = tmp_path_factory.mktemp("config") / "config.json"
    _: int = config_path.write_text(json.dumps(config_data))
    return config_path


@pytest.fixture(scope="module")
def built_site(site_dir: Path, config_file: Path) -> Path:
    """Builds the site once and returns the output directory."""
    config = load_config(config_file)
    build(config, None, site_dir)
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
    <a href="#test_page">
     Home
    </a>
    <a href="#blog">
     Blog
    </a>
   </nav>
  </header>
  <main>
   <section id="test_page">
    <h1>
     Home
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
     Blog
    </h1>
    <hr/>
    <p>
     for the music i'm currently listening to, check out
     <a href="/#listening">
      listening
     </a>
     <p>
      for my current vinyl collection, check out
      <a href="/#vinyl">
       vinyl
      </a>
      <h2>
       2000
      </h2>
      <ul>
       <li>
        <a href="#2000-01-01-test_post">
         <em>
          2000-01-01
         </em>
         - Test page
        </a>
       </li>
      </ul>
     </p>
    </p>
   </section>
   <section id="2000-01-01-test_post">
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
