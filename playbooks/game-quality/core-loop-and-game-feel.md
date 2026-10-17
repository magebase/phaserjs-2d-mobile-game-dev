# Playbook: Core Gameplay Loop Pacing & Game Feel "Juice"

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.core_loop_and_game_feel`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-03 (Broken Core Gameplay Loop)

---

## 1. Purpose & Scope

This playbook guides designing and verifying a tight, satisfying core loop and injecting tactile game feel ("juice") into player interactions: screen shake, hit freezes (freeze-frames), damage flash tints, and floating combat text.

---

## 2. The Complete Mobile Core Loop Blueprint

Every mobile game session must complete a coherent feedback cycle:

```
[Start Session] ──► [30–60s Tactical Action] ──► [Milestone / Reward]
        ▲                                                │
        │                                                ▼
[Restart / Continue] ◄── [Score / Victory / Defeat] ◄───┘
```

**Verification Rule (RB-03)**:
- From clean boot, player can start gameplay without keyboard shortcuts.
- Reaching zero health triggers `GameOverScene` cleanly.
- Tapping "Play Again" restarts the game loop without state pollution.

---

## 3. The "Juice" Feedback Suite

### 3.1 Camera Screen Shake with Decay
```javascript
export function triggerScreenShake(camera, intensity = 0.015, duration = 120) {
  camera.shake(duration, intensity);
}
```

### 3.2 Hit Freeze (Freeze-Frame Impact)
Pausing game physics/movement for 2–3 frames ($30–50\text{ms}$) on a heavy impact gives attacks physical weight:

```javascript
export function triggerHitPause(scene, durationMs = 45) {
  scene.physics.world.pause();
  scene.time.delayedCall(durationMs, () => {
    scene.physics.world.resume();
  });
}
```

### 3.3 Damage Flash Tint
Flash the target entity solid white for $60\text{ms}$ when hit:
```javascript
export function flashDamage(scene, sprite, duration = 60) {
  sprite.setTintFill(0xffffff);
  scene.time.delayedCall(duration, () => {
    sprite.clearTint();
  });
}
```

### 3.4 Floating Combat Text
```javascript
export function spawnFloatingText(scene, x, y, text, color = '#ffdd00') {
  const label = scene.add.text(x, y - 10, text, {
    fontSize: '16px',
    fontStyle: 'bold',
    color: color,
    stroke: '#000000',
    strokeThickness: 3
  }).setOrigin(0.5).setDepth(2000);

  scene.tweens.add({
    targets: label,
    y: y - 45,
    alpha: 0,
    duration: 650,
    ease: 'Cubic.easeOut',
    onComplete: () => label.destroy()
  });
}
```

---

## 4. Verification Checklist

- [ ] Every attack or hit produces at least 3 synchronous feedback cues (flash + sound + floating text or shake).
- [ ] Dying cleanly transitions to game over and allows restarting within 1 tap.
- [ ] No state leaks into the restarted run (scores, HP, enemies reset completely).
