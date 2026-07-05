#!/usr/bin/env python3
"""Check every recipe file for format problems the app would choke on.

Run from anywhere:  python3 tools/validate.py

It mirrors the parsing rules in index.html (documented in
docs/recipe-format.md) and reports:
  - files listed in manifest.json that don't exist, and files on disk
    that the manifest is missing
  - frontmatter problems (missing name/meal/serves, bad meal value)
  - ingredient lines that won't parse (bad quantity, missing fields,
    unknown category)
  - item names that are ALMOST the same across recipes ("lime" vs
    "limes") — those would show up as two lines on the shopping list
    instead of adding together
  - the same item bought in two different units (sometimes fine,
    worth a look)

Exit code 0 = clean (warnings allowed), 1 = real errors.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATEGORIES = {"produce", "meat", "dairy-eggs", "bakery", "frozen", "pantry", "other-store"}
MEALS = {"breakfast", "lunch", "dinner"}

errors = []    # things that break the app
warnings = []  # things worth a look


def parse_qty(text):
    """Accepts '2', '2.5', or '1/2'. Returns a float or None."""
    text = text.strip()
    if "/" in text:
        try:
            a, b = text.split("/")
            return float(a) / float(b)
        except (ValueError, ZeroDivisionError):
            return None
    try:
        return float(text)
    except ValueError:
        return None


def check_recipe(path):
    """Parse one recipe file; return its buy-items for cross-recipe checks."""
    rel = path.relative_to(REPO)
    text = path.read_text(encoding="utf-8")

    # Frontmatter between the first two --- lines.
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        errors.append(f"{rel}: no frontmatter block")
        return []
    front = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            front[key.strip()] = value.strip()

    for key in ("name", "meal", "serves"):
        if key not in front:
            errors.append(f"{rel}: frontmatter is missing '{key}'")
    if front.get("meal") and front["meal"] not in MEALS:
        errors.append(f"{rel}: meal is '{front['meal']}', expected one of {sorted(MEALS)}")
    if front.get("serves") and not front["serves"].isdigit():
        errors.append(f"{rel}: serves is '{front['serves']}', expected a whole number")

    # Ingredient lines: bullets containing | inside the ## Ingredients section.
    items = []
    in_ingredients = False
    for n, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^##\s", line):
            in_ingredients = bool(re.match(r"^##\s+Ingredients", line, re.I))
            continue
        if not (in_ingredients and line.startswith("- ") and "|" in line):
            continue
        parts = [p.strip() for p in line[2:].split("|")]
        if len(parts) not in (3, 4):
            errors.append(f"{rel}:{n}: expected 'qty unit | item | category | note?', got {len(parts)} fields")
            continue
        qty_match = re.match(r"^([\d./]+)\s*(.*)$", parts[0])
        if not qty_match or parse_qty(qty_match.group(1)) is None:
            errors.append(f"{rel}:{n}: can't read a quantity from '{parts[0]}'")
            continue
        if parts[2] not in CATEGORIES:
            errors.append(f"{rel}:{n}: unknown category '{parts[2]}' (see docs/recipe-format.md)")
        items.append({
            "recipe": str(rel),
            "item": parts[1],
            "unit": qty_match.group(2).strip().rstrip("s") if qty_match.group(2) else "",
        })
    if not items:
        warnings.append(f"{rel}: no buy-list ingredient lines found")
    return items


def main():
    manifest_path = REPO / "recipes" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())["recipes"]

    # Manifest and disk must agree, or the app silently misses recipes.
    on_disk = {str(p.relative_to(REPO)) for p in REPO.glob("recipes/*/*.md")}
    for entry in manifest:
        if not (REPO / entry).exists():
            errors.append(f"manifest.json lists {entry}, but the file doesn't exist")
    for path in sorted(on_disk - set(manifest)):
        warnings.append(f"{path} exists on disk but isn't in manifest.json — the app won't see it")

    all_items = []
    for entry in manifest:
        path = REPO / entry
        if path.exists():
            all_items.extend(check_recipe(path))

    # Near-duplicate item names: same after lowercasing and dropping a
    # trailing s, but spelled differently somewhere.
    by_norm = {}
    for it in all_items:
        norm = it["item"].lower().rstrip("s")
        by_norm.setdefault(norm, set()).add(it["item"].lower())
    for norm, spellings in sorted(by_norm.items()):
        if len(spellings) > 1:
            warnings.append(f"item spelled multiple ways, so quantities won't add together: {sorted(spellings)}")

    # Same item in different units across recipes.
    units_by_item = {}
    for it in all_items:
        units_by_item.setdefault(it["item"].lower(), set()).add(it["unit"])
    for item, units in sorted(units_by_item.items()):
        if len(units) > 1:
            warnings.append(f"'{item}' appears with different units {sorted(units)} — listed separately, check it's intended")

    for e in errors:
        print(f"ERROR    {e}")
    for w in warnings:
        print(f"warning  {w}")
    print(f"\n{len(manifest)} recipes checked: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
