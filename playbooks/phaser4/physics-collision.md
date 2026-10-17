# Playbook: Physics & Collision Optimization

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.physics_collision`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides setting up fair, tight, and high-performance 2D collision detection using Phaser Arcade Physics or Matter.js, with fair hitbox offsets and spatial partitioning.

---

## 2. Fair Hitbox Sizing (The "Forgiving Hitbox" Rule)

In mobile games, players get frustrated if they take damage when an enemy grazing a hair pixel hits them. **Visual sprite bounds should always be larger than physical collision bounds**:

```javascript
export function configurePlayerHitbox(player) {
  // Assume visual sprite is 32x32px
  // Set physical collision body to 16x16px centered at the player's feet
  player.body.setSize(16, 16);
  player.body.setOffset(8, 16);
}

export function configureCollectibleHitbox(coin) {
  // For collectibles, make the hitbox LARGER than visual sprite for easy grabbing
  coin.body.setSize(24, 24);
  coin.body.setOffset(-4, -4);
}
```

---

## 3. Collision Groups & Overlaps

Organize entities into distinct groups to minimize pair-wise collision checks:

```javascript
export function setupCollisions(scene, player, enemiesGroup, bulletsGroup, terrainLayer) {
  // 1. Terrain solid collisions
  scene.physics.add.collider(player, terrainLayer);
  scene.physics.add.collider(enemiesGroup, terrainLayer);

  // 2. Projectile hit enemy
  scene.physics.add.overlap(bulletsGroup, enemiesGroup, (bullet, enemy) => {
    bullet.destroy();
    enemy.takeDamage(bullet.damage || 10);
  });

  // 3. Enemy touches player
  scene.physics.add.overlap(player, enemiesGroup, (p, enemy) => {
    p.onHazardContact(enemy);
  });
}
```

---

## 4. Offscreen Entity Culling

Projectiles that fly off into infinity continue to consume CPU physics cycles. Ensure all dynamic entities are recycled or destroyed:

```javascript
// Inside projectile class or update loop:
if (!scene.cameras.main.worldView.contains(this.x, this.y)) {
  this.destroy();
}
```

---

## 5. Verification Checklist

- [ ] Debug collision outlines (`physics.arcade.debug = true`) visually align with character feet and solid walls.
- [ ] Offscreen bullets/particles do not accumulate in `physics.world.bodies.size`.
- [ ] Physics simulation runs at consistent 60 updates per second without jitter.
