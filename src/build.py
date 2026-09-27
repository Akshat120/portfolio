"""Build index.html from template.html and map.json.

map.json comes from isochrone-delivery-areas (Hazratganj, scooter, 5/10/15
min, alpha 250 m). Run from the repo root:  python3 src/build.py
"""
import json
import re
from pathlib import Path

here = Path(__file__).parent
m = json.loads((here / "map.json").read_text())
w, h = m["w"], m["h"]


def top_point(d):
    """Highest vertex of a path, used to anchor each ring's label."""
    nums = list(map(float, re.findall(r"-?\d+\.?\d*", d)))
    pts = list(zip(nums[0::2], nums[1::2]))
    return min(pts, key=lambda p: p[1])


labels = []
for mins in ("15", "10", "5"):
    x, y = top_point(m["iso"][mins])
    labels.append(
        f'<text x="{x:.0f}" y="{y - 14:.0f}" text-anchor="middle" '
        f'paint-order="stroke" stroke="var(--paper)" stroke-width="8">{mins} min</text>'
    )

ox, oy = m["origin"]
svg = f'''<svg viewBox="0 0 {w} {h:.0f}" role="img" aria-labelledby="map-t map-d">
<title id="map-t">15-minute scooter delivery zone around Hazratganj, Lucknow</title>
<desc id="map-d">Three nested areas reachable by scooter in 5, 10 and 15 minutes, drawn over Lucknow's main roads. They cover {m["area"]["5"]}, {m["area"]["10"]} and {m["area"]["15"]} square kilometres.</desc>
<path class="minor" d="{m["minor"]}"/>
<path class="major" d="{m["major"]}"/>
<path class="iso i15" d="{m["iso"]["15"]}"/>
<path class="iso i10" d="{m["iso"]["10"]}"/>
<path class="iso i5" d="{m["iso"]["5"]}"/>
<circle class="halo" cx="{ox}" cy="{oy}" r="13"/>
<circle class="origin" cx="{ox}" cy="{oy}" r="8"/>
<text class="place" x="{ox + 20}" y="{oy + 9}" paint-order="stroke" stroke="var(--paper)" stroke-width="8">Hazratganj</text>
{"".join(labels)}
</svg>'''

html = (here / "template.html").read_text()
html = (html.replace("{{MAP_SVG}}", svg)
            .replace("{{A5}}", str(m["area"]["5"]))
            .replace("{{A10}}", str(m["area"]["10"]))
            .replace("{{A15}}", str(m["area"]["15"])))
(here.parent / "index.html").write_text(html)
print(f"index.html: {len(html) // 1024} KB")
