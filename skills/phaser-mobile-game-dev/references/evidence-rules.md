# Evidence Rules — Ground-Truth Standards for Game Auditing

> **Router Reference:** `phaser-mobile-game-dev`  
> **Rule:** Never assert project health, defects, or performance without verified evidence.

---

## 1. The Three Evidence Tiers

Every finding in an audit report or quality backlog must be classified into one of three tiers:

| Tier | Classification | Criteria |
| :--- | :--- | :--- |
| **Tier 1** | **Confirmed Defect** | Verified by executable tool output, compilation error, runtime stack trace, or missing file 404 in catalog. |
| **Tier 2** | **Likely Issue** | Pattern match in static AST (e.g. `this.sound.play` without user gesture unlock, or hardcoded desktop pixel dimensions on mobile cameras) without live runtime verification. |
| **Tier 3** | **Unverified Area** | Area not currently covered by automated tests or tooling (e.g. visual feel, audio balance on physical hardware). |

---

## 2. Evidence Requirements by Subsystem

### 2.1 Build & Runtime
- **Requirement**: Build status must be substantiated by actual exit codes and compiler output from the project's build command (`npm run build`, etc.).
- **Prohibition**: An agent must never assume a project builds simply because `package.json` contains dependencies.

### 2.2 Asset Verification
- **Requirement**: Every referenced texture key in `this.load.image('key', 'path')` or `this.load.spritesheet(...)` must be matched against a verified file on disk with a valid SHA256 hash.
- **Defects Detected**: Non-power-of-two (NPOT) dimensions for repeating textures, irregular grid sizing (spritesheet dimensions not evenly divisible by frame width/height), and uncompressed oversized PNGs.

### 2.3 Mobile Touch Controls
- **Requirement**: Touch support must be substantiated by searching for `pointerdown`, `pointermove`, `pointerup` handlers, virtual joystick implementations, or touch gesture managers.
- **Defect Criterion**: If keyboard keys (`cursors.left`, `W/A/S/D`) are the sole input mechanism in `update()`, mark **RB-04** as `FAIL`.

### 2.4 Performance
- **Requirement**: FPS assertions must cite frame delta measurements or draw call estimates from `SpriteGPULayer` / `TilemapGPULayer` batching.
- **Defect Criterion**: Frame rates below 30 FPS or update loops allocating objects inside `update(time, delta)` are flagged.
