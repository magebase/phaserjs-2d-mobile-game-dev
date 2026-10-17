#!/usr/bin/env python3
"""Evaluation test: audit report schema conformance and score calculation."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.asset_analyzer import analyze_assets
from tools.lib.common import validate_schema
from tools.lib.probe import probe_project
from tools.lib.reporter import generate_report


def main():
    print("Running Eval: test-report-schema.py...")
    game_dir = repo_root / "fixtures" / "minimal-phaser4-game"

    profile = probe_project(game_dir)
    catalog = analyze_assets(game_dir)
    report = generate_report(profile, catalog)

    # Validate against audit-report schema
    schema_file = repo_root / "schemas" / "audit-report.schema.json"
    valid, err = validate_schema(report, schema_file)
    assert valid, f"Report failed schema validation: {err}"
    print("  ✓ Generated report strictly matches schemas/audit-report.schema.json")

    # Assert basic metrics
    assert report["game_name"] == "minimal-phaser4-game"
    assert len(report["hard_blockers"]) == 8
    assert len(report["dimension_scores"]) == 8
    assert 1.0 <= report["average_score"] <= 10.0
    print(f"  ✓ Metrics valid: status={report['overall_status']}, avg_score={report['average_score']}")

    print("✓ Report schema evaluation passed successfully.")


if __name__ == "__main__":
    main()
