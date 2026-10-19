#!/usr/bin/env python3
"""Evaluation test: hypothesis-driven prove-improvements engine and guardrail verification."""

import copy
import re
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from tools.lib.diff_evaluator import evaluate_diff, render_diff_markdown


def make_sample_report(avg_score=6.5, touch_score=6.0, perf_score=8.0, tech_score=8.0, blockers=None):
    if blockers is None:
        blockers = [
            {"id": "RB-01", "name": "Build & Compilation Failure", "status": "PASS", "evidence": "Clean build"},
            {"id": "RB-02", "name": "Unhandled Runtime Exceptions", "status": "PASS", "evidence": "0 boot exceptions"},
            {"id": "RB-03", "name": "Broken Core Gameplay Loop", "status": "PASS", "evidence": "Gameplay present"},
            {"id": "RB-04", "name": "Unplayable Touch Controls", "status": "PASS", "evidence": "Touch active"},
            {"id": "RB-05", "name": "Missing Asset 404s", "status": "PASS", "evidence": "0 missing"},
            {"id": "RB-06", "name": "Save / Progress Data Loss", "status": "PASS", "evidence": "Local storage"},
            {"id": "RB-07", "name": "Leaked Secrets in Bundle", "status": "PASS", "evidence": "0 leaks"},
            {"id": "RB-08", "name": "Critical FPS Degradation", "status": "PASS", "evidence": "60 FPS"}
        ]
    return {
        "game_name": "TestGame",
        "overall_status": "WARNING",
        "average_score": avg_score,
        "hard_blockers": blockers,
        "dimension_scores": {
            "fun_core_loop": {"score": 7.0, "notes": "fun"},
            "mobile_usability": {"score": touch_score, "notes": "touch"},
            "game_feel_juice": {"score": 6.5, "notes": "juice"},
            "art_cohesion": {"score": 7.0, "notes": "art"},
            "audio_feedback": {"score": 6.0, "notes": "audio"},
            "technical_stability": {"score": tech_score, "notes": "tech"},
            "load_performance": {"score": perf_score, "notes": "perf"},
            "release_readiness": {"score": 6.0, "notes": "release"}
        }
    }


def test_accepted_improvement():
    before = make_sample_report(avg_score=6.5, touch_score=6.0, perf_score=8.0)
    after = make_sample_report(avg_score=7.0, touch_score=8.0, perf_score=8.0)

    hypothesis = {
        "target_dimension": "mobile_usability",
        "expected_delta": 1.5,
        "guardrails": ["load_performance", "technical_stability"]
    }

    res = evaluate_diff(before, after, hypothesis)
    assert res["verdict"] == "ACCEPTED"
    assert res["target_evaluation"]["satisfied"] is True
    print("  ✓ Legitimate improvement correctly ACCEPTED (target satisfied, guardrails preserved)")


def test_rejected_guardrail_regression():
    before = make_sample_report(avg_score=6.5, touch_score=6.0, perf_score=8.5)
    # Touch improved by +2.5, but load_performance regressed by -2.0
    after = make_sample_report(avg_score=6.5, touch_score=8.5, perf_score=6.5)

    hypothesis = {
        "target_dimension": "mobile_usability",
        "expected_delta": 1.5,
        "guardrails": ["load_performance", "technical_stability"]
    }

    res = evaluate_diff(before, after, hypothesis)
    assert res["verdict"] == "REJECTED"
    assert len(res["guardrail_regressions"]) == 1
    assert res["guardrail_regressions"][0]["dimension"] == "load_performance"
    print("  ✓ Improvement with guardrail regression correctly REJECTED")


def test_rejected_new_blocker():
    before = make_sample_report(avg_score=6.5, touch_score=6.0)
    after = make_sample_report(avg_score=7.0, touch_score=8.5)
    # A new hard blocker (RB-01 compilation failure) introduced
    after["hard_blockers"][0]["status"] = "FAIL"
    after["hard_blockers"][0]["evidence"] = "Syntax error in main.js"

    hypothesis = {
        "target_dimension": "mobile_usability",
        "expected_delta": 1.5,
        "guardrails": ["load_performance", "technical_stability"]
    }

    res = evaluate_diff(before, after, hypothesis)
    assert res["verdict"] == "REJECTED"
    assert len(res["newly_failed_blockers"]) == 1
    print("  ✓ Modification introducing new hard blocker correctly REJECTED")


def test_markdown_zero_emoji():
    before = make_sample_report(avg_score=6.5, touch_score=6.0)
    after = make_sample_report(avg_score=7.0, touch_score=8.0)
    res = evaluate_diff(before, after)
    md = render_diff_markdown(res)

    emojis = re.findall(r'[\U00010000-\U0010ffff]', md)
    assert len(emojis) == 0, f"Found forbidden unicode emojis in diff markdown: {emojis}"
    print("  ✓ Zero emoji compliance verified in diff markdown output")


def main():
    print("Running Eval: test-prove-improvements.py...")
    test_accepted_improvement()
    test_rejected_guardrail_regression()
    test_rejected_new_blocker()
    test_markdown_zero_emoji()
    print("✓ All prove-improvements evaluation checks passed successfully.")


if __name__ == "__main__":
    main()
