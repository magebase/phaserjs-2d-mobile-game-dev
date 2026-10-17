# Workflow Contract — Router State Transitions & Data Flows

> **Router Reference:** `phaser-mobile-game-dev`  
> **Target Engine:** Phaser 4.2.1

This document specifies the exact contract governing the 11-step execution loop of the router.

---

## 1. State Machine Definition

| Step | State | Input Data | Active Tool / Operation | Output Artifact | Next State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `DISCOVER` | Project Directory | File tree traversal, package scan | Raw discovery facts | `PROFILE` |
| **2** | `PROFILE` | Raw discovery facts | `./tools/magebase-game probe` | `game-profile.json` | `BASELINE` |
| **3** | `BASELINE` | `game-profile.json` | Project test runner, `./tools/magebase-game audit` | `asset-catalog.json`, test outputs | `ASSESS` |
| **4** | `ASSESS` | Profile + Catalog + Baseline logs | `./tools/magebase-game report` | `audit-report.json`, Hard Blocker status | `PRIORITIZE` |
| **5** | `PRIORITIZE` | Audit Report findings | Priority scoring algorithm | `quality-backlog.json`, `GAME_QUALITY.md` | `SELECT` |
| **6** | `SELECT` | `quality-backlog.json` | Capability registry lookup (`registry/capabilities.json`) | Task assignment + Playbook path | `IMPLEMENT` |
| **7** | `IMPLEMENT` | Task spec + Playbook guidance | Code edit tools (`replace_file_content`, etc.) | Modified source code | `VERIFY` |
| **8** | `VERIFY` | Modified source code | Local test execution, `./tools/magebase-game verify` | Test report, console logs | `REPAIR` (if fail) or `RECORD` (if pass) |
| **9** | `REPAIR` | Failure logs from `VERIFY` | Regression diagnosis & targeted patch | Patched source code | `VERIFY` |
| **10** | `RECORD` | Pass evidence | File writers | Updated `GAME_QUALITY.md` & backlog | `REPEAT` |
| **11** | `REPEAT` | Remaining backlog | Boundary evaluation | Next task or final user report | `SELECT` or `HALT` |

---

## 2. Invariants & Guardrails

1. **Schema Conformity**:
   - `game-profile.json` MUST validate against `schemas/game-profile.schema.json`.
   - `asset-catalog.json` MUST validate against `schemas/asset-catalog.schema.json`.
   - `audit-report.json` MUST validate against `schemas/audit-report.schema.json`.
   - `quality-backlog.json` MUST validate against `schemas/quality-backlog.schema.json`.

2. **Atomic Iterations**:
   - Never implement more than one backlog task per loop.
   - Every loop MUST end with verification.

3. **Truthfulness**:
   - If a test cannot run due to missing browser dependencies, mark that check as `UNVERIFIED` rather than assuming it passed.
