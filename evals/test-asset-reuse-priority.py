#!/usr/bin/env python3
"""Evaluation test: asset audit defect detection and duplicate hashing."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.asset_analyzer import analyze_assets


def main():
    print("Running Eval: test-asset-reuse-priority.py...")
    fixture_dir = repo_root / "fixtures" / "asset-library-sample"

    catalog = analyze_assets(fixture_dir)
    items = catalog["items"]

    # 1. Verify duplicate detection
    duplicates = [i for i in items if any("duplicate_of" in d for d in i["defects"])]
    assert len(duplicates) == 1, f"Expected 1 duplicate asset, found {len(duplicates)}"
    print(f"  ✓ Duplicate asset accurately identified: {duplicates[0]['path']}")

    # 2. Verify NPOT defect detection
    npot_items = [i for i in items if any("non_power_of_two" in d for d in i["defects"])]
    assert len(npot_items) == 1, f"Expected 1 NPOT asset, found {len(npot_items)}"
    assert "enemy_npot.png" in npot_items[0]["path"]
    print(f"  ✓ NPOT texture accurately detected: {npot_items[0]['path']}")

    # 3. Verify clean unique asset has zero defects
    tiles = next(i for i in items if "dungeon_tiles.png" in i["path"])
    assert len(tiles["defects"]) == 0, f"Expected clean dungeon_tiles.png, found defects: {tiles['defects']}"
    print(f"  ✓ Clean asset validated: {tiles['path']}")

    print("✓ All asset analysis evaluation checks passed successfully.")


if __name__ == "__main__":
    main()
