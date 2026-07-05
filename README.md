# Meal Prep

A five-day meal-prep system for two active adults who cook well and shop at Costco: a library of recipes built to be cooked in one Sunday session and eaten across the week, and a small web app that turns the week's picks into an aggregated shopping list.

**The app:** [mikeyjarrell.com/meal-prep](https://mikeyjarrell.com/meal-prep/) — works on a phone in the Costco aisles. (Local option: run `python3 -m http.server 8123` in this folder and open http://localhost:8123.) Check the recipes you want, set how many breakfasts, lunches, and dinners the week needs, and it generates a Costco list — quantities scaled and summed, grouped by store section, with the non-Costco stragglers and check-the-pantry staples split out. Tap any recipe card to read the full recipe.

## How the week works

Sunday: pick 2 lunches and 2 or 3 dinners (plus breakfast burritos every other week), generate the list, shop, cook everything in one afternoon. Weekdays: grab containers. Lunches are individual containers that microwave at work or eat cold; dinners reheat at home, several of them with a deliberately fun 10-minute finish on the flat top, pizza oven, or wok. [docs/sunday-cook-day.md](docs/sunday-cook-day.md) covers sequencing the afternoon, the fridge-freezer split that keeps day 5 honest, and packing.

The library favors food that improves in the fridge — braises, curries, gumbo, marinated things, sturdy salads — because leftover quality is the whole game. There is no fish, no plain chicken breast, and no unseasoned sweet potato anywhere in this repository.

## What's here

| Path | What it is |
|------|-----------|
| [index.html](index.html) | The recipe picker and shopping-list generator |
| [recipes/](recipes/) | One markdown file per recipe: 1 breakfast, 10 lunches, 10 dinners |
| [recipes/manifest.json](recipes/manifest.json) | The list of recipe files the app loads |
| [docs/sunday-cook-day.md](docs/sunday-cook-day.md) | Run-of-show for the cooking afternoon |
| [docs/costco-run.md](docs/costco-run.md) | Standing staples, pack-size math, the non-Costco short list |
| [docs/recipe-format.md](docs/recipe-format.md) | The recipe file format the app parses |
| [tools/validate.py](tools/validate.py) | Format checker — run after editing recipes |

## Adding or changing a recipe

Copy an existing recipe as a template, follow [docs/recipe-format.md](docs/recipe-format.md) (the pipe-delimited ingredient lines are what feed the shopping list), add the file to [recipes/manifest.json](recipes/manifest.json), and run `python3 tools/validate.py`. The app picks it up on the next page load — there is no build step.
