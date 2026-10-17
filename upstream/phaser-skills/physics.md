# Phaser 4 Physics Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Arcade Physics Engine

Lightweight AABB (axis-aligned bounding box) physics engine optimized for 2D platformers, top-down shooters, and mobile performance.

```javascript
// Enable physics on existing sprite
this.physics.add.existing(sprite);

// Velocity and acceleration
sprite.body.setVelocity(100, -200);
sprite.body.setBounce(0.2);
sprite.body.setCollideWorldBounds(true);

// Hitbox sizing and offset
sprite.body.setSize(16, 16);
sprite.body.setOffset(8, 16);

// Colliders vs Overlaps
this.physics.add.collider(player, platforms); // Physical solid separation
this.physics.add.overlap(bullets, enemies, onHit); // Trigger callback without bounce
```
