# Playbook: Progressive Asset Loader & Scene Transitions

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.loading_and_scene_transitions`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blockers:** RB-02 (Runtime Exceptions), RB-05 (Missing Assets)

---

## 1. Purpose & Scope

This playbook guides creating a robust, fail-safe asset loading sequence that prevents white-screen crashes on 404s, renders smooth mobile loading indicators, and manages camera crossfade transitions between scenes.

---

## 2. Fail-Safe Asset Loading Pattern

Network interruptions on mobile connections frequently cause asset downloads to fail. An unhandled load failure must **never crash the game boot**.

```javascript
export class SafePreloader extends Phaser.Scene {
  constructor() {
    super({ key: 'PreloadScene' });
  }

  preload() {
    // 1. Setup fallback texture generator
    this.createPlaceholderTextures();

    // 2. Intercept load errors to prevent hard crash
    this.load.on('loaderror', (file) => {
      console.warn(`[SafePreloader] Failed to load ${file.key} from ${file.url}. Using procedural placeholder.`);
      // Re-map key to fallback texture so game scenes don't crash
      if (!this.textures.exists(file.key)) {
        this.textures.addBase64(file.key, this.textures.getBase64('fallback_placeholder'));
      }
    });

    // 3. Queue assets
    this.load.image('player', 'assets/player.png');
    this.load.image('tiles', 'assets/tileset.png');
  }

  createPlaceholderTextures() {
    // Procedural 16x16 checkerboard for missing textures
    const graphics = this.make.graphics({ x: 0, y: 0, add: false });
    graphics.fillStyle(0xff00ff).fillRect(0, 0, 8, 8);
    graphics.fillStyle(0x000000).fillRect(8, 0, 8, 8);
    graphics.fillStyle(0x000000).fillRect(0, 8, 8, 8);
    graphics.fillStyle(0xff00ff).fillRect(8, 8, 8, 8);
    graphics.generateTexture('fallback_placeholder', 16, 16);
    graphics.destroy();
  }

  create() {
    this.scene.start('MainMenuScene');
  }
}
```

---

## 3. Polished Scene Crossfades

Avoid jarring instant scene cuts. Implement smooth camera fades:

```javascript
export function transitionToScene(currentScene, nextSceneKey, duration = 300) {
  currentScene.cameras.main.fadeOut(duration, 0, 0, 0);

  currentScene.cameras.main.once(Phaser.Cameras.Scene2D.Events.FADE_OUT_COMPLETE, () => {
    currentScene.scene.start(nextSceneKey);
  });
}

// In the destination scene's create():
export function setupFadeIn(scene, duration = 300) {
  scene.cameras.main.fadeIn(duration, 0, 0, 0);
}
```

---

## 4. Verification Checklist

- [ ] Simulating a 404 for an image does not throw an uncaught runtime exception; the game boots to main menu with the procedural placeholder.
- [ ] Crossfades between scenes are smooth with zero white flashes.
- [ ] Loading progress bar tracks from 0% to 100% proportionally.
