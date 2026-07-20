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

1. **Same item, same spelling, same unit, everywhere.** The app adds "limes" to "limes"; it cannot add "lime" to "limes" or "2 oz ginger" to "1 knob ginger". The validator flags near-misses. Check how an existing recipe spells an ingredient before inventing a new name.

2. **Spices and condiments are staples, not buy items.** Anything from the spice cabinet or the door of the fridge goes under a `### Pantry staples` subheading as plain bullets (no pipes). The app lists those in a "check the pantry" section without quantities. The standing roster is in [costco-run.md](costco-run.md).

## Body sections

`## Sunday` (numbered batch-cooking steps), `## Weeknight` (reheat or finish instructions), `## Notes` (swaps, the Kendra-lighter variation, and a day-5 verdict). The app renders these in the recipe view; keep to headings, bullets, numbered lists, and plain paragraphs — the built-in renderer handles nothing fancier.

## Scalable quantities in the body

The recipe view has a servings stepper. Ingredient lines scale automatically because they are structured; quantities inside step text scale only if wrapped in braces:

```
a sauce of {90 g / 5 tbsp} soy, {42 g / 3 tbsp} brown sugar
Dough: {620 g} bread flour, {400 g} cool water
juice of {4} limes
```

`{grams / original volume}` renders as "90 g (5 tbsp)"; `{620 g}` and bare counts like `{4}` also work. Rules:

1. **Grams first, spoons in parentheses.** Any measured formula — sauce, marinade, dressing, dough — is written in grams with the volume equivalent kept as the second measure. Casual amounts ("a glug of olive oil", "a spoon of pickle brine") stay prose and stay unbraced.
2. **Decimals only inside braces** — `0.75 cup`, never `3/4 cup`; the slash separates the two measures.
3. **Never brace times or temperatures.** A braced number scales with servings; nobody wants a 4.5-minute simmer at 9 servings.
4. **Salt stays volumetric.** The recipes call for kosher salt, and kosher brands differ almost 2× in grams per spoon (Diamond ~3 g/tsp, Morton ~5 g), so a gram figure would be false precision.
5. On ingredient lines, dry goods measured for cooking (rice, quinoa, lentils, nuts, yogurt from the tub) are listed in `g`; things bought by container (stock in quarts, coconut milk in cans) keep their buy units, with cup equivalents in the note field.

The validator checks token syntax; `python3 tools/validate.py` after editing, as always.
