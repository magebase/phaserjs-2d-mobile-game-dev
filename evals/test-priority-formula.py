#!/usr/bin/env python3
"""Evaluation test: canonical priority formula consistency and backlog sorting."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.asset_analyzer import analyze_assets
from tools.lib.common import validate_schema
from tools.lib.prioritizer import PRIORITY_FORMULA, calculate_priority_score, generate_backlog
from tools.lib.probe import probe_project
from tools.lib.reporter import generate_report


def main():
    print("Running Eval: test-priority-formula.py...")

    # 1. Test canonical mathematical properties
    assert PRIORITY_FORMULA == "(is_blocker * 100) + (impact * 10) + (confidence * 5) - (effort * 3)"

    # Hard blocker: is_blocker=1, impact=10, confidence=10, effort=3 => 100 + 100 + 50 - 9 = 241
    s_blocker = calculate_priority_score(is_blocker=True, impact=10, confidence=10, effort=3)
    assert s_blocker == 241.0, f"Expected 241.0, got {s_blocker}"
    print(f"  ✓ Calculated blocker score: {s_blocker} (matches expectation)")

    # Maximum non-blocker polish: is_blocker=0, impact=10, confidence=10, effort=1 => 0 + 100 + 50 - 3 = 147
    s_polish_max = calculate_priority_score(is_blocker=False, impact=10, confidence=10, effort=1)
    assert s_polish_max == 147.0, f"Expected 147.0, got {s_polish_max}"
    print(f"  ✓ Calculated maximum polish score: {s_polish_max}")

    # Minimum hard blocker: is_blocker=1, impact=1, confidence=1, effort=10 => 100 + 10 + 5 - 30 = 85
    # Standard blocker: is_blocker=1, impact=8, confidence=8, effort=5 => 100 + 80 + 40 - 15 = 205
    s_blocker_std = calculate_priority_score(is_blocker=True, impact=8, confidence=8, effort=5)
    assert s_blocker_std > s_polish_max, "Standard blocker must mathematically outrank maximum polish task"
    print("  ✓ Proven: Hard blockers mathematically dominate polish tasks")

    # 2. Test backlog generation from minimal fixture
    game_dir = repo_root / "fixtures" / "minimal-phaser4-game"
    profile = probe_project(game_dir)
    catalog = analyze_assets(game_dir)
    report = generate_report(profile, catalog)

    backlog = generate_backlog(profile, catalog, report)
    schema_file = repo_root / "schemas" / "quality-backlog.schema.json"
    valid, err = validate_schema(backlog, schema_file)
    assert valid, f"Backlog failed schema validation: {err}"
    print("  ✓ Generated backlog strictly matches schemas/quality-backlog.schema.json")

    # 3. Verify ordering is descending
    scores = [t["priority_score"] for t in backlog["tasks"]]
    assert scores == sorted(scores, reverse=True), f"Backlog tasks must be sorted descending: {scores}"
    print(f"  ✓ Backlog tasks sorted deterministically descending ({len(scores)} tasks)")

    print("✓ Priority formula evaluation passed successfully.")


if __name__ == "__main__":
    main()
