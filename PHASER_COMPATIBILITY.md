# PHASER_COMPATIBILITY.md — Phaser 4 Matrix, Features & Upstream Policy

> **Pinned Target Release:** Phaser **4.2.1**  
> **Upstream Repository:** [phaserjs/phaser](https://github.com/phaserjs/phaser)  
> **Official Skills Reference:** `https://github.com/phaserjs/phaser/tree/master/skills`

---

## 1. Upstream Relationship & Policy

The official Phaser project now publishes AI-agent skills for core engine systems. This repository builds **above** that framework reference layer rather than duplicating basic API definitions.

### Key Policies:
1. **Framework Reference Layer**: Official Phaser skills under `upstream/phaser-skills/` serve as the immutable engine reference for syntax, signatures, and low-level constructs.
2. **Version Pinning**: All reference skills, fixtures, and evaluations are pinned to **Phaser 4.2.1**.
3. **Magebase-Owned Specialization**: This repository owns mobile ergonomics, existing art reuse, game feel, edge/backend persistence, performance profiling, and autonomous agent orchestration.
4. **Zero Silent Phaser 3 Regressions**: Never apply deprecated Phaser 3 patterns to a Phaser 4 codebase. When inspecting code, detect and migrate legacy Phaser 3 constructs.
5. **Attribution & Licensing**: Upstream skills are copyright (c) Richard Davey / Phaser Studio Inc. and licensed under the MIT License. Upstream license headers are strictly preserved.

---

## 2. Phaser 4 Architectural Advancements vs Phaser 3

Phaser 4 represents a major modernization of the engine, particularly critical for mobile performance:

### 2.1 The RenderNode Architecture
In Phaser 3, rendering was handled through monolithic pipelines. Phaser 4 introduces **RenderNodes**—modular, graph-based rendering nodes that allow:
- Direct WebGL and WebGPU pipeline dispatch.
- Batching game objects into unified draw calls with custom shader passes.
- Low-memory render targets optimized for mobile tile-based GPUs (Apple Silicon, Mali, Adreno).

### 2.2 `SpriteGPULayer` & `TilemapGPULayer`
Phaser 4 introduces dedicated GPU-accelerated layers:
- **`SpriteGPULayer`**: Manages tens of thousands of dynamic sprites (projectiles, particles, coins, mob swarms) with GPU-side vertex buffers and minimal CPU transform overhead.
- **`TilemapGPULayer`**: Bypasses traditional CPU tile culling by pushing chunked tilemap buffers directly to GPU memory, drastically reducing frame time on mobile.

### 2.3 Modernized Input & Multi-Touch
- Pointers support native high-frequency touch event coalescing.
- Multi-touch pinch-to-zoom and multi-finger gestures are built-in primitives without third-party plugins.
- Built-in safe-area coordinate querying relative to the browser viewport.

---

## 3. Deprecated Phaser 3 Patterns vs Phaser 4 Equivalents

When agents inspect or edit Phaser code, they must check for and replace these deprecated patterns:

| Deprecated Phaser 3 Pattern | Modern Phaser 4 Equivalent | Rationale / Benefit |
| :--- | :--- | :--- |
| `this.add.particles(x, y, 'texture', config)` (old emitter manager) | `this.add.particles('texture', config)` or `this.add.particleEmitter(config)` | Simplified hierarchy; emitters are first-class Game Objects. |
| `this.cameras.main.setRoundPixels(true)` everywhere | `this.scale.pixelArt = true` in game config or layer-level antialias | Engine-level subpixel positioning is now managed cleanly without camera jitter. |
| Custom camera hack for mobile letterbox | `this.scale.scaleMode = Phaser.Scale.FIT` with `autoCenter: Phaser.Scale.CENTER_BOTH` | Native safe area and aspect ratio preservation. |
| Manual WebGL pipeline binding `setPipeline('Custom')` | `this.setRenderNode('CustomNode')` or filter attachments | RenderNodes provide safe lifecycle hooks and multi-pass support. |
| Static tilemap layer CPU iterate `layer.forEachTile(...)` | `layer.setCollisionByProperty(...)` on `TilemapGPULayer` | Keeps collision queries fast without thrashing JavaScript heaps. |
| Mixing Canvas and WebGL game configs | Pure `Phaser.WEBGL` or `Phaser.AUTO` with GPU feature detection | Canvas fallback in modern mobile browsers is slower than hardware WebGL. |
| `this.sound.play('key')` before user gesture | `this.sound.unlock()` handled inside pointerdown overlay scene | Avoids silent audio context rejection on iOS Safari. |

---

## 4. Controlled Upstream Synchronization

To synchronize or update the vendored upstream reference skills:

```bash
# Run the upstream sync utility
./upstream/sync-phaser-skills.sh --tag v4.2.1
```

The sync utility:
1. Clones/fetches the specific release tag from `phaserjs/phaser`.
2. Verifies git tag signature and commit hash.
3. Copies the relevant skill files into `upstream/phaser-skills/`.
4. Runs `scripts/validate-skills.py` to ensure all links and schemas remain valid.
