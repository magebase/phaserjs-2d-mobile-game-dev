# PHASER_COMPATIBILITY.md — Phaser 4 Matrix, Features & Technical Verification

> **Pinned Target Release:** Phaser **4.2.1**  
> **Upstream Repository:** [phaserjs/phaser](https://github.com/phaserjs/phaser)  
> **Official Skills Reference:** `https://github.com/phaserjs/phaser/tree/master/skills`

---

## 1. Upstream Relationship & Policy

The official Phaser project publishes AI-agent skills for core engine systems. This repository builds **above** that framework reference layer rather than duplicating basic API definitions.

### Key Policies:
1. **Framework Reference Layer**: Official Phaser skills under `upstream/phaser-skills/` serve as the immutable engine reference for syntax, signatures, and low-level constructs.
2. **Version Pinning**: All reference skills, fixtures, and evaluations are pinned to **Phaser 4.2.1**.
3. **Magebase-Owned Specialization**: This repository owns mobile ergonomics, existing art reuse, game feel, edge/backend persistence, performance profiling, and autonomous agent orchestration.
4. **Zero Silent Phaser 3 Regressions**: Never apply deprecated Phaser 3 patterns to a Phaser 4 codebase. When inspecting code, detect and migrate legacy Phaser 3 constructs.
5. **Attribution & Licensing**: Upstream skills are copyright (c) Richard Davey / Phaser Studio Inc. and licensed under the MIT License. Upstream license headers are strictly preserved.

---

## 2. Technical Capabilities & Render Architecture

### 2.1 WebGL Production Standard & WebGPU Reality
- **Primary Production Standard:** **WebGL2 / WebGL1** is the authoritative, production-grade target across all mobile browsers (iOS Safari and Android Chrome).
- **WebGPU Status:** While experimental/development branches explore WebGPU via modular `RenderNode` pipelines, production Phaser 4 games MUST target WebGL (`Phaser.WEBGL` or `Phaser.AUTO`). Never deploy WebGPU-only constructs without automated WebGL fallback.
- **RenderNode Architecture:** Phaser 4 modularizes rendering through RenderNodes, decoupling scene graph transformations from GPU dispatch to minimize CPU-side transform thrashing on mobile tile-based GPUs (Apple Silicon, Mali, Adreno).

### 2.2 Texture Power-of-Two (POT) vs Non-Power-of-Two (NPOT) Nuance
- **WebGL2 Support (Standard):** WebGL2 has been universal on iOS Safari and Android Chrome since 2021. In WebGL2, NPOT textures are natively supported for linear/nearest filtering and `CLAMP_TO_EDGE` without restriction.
- **WebGL1 Wrapping Constraints:** In WebGL1, NPOT textures are supported only with `CLAMP_TO_EDGE` and no mipmaps. Repeating (`REPEAT` or `MIRRORED_REPEAT`) with mipmapping still requires power-of-two dimensions or runtime texture padding.
- **Audit Policy:** NPOT textures are treated as **informational warnings**, not critical binary blockers. If an asset is used as a standard sprite or UI element, NPOT dimensions are fully acceptable. They only warrant refactoring if repeat-wrapping or custom mipmap pyramids are explicitly utilized.

### 2.3 `SpriteGPULayer` & `TilemapGPULayer`
- **`SpriteGPULayer`**: Manages dynamic sprite batches (projectiles, particles, coins, mob swarms) with GPU-side vertex buffers.
- **`TilemapGPULayer`**: Bypasses traditional CPU tile culling by pushing chunked tilemap buffers directly to GPU memory, reducing mobile frame time.

---

## 3. Performance Metrics: Frame-Time Distributions vs Simple Average FPS

Evaluating mobile performance using only mean/average FPS creates false confidence: a game can average 58 FPS while suffering severe 100ms hitches on impact or scene changes.

Phaser 4 mobile games are evaluated on **frame-time percentiles** over 60-second active gameplay loops:

| Metric | Target (Mid-Tier Mobile) | Critical Blocker Threshold | Purpose |
| :--- | :---: | :---: | :--- |
| **p50 (Median Frame Time)** | $\le 16.6\text{ms}$ ($60\text{ FPS}$) | $> 33.3\text{ms}$ ($< 30\text{ FPS}$) | Measures typical runtime smoothness. |
| **p95 (95th Percentile)** | $\le 22.2\text{ms}$ ($> 45\text{ FPS}$) | $> 33.3\text{ms}$ ($< 30\text{ FPS}$) | Detects recurring input latency and stutter. |
| **p99 (99th Percentile)** | $\le 33.3\text{ms}$ ($> 30\text{ FPS}$) | $> 50.0\text{ms}$ ($< 20\text{ FPS}$) | Captures garbage collection pauses and spikes. |
| **Jank Frames** | $\le 3$ frames per minute | $> 10$ frames per minute | Count of frames taking $> 33.3\text{ms}$ to render. |

---

## 4. Backend Ownership Boundaries (Django SaaS Factory + Cloudflare Edge)

When games integrate with server persistence, the architecture strictly obeys factory boundaries:

1. **Client Game (Phaser 4):** Completely stateless on startup; reads local cache / IndexedDB first, then synchronizes state asynchronously via short-lived HTTP requests.
2. **Cloudflare Workers:** Stateless edge compute; runtime memory strictly capped at 128 MB. No long-lived socket holds or heavy in-memory state manipulation.
3. **Cloudflare D1:** Serverless SQL with rows-touched billing. Hot paths must use explicit indexed queries; leading-wildcard `LIKE '%term%'` is strictly prohibited.
4. **Cloudflare R2:** Direct upload via presigned URLs for save snapshots, user screenshots, or custom level files. Never proxy large binary buffers through Worker memory.
5. **Django Backend:** Used for admin back-office, analytics aggregations, and account identity; communicates via private service bindings or REST contracts. Never introduce long-lived celery/redis dependencies for game loops.

---

## 5. Deprecated Phaser 3 Patterns vs Phaser 4 Equivalents

| Deprecated Phaser 3 Pattern | Modern Phaser 4 Equivalent | Rationale / Benefit |
| :--- | :--- | :--- |
| `this.add.particles(x, y, 'texture', config)` (old emitter manager) | `this.add.particles('texture', config)` or `this.add.particleEmitter(config)` | Simplified hierarchy; emitters are first-class Game Objects. |
| `this.cameras.main.setRoundPixels(true)` everywhere | `this.scale.pixelArt = true` in game config or layer-level antialias | Subpixel positioning managed cleanly without camera jitter. |
| Custom camera hack for mobile letterbox | `this.scale.scaleMode = Phaser.Scale.FIT` with `autoCenter: Phaser.Scale.CENTER_BOTH` | Native safe area and aspect ratio preservation. |
| Manual WebGL pipeline binding `setPipeline('Custom')` | `this.setRenderNode('CustomNode')` or filter attachments | RenderNodes provide safe lifecycle hooks and multi-pass support. |
| Static tilemap layer CPU iterate `layer.forEachTile(...)` | `layer.setCollisionByProperty(...)` on `TilemapGPULayer` | Keeps collision queries fast without thrashing JS heaps. |
| Mixing Canvas and WebGL game configs | Pure `Phaser.WEBGL` or `Phaser.AUTO` with GPU feature detection | Canvas fallback in modern mobile browsers is slower than hardware WebGL. |
| `this.sound.play('key')` before user gesture | `this.sound.unlock()` handled inside pointerdown overlay scene | Avoids silent audio context rejection on iOS Safari. |
