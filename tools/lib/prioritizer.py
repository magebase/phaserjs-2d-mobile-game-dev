"""Canonical prioritization engine and backlog generator for phaserjs-2d-mobile-game-dev."""

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


PRIORITY_FORMULA = "(is_blocker * 100) + (impact * 10) + (confidence * 5) - (effort * 3)"


def calculate_priority_score(is_blocker: bool, impact: int, confidence: int, effort: int) -> float:
    """
    Calculate deterministic priority score according to canonical formula:
    Priority = (IsBlocker * 100) + (Impact * 10) + (Confidence * 5) - (Effort * 3)
    """
    blocker_val = 1 if is_blocker else 0
    score = (blocker_val * 100) + (int(impact) * 10) + (int(confidence) * 5) - (int(effort) * 3)
    return float(score)


def map_blocker_to_task(blocker: Dict[str, Any], idx: int) -> Dict[str, Any]:
    """Convert a failed or unverified hard release blocker into a prioritized backlog task."""
    bid = blocker["id"]
    playbook_map = {
        "RB-01": ("lifecycle.release_readiness", "playbooks/lifecycle/release-readiness.md", 10, 10, 3),
        "RB-02": ("phaser4.architecture_scenes", "playbooks/phaser4/architecture-scenes.md", 10, 9, 3),
        "RB-03": ("game_quality.core_loop_and_game_feel", "playbooks/game-quality/core-loop-and-game-feel.md", 9, 8, 4),
        "RB-04": ("phaser4.input_and_controls", "playbooks/phaser4/input-and-controls.md", 9, 9, 3),
        "RB-05": ("art_pipeline.generate_or_reuse_assets", "playbooks/art-pipeline/generate-or-reuse-assets.md", 8, 9, 2),
        "RB-06": ("backend.identity_save_state_and_progression", "playbooks/backend/identity-save-state-and-progression.md", 8, 8, 4),
        "RB-07": ("backend.security_and_abuse", "playbooks/backend/security-and-abuse.md", 9, 9, 2),
        "RB-08": ("phaser4.performance", "playbooks/phaser4/performance.md", 9, 8, 4),
    }

    cap_id, playbook, impact, confidence, effort = playbook_map.get(
        bid, ("lifecycle.prioritize_improvements", "playbooks/lifecycle/prioritize-improvements.md", 8, 8, 3)
    )

    priority = calculate_priority_score(is_blocker=True, impact=impact, confidence=confidence, effort=effort)

    return {
        "id": f"TASK-B{idx:02d}",
        "title": f"Resolve Hard Blocker {bid}: {blocker['name']}",
        "category": "lifecycle" if bid in ("RB-01", "RB-02") else ("phaser4" if bid in ("RB-04", "RB-08") else "game-quality"),
        "capability_id": cap_id,
        "is_blocker": True,
        "blocker_id": bid,
        "impact": impact,
        "confidence": confidence,
        "effort": effort,
        "priority_score": priority,
        "status": "pending",
        "prerequisites": [],
        "playbook": playbook,
        "verification_command": f"./tools/magebase-game verify .",
        "notes": blocker["evidence"],
    }


