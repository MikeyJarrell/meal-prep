# Recipe file format

last-reviewed: 2026-07-05

Every recipe is one markdown file in `recipes/breakfast/`, `recipes/lunch/`, or `recipes/dinner/`. The shopping-list app ([index.html](../index.html)) parses these files directly, so the format below is load-bearing. After adding or editing a recipe, run `python3 tools/validate.py` and add any new file to [recipes/manifest.json](../recipes/manifest.json) — the app only loads what the manifest lists.

## Frontmatter

The block between the two `---` lines at the top. The app requires `name`, `meal` (breakfast, lunch, or dinner), and `serves` (a whole number — quantities scale linearly from it). The rest is display text shown on the recipe cards: `good_cold` (yes/no — shows the badge Kendra filters by), `weeknight` (what reheating takes), `sunday_active` and `sunday_passive` (cook-day budgeting), `calories`, `protein` (rough estimates, say so), and `tags`.

## Ingredient lines

Buy-list items live under `## Ingredients` as pipe-delimited bullets:

```
- 3 lb | boneless skinless chicken thighs | meat | half a Kirkland pack
- 2 cans | black beans | pantry
- 6 cloves | garlic | produce
```

Four fields, pipes between: quantity with optional unit, item name, category, optional note. Quantities are decimals or simple fractions. Categories must be one of: `produce`, `meat`, `dairy-eggs`, `bakery`, `frozen`, `pantry`, `other-store` (that last one groups the short regular-grocery-store run — tomatillos, lemongrass, curry paste — separately from the Costco walk).

Two discipline rules make aggregation work:

1. **Same item, same spelling, same unit, everywhere.** The app adds "limes" to "limes"; it cannot add "lime" to "limes" or "2 oz ginger" to "1 knob ginger". The validator flags near-misses. Check how an existing recipe spells an ingredient before inventing a new name.

2. **Spices and condiments are staples, not buy items.** Anything from the spice cabinet or the door of the fridge goes under a `### Pantry staples` subheading as plain bullets (no pipes). The app lists those in a "check the pantry" section without quantities. The standing roster is in [costco-run.md](costco-run.md).

## Body sections

`## Sunday` (numbered batch-cooking steps), `## Weeknight` (reheat or finish instructions), `## Notes` (swaps, the Kendra-lighter variation, and a day-5 verdict). The app renders these in the recipe view; keep to headings, bullets, numbered lists, and plain paragraphs — the built-in renderer handles nothing fancier.
