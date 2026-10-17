# Playbook: Implement, Verify & Repair Loop

> **Domain:** Lifecycle  
> **Capability ID:** `lifecycle.implement_verify_repair`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides the execution of code changes for a selected task. It mandates focused, atomic edits, immediate localized verification, regression detection, and autonomous repair before marking a task complete.

---

## 2. Trigger Conditions

Run this playbook when:
- A task has been selected from `quality-backlog.json`.
- Implementing fixes for touch controls, rendering, audio, physics, or backend bindings.

---

## 3. Step-by-Step Procedure

### Step 1: Pre-Implementation Check
- Confirm working directory is clean or changes are tracked.
- Read existing file contents completely before editing.
- Note existing indentation, semicolons, naming conventions, and module formats (`ESM` vs `CommonJS`).

### Step 2: Implement Focused Slice
- Edit only the lines necessary to satisfy the task.
- Follow the corresponding domain playbook (e.g. `playbooks/phaser4/input-and-controls.md`).
- Never introduce new third-party dependencies unless strictly required.

### Step 3: Localized Verification
Run the fastest relevant check:
```bash
# If a specific test exists:
npm test -- test/scenes/GameScene.test.js

# Or compile check:
npm run build
```

### Step 4: Repair Loop (If Tests Fail)
If an error or regression is introduced:
1. Read the exact compiler or test stack trace.
2. Isolate whether the error is syntax, undefined object reference, or broken asset key.
3. Apply targeted fix.
4. Rerun verification.
5. **Never disable tests or lower thresholds to bypass a failure.**

### Step 5: Full Suite & Smoke Check
Run the unified verification command:
```bash
./tools/magebase-game verify /path/to/game
```

---

## 4. Output Artifacts

- Clean, verified source code modifications.
- Updated verification records in `GAME_QUALITY.md`.
