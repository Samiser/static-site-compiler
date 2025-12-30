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

<div class="dive-accordion">
   
  <details class="dive">
    <summary>
      <span class="num">#1</span>
      <span class="date">
        <time datetime="2025-09-23T11:37:00">
          2025-09-23</time>
        <span class="location">Wraysbury Dive Centre</span>
      </span>
      <span class="time">11:37</span>
    </summary>

    <div class="dive-details">
      <dl>
        <div><dt>Depth</dt><dd>7.7m</dd></div>
        <div><dt>Duration</dt><dd>32:00</dd></div>
        <div><dt>Rating</dt><dd>3</dd></div>
        <div><dt>Visibility</dt><dd>3</dd></div>
      </dl>

      
      <div class="notes">
        <h3>Notes</h3>
        <p>here&#39;s a bunch of notes!<br />- list<br />- of<br />- things</p>
      </div>
      
    </div>
  </details>
  
</div>

<style>
  .dive-accordion {
    display: grid;
    gap: 0.6rem;
  }
  details.dive {
    border: 1px solid currentColor;
    border-radius: 10px;
    overflow: clip;
    background: var(--bgcolor);
    opacity: 0.9;
  }
  details.dive > summary {
    display: grid;
    grid-template-columns: 50px 1fr auto;
    gap: 0.75rem;
    align-items: center;
    padding: 0.6rem 0.8rem;
    cursor: pointer;
    list-style: none;
  }
  details.dive > summary::-webkit-details-marker {
    display: none;
  }
  details.dive[open] > summary {
    border-bottom: 1px solid currentColor;
    opacity: 0.3;
  }
  .num {
    font-weight: 600;
  }
  .date .location {
    opacity: 0.7;
    margin-left: 0.2rem;
  }
  .dive-details {
    padding: 0.75rem 0.9rem 1rem;
  }
  .dive-details dl {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  .dive-details dl > div {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }
  .dive-details dt {
    opacity: 0.6;
    font-size: 0.85em;
  }
  .dive-details dd {
    font-weight: 600;
  }
  .dive-details .notes h3 {
    margin-bottom: 0.3rem;
  }
  @media (max-width: 500px) {
    .dive-details dl {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>""",
    )
