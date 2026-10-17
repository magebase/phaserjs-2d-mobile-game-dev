# Playbook: Mobile Audio Unlock & Sound Feedback

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.audio_feedback`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides resolving mobile Web Audio context restrictions (iOS Safari / Android Chrome silent lockups), implementing polyphony limiting, volume channels, and background tab pausing.

---

## 2. Guaranteed Mobile Web Audio Unlock

Mobile browsers suspend the `AudioContext` until a hardware touch gesture occurs.

### "Tap to Play" Unlock Overlay:
```javascript
export function ensureAudioUnlocked(scene, onUnlocked) {
  if (scene.sound.locked) {
    const { width, height } = scene.scale;
    const overlay = scene.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.7)
      .setInteractive()
      .setDepth(9999);

    const prompt = scene.add.text(width / 2, height / 2, 'TAP TO START', {
      fontSize: '24px',
      color: '#00ff88',
      fontStyle: 'bold'
    }).setOrigin(0.5).setDepth(10000);

    overlay.once('pointerdown', () => {
      scene.sound.unlock();
      overlay.destroy();
      prompt.destroy();
      onUnlocked();
    });
  } else {
    onUnlocked();
  }
}
```

---

## 3. Polyphony Limiting (Harsh Audio Clipping Elimination)

If a bomb hits 20 enemies simultaneously, playing 20 explosion sounds at once causes harsh digital distortion and clipping.

### Cooldown Limiter:
```javascript
export class SoundManager {
  constructor(scene) {
    this.scene = scene;
    this.lastPlayed = new Map();
    this.cooldownMs = 60; // Max 1 instance per 60ms
  }

  playSFX(key, volume = 1.0) {
    const now = Date.now();
    const last = this.lastPlayed.get(key) || 0;
    if (now - last < this.cooldownMs) {
      return; // Skip overlapping sound
    }
    this.lastPlayed.set(key, now);

    if (this.scene.registry.get('soundEnabled') !== false) {
      this.scene.sound.play(key, { volume });
    }
  }
}
```

---

## 4. Background Tab Auto-Mute

When a player minimizes the browser or switches tabs, audio must pause:

```javascript
export function setupTabVisibilityMuting(game) {
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      game.sound.mute = true;
    } else {
      game.sound.mute = game.registry.get('soundEnabled') === false;
    }
  });
}
```

---

## 5. Verification Checklist

- [ ] Audio plays reliably on first tap on physical iOS Safari.
- [ ] Swapping browser tabs immediately mutes audio output.
- [ ] Mass enemy collisions do not cause audio distortion or clipping.
