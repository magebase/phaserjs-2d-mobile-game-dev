#!/usr/bin/env python3
"""Evaluation test: hard release blocker triggers on defective profiles."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.asset_analyzer import analyze_assets
from tools.lib.probe import probe_project
from tools.lib.reporter import generate_report


def main():
    print("Running Eval: test-quality-contract.py...")
    game_dir = repo_root / "fixtures" / "minimal-phaser4-game"

    base_profile = probe_project(game_dir)
    base_catalog = analyze_assets(game_dir)

    # 1. Normal game should not fail touch controls
    rep1 = generate_report(base_profile, base_catalog)
    rb04 = next(b for b in rep1["hard_blockers"] if b["id"] == "RB-04")
    assert rb04["status"] == "PASS", "Expected RB-04 to pass on minimal game"
    print("  ✓ Clean profile passes RB-04 (Touch Controls)")

    # 2. Defective profile: disable touch controls -> RB-04 must FAIL
    broken_touch_profile = dict(base_profile)
    broken_touch_profile["mobile"] = dict(base_profile["mobile"])
    broken_touch_profile["mobile"]["touch_controls"] = {"enabled": False, "type": "none"}
    
    rep2 = generate_report(broken_touch_profile, base_catalog)
    rb04_broken = next(b for b in rep2["hard_blockers"] if b["id"] == "RB-04")
    assert rb04_broken["status"] == "FAIL", "Expected RB-04 to fail when touch controls disabled"
    assert rep2["overall_status"] == "BLOCKED"
    print("  ✓ Defective profile accurately fails RB-04 and marks status BLOCKED")

    # 3. Defective profile: missing gameplay scene -> RB-03 must FAIL
    broken_scene_profile = dict(base_profile)
    broken_scene_profile["architecture"] = {
        "entry_point": "src/main.js",
        "scene_graph": [{"key": "BootScene", "file": "src/Boot.js", "type": "ui"}]
    }
    rep3 = generate_report(broken_scene_profile, base_catalog)
    rb03_broken = next(b for b in rep3["hard_blockers"] if b["id"] == "RB-03")
    assert rb03_broken["status"] == "FAIL", "Expected RB-03 to fail when gameplay scene missing"
    print("  ✓ Missing gameplay scene accurately fails RB-03")

    print("✓ Hard blocker contract evaluation passed successfully.")


if __name__ == "__main__":
    main()
