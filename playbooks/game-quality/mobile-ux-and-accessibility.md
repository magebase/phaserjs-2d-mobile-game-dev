# Playbook: Mobile UX, Thumb Zones & Accessibility

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.mobile_ux_and_accessibility`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-04 (Unplayable Touch Controls)

---

## 1. Purpose & Scope

This playbook guides designing mobile-first UI layouts that respect biological thumb zones, guarantee $\ge 44\text{px}$ touch targets, enforce high-contrast typography, and implement an accessible pause menu.

---

## 2. Thumb Zone Mapping (One-Handed & Two-Thumb Play)

Mobile phone screens are divided into three physical reach zones:

```
┌──────────────────────────┐
│   HARD-TO-REACH ZONE     │ ◄── Passive stats: HP bar, Score, Pause button
│   (Top 30% of screen)    │
├──────────────────────────┤
│      STRETCH ZONE        │ ◄── World action & dialogue prompts
│   (Middle 30% of screen) │
├──────────────────────────┤
│      NATURAL ZONE        │ ◄── Interactive controls: Virtual stick, Attack,
│   (Bottom 40% of screen) │     Jump, Skill buttons
└──────────────────────────┘
```

**Rule**: Never place high-frequency combat or movement buttons in the top 30% of the screen.

---

## 3. High-Contrast Accessible Typography

Low-contrast text on mobile screens is unreadable in outdoor sunlight:

```javascript
export function createAccessibleLabel(scene, x, y, text, options = {}) {
  const fontSize = options.fontSize || '16px';
  const color = options.color || '#ffffff';
  
  return scene.add.text(x, y, text, {
    fontFamily: 'system-ui, -apple-system, sans-serif',
    fontSize: fontSize,
    fontStyle: 'bold',
    color: color,
    stroke: '#000000',
    strokeThickness: 4, // Guaranteed contrast outline
    shadow: {
      offsetX: 1,
      offsetY: 2,
      color: '#000000',
      blur: 2,
      fill: true
    }
  });
}
```

---

## 4. Modal Pause Menu Pattern

Tapping the pause button must reliably pause gameplay without losing touch coordinates:

```javascript
export function openPauseMenu(scene) {
  scene.scene.pause('GameScene');
  scene.scene.launch('PauseMenuScene');
}
```

In `PauseMenuScene`:
- Render semi-transparent dark backdrop (`fillStyle(0x000000, 0.7)`).
- Provide "Resume", "Restart", and "Mute Sound" buttons with large touch targets.

---

## 5. Verification Checklist

- [ ] Interactive touch targets are measured at $\ge 44\times 44\text{px}$.
- [ ] Text maintains a minimum 4.5:1 contrast ratio against the background.
- [ ] Pausing freezes all entities and timers, and resuming restores them cleanly.
