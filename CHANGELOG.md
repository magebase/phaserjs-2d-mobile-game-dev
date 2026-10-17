# CHANGELOG

All notable changes to `phaserjs-2d-mobile-game-dev` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-17

### Added
- **Canonical Router Skill**: `skills/phaser-mobile-game-dev/SKILL.md` with single-invocation entry point and 11-step execution loop.
- **Reference Contracts**: `workflow-contract.md`, `evidence-rules.md`, `quality-rubric.md`, and `safety-and-permissions.md`.
- **Quality System**: `GAME_QUALITY_CONTRACT.md` establishing 8 Hard Release Blockers (RB-01 through RB-08) and 8 Dimensional Quality Rubrics.
- **Phaser 4 Matrix**: `PHASER_COMPATIBILITY.md` documenting pinned Phaser 4.2.1 support, `RenderNodes`, `SpriteGPULayer`, `TilemapGPULayer`, and deprecation replacements.
- **Authoritative JSON Schemas**:
  - `schemas/game-profile.schema.json`
  - `schemas/asset-catalog.schema.json`
  - `schemas/audit-report.schema.json`
  - `schemas/quality-backlog.schema.json`
- **Capability Registry**: `registry/capabilities.json` mapping 35+ granular capabilities across lifecycle, phaser4, game-quality, art-pipeline, backend, and QA.
- **Executable CLI Tools**:
  - `tools/project-probe`: AST and project inspector.
  - `tools/asset-audit`: Texture, frame slice, alpha channel, and audio auditor.
  - `tools/report`: Quality report generator producing machine JSON and human `GAME_QUALITY.md`.
  - `tools/magebase-game`: Unified CLI dispatcher.
- **Domain Playbooks**:
  - Lifecycle: `inspect-project`, `prioritize-improvements`, `implement-verify-repair`, `release-readiness`.
  - Phaser 4: `architecture-scenes`, `input-and-controls`, `cameras-and-scaling`, `rendering-filters-lighting`, `animation-particles-vfx`, `physics-collision`, `loading-and-scene-transitions`, `performance`.
  - Game Quality: `core-loop-and-game-feel`, `combat-and-interaction`, `progression-and-balance`, `procedural-content`, `mobile-ux-and-accessibility`, `audio-feedback`, `monetization-and-analytics`, `retention-and-live-ops`.
  - Art Pipeline: `discover-and-catalog`, `asset-selection-and-style`, `sprite-sheet-and-animation-qa`, `visual-polish`, `generate-or-reuse-assets`.
  - Backend: `django-api-contracts`, `identity-save-state-and-progression`, `cloudflare-workers`, `d1-r2-kv-queues-durable-objects`, `reliability-and-observability`, `security-and-abuse`.
  - QA: `unit-integration-gameplay-tests`, `browser-and-device-smoke-tests`, `visual-regression`, `performance-budget`, `build-store-release-checklist`.
- **Upstream Reference**: Pinned subset of official Phaser 4 skills under `upstream/phaser-skills/` and `sync-phaser-skills.sh`.
- **Fixtures & Evals**: Minimal Phaser 4 test game, asset library fixture, and 4 automated evaluation test suites.
- **CI / CD**: GitHub Actions workflow in `.github/workflows/ci.yml`.
