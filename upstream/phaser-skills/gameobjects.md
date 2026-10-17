# Phaser 4 GameObjects Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Core Visual Game Objects

### 1.1 `Phaser.GameObjects.Sprite`
```javascript
const sprite = this.add.sprite(x, y, 'textureKey', 'frameKey');
sprite.play('walk_animation');
```

### 1.2 `Phaser.GameObjects.Image`
Optimized static visual element (no animation manager attached):
```javascript
const img = this.add.image(x, y, 'textureKey');
img.setOrigin(0.5, 0.5);
img.setScale(2.0);
```

### 1.3 `Phaser.GameObjects.Container`
Groups multiple Game Objects with unified transform hierarchy:
```javascript
const container = this.add.container(x, y, [bgImage, labelText]);
container.setScale(1.2);
```

---

## 2. Phaser 4 Hardware Accelerated GameObjects

### 2.1 `SpriteGPULayer`
Hardware-accelerated batched layer for high-density sprite counts:
```javascript
const layer = this.add.spriteGPULayer('particles_texture', 2000);
const p = layer.create(x, y, 'spark');
```
