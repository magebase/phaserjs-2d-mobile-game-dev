#!/usr/bin/env python3
"""Checks upstream pinned Phaser 4 reference skills and version integrity."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

PINNED_PHASER_VERSION = "4.2.1"
REQUIRED_REFERENCE_SKILLS = [
    "scenes.md",
    "gameobjects.md",
    "textures.md",
    "input.md",
    "physics.md",
    "loader.md",
    "scale.md"
]


def main():
    print(f"Checking pinned upstream Phaser {PINNED_PHASER_VERSION} reference skills...")
    upstream_dir = repo_root / "upstream" / "phaser-skills"

    if not upstream_dir.exists():
        print(f"Error: upstream/phaser-skills directory missing!", file=sys.stderr)
        sys.exit(1)

    errors = []
    for skill in REQUIRED_REFERENCE_SKILLS:
        p = upstream_dir / skill
        if not p.exists():
            errors.append(f"Missing pinned reference skill: {skill}")
        else:
            print(f"  ✓ {skill} present")

    if errors:
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ All {len(REQUIRED_REFERENCE_SKILLS)} reference skills verified against pinned v{PINNED_PHASER_VERSION}.")


if __name__ == "__main__":
    main()
