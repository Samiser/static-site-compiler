import json
from ssc.custom_pages.discogs.types import Releases
from pathlib import Path
from ssc.render import render_template
from expecttest import assert_expected_inline

# Sample JSON response mimicking Discogs API
sample_json = """
{
  "releases": [
    {
      "id": 18420268,
      "instance_id": 1404031020,
      "date_added": "2023-07-12T14:55:12-07:00",
      "rating": 0,
      "basic_information": {
        "id": 18420268,
        "master_id": 2091856,
        "master_url": "https://api.discogs.com/masters/2091856",
        "resource_url": "https://api.discogs.com/releases/18420268",
        "thumb": "",
        "cover_image": "",
        "title": "Bring Backs",
        "year": 2021,
        "formats": [
          {
            "name": "Vinyl",
            "qty": "1",
            "text": "Gatefold",
            "descriptions": [
              "LP",
              "Album"
            ]
          }
        ],
        "artists": [
          {
            "name": "Alfa Mist",
            "anv": "",
            "join": "",
            "role": "",
            "tracks": "",
            "id": 4751065,
            "resource_url": "https://api.discogs.com/artists/4751065"
          }
        ],
        "labels": [
          {
            "name": "Anti-",
            "catno": "7789-1",
            "entity_type": "1",
            "entity_type_name": "Label",
            "id": 1873,
            "resource_url": "https://api.discogs.com/labels/1873"
          }
        ],
        "genres": [
          "Jazz"
        ],
        "styles": [
          "Contemporary Jazz"
        ]
      }
    }
  ]
}
"""


def test_rendering_discogs():
    discogs_data: Releases = json.loads(sample_json)
    rendered_output = render_template(
        Path(__file__).parent.parent
        / "src"
        / "ssc"
        / "custom_pages"
        / "discogs"
        / "templates",
        "discogs.html",
        discogs_data,
    )

    assert_expected_inline(
        rendered_output,
        """\
<p>
  welcome to my vinyl collection! powered by
  <a href="https://www.discogs.com/user/vinyl.enjoyer/collection">discogs</a>
</p>
<div class="collection">
  
  <div class="collection-cell">
    <a href="https://www.discogs.com/release/18420268">
      <img
        loading="lazy"
        src=""
        alt="Bring Backs"
      />
    </a>
  </div>
  
</div>""",
    )
