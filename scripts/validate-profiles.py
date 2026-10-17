#!/usr/bin/env python3
"""Validation script for game-profile JSON files against schemas/game-profile.schema.json."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.common import load_json, validate_schema


def main():
    print("Validating all game profile files against schema...")
    schema_file = repo_root / "schemas" / "game-profile.schema.json"
    
    candidates = [
        repo_root / "templates" / "game-profile.json",
        repo_root / "fixtures" / "minimal-phaser4-game" / "game-profile.json"
    ]
    
    # Also find any other game-profile.json in the repo
    for p in repo_root.rglob("game-profile.json"):
        if p not in candidates and "node_modules" not in p.parts:
            candidates.append(p)

    errors = []
    for f in candidates:
        if not f.exists():
            continue
        try:
            data = load_json(f)
            valid, err = validate_schema(data, schema_file)
            if not valid:
                errors.append(f"{f.relative_to(repo_root)}: {err}")
            else:
                print(f"  ✓ {f.relative_to(repo_root)} is valid")
        except Exception as e:
            errors.append(f"{f.relative_to(repo_root)}: {str(e)}")

    if errors:
        print(f"\nFound {len(errors)} profile validation errors:", file=sys.stderr)
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        sys.exit(1)

    print("✓ All game profiles match schema successfully.")


if __name__ == "__main__":
    main()
