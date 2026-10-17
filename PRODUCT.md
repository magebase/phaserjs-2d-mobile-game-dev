# PRODUCT.md — Product Vision, Principles & Scope

> **Product:** `magebase/phaserjs-2d-mobile-game-dev`  
> **Classification:** Agentic Game Engineering Operating System  
> **Target Audience:** Autonomous AI coding agents and human engineers building mobile 2D games with Phaser 4.

---

## 1. Product Vision

The goal of `phaserjs-2d-mobile-game-dev` is to turn any working or prototype 2D web game built with Phaser 4 into a rock-solid, production-grade, mobile-ready release with minimal human intervention.

Most web game prototypes stall during the transition to mobile because of:
- Unresponsive or broken touch controls;
- Improper viewport scaling and letterboxing on modern device aspect ratios (notch/island cutouts);
- Bloated texture memory and frame rate drops on low-to-mid tier mobile devices;
- Disconnected save systems and lack of cloud state persistence;
- Incoherent asset styles from haphazardly mixed art packs;
- Missing release gates and smoke testing on mobile browsers.

This repository provides an automated, repeatable engineering layer that resolves these bottlenecks systematically.

---

## 2. Target Personas

1. **Autonomous AI Coding Agents**
   - Requires clear, non-ambiguous step-by-step playbooks, JSON schemas, and machine-readable capability registries.
   - Demands strict verification criteria so it can self-correct regressions before notifying humans.

2. **Indie Game Developers & Solopreneurs**
   - Wants a fast, automated audit that identifies exactly what is holding their game back from mobile release.
   - Values existing art reuse over spending money on new assets.

3. **Studio Teams & LiveOps Engineers**
   - Needs consistent standards across multiple web/mobile game titles.
   - Relies on automated CI gates, performance budgets, and backend contracts (Django / Cloudflare Workers).

---

## 3. Core Principles

### 3.1 Mobile Ergonomics First
A game cannot be declared "done" if it only plays well with a keyboard and mouse. Touch controls (dynamic virtual sticks, gestures, touch targets $\ge 48\times 48\text{px}$), safe-area notch compliance, and orientation handling are first-class functional requirements.

### 3.2 Existing Art Asset Stewardship
Artistic consistency is easily destroyed by generating disjointed new assets. Agents must discover, catalog, slice, and repurpose assets already present in the repository before authoring or requesting replacements.

### 3.3 Zero Unhandled Runtime Crashes
A mobile game that throws an unhandled exception in an animation callback or audio decode loop will freeze or crash the browser tab. The Definition of Done requires comprehensive runtime exception boundaries, asset preloading safeguards, and fallback states.

### 3.4 Non-Destructive Progression & Edge-Ready Persistence
Player progress must be resilient. Games must support seamless offline play with local fallback (`localStorage` / `IndexedDB`) and robust synchronisation with Django REST APIs or Cloudflare edge primitives (Workers, D1, KV, Durable Objects).

---

## 4. Domain Terminology

| Term | Definition |
| :--- | :--- |
| **Game Profile** | A standardized JSON structure (`game-profile.json`) capturing the game's engine version, scenes, bundler, viewports, art paths, and backend bindings. |
| **Asset Catalog** | An indexed inventory (`asset-catalog.json`) of all visual, audio, and font files including hashes, pixel dimensions, frame slices, and scene references. |
| **Hard Blocker** | One of 8 critical release failure conditions that immediately halts release qualification regardless of cosmetic polish. |
| **Quality Rubric** | A multi-dimensional 1–10 scoring rubric covering Game Feel, Mobile Usability, Combat, Audio, Performance, and Stability. |
| **RenderNode** | Phaser 4's modernized rendering pipeline unit that groups WebGL/WebGPU draw commands and custom shaders efficiently. |
| **SpriteGPULayer** | Hardware-accelerated batch layer in Phaser 4 for thousands of concurrent mobile sprites with zero CPU draw overhead. |
| **TilemapGPULayer** | Modernized tilemap renderer in Phaser 4 optimized for WebGL/WebGPU mobile memory constraints. |
| **Juice / Game Feel** | Micro-feedback elements (screen shake, hit pauses, particle bursts, squash-and-stretch, audio stingers) that make gameplay tactile and satisfying. |
| **Safe Area Insets** | Visual margins preventing interactive UI elements from being obscured by display cutouts (iPhone notch, dynamic island, home indicator bar). |

---

## 5. Scope Boundaries

### In Scope
- Auditing existing Phaser 4 codebases and diagnosing mobile deficiencies.
- Enhancing touch controls, virtual joysticks, gestures, and UI hitboxes.
- Tuning camera scaling, letterboxing, dynamic viewport adaptation, and safe area insets.
- Upgrading legacy Phaser 3 rendering to Phaser 4 hardware features (`RenderNodes`, `SpriteGPULayer`).
- Cataloging and reusing existing sprite sheets, tiles, and audio assets.
- Wiring persistence to Django REST backends or Cloudflare serverless edge bindings.
- Executing automated mobile browser smoke tests and visual regression checks.

### Out of Scope
- Building new game engines from scratch.
- Acting as a general-purpose prompt generator without code execution.
- Arbitrarily replacing the user's chosen UI framework or bundler without a stated requirement.
- Authoring non-2D / 3D game pipelines (e.g. Three.js, Babylon.js, PlayCanvas).
