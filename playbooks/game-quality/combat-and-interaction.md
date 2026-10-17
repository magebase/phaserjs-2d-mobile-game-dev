# Playbook: Tactile Combat & Interaction Mechanics

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.combat_and_interaction`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides implementing responsive, tactile 2D combat: attack telegraphing, knockback momentum, invulnerability frames (i-frames), and critical hit calculations.

---

## 2. Attack Telegraphing & Windup

In mobile action games, fair combat requires visible telegraphing so players have time to react or dodge:

```javascript
export function telegraphEnemyAttack(scene, enemy, onStrike) {
  // 1. Telegraph phase (windup flash)
  scene.tweens.add({
    targets: enemy,
    tint: 0xff3333,
    scaleX: enemy.scaleX * 1.15,
    duration: 350,
    yoyo: true,
    ease: 'Quad.easeInOut',
    onComplete: () => {
      enemy.clearTint();
      // 2. Strike phase
      onStrike();
    }
  });
}
```

---

## 3. Recoil Knockback Vector

When a projectile or melee weapon connects, knock the recipient back along the impact vector:

```javascript
export function applyKnockback(target, sourceX, sourceY, force = 250) {
  const angle = Phaser.Math.Angle.Between(sourceX, sourceY, target.x, target.y);
  target.setVelocity(Math.cos(angle) * force, Math.sin(angle) * force);
  
  // Re-enable normal AI navigation after brief stun
  target.scene.time.delayedCall(150, () => {
    if (target.active) {
      target.isStunned = false;
    }
  });
}
```

---

## 4. Invulnerability Frames (i-Frames)

Prevent players from suffering rapid multi-tick instant deaths:

```javascript
export function grantInvulnerability(scene, player, durationMs = 1000) {
  player.isInvulnerable = true;

  // Visual flicker
  const flashTween = scene.tweens.add({
    targets: player,
    alpha: 0.3,
    duration: 100,
    yoyo: true,
    repeat: Math.floor(durationMs / 200),
    onComplete: () => {
      player.setAlpha(1.0);
      player.isInvulnerable = false;
    }
  });
}
```

---

## 5. Verification Checklist

- [ ] Taking damage grants at least $800\text{ms}$ of i-frames with clear alpha flickering.
- [ ] Knockback pushes entities away from the damage source without clipping through solid tiles.
- [ ] Enemy attacks display visible visual or audio telegraphing before dealing damage.
