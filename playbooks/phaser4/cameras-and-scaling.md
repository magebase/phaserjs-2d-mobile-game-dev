# Playbook: Camera Scaling & Mobile Safe Area Insets

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.cameras_and_scaling`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides configuring responsive viewport scaling, aspect ratio preservation, camera following with deadzones, and dynamic safe area inset handling to accommodate mobile device notches and home indicator bars.

---

## 2. Pinned Scale Manager Configuration

In the main game config (`src/main.js` or `src/config.js`):

```javascript
import Phaser from 'phaser';

export const gameConfig = {
  type: Phaser.AUTO,
  width: 390,  // Base logical mobile resolution (portrait)
  height: 844,
  parent: 'game-container',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    min: { width: 320, height: 480 },
    max: { width: 768, height: 1600 }
  },
  render: {
    pixelArt: true,
    antialias: false,
    roundPixels: true
  }
};
```

---

## 3. Safe Area Insets (iPhone Notch / Island Protection)

Modern phones have screen cutouts. Interactive buttons must not clip under the status bar or bottom home indicator.

### Reading CSS Safe Insets into Phaser:
```javascript
export function getSafeAreaInsets() {
  const div = document.createElement('div');
  div.style.paddingTop = 'env(safe-area-inset-top, 0px)';
  div.style.paddingBottom = 'env(safe-area-inset-bottom, 0px)';
  div.style.position = 'absolute';
  div.style.visibility = 'hidden';
  document.body.appendChild(div);

  const style = window.getComputedStyle(div);
  const top = parseInt(style.paddingTop, 10) || 44;
  const bottom = parseInt(style.paddingBottom, 10) || 34;
  document.body.removeChild(div);

  return { top, bottom, left: 0, right: 0 };
}
```

### Positioning HUD Relative to Safe Areas:
```javascript
// In UIScene.create():
const safe = getSafeAreaInsets();
const { width, height } = this.scale;

// Position pause button inside safe boundary
const pauseBtn = this.add.image(width - 40, safe.top + 20, 'pause_icon')
  .setScrollFactor(0)
  .setInteractive();

// Position bottom inventory bar above home indicator
const inventory = this.add.container(width / 2, height - safe.bottom - 30)
  .setScrollFactor(0);
```

---

## 4. Camera Follow & Smooth Deadzones

To keep mobile movement fluid and avoid motion sickness:
```javascript
export function setupGameCamera(camera, player, mapBounds) {
  // Clamp camera to map borders
  camera.setBounds(0, 0, mapBounds.width, mapBounds.height);

  // Smooth lerp (0.08 = gentle lag, 1.0 = instant snap)
  camera.startFollow(player, true, 0.08, 0.08);

  // Deadzone: player can move within center box before camera scrolls
  const deadzoneW = camera.width * 0.25;
  const deadzoneH = camera.height * 0.25;
  camera.setDeadzone(deadzoneW, deadzoneH);
}
```

---

## 5. Verification Checklist

- [ ] On tall phones ($19.5:9$), game centers cleanly without black borders clipping UI.
- [ ] Top pause button and score displays sit below the camera cutout/island.
- [ ] Bottom touch buttons sit above the iOS home swipe bar.
