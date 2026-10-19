# Playbook: Prove Improvements & Guardrail Verification

> **Domain:** Lifecycle  
> **Capability ID:** `lifecycle.prove_improvements`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook defines the hypothesis-driven improvement loop. An agent must never claim an improvement is worthwhile merely because a change was implemented or a single metric shifted. Every modification must be validated against a formal hypothesis and guarded against regressions across secondary dimensions.

---

## 2. Trigger Conditions

Run this playbook when:
- Executing any non-trivial code modification or gameplay polish task.
- Tuning visual effects (screenshake, particles, shaders) where readability or frame rate might be compromised.
- Changing physics, input controllers, or asset compression where memory or input latency could regress.

---

## 3. The 6-Phase Improvement Cycle

```
[1. Formulate Hypothesis] -> [2. Capture Baseline] -> [3. Atomic Edit] 
       -> [4. Capture Post-Audit] -> [5. Diff & Guardrail Check] -> [6. Accept or Rollback]
```

### Phase 1: Formulate the Hypothesis
Create `hypothesis.json` defining the target lift and non-negotiable guardrails:
```json
{
  "target_dimension": "mobile_usability",
  "expected_delta": 1.5,
  "proposed_change": "Implement floating virtual joystick with adaptive safe-area repositioning",
  "guardrails": ["technical_stability", "load_performance", "fun_core_loop"]
}
```

### Phase 2: Capture Baseline
Capture baseline state before making any changes:
```bash
./tools/magebase-game report /path/to/game --json-out before.json
```

### Phase 3: Execute Atomic Edit
Make focused, minimal code edits following domain playbooks (e.g. `playbooks/phaser4/input-and-controls.md`).

### Phase 4: Capture Post-Implementation State
Capture the new state following the modification:
```bash
./tools/magebase-game report /path/to/game --json-out after.json
```

### Phase 5: Diff & Guardrail Evaluation
Run the automated comparison tool:
```bash
./tools/magebase-game prove --before before.json --after after.json --hypothesis hypothesis.json -o PROVE_IMPROVEMENTS.md
```

### Phase 6: Decision Gate
- **ACCEPTED:** Target dimension met or exceeded expected delta, zero guardrail regressions occurred, and no new hard blockers were introduced.
- **REJECTED:** If any guardrail regressed (e.g. FPS dropped, asset size spiked) or target failed to improve:
  ```bash
  git restore .
  git clean -fd
  ```
  Immediately revert code changes and log the rejected experiment in `GAME_QUALITY.md`.

---

## 4. Output Artifacts

- `PROVE_IMPROVEMENTS.md` containing full delta comparison tables.
- Validated code changes or clean rollback.
