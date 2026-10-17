# Phaser 4 Scale Manager Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Class: `Phaser.Scale.ScaleManager`

Accessed via `this.scale`.

```javascript
// Scale Modes:
// Phaser.Scale.FIT: Scales canvas to fit within parent container preserving aspect ratio
// Phaser.Scale.ENVELOP: Scales canvas to cover container entirely
// Phaser.Scale.RESIZE: Resizes canvas resolution to match container dynamically

// Auto-centering:
// Phaser.Scale.CENTER_BOTH
// Phaser.Scale.CENTER_HORIZONTALLY
// Phaser.Scale.CENTER_VERTICALLY

// Handling mobile screen rotation / resize
this.scale.on('resize', (gameSize, baseSize, displaySize, resolution) => {
  console.log(`Resized to: ${gameSize.width}x${gameSize.height}`);
});

// Fullscreen toggle
if (this.scale.fullscreen.available) {
  this.scale.startFullscreen();
}
```
