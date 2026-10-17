# Playbook: Prioritize Quality Gaps & Triage Blockers

> **Domain:** Lifecycle  
> **Capability ID:** `lifecycle.prioritize_improvements`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook defines how to take diagnostic findings from the project probe and asset audit, compare them against `GAME_QUALITY_CONTRACT.md`, compute priority scores, and select the single highest-leverage task to execute next.

---

## 2. Trigger Conditions

Run this playbook when:
- Multiple deficiencies or defects are observed.
- Selecting the next task in the autonomous execution loop.
- Evaluating which gaps block release readiness.

---

## 3. Prioritization Algorithm

For every identified defect, calculate its deterministic Priority Score:

$$\text{Priority} = (\text{IsBlocker} \times 100) + (\text{Impact} \times 10) + (\text{Confidence} \times 5) - (\text{Effort} \times 3)$$

- **IsBlocker (1 or 0)**: 1 if it resolves any Hard Blocker (**RB-01** to **RB-08**); 0 otherwise.
- **Impact (1–10)**: Estimated lift to the affected quality dimension.
- **Confidence (1–10)**: Certainty that the task can be completed without regressions.
- **Effort (1–10)**: Code complexity, lines touched, and dependencies affected.

---

## 4. Step-by-Step Procedure

### Step 1: Run Quality Report Tool
Generate the baseline audit report:
```bash
./tools/magebase-game report /path/to/game --output GAME_QUALITY.md
```

### Step 2: Separate Hard Blockers from Polish
- If any Hard Blocker is marked `FAIL`, it MUST be prioritized over any cosmetic polish.
- Order hard blockers by dependency:
  1. **RB-01** (Build failure) $\to$ Must be resolved first.
  2. **RB-02** (Boot exceptions) $\to$ Fix crash before tuning mechanics.
  3. **RB-05** (Missing assets) $\to$ Restore broken textures before fixing rendering.
  4. **RB-04** (Touch controls) $\to$ Enable touch input before polishing game feel.
  5. **RB-03** (Core loop) $\to$ Ensure complete win/loss loop.
  6. **RB-06** (Save state loss) $\to$ Ensure progress persists.
  7. **RB-08** (FPS drops) $\to$ Batch rendering and profile.
  8. **RB-07** (Secret leaks) $\to$ Scrub distribution files.

### Step 3: Populate Quality Backlog
Write prioritized tasks to `quality-backlog.json` adhering to `schemas/quality-backlog.schema.json`.

---

## 5. Output Artifacts

- Updated `quality-backlog.json`
- Updated `GAME_QUALITY.md`
