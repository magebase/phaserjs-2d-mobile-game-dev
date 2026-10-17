# Playbook: GPU Particle Emitters & Animation Blending

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.animation_particles_vfx`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides creating high-performance visual effects (VFX) in Phaser 4: reusable particle emitter pools, impact sparks, squash-and-stretch tween feedback, and clean sprite animation state machines.

---

## 2. Reusable Particle Emitter Pool

Creating and destroying particle managers during gameplay causes JavaScript garbage collection spikes. Instead, create a pooled emitter at scene boot:

```javascript
export class SparkFX {
  constructor(scene) {
    this.emitter = scene.add.particles(0, 0, 'spark_particle', {
      lifespan: { min: 200, max: 400 },
      speed: { min: 80, max: 220 },
      scale: { start: 1.0, end: 0.1 },
      alpha: { start: 1.0, end: 0 },
      blendMode: 'ADD',
      emitting: false
    });
    this.emitter.setDepth(999);
  }

  burst(x, y, count = 12) {
    this.emitter.explode(count, x, y);
  }
}
```

---

## 3. Squash-and-Stretch Tween Mechanics

Squash-and-stretch gives characters visual weight and elasticity:

```javascript
export function playImpactSquash(scene, target) {
  scene.tweens.add({
    targets: target,
    scaleX: target.scaleX * 1.3,
    scaleY: target.scaleY * 0.7,
    duration: 60,
    yoyo: true,
    ease: 'Quad.easeOut',
    onComplete: () => {
      target.setScale(1.0); // Reset exactly
    }
  });
}

export function playJumpStretch(scene, target) {
  scene.tweens.add({
    targets: target,
    scaleX: target.scaleX * 0.8,
    scaleY: target.scaleY * 1.25,
    duration: 80,
    yoyo: true,
    ease: 'Cubic.easeOut'
  });
}
```

---

## 4. Animation Frame Events & Hitbox Synchronization

Never trigger damage on fixed timers when an animation has an attack swing. Bind combat events to exact animation frames:

```javascript
// Register animation with frame event
this.anims.create({
  key: 'player_attack',
  frames: this.anims.generateFrameNumbers('hero', { start: 10, end: 14 }),
  frameRate: 15,
  repeat: 0
});

// Listen for the active hit frame (e.g. frame 12 is peak sword swing)
player.on('animationupdate', (anim, frame) => {
  if (anim.key === 'player_attack' && frame.index === 3) {
    this.triggerMeleeHitbox(player);
  }
});
```

---

## 5. Verification Checklist

- [ ] Particle emitters are initialized once in `create()` and triggered via `.explode()`.
- [ ] No new particle systems are instantiated inside `update()` or collision callbacks.
- [ ] Tweens return scale to baseline $(1.0, 1.0)$ on completion.
