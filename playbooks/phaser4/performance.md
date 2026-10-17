# Playbook: Mobile Frame Rate & Performance Optimization

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.performance`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-08 (Critical FPS Degradation)

---

## 1. Purpose & Scope

This playbook guides achieving a consistent 60 FPS on mid-tier mobile hardware (Apple A13+, Snapdragon 7xx) by leveraging Phaser 4's `SpriteGPULayer`, `TilemapGPULayer`, zero-allocation update loops, and texture atlases.

---

## 2. Phaser 4 GPU-Accelerated Layers

### 2.1 `SpriteGPULayer` for High Entity Counts
When rendering bullet hell projectiles, mob swarms, or coin drops, traditional Phaser Game Object lists iterate transforms on the CPU. Phaser 4 introduces `SpriteGPULayer`:

```javascript
// Inside GameScene.create():
const bulletLayer = this.add.spriteGPULayer('projectiles', 2000);

// Spawning a GPU-batched sprite:
const bullet = bulletLayer.create(x, y, 'bullet_frame');
bullet.setVelocity(vx, vy);
```
*Result: Reduces CPU draw overhead by up to 80% for 500+ on-screen entities.*

### 2.2 `TilemapGPULayer`
For tilemaps, use `TilemapGPULayer` instead of CPU-culling static layers:
```javascript
const map = this.make.tilemap({ key: 'level1' });
const tileset = map.addTilesetImage('tiles', 'tileset_texture');

// Modern Phaser 4 GPU layer:
const groundLayer = map.createGPULayer('Ground', tileset, 0, 0);
```

---

## 3. Zero-Allocation Update Loops (GC Spike Elimination)

Garbage Collection (GC) pauses are the #1 cause of stutter on mobile browsers.

### The Antipattern (Allocating in `update`):
```javascript
// BAD: Allocates a new object every 16ms (60 times per second)
update(time, delta) {
  const target = { x: player.x, y: player.y }; // GC pressure!
  const dist = new Phaser.Math.Vector2(enemy.x, enemy.y).distance(target); // GC pressure!
}
```

### The Fix (Pre-allocated Scratch Variables):
```javascript
export class GameScene extends Phaser.Scene {
  create() {
    // Scratch vector allocated once
    this.scratchVec = new Phaser.Math.Vector2();
  }

  update(time, delta) {
    this.scratchVec.set(player.x - enemy.x, player.y - enemy.y);
    const dist = this.scratchVec.length();
  }
}
```

---

## 4. Texture Atlas Batching

Loose individual PNG files force the WebGL renderer to break draw batches every time the bound texture changes.
- Combine character, enemy, projectile, and UI textures into a single texture atlas (`assets/spritesheet.png` + `assets/spritesheet.json`).
- Verify WebGL draw calls remain $< 15$ per frame.

---

## 5. Verification Checklist

- [ ] Chrome DevTools Performance recording shows flat memory heap during 60s of active gameplay (sawtooth GC spikes are eliminated).
- [ ] Median FPS remains $\ge 58$ FPS on throttled CPU 4x mobile emulation.
- [ ] WebGL draw calls stay below 20 for typical gameplay scenes.
