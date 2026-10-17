# Playbook: Player Progression & Balancing Curves

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.progression_and_balance`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides structuring mathematical progression curves, level-up card drafting, stat growth, and enemy scaling without arbitrary hardcoded magic numbers.

---

## 2. Mathematical Progression Formulas

### 2.1 Exponential XP Curve
```javascript
export function getXpRequiredForLevel(level) {
  // Level 1: 100 XP, Level 5: ~1,118 XP, Level 10: ~3,162 XP
  return Math.floor(100 * Math.pow(level, 1.5));
}
```

### 2.2 Enemy Stat Scaling by Wave/Minutes
```javascript
export function getScaledEnemyStats(baseStats, elapsedMinutes) {
  const scale = 1.0 + (elapsedMinutes * 0.15); // +15% per minute
  return {
    hp: Math.floor(baseStats.hp * scale),
    damage: Math.floor(baseStats.damage * (1.0 + elapsedMinutes * 0.1)),
    speed: Math.min(baseStats.speed * 1.3, baseStats.speed * (1.0 + elapsedMinutes * 0.05))
  };
}
```

---

## 3. Roguelike 3-Card Upgrade Selection Pattern

When the player levels up, pause gameplay and present 3 randomized non-duplicate upgrades:

```javascript
export function presentLevelUpDraft(scene, upgradePool, onSelect) {
  scene.scene.pause('GameScene');
  scene.scene.launch('UpgradeDraftScene', {
    options: Phaser.Utils.Array.Shuffle([...upgradePool]).slice(0, 3),
    onChoose: (choice) => {
      onSelect(choice);
      scene.scene.stop('UpgradeDraftScene');
      scene.scene.resume('GameScene');
    }
  });
}
```

---

## 4. Verification Checklist

- [ ] XP values never cause integer overflow or negative requirements.
- [ ] Upgrade drafting pauses physics and input in `GameScene` without breaking camera coordinates.
- [ ] Level-up stats persist cleanly across scene transitions.
