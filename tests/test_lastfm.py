import json
from ssc.custom_pages.lastfm.types import MyTopAlbums
from ssc.render import render_template
from expecttest import assert_expected_inline
from pathlib import Path

# Sample JSON response
sample_json = """
{
  "albums": {
    "week": [
      {
        "artist": {
          "url": "https://www.last.fm/music/clipping.",
          "name": "clipping.",
          "mbid": "84ca8fa4-7cca-4948-a90a-cb44db29853d"
        },
        "image": [
          {
            "size": "small",
            "#text": "https://lastfm.freetls.fastly.net/i/u/34s/ed7fd62962ee0e28b8c26555d67521ba.png"
          },
          {
            "size": "medium",
            "#text": "https://lastfm.freetls.fastly.net/i/u/64s/ed7fd62962ee0e28b8c26555d67521ba.png"
          },
          {
            "size": "large",
            "#text": "https://lastfm.freetls.fastly.net/i/u/174s/ed7fd62962ee0e28b8c26555d67521ba.png"
          },
          {
            "size": "extralarge",
            "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/ed7fd62962ee0e28b8c26555d67521ba.png"
          }
        ],
        "mbid": "4a18986d-1598-43a8-b15f-0340af442ffe",
        "url": "https://www.last.fm/music/clipping./Dead+Channel+Sky",
        "playcount": "98",
        "@attr": {
          "rank": "1"
        },
        "name": "Dead Channel Sky"
      }
    ],
    "month": [],
    "year": []
  }
}
"""


def test_rendering():
    lastfm_data: MyTopAlbums = json.loads(sample_json)
    rendered_output = render_template(
        Path(__file__).parent.parent
        / "src"
        / "ssc"
        / "custom_pages"
        / "lastfm"
        / "templates",
        "lastfm.html",
        lastfm_data,
    )

    assert_expected_inline(
        rendered_output,
        """\
<p>
 this page shows my most listened to albums of the past week, month and year
</p>
<p>
 the data comes from my
 <a href="https://www.last.fm/user/Samiser">
  lastfm profile
 </a>
 and it's updated
  every minute
</p>
<h2>
 week
</h2>
<div class="album">
 <img alt="Dead Channel Sky" class="album-cover" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/ed7fd62962ee0e28b8c26555d67521ba.png"/>
 <div class="album-info">
  <h2 class="album-title">
   Dead Channel Sky
  </h2>
  <p class="album-artist">
   clipping.
  </p>
  <p class="album-plays">
   song plays: 98
  </p>
 </div>
</div>
<h2>
 month
</h2>
<h2>
 year
</h2>
""",
    )
