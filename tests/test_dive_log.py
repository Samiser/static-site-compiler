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
          2025-09-23 </time
        >
      </span>
      <span class="time"
        >11:37</span
      >
      <span class="depth">
         7.7 m 
      </span>
      <span class="duration">
              32:00  
      </span>
      <span class="rating">
         3 
      </span>
      <span class="vis"
        >3</span
      >
    </summary>

    <div class="notes">
      <h3>Notes</h3>
      
      <p>here&#39;s a bunch of notes!<br />- list<br />- of<br />- things</p>
      
    </div>
  </details>
  
</div>

<style>
  .dive-accordion {
    display: grid;
    gap: 0.6rem;
  }
  details.dive {
    border: 1px solid var(--border, #e3e3e3);
    border-radius: 10px;
    overflow: clip;
    background: var(--bg, #fff);
  }
  details.dive > summary {
    display: grid;
    grid-template-columns: 64px 130px 80px 120px 120px 110px 1fr;
    gap: 0.75rem;
    align-items: center;
    padding: 0.6rem 0.8rem;
    cursor: pointer;
    list-style: none; /* hide default marker in some browsers */
  }
  details.dive > summary::-webkit-details-marker {
    display: none;
  }
  details.dive[open] > summary {
    border-bottom: 1px solid var(--border, #e3e3e3);
  }
  details.dive .notes {
    padding: 0.75rem 0.9rem 1rem;
  }
  .muted {
    opacity: 0.65;
  }

  /* Make it look table-ish and tidy */
  .num {
    font-weight: 600;
  }
  .rating {
    letter-spacing: 0.08em;
  }

  /* Responsive: collapse to fewer columns on narrow screens */
  @media (max-width: 640px) {
    details.dive > summary {
      grid-template-columns: 60px 1fr 1fr;
      grid-auto-rows: minmax(0, auto);
      row-gap: 0.25rem;
    }
    .depth,
    .duration,
    .rating,
    .vis {
      opacity: 0.9;
      font-size: 0.95em;
    }
  }
</style>""",
    )
