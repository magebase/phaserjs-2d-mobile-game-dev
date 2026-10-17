# phaserjs-2d-mobile-game-dev

> **Agent-First Engineering Operating System for Phaser 4 Mobile 2D Game Development**

[![CI](https://github.com/magebase/phaserjs-2d-mobile-game-dev/actions/workflows/ci.yml/badge.svg)](https://github.com/magebase/phaserjs-2d-mobile-game-dev/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Phaser Version](https://img.shields.io/badge/Phaser-4.2.1%20Pinned-orange.svg)](PHASER_COMPATIBILITY.md)
[![Target Platform](https://img.shields.io/badge/Platform-Mobile%20Web%20%7C%20PWA%20%7C%20Capacitor-brightgreen.svg)](GAME_QUALITY_CONTRACT.md)

---

## 1. Mission

`phaserjs-2d-mobile-game-dev` is a reusable, agent-first engineering skill repository designed to take an existing Phaser 4 game from its current state toward a polished, reliable, mobile-ready, release-ready product—with minimal human orchestration.

This is **not a prompt collection**. It is an operating system for repeatable game development work:
- **Router Skill**: A single entry point that orchestrates audits, fixes, and gates.
- **Domain Playbooks**: 35+ executable playbooks spanning architecture, touch controls, camera scaling, rendering, game feel, art reuse, Django/Cloudflare backend sync, and QA.
- **Executable Tooling**: Native Python/Node CLI probes for AST inspection, asset hashing, and quality reporting.
- **Project Profile & Contracts**: Formal JSON schemas and a strict 2-layer Quality Contract (8 hard blockers + 8 dimensional scores).
- **Existing Art Library Intelligence**: Prioritizes discovery, slicing, and reuse of existing sprites, tiles, and animations before generating new assets.
- **Upstream Reference Layer**: Builds cleanly on top of official Phaser 4 skills (`skills/`) pinned at v4.2.1 without duplicating core framework documentation.

---

## 2. The Primary User Experience

Invoke the skill with a single natural-language instruction:

```text
Use the Phaser mobile game development skill. Inspect this game, identify the highest-impact gaps, implement improvements, and verify them until the next meaningful blocker.
```

The agent will autonomously:
1. **Discover**: Find game roots, Phaser version, scene graph, asset catalog, bundlers, and backend bindings.
2. **Profile**: Build or update a truthful `game-profile.json`.
3. **Baseline**: Run headless diagnostic checks, asset audits, and console smoke tests.
4. **Assess**: Evaluate against the 8 hard release blockers and 8 quality dimensions in `GAME_QUALITY_CONTRACT.md`.
5. **Prioritize**: Rank gaps by player impact, risk reduction, and release blocker status.
6. **Select & Implement**: Execute focused, convention-preserving improvements (one coherent slice at a time).
7. **Verify & Repair**: Re-run automated tests, phone viewport checks, and verify regressions are absent.
8. **Record**: Update `GAME_QUALITY.md`, the quality backlog, and report clear findings to the developer.

---

## 3. Architecture & Repository Map

```
phaserjs-2d-mobile-game-dev/
├── README.md                          # Repository overview & quickstart
├── AGENTS.md                          # Autonomous agent engineering contract
├── PRODUCT.md                         # Product vision, principles & vocabulary
├── GAME_QUALITY_CONTRACT.md           # Authoritative Definition of Done & blocker list
├── PHASER_COMPATIBILITY.md            # Pinned v4.2.1 matrix & migration guardrails
├── CONTRIBUTING.md                    # Contributor guide & validation workflow
├── SECURITY.md                        # Security policy & bundle hygiene
├── LICENSE                            # MIT License
├── CHANGELOG.md                       # Semantic version release notes
├── skills/
│   └── phaser-mobile-game-dev/
│       ├── SKILL.md                   # Canonical router skill definition
│       └── references/                # Router reference contracts & rubrics
├── playbooks/
│   ├── lifecycle/                     # Project inspection, prioritization, repair
│   ├── phaser4/                       # Scenes, input, camera, RenderNodes, GPU layers
│   ├── game-quality/                  # Game feel, combat, progression, mobile UX, audio
│   ├── art-pipeline/                  # Asset cataloging, reuse-first pipeline, animation QA
│   ├── backend/                       # Django APIs, Cloudflare Workers, D1/KV/R2 state sync
│   └── qa/                            # Smoke tests, visual regression, performance budgets
├── registry/
│   ├── capabilities.json              # Machine-readable capability registry
│   └── schema.json                    # Schema for capability catalog
├── schemas/                           # Authoritative JSON Schemas
│   ├── game-profile.schema.json
│   ├── asset-catalog.schema.json
│   ├── audit-report.schema.json
│   └── quality-backlog.schema.json
├── templates/                         # Starting templates for game projects
│   ├── game-profile.json
│   ├── GAME_QUALITY.md
│   └── release-checklist.md
├── tools/                             # Executable command-line inspection tools
│   ├── magebase-game                  # Unified CLI wrapper
│   ├── project-probe                  # Project stack & scene AST analyzer
│   ├── asset-audit                    # Deep texture/spritesheet analyzer
│   ├── report                         # Quality score & blocker evaluator
│   └── lib/                           # Shared Python/Node inspection modules
├── upstream/
│   ├── phaser-skills/                 # Pinned upstream Phaser 4 reference skills
│   └── sync-phaser-skills.sh          # Controlled upstream sync script
├── fixtures/                          # Test fixtures for test-driven validation
│   ├── minimal-phaser4-game/          # Minimal runnable Phaser 4 reference game
│   └── asset-library-sample/          # Asset library with clean & defective assets
├── evals/                             # Evaluation suites verifying skill accuracy
└── scripts/                           # Validation and CI test runners
```

---

## 4. Strategic Principles

### 4.1 Build Above the Official Phaser 4 Skill Layer
Phaser 4 introduces significant architectural upgrades over Phaser 3:
- WebGL/WebGPU hardware acceleration pipeline (`RenderNodes`, `SpriteGPULayer`, `TilemapGPULayer`).
- Direct modern event loop and revised lifecycle hooks.
- Native mobile touch enhancements and viewport scale managers.

Rather than re-documenting every basic API, this repository pins the official framework skills (`upstream/phaser-skills/`) and builds high-leverage mobile quality, game feel, art reuse, and edge integration on top.

### 4.2 Detect the Stack — Never Force a Rewrite
The skill inspects existing project conventions before proposing changes:
- **No unwanted frameworks**: Does not inject Svelte, React, or custom UI frameworks into the canvas unless requested.
- **No tooling churn**: Preserves existing bundlers (Vite, Webpack, esbuild, or zero-build script tags) and package managers (`npm`, `pnpm`, `yarn`, `bun`).
- **Backend detection**: Gracefully adapts to standalone client builds, Django REST API backends, or Cloudflare Workers (Python/JS) utilizing D1, KV, R2, and Durable Objects.

### 4.3 Existing Art Library Intelligence (Reuse First)
Generating new art when an existing sprite library already exists creates stylistic incoherence and wasted storage. The skill mandates:
1. Scanning all existing image, spritesheet, atlas, and audio directories.
2. Indexing slice points, animation frames, color palettes, and themes.
3. Matching missing gameplay roles against existing unused art before generating replacements.

---

## 5. Tooling Quickstart

The repository includes executable CLI utilities inside `tools/` that can be run directly inside any game project:

```bash
# 1. Probe game structure, scenes, Phaser version, and backend bindings
./tools/magebase-game probe /path/to/game --output game-profile.json

# 2. Audit textures, spritesheets, audio, and detect defective assets
./tools/magebase-game audit /path/to/game --output asset-catalog.json

# 3. Evaluate game quality against the Definition of Done and generate markdown report
./tools/magebase-game report /path/to/game --profile game-profile.json --catalog asset-catalog.json --output GAME_QUALITY.md

# 4. Run automated verification gates
./tools/magebase-game verify /path/to/game
```

---

## 6. Verification & Quality Gates

Run the automated test and validation suite:

```bash
# Validate JSON schemas and registry capabilities
python3 scripts/validate-skills.py
python3 scripts/validate-registry.py

# Run evaluation harness
python3 scripts/run-evals.py
```

---

## 7. License & Upstream Attribution

- `phaserjs-2d-mobile-game-dev` is licensed under the [MIT License](LICENSE).
- Official Phaser skills included under `upstream/phaser-skills/` are copyright (c) Richard Davey / Phaser Studio Inc. and licensed under the MIT License. See [PHASER_COMPATIBILITY.md](PHASER_COMPATIBILITY.md) for details.
