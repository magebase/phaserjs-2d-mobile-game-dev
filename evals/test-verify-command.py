#!/usr/bin/env python3
"""Evaluation test: profile-driven verification command and release blocker enforcement."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.common import load_json


def test_verify_clean_game():
    """Verify that a working game compiles, runs tests, and completes verification."""
    game_dir = repo_root / "fixtures" / "minimal-phaser4-game"
    verify_bin = repo_root / "tools" / "magebase-game"

    res = subprocess.call([str(verify_bin), "verify", str(game_dir)])
    assert res == 0, f"Expected verify to exit 0 on clean fixture, got {res}"

    # Assert mechanical results
    mech_file = game_dir / ".mechanical-results.json"
    assert mech_file.exists(), "Expected .mechanical-results.json to be generated"
    mech = load_json(mech_file)
    assert mech["build"]["status"] == "PASS", f"Expected build PASS, got {mech['build']}"
    assert mech["tests"]["status"] == "PASS", f"Expected tests PASS, got {mech['tests']}"
    print("  ✓ Clean fixture verified: build executed, tests executed, exit code 0")


def test_verify_failing_build():
    """Verify that a broken build command fails RB-01 and halts verification with exit code 1."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Copy minimal fixture to temporary directory
        src_fixture = repo_root / "fixtures" / "minimal-phaser4-game"
        for item in src_fixture.iterdir():
            if item.is_dir() and item.name in ("dist", "tmp", "fixtures"):
                continue
            if item.is_dir():
                shutil.copytree(item, tmp_path / item.name)
            else:
                shutil.copy2(item, tmp_path / item.name)

        # Break package.json build script to fail deliberately
        pkg_file = tmp_path / "package.json"
        pkg_data = json.loads(pkg_file.read_text(encoding="utf-8"))
        pkg_data["scripts"]["build"] = "node -e 'console.error(\"Compilation error\"); process.exit(1)'"
        pkg_file.write_text(json.dumps(pkg_data, indent=2), encoding="utf-8")

        verify_bin = repo_root / "tools" / "magebase-game"
        res = subprocess.call([str(verify_bin), "verify", str(tmp_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert res != 0, "Expected verify to exit with non-zero code on build failure"

        # Assert report shows RB-01 FAIL
        report_file = tmp_path / "audit-report.json"
        assert report_file.exists()
        report = load_json(report_file)
        rb01 = next(b for b in report["hard_blockers"] if b["id"] == "RB-01")
        assert rb01["status"] == "FAIL"
        assert report["overall_status"] == "BLOCKED"
        print("  ✓ Failing build correctly fails RB-01, marks BLOCKED, and exits with code 1")


def test_verify_unverified_tooling():
    """Verify that missing build/test scripts report UNVERIFIED instead of claiming passed."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        src_fixture = repo_root / "fixtures" / "minimal-phaser4-game"
        for item in src_fixture.iterdir():
            if item.is_dir() and item.name in ("dist", "tmp", "fixtures"):
                continue
            if item.is_dir():
                shutil.copytree(item, tmp_path / item.name)
            else:
                shutil.copy2(item, tmp_path / item.name)

        # Remove package.json build & test
        pkg_file = tmp_path / "package.json"
        pkg_data = json.loads(pkg_file.read_text(encoding="utf-8"))
        pkg_data["scripts"] = {}
        pkg_file.write_text(json.dumps(pkg_data, indent=2), encoding="utf-8")

        # Update game-profile.json
        profile_file = tmp_path / "game-profile.json"
        if profile_file.exists():
            profile_data = json.loads(profile_file.read_text(encoding="utf-8"))
            profile_data["tooling"]["build_cmd"] = ""
            profile_data["tooling"]["test_cmd"] = ""
            profile_file.write_text(json.dumps(profile_data, indent=2), encoding="utf-8")

        verify_bin = repo_root / "tools" / "magebase-game"
        res = subprocess.call([str(verify_bin), "verify", str(tmp_path)], stdout=subprocess.DEVNULL)
        assert res == 0, "Missing tooling without failures issues warning and exits 0"

        report = load_json(tmp_path / "audit-report.json")
        rb01 = next(b for b in report["hard_blockers"] if b["id"] == "RB-01")
        assert rb01["status"] == "UNVERIFIED"
        assert report["release_tier_achieved"] != "GOLD", "Project with UNVERIFIED blockers cannot achieve GOLD"
        print("  ✓ Missing build/test tooling correctly reported as UNVERIFIED, preventing false GOLD")


def main():
    print("Running Eval: test-verify-command.py...")
    test_verify_clean_game()
    test_verify_failing_build()
    test_verify_unverified_tooling()
    print("✓ Verification command release readiness evaluations passed successfully.")


if __name__ == "__main__":
    main()
