import json
from blog.lastfm_types import MyTopAlbums
from blog.render import render_template
from expecttest import assert_expected_inline

# Sample JSON response
sample_json = """
{
    "albums": {
        "week": [
            {
                "artist": {"url": "https://example.com", "name": "Snoop Dogg", "mbid": "f90e8b26-9e52-4669-a5c9-e28529c47894"},
                "image": [
                    {"size": "small", "text": "https://example.com/small.png"},
                    {"size": "large", "text": "https://example.com/large.png"}
                ]
            }
        ],
        "month": [],
        "year": []
    }
}
"""


def test_rendering():
    lastfm_data: MyTopAlbums = json.loads(sample_json)
    rendered_output = render_template("lastfm.html", lastfm_data)

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
 <img alt="" class="album-cover" loading="lazy" src="https://example.com/large.png"/>
 <div class="album-info">
  <h2 class="album-title">
  </h2>
  <p class="album-artist">
   Snoop Dogg
  </p>
  <p class="album-plays">
   song plays:
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
