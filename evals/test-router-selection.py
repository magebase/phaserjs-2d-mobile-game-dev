#!/usr/bin/env python3
"""Evaluation test: router capability selection based on natural language intent."""

import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent


def score_match(query: str, triggers: list[str]) -> float:
    query_lower = query.lower()
    score = 0.0
    for trigger in triggers:
        t_lower = trigger.lower()
        if t_lower in query_lower:
            score += 2.0
        words = t_lower.split()
        matched = sum(1 for w in words if w in query_lower)
        score += matched / len(words)
    return score


def route_intent(query: str, capabilities: list[dict]) -> str:
    best_cap = None
    best_score = -1.0
    for cap in capabilities:
        s = score_match(query, cap.get("triggers", []))
        if s > best_score:
            best_score = s
            best_cap = cap["id"]
    return best_cap


def main():
    print("Running Eval: test-router-selection.py...")
    registry_file = repo_root / "registry" / "capabilities.json"
    registry = json.loads(registry_file.read_text(encoding="utf-8"))
    caps = registry["capabilities"]

    test_cases = [
        ("Improve touch controls for iPhone and add a virtual joystick", "phaser4.input_and_controls"),
        ("Audit existing art library before we generate any new assets", "art_pipeline.discover_and_catalog"),
        ("Check if this game is ready for release and can we ship", "lifecycle.release_readiness"),
        ("Fix game feel and add screen shake juice", "game_quality.core_loop_and_game_feel"),
        ("Hook up cloud save state and sync progression", "backend.identity_save_state_and_progression"),
        ("Optimize frame drops and mobile fps performance", "phaser4.performance")
    ]

    passed = 0
    for query, expected in test_cases:
        selected = route_intent(query, caps)
        if selected == expected:
            print(f"  ✓ '{query[:40]}...' -> {selected}")
            passed += 1
        else:
            print(f"  ✗ FAILED '{query}' -> Expected: {expected}, Got: {selected}", file=sys.stderr)

    assert passed == len(test_cases), f"Passed {passed}/{len(test_cases)}"
    print(f"✓ All {passed} routing test cases passed perfectly.")


if __name__ == "__main__":
    main()
