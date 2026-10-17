# Phaser 4 Input Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Unified Pointer Architecture

Phaser 4 unifies mouse and touch inputs into `Phaser.Input.Pointer` instances:

```javascript
// Active pointer properties:
// pointer.x, pointer.y (camera-relative or screen-relative)
// pointer.isDown (boolean)
// pointer.id (touch identifier)

// Global scene pointer events:
this.input.on('pointerdown', (pointer) => {
  console.log(`Pointer ${pointer.id} pressed at (${pointer.x}, ${pointer.y})`);
});

this.input.on('pointermove', (pointer) => {
  if (pointer.isDown) {
    // Drag gesture
  }
});

this.input.on('pointerup', (pointer) => {
  // Release gesture
});
```

---

## 2. Interactive GameObjects

Make any GameObject respond to touch events:

```javascript
const button = this.add.image(x, y, 'btn_play');
button.setInteractive({ useHandCursor: true });

button.on('pointerdown', () => {
  button.setScale(0.95);
});
button.on('pointerup', () => {
  button.setScale(1.0);
  this.scene.start('GameScene');
});
```
