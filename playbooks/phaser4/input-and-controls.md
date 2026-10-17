# Playbook: Mobile Touch Controls & Virtual Joystick

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.input_and_controls`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-04 (Unplayable Touch Controls)

---

## 1. Purpose & Scope

This playbook guides implementing responsive, low-latency mobile touch controls in Phaser 4. It covers floating virtual joysticks, action buttons with $\ge 44\text{px}$ hitboxes, multi-touch event coalescing, and desktop keyboard fallback.

---

## 2. Multi-Touch Initialization

By default, Phaser enables 2 pointers. For complex mobile gameplay (moving + attacking simultaneously), initialize 3 pointers:

```javascript
// In BootScene or GameScene create():
this.input.addPointer(2); // Gives 3 active touch pointers (pointer1, pointer2, pointer3)
```

---

## 3. Production Virtual Joystick Component

Here is a lightweight, zero-dependency floating virtual joystick implementation for Phaser 4:

```javascript
export class VirtualJoystick {
  constructor(scene, options = {}) {
    this.scene = scene;
    this.radius = options.radius || 50;
    this.baseRadius = options.baseRadius || 70;
    this.activePointer = null;
    this.vector = { x: 0, y: 0 };
    this.isDown = false;

    // Visual graphics
    this.base = scene.add.circle(0, 0, this.baseRadius, 0xffffff, 0.15)
      .setScrollFactor(0)
      .setDepth(1000)
      .setVisible(false);

    this.stick = scene.add.circle(0, 0, this.radius / 2, 0x00ff88, 0.5)
      .setScrollFactor(0)
      .setDepth(1001)
      .setVisible(false);

    this.setupListeners();
  }

  setupListeners() {
    this.scene.input.on('pointerdown', (pointer) => {
      // Only capture touches on left 60% of viewport
      if (pointer.x > this.scene.scale.width * 0.6) return;
      if (this.activePointer) return;

      this.activePointer = pointer;
      this.isDown = true;
      this.base.setPosition(pointer.x, pointer.y).setVisible(true);
      this.stick.setPosition(pointer.x, pointer.y).setVisible(true);
    });

    this.scene.input.on('pointermove', (pointer) => {
      if (pointer !== this.activePointer) return;

      const dx = pointer.x - this.base.x;
      const dy = pointer.y - this.base.y;
      const dist = Math.hypot(dx, dy);
      const angle = Math.atan2(dy, dx);

      const clampedDist = Math.min(dist, this.radius);
      this.stick.x = this.base.x + Math.cos(angle) * clampedDist;
      this.stick.y = this.base.y + Math.sin(angle) * clampedDist;

      this.vector.x = (this.stick.x - this.base.x) / this.radius;
      this.vector.y = (this.stick.y - this.base.y) / this.radius;
    });

    const onPointerUp = (pointer) => {
      if (pointer === this.activePointer) {
        this.activePointer = null;
        this.isDown = false;
        this.vector.x = 0;
        this.vector.y = 0;
        this.base.setVisible(false);
        this.stick.setVisible(false);
      }
    };

    this.scene.input.on('pointerup', onPointerUp);
    this.scene.input.on('pointerupoutside', onPointerUp);
  }

  destroy() {
    this.base.destroy();
    this.stick.destroy();
  }
}
```

---

## 4. On-Screen Action Buttons with Safe Hitboxes

Ensure mobile buttons have touch padding to prevent missed taps:

```javascript
export function createTouchButton(scene, x, y, label, callback) {
  const container = scene.add.container(x, y).setScrollFactor(0).setDepth(1000);
  
  // Visual button background
  const bg = scene.add.rectangle(0, 0, 64, 64, 0x333333, 0.8)
    .setStrokeStyle(2, 0x00ff88);
  const text = scene.add.text(0, 0, label, { fontSize: '18px', color: '#ffffff' }).setOrigin(0.5);

  container.add([bg, text]);

  // Expand interactive area to 72x72px for thumb forgiveness
  bg.setInteractive(new Phaser.Geom.Rectangle(-4, -4, 72, 72), Phaser.Geom.Rectangle.Contains);
  
  bg.on('pointerdown', () => {
    container.setScale(0.92);
    callback();
  });
  bg.on('pointerup', () => container.setScale(1.0));
  bg.on('pointerout', () => container.setScale(1.0));

  return container;
}
```

---

## 5. Keyboard & Desktop Fallback Pattern

In `update(time, delta)`:
```javascript
// Read virtual stick or keyboard
let moveX = this.joystick.vector.x;
let moveY = this.joystick.vector.y;

if (this.cursors.left.isDown) moveX = -1;
else if (this.cursors.right.isDown) moveX = 1;

if (this.cursors.up.isDown) moveY = -1;
else if (this.cursors.down.isDown) moveY = 1;

player.setVelocity(moveX * speed, moveY * speed);
```

---

## 6. Verification Checklist

- [ ] Multi-touch verified: moving virtual stick while tapping action button does not cancel movement.
- [ ] Hitboxes are $\ge 44\times 44\text{px}$.
- [ ] No controls overlap device notch or dynamic island (respect safe area insets).
