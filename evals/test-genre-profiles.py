#!/usr/bin/env python3
"""Evaluation test: genre-specific quality profiles, rubrics, and anti-pattern detectors."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.reporter import evaluate_genre, generate_report, score_dimensions


def test_turn_based_roguelike_anti_pattern():
    """Verify that virtual joystick on a turn-based roguelike is flagged as an anti-pattern."""
    profile = {
        "identity": {
            "name": "Gravebound",
            "slug": "gravebound",
            "genre": "turn_based_roguelike"
        },
        "mobile": {
            "touch_controls": {
                "enabled": True,
                "type": "virtual_joystick"
            },
            "safe_areas": { "enabled": True }
        },
        "architecture": {
            "scene_graph": [
                {"key": "BootScene", "type": "ui"},
                {"key": "DungeonScene", "type": "gameplay"},
                {"key": "CombatScene", "type": "gameplay"}
            ]
        },
        "backend": {
            "persistence": "local_storage"
        },
        "quality": {
            "target_fps": 60
        },
        "tooling": {
            "build_cmd": "npm run build"
        }
    }
    catalog = {
        "total_files": 10,
        "total_bytes": 1024 * 1024,
        "summary": { "images_count": 8, "audio_count": 2, "defect_count": 0 },
        "items": []
    }

    # Evaluate genre
    genre_eval = evaluate_genre("turn_based_roguelike", profile, catalog)
    anti_patterns = genre_eval["anti_patterns_detected"]
    assert len(anti_patterns) >= 1, "Expected anti-pattern for virtual joystick on turn-based roguelike"
    assert any("Virtual Joystick" in ap["anti_pattern"] for ap in anti_patterns)
    print("  ✓ Correctly flagged anti-pattern: Virtual Joystick on Turn-Based Roguelike")

    # Score dimensions with penalization
    dims = score_dimensions(profile, catalog, genre="turn_based_roguelike")
    mob_score = dims["mobile_usability"]["score"]
    assert mob_score <= 6.0, f"Expected penalized mobile usability score <= 6.0, got {mob_score}"
    assert "virtual joystick anti-pattern" in dims["mobile_usability"]["notes"]
    print(f"  ✓ Mobile usability score penalized to {mob_score} due to genre mismatch")


def test_turn_based_roguelike_clean():
    """Verify clean turn-based roguelike with tap-to-move passes with zero anti-patterns."""
    profile = {
        "identity": {
            "name": "Gravebound Clean",
            "slug": "gravebound-clean",
            "genre": "turn_based_roguelike"
        },
        "mobile": {
            "touch_controls": {
                "enabled": True,
                "type": "tap_to_move",
                "multitouch": True
            },
            "safe_areas": { "enabled": True }
        },
        "architecture": {
            "scene_graph": [
                {"key": "BootScene", "type": "ui"},
                {"key": "DungeonScene", "type": "gameplay"},
                {"key": "CombatScene", "type": "gameplay"},
                {"key": "DeckScene", "type": "ui"}
            ]
        },
        "backend": {
            "persistence": "offline_first_sync"
        },
        "quality": {
            "target_fps": 60
        },
        "tooling": {
            "build_cmd": "npm run build"
        }
    }
    catalog = {
        "total_files": 15,
        "total_bytes": 2 * 1024 * 1024,
        "summary": { "images_count": 12, "audio_count": 3, "defect_count": 0 },
        "items": []
    }

    report = generate_report(profile, catalog)
    genre_eval = report["genre_evaluation"]
    assert len(genre_eval["anti_patterns_detected"]) == 0, f"Expected 0 anti-patterns, got {genre_eval['anti_patterns_detected']}"
    assert report["dimension_scores"]["mobile_usability"]["score"] == 8.0
    print("  ✓ Clean turn-based roguelike passed with 0 anti-patterns and high usability score")


def test_action_shooter_multitouch_requirement():
    """Verify that action shooter without multitouch triggers an anti-pattern warning."""
    profile = {
        "identity": {
            "name": "Star Fighter",
            "slug": "star-fighter",
            "genre": "action_shooter"
        },
        "mobile": {
            "touch_controls": {
                "enabled": True,
                "type": "single_touch",
                "multitouch": False
            },
            "safe_areas": { "enabled": True }
        },
        "architecture": {
            "scene_graph": [
                {"key": "BootScene", "type": "ui"},
                {"key": "SpaceScene", "type": "gameplay"}
            ]
        },
        "backend": { "persistence": "local_storage" },
        "quality": { "target_fps": 60 }
    }
    catalog = {
        "total_files": 5,
        "total_bytes": 1024 * 500,
        "summary": { "images_count": 4, "audio_count": 1, "defect_count": 0 },
        "items": []
    }

    genre_eval = evaluate_genre("action_shooter", profile, catalog)
    anti_patterns = genre_eval["anti_patterns_detected"]
    assert any("Single-Touch" in ap["anti_pattern"] or "Multi-Touch" in ap["anti_pattern"] for ap in anti_patterns)
    print("  ✓ Correctly flagged anti-pattern: Single-Touch on Action Shooter")


def main():
    print("Running Eval: test-genre-profiles.py...")
    test_turn_based_roguelike_anti_pattern()
    test_turn_based_roguelike_clean()
    test_action_shooter_multitouch_requirement()
    print("✓ All genre profile and rubric evaluations passed successfully.")


if __name__ == "__main__":
    main()
