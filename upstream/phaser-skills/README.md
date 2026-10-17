# Upstream Phaser Skills Reference

> **Upstream Source:** [phaserjs/phaser/skills](https://github.com/phaserjs/phaser/tree/master/skills)  
> **Pinned Framework Release:** **Phaser 4.2.1**  
> **License:** MIT (Copyright (c) Richard Davey / Phaser Studio Inc.)

---

## 1. Overview & Policy

This directory contains a pinned reference subset of the official AI-agent skills published by the Phaser project.

### Core Operating Rules:
1. **Framework Reference Layer**: These files document official Phaser 4 core engine APIs, classes, and signatures.
2. **Read-Only Upstream Layer**: Do not edit these files directly. Update them only via `upstream/sync-phaser-skills.sh`.
3. **Magebase Layer Separation**: Magebase-specific mobile engineering, touch controls, art reuse, and edge persistence playbooks live under `playbooks/` and `skills/phaser-mobile-game-dev/`.

---

## 2. Pinned Reference Modules

| Reference Skill | Scope & Framework API |
| :--- | :--- |
| `scenes.md` | Core `Phaser.Scene` lifecycle, systems, and transition APIs |
| `gameobjects.md` | `Sprite`, `Image`, `Container`, `SpriteGPULayer`, `Graphics` |
| `textures.md` | `TextureManager`, frame slicing, dynamic textures, WebGL texture binding |
| `input.md` | Unified Pointer system, multi-touch event coalescing, drag and gestures |
| `physics.md` | Arcade Physics body configuration, spatial velocity, collision pairs |
| `loader.md` | `LoaderPlugin`, file types, progress callbacks, asset packs |
| `scale.md` | `ScaleManager`, fit modes, centering, auto-resize listeners |

---

## 3. Synchronizing Upstream

To check or synchronize against the official repository:

```bash
./upstream/sync-phaser-skills.sh --tag v4.2.1
```
