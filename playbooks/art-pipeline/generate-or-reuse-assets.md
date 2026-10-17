# Playbook: Reuse-First Asset Resolution & Slicing

> **Domain:** Art Pipeline  
> **Capability ID:** `art_pipeline.generate_or_reuse_assets`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook enforces the **Reuse Before Inventing** prime directive: when a game mechanic requires a visual or audio asset (e.g. projectile, coin, potion, explosion SFX), the agent must first search, slice, or recolor assets already present in `asset-catalog.json` before authoring new files.

---

## 2. Asset Resolution Decision Hierarchy

```
[Missing Gameplay Entity]
          │
          ▼
1. Query `asset-catalog.json` for unused sprites / frames
    ├─► Found candidate? ──► Slice / Bind in code
    │
    ▼ (No candidate)
2. Derive from existing asset (Recolor, Flip, Scale, Combine)
    ├─► Success? ──────────► Save non-destructive derived asset
    │
    ▼ (No suitable source)
3. Procedural / Programmatic Generation
    ├─► Vector/Canvas? ────► `scene.make.graphics()` procedural texture
    │
    ▼ (Only if complex art required)
4. Invoke Antigravity `image-generator` subagent with exact style constraints
```

---

## 3. Practical Reuse Examples

### 3.1 Procedural Re-coloring (e.g. Fire Slime from Green Slime)
Instead of generating a whole new spritesheet, apply a runtime tint or canvas palette swap:

```javascript
// Spawn an elite fire variant using existing 'slime_green' asset
export function createFireSlime(scene, x, y) {
  const slime = scene.add.sprite(x, y, 'slime_green');
  slime.setTint(0xff4422); // Re-palette to fiery red
  slime.damage = 25; // Elite damage
  return slime;
}
```

### 3.2 Slicing Unused Tiles for Items
Often, a tileset contains potion bottles, keys, or weapon icons in unreferenced tile cells:

```javascript
// Register a single 16x16 frame from a master tileset as a standalone icon
this.textures.addSpriteSheetFromTexture('gold_key', {
  frameWidth: 16,
  frameHeight: 16,
  startFrame: 42,
  endFrame: 42
});
```

---

## 4. Verification Checklist

- [ ] Search of `asset-catalog.json` completed and documented before requesting new assets.
- [ ] Derived textures do not overwrite original source files on disk.
- [ ] Recolored or sliced assets match original pixel dimensions and resolution.
