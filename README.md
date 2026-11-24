# POV Histories sources site

Public source notes for POV Histories, a daily short film about ordinary days of ordinary people across time. Served by GitHub Pages from `main` at https://offloadapps.github.io/povhistories-site/.

## Add an episode

1. Copy `data/episodes/ep000.json` to `data/episodes/ep014.json` and fill it from the research dossier. Remove `"example": true`.
2. `series` is `Forgotten Jobs` or `An Ordinary Day`.
3. Each source has a `type`: `first-person`, `academic` or `archive`. Pages list them in that order.
4. Add later fixes to `corrections` as `{"date": "2027-01-10", "text": "..."}`.
5. Run `python3 build.py` and commit the generated `index.html` and `ep014/` folder.

`python3 build.py --examples` includes the example page for a local preview. Do not commit `ep000/`.

Design pass based on the unslop skill by Damir Sokolovsky (CC BY 4.0), copy checked against theclaymethod/unslop's taboo phrase list.
