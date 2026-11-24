# POV Histories sources site

Static site for GitHub Pages. One page per episode listing its sources.

- Add an episode: copy `data/episodes/ep000.json` to `data/episodes/ep014.json`, fill it from the research dossier, set `"example": false` (or remove it).
- Build: `python3 build.py` (add `--examples` to include the example page while previewing).
- Publish: commit the generated `index.html`, `epNNN/` folders and `style.css`; GitHub Pages serves from the main branch root.
- Source types: `first-person`, `academic`, `archive` (shown in that order, primary first).
- Corrections after posting: add `{"date": "2027-01-10", "text": "..."}` to `corrections`.
