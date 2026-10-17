# Playbook: Phaser 4 Scene Architecture & Lifecycle

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.architecture_scenes`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-02 (Unhandled Runtime Exceptions)

---

## 1. Purpose & Scope

This playbook guides structuring a Phaser 4 mobile game into modular, decoupled scenes with proper initialization, clean state transitions, and memory-safe teardowns.

---

## 2. Standard Mobile Scene Hierarchy

A production-ready mobile game must separate lifecycle and rendering concerns into distinct scenes:

```
[BootScene]
    │ (Initializes scale mode, orientation listener, device detection)
    ▼
[PreloadScene]
    │ (Loads asset bundles, shows progress bar, prepares audio context)
    ▼
[MainMenuScene]
    │ (Title screen, settings, high score display)
    ▼
[GameScene] ◄──► [UIScene / HUD] (Runs concurrently in parallel)
    │
    ▼
[GameOverScene] (or PauseScene modal overlay)
```

---

## 3. Implementation Blueprint

### 3.1 BootScene (Initialization & Scaling)
```javascript
import Phaser from 'phaser';

export class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: 'BootScene' });
  }

  create() {
    // Lock or adapt to mobile scale
    this.scale.refresh();
    
    // Global game state defaults in registry
    this.registry.set('highScore', localStorage.getItem('game_high_score') || 0);
    this.registry.set('soundEnabled', localStorage.getItem('game_sound') !== 'false');

    this.scene.start('PreloadScene');
  }
}
```

### 3.2 PreloadScene (Visual Progress & Resilient Loader)
```javascript
export class PreloadScene extends Phaser.Scene {
  constructor() {
    super({ key: 'PreloadScene' });
  }

  preload() {
    const { width, height } = this.scale;
    const progressBox = this.add.graphics();
    const progressBar = this.add.graphics();
    progressBox.fillStyle(0x222222, 0.8).fillRect(width / 2 - 160, height / 2 - 15, 320, 30);

    this.load.on('progress', (value) => {
      progressBar.clear();
      progressBar.fillStyle(0x00ff88, 1);
      progressBar.fillRect(width / 2 - 155, height / 2 - 10, 310 * value, 20);
    });

    this.load.on('complete', () => {
      progressBar.destroy();
      progressBox.destroy();
    });

    // Load actual game assets
    this.load.image('player', 'assets/player.png');
    this.load.spritesheet('enemies', 'assets/enemies.png', { frameWidth: 16, frameHeight: 16 });
  }

  create() {
    this.scene.start('MainMenuScene');
  }
}
```

### 3.3 Parallel HUD Pattern
Launch the UI overlay scene on top of the gameplay scene so UI elements don't scroll with the game camera:
```javascript
// Inside GameScene.create():
this.scene.launch('UIScene');
```

---

## 4. Teardown & Memory Leak Prevention

In mobile browsers, scenes that do not unbind event listeners create memory leaks that crash the browser tab after prolonged play.

**Always unbind listeners in `SHUTDOWN`**:
```javascript
create() {
  const onScoreUpdate = (score) => this.updateScoreDisplay(score);
  this.game.events.on('score_changed', onScoreUpdate);

  // Clean shutdown
  this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
    this.game.events.off('score_changed', onScoreUpdate);
    this.time.removeAllEvents();
    this.tweens.killAll();
  });
}
```

---

## 5. Verification Checklist

- [ ] All scenes use `super({ key: 'SceneName' })`.
- [ ] No game state is stored in global variables; use `this.registry`.
- [ ] `SHUTDOWN` event unregisters event listeners and clears active timers.
- [ ] Switching between scenes 20 times produces stable memory in Chrome DevTools Memory tab.
