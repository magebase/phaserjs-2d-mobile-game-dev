---
name: phaser-mobile-game-dev
description: Master router skill for Phaser 4 2D mobile game development. Inspects games, discovers architecture and assets, prioritizes quality gaps, selects playbooks, and executes verified improvements toward release readiness.
---

# Phaser 4 Mobile 2D Game Development Router

> **Skill Identifier:** `phaser-mobile-game-dev`  
> **Target Framework:** Phaser 4.2.1  
> **Operating Mode:** Autonomous Router & Capability Dispatcher

---

## 1. When to Use

Invoke this skill whenever a user wants to:
- Inspect an existing Phaser game and determine what is needed for mobile release.
- Fix broken mobile touch controls, viewport scaling, safe-area cutouts, or orientation issues.
- Audit the game's existing art library, texture atlases, or audio assets to reuse them before generating new assets.
- Upgrade or optimize Phaser 4 rendering using RenderNodes, `SpriteGPULayer`, and `TilemapGPULayer`.
- Hook up game persistence, cloud saves, leaderboards, or telemetry to Django or Cloudflare Workers.
- Inject "game feel" and juice (screen shake, freeze-frames, impact particles, audio feedback).
- Run automated release gates against the 8 Hard Release Blockers in `GAME_QUALITY_CONTRACT.md`.

---

## 2. Canonical Trigger Example

```text
Use the Phaser mobile game development skill. Inspect this game, identify the highest-impact gaps, implement improvements, and verify them until the next meaningful blocker.
```

---

## 3. The 11-Step Execution Loop

Follow this strict state machine sequentially:

```
1. Discover ──► 2. Profile ──► 3. Baseline ──► 4. Assess ──► 5. Prioritize
                                                                  │
11. Repeat ◄── 10. Record ◄── 9. Repair ◄── 8. Verify ◄── 7. Impl ◄── 6. Select
```

### Step 1: Discover
1. Inspect the workspace root to locate the game's package manifest (`package.json`, etc.) or script tags.
2. Confirm the Phaser version (pinned target: `Phaser 4.2.1`).
3. Scan scene files in `src/` or `js/` to map the scene graph.
4. Locate visual and audio asset folders (`public/assets/`, `assets/`, `static/`).
5. Check for backend touchpoints (Django URLs, `wrangler.jsonc`, `wrangler.toml`).

### Step 2: Profile
1. Run `./tools/magebase-game probe <path>` (or invoke the Python/Node probe tool directly) to generate or update `game-profile.json`.
2. Validate the generated profile against `schemas/game-profile.schema.json`.

### Step 3: Baseline
1. Run the project's native build and test commands (e.g. `npm test`, `npm run build`).
2. Run `./tools/magebase-game audit <path>` to catalog assets, dimensions, and detect broken links or non-power-of-two textures.
3. Validate `asset-catalog.json` against `schemas/asset-catalog.schema.json`.

### Step 4: Assess
1. Evaluate the project against `GAME_QUALITY_CONTRACT.md`:
   - Check the 8 Hard Release Blockers (**RB-01** through **RB-08**).
   - Rate the 8 Quality Dimensions (1–10 scale).
2. Generate an audit evaluation report using `./tools/magebase-game report <path>`.

### Step 5: Prioritize
1. Compute the priority score for each identified deficiency:
   $$\text{Priority} = (\text{IsBlocker} \times 100) + (\text{Impact} \times 10) + (\text{Confidence} \times 5) - (\text{Effort} \times 3)$$
2. Generate `quality-backlog.json` and update `GAME_QUALITY.md`.

### Step 6: Select
1. Choose the single highest-priority task that has all prerequisites satisfied.
2. Map the task to a capability ID in `registry/capabilities.json`.
3. Read the assigned playbook from `playbooks/<domain>/<playbook>.md`.

### Step 7: Implement
1. Apply focused code modifications following existing project conventions.
2. Never invent new frameworks or replace tooling without explicit requirement.
3. Reuse existing art from `asset-catalog.json` before introducing new visual files.

### Step 8: Verify
1. Run localized unit/integration checks for the modified subsystem.
2. Run `./tools/magebase-game verify <path>` or the project's test suite.
3. Inspect console logs and mobile viewport rendering for regressions.

### Step 9: Repair
1. If tests fail or regressions occur, diagnose and repair immediately.
2. Re-run verification until all checks pass cleanly.

### Step 10: Record
1. Update `GAME_QUALITY.md` with resolved items and current scores.
2. Record change notes in the project's documentation.

### Step 11: Repeat or Stop
1. Check stopping conditions:
   - If the next task requires external credentials, payment, or human product decisions: **STOP and ask the user**.
   - Otherwise, loop back to **Step 5 (Prioritize)** for the next iteration.

---

## 4. Reference Documents

- [Workflow Contract](references/workflow-contract.md): Detailed state transitions and data flows.
- [Evidence Rules](references/evidence-rules.md): Standards for evidence gathering (no assumptions).
- [Quality Rubric](references/quality-rubric.md): Concrete 1–10 scoring criteria for all dimensions.
- [Safety & Permissions](references/safety-and-permissions.md): Boundaries between autonomous work and human escalation.
