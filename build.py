#!/usr/bin/env python3
"""Build the History Insta sources site from data/episodes/*.json.

Each JSON file = one episode. Run `python3 build.py` from this folder; it writes
index.html and <id>/index.html (e.g. ep014/index.html -> /ep014/). Episodes with
"example": true are skipped unless --examples is passed.
"""
import json, sys, html
from pathlib import Path

ROOT = Path(__file__).parent
LABELS = {"first-person": "First-person accounts", "academic": "Academic sources", "archive": "Museums and archives"}
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Silkscreen&display=swap" rel="stylesheet">'

def page(title, body, depth):
    css = "../" * depth + "style.css"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>{FONT}<link rel="stylesheet" href="{css}"></head>
<body><main>{body}
<footer>POV Histories · first-person days from forgotten history. Instagram @povhistories · TikTok @povhistories4</footer>
</main></body></html>
"""

def esc(s): return html.escape(s or "")

def episode_html(ep):
    groups = []
    for t in ["first-person", "academic", "archive"]:
        items = []
        for src in [x for x in ep["sources"] if x["type"] == t]:
            link = f' <a href="{esc(src["url"])}" rel="noopener">Link</a>' if src.get("url") else ""
            items.append(f'<li>{esc(src["citation"])}{link}</li>')
        if items:
            groups.append(f'<h2>{esc(LABELS[t])}</h2><ol class="sources">{"".join(items)}</ol>')
    corr = ep.get("corrections") or []
    corr_html = "".join(f'<li><strong>{esc(c.get("date"))}</strong> {esc(c.get("text"))}</li>' for c in corr)
    body = f"""<a class="brand" href="../">← POV HISTORIES · SOURCES</a>
<h1>{esc(ep["id"])} · {esc(ep["title"])}</h1>
<p class="meta">{esc(ep["era"])} · {esc(ep["place"])}</p>
<p>{esc(ep.get("summary"))}</p>
{''.join(groups)}
<h2>What we simplified</h2>
<p class="note">{esc(ep.get("simplified")) or "Nothing beyond normal compression of a full day into about a minute."}</p>
<h2>Corrections</h2>
<ul class="note">{corr_html or "<li>None so far. Spotted an error? Comment on the video and we will check it.</li>"}</ul>"""
    return page(f'{ep["id"]} sources · POV Histories', body, 1)

def main():
    examples = "--examples" in sys.argv
    eps = [json.loads(p.read_text()) for p in sorted((ROOT / "data/episodes").glob("*.json"))]
    eps = [e for e in eps if examples or not e.get("example")]
    eps.sort(key=lambda e: e.get("post_date", ""), reverse=True)
    for ep in eps:
        out = ROOT / ep["id"].lower() / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(episode_html(ep))
    rows = "".join(f'<li><span class="code">{esc(e["id"])}</span><a href="{e["id"].lower()}/">{esc(e["title"])}</a> <span class="note">· {esc(e["era"])}, {esc(e["place"])}</span></li>' for e in eps)
    body = f"""<span class="brand">POV HISTORIES · SOURCES</span>
<h1>Where every episode comes from</h1>
<p>Each video is a first-person day in a real historical trade. Every detail is checked against academic work, first-person accounts and museum collections, listed here per episode, newest first.</p>
<ul class="episodes">{rows or '<li class="note">First episode arrives 4 January 2027.</li>'}</ul>"""
    (ROOT / "index.html").write_text(page("Sources · POV Histories", body, 0))
    print(f"built {len(eps)} episode page(s)")

if __name__ == "__main__":
    main()
