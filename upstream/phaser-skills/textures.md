# Phaser 4 Textures Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Class: `Phaser.Textures.TextureManager`

Access via `this.textures` in any scene.

```javascript
// Check if texture exists
if (this.textures.exists('player')) {
  const tex = this.textures.get('player');
  console.log(`Dimensions: ${tex.source[0].width}x${tex.source[0].height}`);
}

// Slice sprite frames programmatically from an existing texture
this.textures.addSpriteSheetFromTexture('tileset_sliced', {
  frameWidth: 16,
  frameHeight: 16
});

// Create procedural dynamic texture
const dyn = this.textures.createCanvas('scratch_canvas', 128, 128);
const ctx = dyn.getContext();
ctx.fillStyle = '#00ff00';
ctx.fillRect(0, 0, 128, 128);
dyn.refresh();
```
