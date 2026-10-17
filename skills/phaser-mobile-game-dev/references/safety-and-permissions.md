# Safety & Permissions — Boundaries & Escalation Triggers

> **Router Reference:** `phaser-mobile-game-dev`  
> **Rule:** Maximize autonomous velocity on reversible local engineering; escalate only on real operational risk.

---

## 1. Autonomous Operations (Proceed Without Prompting)

Agents are fully authorized to perform the following actions autonomously:

1. **Inspection & Profiling**:
   - Running `./tools/magebase-game probe`, `./tools/magebase-game audit`, `./tools/magebase-game report`.
   - Parsing ASTs, file trees, package manifests, and configuration files.

2. **Code Implementation & Refactoring**:
   - Implementing touch controls, virtual joysticks, and safe-area adjustments.
   - Refactoring scenes to modern Phaser 4 lifecycle patterns.
   - Optimizing rendering with `RenderNodes`, `SpriteGPULayer`, and `TilemapGPULayer`.
   - Wiring client-side API adapters for Django or Cloudflare Worker endpoints.

3. **Asset Stewardship**:
   - Slicing existing sprite sheets into individual animation frames.
   - Re-indexing existing asset catalogs and updating manifest files.
   - Generating non-destructive derived asset definitions.

4. **Verification & Testing**:
   - Running local test suites (`npm test`, `pytest`, `playwright`).
   - Launching headless browser smoke tests on local dev servers.
   - Measuring frame deltas and memory footprints.
   - Repairing test failures and regressions.

---

## 2. Escalation Triggers (Stop and Ask the User)

An agent MUST pause and ask the human user for explicit approval or input when:

1. **Secrets & Credentials**:
   - Needing production API keys, signing certificates, or deployment tokens that cannot be found in local `.env.example` templates.

2. **Financial Cost & Paid Services**:
   - Invoking paid third-party generation APIs, cloud infrastructure provisioning, or app store submission fees.

3. **Destructive Operations**:
   - Deleting non-derived original art assets, dropping production database tables, or running `git reset --hard` / `git push --force`.

4. **Irreversible Schema Migrations**:
   - Modifying production database schemas with destructive column drops or data migrations without an approved rollback script.

5. **Fundamental Product Ambiguities**:
   - Deciding core gameplay rules, narrative branches, or monetization models where the existing codebase and assets offer no clear evidence.
