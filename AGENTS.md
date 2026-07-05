# AGENTS.md — meal-prep

**What this is:** Mikey and Kendra's household meal-prep system — a library of recipes cooked in one Sunday batch session and eaten across five weekdays, plus a static web app (index.html) that turns recipe picks into an aggregated Costco shopping list. Personal repo, not research.

## Start here

- [README.md](README.md) — orientation, the weekly rhythm, repo map
- [docs/recipe-format.md](docs/recipe-format.md) — read before creating or editing any recipe; the app parses recipe files directly and the format is load-bearing
- [docs/sunday-cook-day.md](docs/sunday-cook-day.md) — how the cooking afternoon is sequenced
- [docs/costco-run.md](docs/costco-run.md) — standing staples, pack sizes, the non-Costco list
- [PROJECT_INDEX.md](PROJECT_INDEX.md) — dashboard

## Rules that always apply

- After adding or editing a recipe: add new files to [recipes/manifest.json](recipes/manifest.json) and run `python3 tools/validate.py`. The app only sees what the manifest lists, and only parses what matches the format.
- Reuse existing ingredient names and units exactly (check the validator's near-duplicate warnings) — differently spelled items don't aggregate on the shopping list.
- New recipes must earn their place on leftover quality: good at day 4 to 5, or a deliberate fast-finish design like the smash burgers. No fish. Spices and fridge-door condiments are pantry staples, never buy-list items.
- index.html stays a single dependency-free file: no build step, no libraries, nothing fetched from outside the repo. It must keep working on GitHub Pages and via `python3 -m http.server`.
- Writing follows `~/.claude/writing-style-guide.md`.
- **Template deviation, deliberate:** no `data/`, `paper/`, `deep-research/`, or `feedback/` folders — this is a recipe library with a static app, and none of the research-template machinery applies. If research-style artifacts ever land here, add the standard folders then.

## Current focus

Built 2026-07-05. Live on GitHub Pages (URL in the README). Next milestone: the first full cook-day shakes out real-world quantity and timing corrections — expect recipe edits in the first few weeks.
