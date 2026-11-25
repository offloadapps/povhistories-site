#!/usr/bin/env python3
"""Build the POV Histories sources site from data/episodes/*.json.

Each JSON file is one episode. Run `python3 build.py` here; it writes index.html and
<id>/index.html (ep014/index.html is served at /ep014/). Files with "example": true are
skipped unless you pass --examples.
"""
import json, sys, html
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
ORDER = [("first-person", "First-person accounts"), ("academic", "Scholarship"), ("archive", "Museums and archives")]
HEAD = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">')
ABOUT = ("POV Histories shows ordinary days of ordinary people across time. Each daily episode puts you "
         "in someone's hands for about a minute: the work they did, the food they ate, and the routines that "
         "filled their day. These pages list the sources behind each one.")

def esc(s): return html.escape(s or "")

def page(title, desc, body, depth):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{HEAD}<link rel="stylesheet" href="{up}style.css"></head>
<body><main>
<header class="masthead"><a class="wordmark" href="{up}">POV Histories</a><span class="section">Sources and notes</span></header>
{body}
<footer>New episodes daily on <a href="https://www.instagram.com/povhistories/">Instagram</a>, <a href="https://www.tiktok.com/@povhistories4">TikTok</a> and <a href="https://www.youtube.com/@povhistories0">YouTube</a>. Spotted an error? Comment on the video and we will check it.</footer>
</main></body></html>
"""

def domain(url):
    d = urlparse(url).netloc
    return d[4:] if d.startswith("www.") else d

def episode_html(ep):
    groups = []
    for key, label in ORDER:
        items = []
        for src in [x for x in ep["sources"] if x["type"] == key]:
            link = f' <a class="src" href="{esc(src["url"])}" rel="noopener">{esc(domain(src["url"]))}</a>' if src.get("url") else ""
            items.append(f'<li>{esc(src["citation"])}{link}</li>')
        if items:
            groups.append(f'<h2>{label}</h2>\n<ul class="bib">{"".join(items)}</ul>')
    corr = ep.get("corrections") or []
    corr_html = "".join(f'<li>{esc(c.get("date"))}. {esc(c.get("text"))}</li>' for c in corr)
    body = f"""<p class="shelfmark">{esc(ep["id"])}{" · " + esc(ep["series"]) if ep.get("series") else ""} · {esc(ep["era"])} · {esc(ep["place"])}</p>
<h1>{esc(ep["title"])}</h1>
<p class="lede">{esc(ep.get("summary"))}</p>
{chr(10).join(groups)}
<h2>What the film simplifies</h2>
<p class="note">{esc(ep.get("simplified")) or "Nothing beyond compressing a full day into about a minute."}</p>
<h2>Corrections</h2>
{f'<ul class="bib">{corr_html}</ul>' if corr_html else '<p class="note">None so far.</p>'}"""
    return page(f'{ep["id"]}: {ep["title"]} · POV Histories', ep.get("summary", ""), body, 1)

def main():
    examples = "--examples" in sys.argv
    eps = [json.loads(p.read_text()) for p in sorted((ROOT / "data/episodes").glob("*.json"))]
    eps = [e for e in eps if examples or not e.get("example")]
    eps.sort(key=lambda e: e.get("post_date", ""), reverse=True)
    for ep in eps:
        out = ROOT / ep["id"].lower() / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(episode_html(ep))
    rows = "".join(f'<li><span class="code">{esc(e["id"])}</span><a href="{e["id"].lower()}/">{esc(e["title"])}</a><span class="where">{esc(e["era"])}, {esc(e["place"])}</span></li>' for e in eps)
    body = f"""<h1>Sources for every episode</h1>
<p class="lede">{ABOUT}</p>
<p>We work from first-person accounts first, then scholarship, then museum and archive collections. Where a film simplifies something or the evidence is thin, its page says so.</p>
<h2>Episodes</h2>
{f'<ul class="toc">{rows}</ul>' if rows else '<p class="empty">The first episode is published on 4 January 2027.</p>'}"""
    (ROOT / "index.html").write_text(page("POV Histories · Sources and notes", ABOUT, body, 0))
    print(f"built {len(eps)} episode page(s)")

if __name__ == "__main__":
    main()
