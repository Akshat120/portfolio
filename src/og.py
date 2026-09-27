"""Render img/og.png, the 1200x630 link-preview image, with headless Chrome.

Run after build.py:  python3 src/og.py
"""
import re
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).parent.parent
svg = re.search(r"<svg viewBox.*?</svg>", (root / "index.html").read_text(), re.S).group(0)

page = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,500&display=swap" rel="stylesheet">
<style>
:root{{--paper:#f4f1ea;--ink:#23211d;--soft:#5f5a51;--faint:#938c80;--rule:#dcd6ca;--road:#cfc8ba;--road-major:#a9a193;--iso:#c2531b}}
body{{margin:0;width:1200px;height:630px;background:var(--paper);color:var(--ink);display:grid;grid-template-columns:560px 1fr;overflow:hidden}}
.text{{padding:72px 0 64px 72px;display:flex;flex-direction:column}}
h1{{font:500 76px/1.02 Newsreader,Georgia,serif;letter-spacing:-.02em;margin:0 0 18px}}
p{{font:400 30px/1.35 Newsreader,Georgia,serif;color:var(--soft);margin:0}}
.foot{{margin-top:auto;font:500 24px 'IBM Plex Mono',monospace;color:var(--iso)}}
.map{{padding:24px 24px 24px 0}}
svg{{width:100%;height:100%}}
.minor{{fill:none;stroke:var(--road);stroke-width:.8}}.major{{fill:none;stroke:var(--road-major);stroke-width:1.5}}
.iso{{fill:var(--iso);stroke:var(--iso);stroke-width:1.6}}.i15{{fill-opacity:.07}}.i10{{fill-opacity:.1}}.i5{{fill-opacity:.16}}
.origin{{fill:var(--iso)}}.halo{{fill:var(--paper)}}
text{{font:500 26px 'IBM Plex Mono',monospace;fill:var(--iso)}}text.place{{fill:var(--ink);font-weight:400}}
</style></head><body>
<div class="text"><h1>Akshat<br>Dhiman</h1><p>Backend engineer in Lucknow.<br>Go services and geospatial systems.<br>Ex-Deliveroo · NIT Warangal.</p>
<div class="foot">akshatdhiman.in</div></div>
<div class="map">{svg}</div></body></html>"""

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
    fh.write(page)
subprocess.run([chrome, "--headless=new", "--hide-scrollbars", "--window-size=1200,630",
                "--force-device-scale-factor=1", "--virtual-time-budget=4000",
                f"--screenshot={root / 'img' / 'og.png'}", f"file://{fh.name}"],
               check=True, capture_output=True)
print("wrote img/og.png")
