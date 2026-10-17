# AGENTS.md — Contributor & Agent Engineering Contract

> **Repository:** `magebase/phaserjs-2d-mobile-game-dev`  
> **Target Framework:** Phaser 4.2.1 (Pinned reference)  
> **Target Platforms:** Mobile Web (Safari iOS, Chrome Android), PWA, Capacitor / Cordova  
> **Associated Backends:** Standalone, Django (REST), Cloudflare Workers (Python/JS, D1, R2, KV, Queues)

---

## 1. Prime Directives for Autonomous Agents

When operating within this repository or applying its skills to an external Phaser game repository, you MUST follow these non-negotiable directives:

1. **Reuse Before Inventing**: Always query the game's existing art library, texture atlases, audio folders, and codebase utilities before generating or importing new assets or dependencies.
2. **Detect, Do Not Rewrite**: Never introduce a new build tool (e.g. Vite, Webpack, esbuild), framework (React, Svelte, Vue), language rewrite (JS to TS), or package manager unless explicitly instructed by the user or required by hard platform constraints. Respect the project's existing conventions.
3. **Evidence-Based Auditing**: Never make claims about project health, missing assets, broken controls, or performance bottlenecks without running verifiable diagnostic tools or reading concrete lines of code.
4. **Focused, Safe Increments**: Implement one cohesive slice at a time. Never undertake sprawling multi-system refactors in a single pass.
5. **No Regressions & Strict Verification**: Every code change must be accompanied by relevant verification: running tests, checking console errors, testing asset integrity, and verifying viewports. Never disable failing tests to achieve green status.
6. **Zero Secrets in Artifacts**: Never write private API keys, database credentials, Cloudflare tokens, or user secrets into profiles, reports, code snippets, or commit messages.
7. **Two-Layer Quality Enforcement**: Enforce both the 8 Hard Release Blockers (binary pass/fail) and the 8 Dimensional Quality Scores from `GAME_QUALITY_CONTRACT.md`.
8. **Honor the Upstream Boundary**: Do not duplicate basic Phaser 4 API documentation. Direct reference questions to the pinned upstream reference layer in `upstream/phaser-skills/` and official Phaser documentation.

---

## 2. Autonomous Execution Loop

When given the open-ended instruction:
> *"Use the Phaser mobile game development skill. Inspect this game, identify the highest-impact gaps, implement improvements, and verify them until the next meaningful blocker."*

Execute the following bounded 11-step state machine:

```
┌────────────┐     ┌───────────┐     ┌────────────┐     ┌───────────┐
│ 1 Discover │ ──► │ 2 Profile │ ──► │ 3 Baseline │ ──► │ 4 Assess  │
└────────────┘     └───────────┘     └────────────┘     └─────┬─────┘
                                                              │
┌────────────┐     ┌───────────┐     ┌────────────┐           ▼
│ 7 Impl     │ ◄── │ 6 Select  │ ◄── │5 Prioritize│ ◄─────────┘
└─────┬──────┘     └───────────┘     └────────────┘
      │
      ▼
┌────────────┐     ┌───────────┐     ┌────────────┐     ┌───────────┐
│ 8 Verify   │ ──► │ 9 Repair  │ ──► │ 10 Record  │ ──► │ 11 Repeat │
└────────────┘     └───────────┘     └────────────┘     └───────────┘
```

### Phase Details

1. **Discover**:
   - Locate the project root, package manifest (`package.json`, `pyproject.toml`, etc.), and bundler configuration.
   - Identify Phaser version from dependencies or script tags.
   - Scan scene files, game configurations, asset folders, and backend integration touchpoints.
   - Read existing `README.md`, `AGENTS.md`, and project documentation.

2. **Profile**:
   - Run `./tools/magebase-game probe <path>` or read existing `game-profile.json`.
   - Record engine version, orientation, target viewports, scene graph, asset directories, and backend bindings.
   - Mark unverified fields explicitly as provisional.

3. **Baseline**:
   - Execute project's existing build and test commands (e.g. `npm test`, `npm run build`).
   - Run `./tools/magebase-game audit <path>` to check texture dimensions, POT (power of two) compliance, and broken links.
   - Check for console runtime crashes on clean boot using headless browser smoke test where feasible.

4. **Assess**:
   - Compare baseline findings against `GAME_QUALITY_CONTRACT.md`.
   - Check the 8 Hard Release Blockers.
   - Score the 8 Quality Dimensions (1–10).

5. **Prioritize**:
   - Rank identified gaps using the formula:
     $$\text{Priority Score} = (\text{Blocker Weight} \times 10) + (\text{Impact} \times 3) + (\text{Confidence} \times 2) - \text{Effort}$$
   - Hard release blockers take absolute priority over cosmetic polish.

6. **Select**:
   - Choose the single highest-value actionable item that can be delivered as an atomic change.
   - Confirm prerequisites are satisfied.

7. **Implement**:
   - Apply focused edits following existing project code patterns and conventions.
   - Preserve unrelated lines, comments, and structure.

8. **Verify**:
   - Run the fastest specific check for the edited subsystem first.
   - Run the full build and unit/integration suite.
   - Check visual rendering and touch response on target mobile viewports (e.g. iPhone 14/15, Pixel 7) when browser tooling is available.

9. **Repair**:
   - If tests or verification fail, diagnose and fix the regression immediately.
   - Do not commit broken intermediate states.
   - Rerun checks until green.

10. **Record**:
    - Update `game-profile.json`, `asset-catalog.json`, and `GAME_QUALITY.md`.
    - Log what was changed, what passed, and what remains unverified.

11. **Repeat or Stop**:
    - Continue to the next highest-priority task unless a hard stopping condition is met.

---

## 3. Stopping Conditions & Human Escalation

Agents must work autonomously for all routine development, code refactoring, bug fixes, asset reuse, and local testing.

**STOP immediately and ask the human user ONLY when:**
1. **Credentials & Secrets Needed**: Access to private registries, production API keys, signing certificates, or deployment tokens.
2. **Financial Cost**: Work requiring paid API calls, cloud provisioning, or store submission fees.
3. **Destructive Operations**: Dropping production databases, overwriting uncommitted user work, or running force pushes to Git remotes.
4. **Irreversible Schema Migrations**: Destructive alterations to production databases (e.g. dropping columns with live customer data).
5. **Major Ambiguous Product Decisions**: Core gameplay rules, monetization strategy, or fundamental theme choices that cannot be safely inferred from existing assets and code.
6. **Persistent Unstable Test Infrastructure**: Broken host environment or missing system binaries that cannot be resolved locally.

---

## 4. Capability Registry Integration

All agent routing decisions must map through `registry/capabilities.json`.
- When a task requires a domain-specific playbook, match the required intent to the registry capability `id`.
- Follow the declared `playbook` path, `prerequisites`, `inputs`, and `outputs`.
- Never execute arbitrary improvised procedures when a standardized playbook exists.