def map_dimension_gap_to_task(dim_key: str, dim_data: Dict[str, Any], idx: int) -> Optional[Dict[str, Any]]:
    """Convert a low-scoring quality dimension into a prioritized improvement task."""
    score = dim_data["score"]
    if score >= 8.0:
        return None  # Already high quality

    dim_map = {
        "fun_core_loop": ("game_quality.core_loop_and_game_feel", "playbooks/game-quality/core-loop-and-game-feel.md", 8, 7, 5),
        "mobile_usability": ("game_quality.mobile_ux_and_accessibility", "playbooks/game-quality/mobile-ux-and-accessibility.md", 7, 8, 3),
        "game_feel_juice": ("game_quality.combat_and_interaction", "playbooks/game-quality/combat-and-interaction.md", 7, 8, 3),
        "art_cohesion": ("art_pipeline.asset_selection_and_style", "playbooks/art-pipeline/asset-selection-and-style.md", 6, 8, 3),
        "audio_feedback": ("game_quality.audio_feedback", "playbooks/game-quality/audio-feedback.md", 6, 9, 2),
        "technical_stability": ("phaser4.performance", "playbooks/phaser4/performance.md", 7, 8, 4),
        "load_performance": ("qa.performance_budget", "playbooks/qa/performance-budget.md", 7, 8, 3),
        "release_readiness": ("lifecycle.release_readiness", "playbooks/lifecycle/release-readiness.md", 8, 8, 3),
    }

    cap_id, playbook, base_impact, base_conf, base_effort = dim_map.get(
        dim_key, ("game_quality.core_loop_and_game_feel", "playbooks/game-quality/core-loop-and-game-feel.md", 6, 7, 3)
    )

    # Lower scores mean higher urgent impact
    impact = min(10, int(base_impact + (8.0 - score)))
    confidence = base_conf
    effort = base_effort
    priority = calculate_priority_score(is_blocker=False, impact=impact, confidence=confidence, effort=effort)

    title_map = {
        "fun_core_loop": "Deepen Core Loop & Meaningful Player Choices",
        "mobile_usability": "Enhance Mobile Touch Ergonomics & Safe Areas",
        "game_feel_juice": "Add Combat Juice, Hit-Stop & Camera Trauma",
        "art_cohesion": "Standardize Visual Style & Palette Consistency",
        "audio_feedback": "Implement Reactive Audio Cues & Pitch Jitter",
        "technical_stability": "Optimize Memory Allocation & Scene Lifecycles",
        "load_performance": "Reduce Initial Asset Payload & Frame Drops",
        "release_readiness": "Finalize PWA Manifest & App Store Compliance",
    }

    return {
        "id": f"TASK-Q{idx:02d}",
        "title": title_map.get(dim_key, f"Improve Quality Dimension: {dim_key}"),
        "category": "game-quality" if "game_quality" in cap_id else ("art-pipeline" if "art" in cap_id else "phaser4"),
        "capability_id": cap_id,
        "is_blocker": False,
        "blocker_id": None,
        "impact": impact,
        "confidence": confidence,
        "effort": effort,
        "priority_score": priority,
        "status": "pending",
        "prerequisites": [],
        "playbook": playbook,
        "verification_command": "./tools/magebase-game verify .",
        "notes": dim_data.get("notes", ""),
    }


def generate_backlog(
    arg1: Dict[str, Any],
    arg2: Optional[Dict[str, Any]] = None,
    arg3: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Compile prioritized quality backlog adhering to quality-backlog.schema.json.
    Supports either generate_backlog(report) or generate_backlog(profile, catalog, report).
    """
    if arg3 is not None and isinstance(arg3, dict) and "hard_blockers" in arg3:
        profile = arg1
        catalog = arg2 or {}
        report = arg3
    else:
        report = arg1
        profile = arg2 or {}
        catalog = arg3 or {}

    game_slug = (
        profile.get("identity", {}).get("slug")
        or report.get("game_name", "unknown-game")
    )
    tasks: List[Dict[str, Any]] = []

    # 1. Map all failing or unverified hard release blockers first
    blocker_idx = 1
    for b in report.get("hard_blockers", []):
        if b.get("status") in ("FAIL", "UNVERIFIED"):
            tasks.append(map_blocker_to_task(b, blocker_idx))
            blocker_idx += 1

    # 2. Map quality dimension gaps
    dim_idx = 1
    for dim_key, dim_data in report.get("dimension_scores", {}).items():
        task = map_dimension_gap_to_task(dim_key, dim_data, dim_idx)
        if task:
            tasks.append(task)
            dim_idx += 1

    # 3. Sort tasks descending by priority score
    tasks.sort(key=lambda t: t["priority_score"], reverse=True)

    return {
        "game_slug": game_slug,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tasks": tasks,
    }
