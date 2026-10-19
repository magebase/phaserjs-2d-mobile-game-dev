#!/usr/bin/env python3
"""Evaluation test: art-intelligence metadata, transparent bounds, semantic roles, and palettes."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.asset_analyzer import analyze_assets
from tools.lib.common import validate_schema


def main():
    print("Running Eval: test-art-intelligence.py...")
    fixture_dir = repo_root / "fixtures" / "asset-library-sample"

    catalog = analyze_assets(fixture_dir)
    items = catalog["items"]

    # 1. Verify schema compliance of enriched catalog
    schema_file = repo_root / "schemas" / "asset-catalog.schema.json"
    valid, err = validate_schema(catalog, schema_file)
    assert valid, f"Asset catalog failed schema validation: {err}"
    print("  ✓ Enriched asset catalog strictly matches schemas/asset-catalog.schema.json")

    # 2. Verify semantic roles
    hero = next(i for i in items if "hero.png" in i["path"])
    assert "hero" in hero.get("semantic_roles", []), f"Expected 'hero' in semantic_roles, got {hero.get('semantic_roles')}"
    print(f"  ✓ Semantic role detected accurately for hero: {hero['semantic_roles']}")

    enemy = next(i for i in items if "enemy_npot.png" in i["path"])
    assert "enemy" in enemy.get("semantic_roles", []), f"Expected 'enemy' in semantic_roles, got {enemy.get('semantic_roles')}"
    print(f"  ✓ Semantic role detected accurately for enemy: {enemy['semantic_roles']}")

    tile = next(i for i in items if "dungeon_tiles.png" in i["path"])
    assert "tile" in tile.get("semantic_roles", []), f"Expected 'tile' in semantic_roles, got {tile.get('semantic_roles')}"
    print(f"  ✓ Semantic role detected accurately for tilemap tileset: {tile['semantic_roles']}")

    # 3. Verify transparent bounds and trim ratio
    assert "transparent_bounds" in hero, "Expected transparent_bounds for hero.png"
    tb = hero["transparent_bounds"]
    assert "content_width" in tb and "content_height" in tb
    assert 0.0 < tb["trim_ratio"] <= 1.0
    print(f"  ✓ Transparent bounds computed: {tb['content_width']}x{tb['content_height']} (trim_ratio={tb['trim_ratio']})")

    # 4. Verify dominant palette
    assert "dominant_palette" in hero
    assert len(hero["dominant_palette"]) >= 1
    assert hero["dominant_palette"][0].startswith("#")
    print(f"  ✓ Dominant palette sampled: {hero['dominant_palette']}")

    # 5. Verify facing direction and suitability
    assert hero.get("facing_direction") in ["left", "right", "centered", "omni"]
    assert "suitability" in hero
    assert 1.0 <= hero["suitability"]["score"] <= 10.0
    print(f"  ✓ Facing direction: {hero['facing_direction']}, Suitability score: {hero['suitability']['score']}")

    print("✓ Art-intelligence evaluation passed successfully.")


if __name__ == "__main__":
    main()
