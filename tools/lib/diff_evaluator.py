"""Diff evaluator and hypothesis verification engine for proving game improvements."""

from typing import Any, Dict, List, Optional


def evaluate_diff(
    before_report: Dict[str, Any],
    after_report: Dict[str, Any],
    hypothesis: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Compare before and after audit reports to evaluate an improvement hypothesis."""
    before_avg = before_report.get("average_score", 0.0)
    after_avg = after_report.get("average_score", 0.0)
    avg_delta = round(after_avg - before_avg, 2)
    
    # 1. Dimension deltas
    dimension_deltas: Dict[str, Dict[str, Any]] = {}
    before_dims = before_report.get("dimension_scores", {})
    after_dims = after_report.get("dimension_scores", {})
    
    all_dims = sorted(set(list(before_dims.keys()) + list(after_dims.keys())))
    for dim in all_dims:
        b_score = before_dims.get(dim, {}).get("score", 0.0)
        a_score = after_dims.get(dim, {}).get("score", 0.0)
        delta = round(a_score - b_score, 2)
        dimension_deltas[dim] = {
            "before": b_score,
            "after": a_score,
            "delta": delta,
            "regressed": delta < -0.01,
            "improved": delta > 0.01
        }
        
    # 2. Hard blocker transitions
    before_blockers = {b["id"]: b["status"] for b in before_report.get("hard_blockers", [])}
    newly_failed_blockers = []
    resolved_blockers = []
    
    for b in after_report.get("hard_blockers", []):
        bid = b["id"]
        old_status = before_blockers.get(bid, "UNVERIFIED")
        new_status = b["status"]
        if new_status == "FAIL" and old_status != "FAIL":
            newly_failed_blockers.append({"id": bid, "name": b["name"], "evidence": b["evidence"]})
        elif new_status == "PASS" and old_status in ("FAIL", "UNVERIFIED"):
            resolved_blockers.append({"id": bid, "name": b["name"], "evidence": b["evidence"]})
            
    # 3. Guardrail checks
    hyp = hypothesis or {}
    guardrails = hyp.get("guardrails", ["technical_stability", "load_performance"])
    guardrail_regressions = []
    for g in guardrails:
        if g in dimension_deltas and dimension_deltas[g]["regressed"]:
            guardrail_regressions.append({
                "dimension": g,
                "delta": dimension_deltas[g]["delta"],
                "before": dimension_deltas[g]["before"],
                "after": dimension_deltas[g]["after"]
            })
            
    # 4. Target dimension evaluation
    target_dim = hyp.get("target_dimension")
    expected_delta = hyp.get("expected_delta", 0.5)
    target_evaluation = None
    target_satisfied = True
    
    if target_dim:
        t_data = dimension_deltas.get(target_dim, {"before": 0.0, "after": 0.0, "delta": 0.0})
        t_delta = t_data["delta"]
        target_satisfied = t_delta >= (expected_delta - 0.01)
        target_evaluation = {
            "target_dimension": target_dim,
            "expected_delta": expected_delta,
            "actual_delta": t_delta,
            "satisfied": target_satisfied
        }
        
    # 5. Formulate verdict
    if newly_failed_blockers:
        verdict = "REJECTED"
        reason = f"Rejected: Introduced {len(newly_failed_blockers)} new hard blocker(s): {[b['id'] for b in newly_failed_blockers]}"
    elif guardrail_regressions:
        verdict = "REJECTED"
        reg_names = [r["dimension"] for r in guardrail_regressions]
        reason = f"Rejected: Guardrail regression detected in {reg_names}"
    elif target_dim and not target_satisfied:
        verdict = "REJECTED"
        reason = f"Rejected: Target dimension '{target_dim}' gained {target_evaluation['actual_delta']}, falling short of expected +{expected_delta}"
    elif avg_delta < 0.0:
        verdict = "REJECTED"
        reason = f"Rejected: Average quality score decreased by {avg_delta:+.2f}"
    else:
        verdict = "ACCEPTED"
        reason = f"Accepted: Target satisfied, average score delta is {avg_delta:+.2f}, zero regressions in guardrails or blockers"
        
    return {
        "verdict": verdict,
        "reason": reason,
        "before_status": before_report.get("overall_status"),
        "after_status": after_report.get("overall_status"),
        "before_average": before_avg,
        "after_average": after_avg,
        "average_delta": avg_delta,
        "target_evaluation": target_evaluation,
        "dimension_deltas": dimension_deltas,
        "newly_failed_blockers": newly_failed_blockers,
        "resolved_blockers": resolved_blockers,
        "guardrail_regressions": guardrail_regressions
    }


def render_diff_markdown(diff_result: Dict[str, Any]) -> str:
    """Render diff evaluation as clean GitHub Markdown (Rule 32 Zero-Emoji compliant)."""
    lines = [
        "# PROVE_IMPROVEMENTS.md — Hypothesis & Quality Diff Report",
        "",
        f"> **Verdict:** `[{diff_result['verdict']}]`  ",
        f"> **Decision Reason:** {diff_result['reason']}  ",
        f"> **Overall Status:** `[{diff_result['before_status']}]` -> `[{diff_result['after_status']}]`  ",
        f"> **Average Score Change:** `{diff_result['before_average']} / 10.0` -> `{diff_result['after_average']} / 10.0` (`{diff_result['average_delta']:+.2f}`)",
        "",
        "---",
        "",
        "## 1. Dimensional Score Deltas",
        "",
        "| Dimension | Before | After | Delta | Status |",
        "| :--- | :---: | :---: | :---: | :---: |"
    ]
    
    for dim, data in diff_result["dimension_deltas"].items():
        delta_str = f"{data['delta']:+.2f}"
        if data["improved"]:
            status_tag = "[IMPROVED]"
        elif data["regressed"]:
            status_tag = "[REGRESSED]"
        else:
            status_tag = "[UNCHANGED]"
        dim_title = dim.replace("_", " ").title()
        lines.append(f"| **{dim_title}** | `{data['before']}` | `{data['after']}` | `{delta_str}` | `{status_tag}` |")
        
    lines.extend([
        "",
        "---",
        "",
        "## 2. Hard Blocker Transitions",
        ""
    ])
    
    if diff_result["resolved_blockers"]:
        lines.append("### Resolved Blockers:")
        for b in diff_result["resolved_blockers"]:
            lines.append(f"- **[RESOLVED] {b['id']} ({b['name']})**: {b['evidence']}")
        lines.append("")
        
    if diff_result["newly_failed_blockers"]:
        lines.append("### Newly Introduced Blockers (CRITICAL REGRESSION):")
        for b in diff_result["newly_failed_blockers"]:
            lines.append(f"- **[FAIL] {b['id']} ({b['name']})**: {b['evidence']}")
        lines.append("")
        
    if not diff_result["resolved_blockers"] and not diff_result["newly_failed_blockers"]:
        lines.append("No changes in hard blocker status.")
        lines.append("")
        
    lines.extend([
        "---",
        "",
        "## 3. Guardrail & Hypothesis Checks",
        ""
    ])
    
    target_eval = diff_result.get("target_evaluation")
    if target_eval:
        status_label = "[SATISFIED]" if target_eval["satisfied"] else "[FAILED]"
        lines.append(f"- **Target Dimension:** `{target_eval['target_dimension']}`")
        lines.append(f"- **Expected Delta:** `+{target_eval['expected_delta']}`")
        lines.append(f"- **Actual Delta:** `{target_eval['actual_delta']:+.2f}` (`{status_label}`)")
        lines.append("")
        
    if diff_result["guardrail_regressions"]:
        lines.append("### Guardrail Regressions:")
        for r in diff_result["guardrail_regressions"]:
            lines.append(f"- **[VIOLATION] {r['dimension']}** decreased by `{r['delta']:+.2f}` (from {r['before']} to {r['after']})")
        lines.append("")
    else:
        lines.append("All guardrail dimensions preserved without regression.")
        lines.append("")
        
    return "\n".join(lines)
