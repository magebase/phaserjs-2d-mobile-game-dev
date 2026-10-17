#!/usr/bin/env python3
"""Validation script for skill definitions, frontmatter, and playbook links."""

import re
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent


def validate_skill_file(skill_path: Path) -> list[str]:
    errors = []
    if not skill_path.exists():
        return [f"Missing skill file: {skill_path}"]

    content = skill_path.read_text(encoding="utf-8")

    # Check YAML frontmatter
    if not content.startswith("---"):
        errors.append(f"{skill_path}: Missing opening frontmatter '---'")
    else:
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(f"{skill_path}: Malformed YAML frontmatter")
        else:
            frontmatter = parts[1]
            if "name:" not in frontmatter:
                errors.append(f"{skill_path}: Missing 'name' in frontmatter")
            if "description:" not in frontmatter:
                errors.append(f"{skill_path}: Missing 'description' in frontmatter")

    # Check local markdown links
    link_matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    for text, link in link_matches:
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto"):
            continue
        # Strip anchor if present
        clean_link = link.split("#")[0]
        if clean_link:
            target = (skill_path.parent / clean_link).resolve()
            if not target.exists():
                errors.append(f"{skill_path}: Broken link '{link}' (target not found: {target})")

    return errors


def validate_playbook_links(playbooks_dir: Path) -> list[str]:
    errors = []
    for md_file in playbooks_dir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        link_matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for text, link in link_matches:
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto"):
                continue
            clean_link = link.split("#")[0]
            if clean_link:
                target = (md_file.parent / clean_link).resolve()
                if not target.exists():
                    errors.append(f"{md_file.relative_to(repo_root)}: Broken link '{link}'")
    return errors


def main():
    print("Validating skill definitions and markdown integrity...")
    all_errors = []

    # 1. Check canonical router skill
    router_skill = repo_root / "skills" / "phaser-mobile-game-dev" / "SKILL.md"
    all_errors.extend(validate_skill_file(router_skill))

    # 2. Check playbooks links
    playbooks_dir = repo_root / "playbooks"
    if playbooks_dir.exists():
        all_errors.extend(validate_playbook_links(playbooks_dir))
    else:
        all_errors.append("playbooks directory does not exist")

    if all_errors:
        print(f"\nFound {len(all_errors)} validation errors:", file=sys.stderr)
        for err in all_errors:
            print(f"  ✗ {err}", file=sys.stderr)
        sys.exit(1)

    print("✓ All skill files and internal links validated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
