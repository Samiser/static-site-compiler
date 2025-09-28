from ssc.custom_pages.dive_log.types import Dive
from ssc.custom_pages.dive_log.parser import parse_uddf
from pathlib import Path
from ssc.render import render_template
from expecttest import assert_expected_inline

sample_uddf = """
"""


def test_rendering_discogs():
    dives: dict[int, Dive] = parse_uddf(
        Path(__file__).parent / "test_data" / "dives.uddf"
    )

    rendered_output = render_template(
        Path(__file__).parent.parent
        / "src"
        / "ssc"
        / "custom_pages"
        / "dive_log"
        / "templates",
        "dive_log.html",
        {"dives": dives},
    )

    assert_expected_inline(
        rendered_output,
        """\
<p>
  my dive log, parsed from uddf exported from
  <a href="https://subsurface-divelog.org/">subsurface</a>
</p>

<table class="dive-log">
  <thead>
    <tr>
      <th>#</th>
      <th>Date</th>
      <th>Time</th>
      <th>Max depth</th>
      <th>Duration</th>
      <th>Rating</th>
      <th>Vis</th>
      <!-- <th style="min-width: 240px">Notes</th> -->
    </tr>
  </thead>
  <tbody>
     
    <tr>
      <td>#1</td>
      <td>
        2025-09-23
      </td>
      <td>11:37</td>

      <td>
         7.7 m 
      </td>

      <td>
              32:00  
      </td>

      <td> 3 </td>

      <td>3</td>

      <!-- <td>here's a bunch of notes!
- list
- of
- things</td> -->
    </tr>
    
  </tbody>
</table>

<style>
  table.dive-log {
    width: 100%;
    border-collapse: collapse;
  }
  table.dive-log th,
  table.dive-log td {
    padding: 0.5rem 0.6rem;
    border-bottom: 1px solid var(--border, #e3e3e3);
    text-align: left;
  }
  table.dive-log thead th {
    position: sticky;
    top: 0;
    background: var(--bg, #fff);
  }
</style>""",
    )
