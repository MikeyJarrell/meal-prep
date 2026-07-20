# Recipe file format

last-reviewed: 2026-07-20

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

1. **Same item, same spelling, same unit, everywhere.** The app adds "limes" to "limes"; it cannot add "lime" to "limes" or "30 g ginger" to "1 knob ginger". The validator flags near-misses. Check how an existing recipe spells an ingredient before inventing a new name.

2. **Spices and condiments are staples, not buy items.** Anything from the spice cabinet or the door of the fridge goes under a `### Pantry staples` subheading as plain bullets (no pipes). The app lists those in a "check the pantry" section without quantities. The standing roster is in [costco-run.md](costco-run.md).

## Body sections

`## Sunday` (numbered batch-cooking steps), `## Weeknight` (reheat or finish instructions), `## Notes` (swaps, the Kendra-lighter variation, and a day-5 verdict). The app renders these in the recipe view; keep to headings, bullets, numbered lists, and plain paragraphs — the built-in renderer handles nothing fancier.

## Scalable quantities in the body

The recipe view has a servings stepper. Ingredient lines scale automatically because they are structured; quantities inside step text scale only if wrapped in braces:

```
a sauce of {90 g} soy, {42 g} brown sugar
Dough: {620 g} bread flour, {400 g} cool water
juice of {4} limes
```

`{620 g}` renders as "620 g" and rescales with the stepper; bare counts like `{4}` work too. (The renderer also accepts a dual form `{90 g / 5 tbsp}`, but the house style below means new recipes never need it.) Rules:

1. **Grams, only grams.** No tablespoons, teaspoons, cups, ounces, or pints anywhere — every measured quantity is a single gram figure. This includes salt: by weight, the kosher-brand problem disappears (a gram of salt is a gram of salt; the old teaspoon converted at roughly 5 g). Casual amounts ("a glug of olive oil", "a pinch of sugar", "a spoon of pickle brine") stay prose and stay unbraced — no fake precision.
2. **Decimals only inside braces** — `2.5 g`, never `2 1/2 g`.
3. **Never brace times, temperatures, or per-unit weights.** A braced number scales with servings; nobody wants a 4.5-minute simmer at 9 servings. Per-unit weights stay bare and the *count* gets braced instead: "{4} balls of 260 g each" scales the number of dough balls, not the ball.
4. On ingredient lines, everything weighable is listed in `g`, including liquids like stock (the note field carries the buy hint, e.g. "two quart boxes"). The exceptions: counts (cans, bunches, cloves, whole vegetables) and meat in `lb`, because Costco's own price labels are in pounds. Can sizes in item names are metric: "crushed tomatoes (800 g can)".

The validator checks token syntax; `python3 tools/validate.py` after editing, as always.
