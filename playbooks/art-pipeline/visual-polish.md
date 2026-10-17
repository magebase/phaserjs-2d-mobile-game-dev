# Playbook: Visual Polish, Parallax & Ambient FX

> **Domain:** Art Pipeline  
> **Capability ID:** `art_pipeline.visual_polish`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides adding depth and immersion through multi-layer parallax scrolling, ambient particle effects (dust motes, embers, fireflies), and character drop shadows.

---

## 2. Multi-Layer Parallax Backgrounds

Add visual depth by having distant background layers move slower than the gameplay foreground:

```javascript
export function createParallaxBackground(scene, textureKeys) {
  const { width, height } = scene.scale;
  
  // Layer 1: Distant sky / mountains (near stationary)
  scene.add.tileSprite(0, 0, width, height, textureKeys.sky)
    .setOrigin(0, 0)
    .setScrollFactor(0.05)
    .setDepth(-30);

  // Layer 2: Midground hills
  scene.add.tileSprite(0, 0, width, height, textureKeys.hills)
    .setOrigin(0, 0)
    .setScrollFactor(0.3)
    .setDepth(-20);

  // Layer 3: Near foliage
  scene.add.tileSprite(0, 0, width, height, textureKeys.trees)
    .setOrigin(0, 0)
    .setScrollFactor(0.7)
    .setDepth(-10);
}
```

---

## 3. Ambient Environmental Particles

Gentle ambient particles bring static environments to life with minimal CPU cost:

```javascript
export function createAmbientDust(scene) {
  return scene.add.particles(0, 0, 'dust_particle', {
    x: { min: 0, max: scene.scale.width },
    y: { min: 0, max: scene.scale.height },
    lifespan: 4000,
    speedX: { min: -10, max: 10 },
    speedY: { min: -20, max: -5 },
    scale: { start: 0.3, end: 0.8 },
    alpha: { start: 0, end: 0.4 },
    blendMode: 'ADD',
    frequency: 300
  }).setScrollFactor(0.5).setDepth(50);
}
```

---

## 4. Ground Contact Drop Shadows

Sprites appear floating if they lack ground contact shadows. Add a subtle scaled ellipse beneath the character:

```javascript
export function attachDropShadow(scene, character) {
  const shadow = scene.add.ellipse(character.x, character.y + 14, 18, 8, 0x000000, 0.3)
    .setDepth(character.depth - 1);

  // In update(): sync shadow position with character
  character.on('destroy', () => shadow.destroy());
  return shadow;
}
```

---

## 5. Verification Checklist

- [ ] Parallax scrolling layers do not exhibit seam tearing or stutter.
- [ ] Ambient particles do not exceed 50 active particles concurrently.
- [ ] Drop shadows scale realistically when characters jump or take damage.
