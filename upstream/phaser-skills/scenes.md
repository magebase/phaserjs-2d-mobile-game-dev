# Phaser 4 Scene Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Class: `Phaser.Scene`

Every Phaser scene inherits from `Phaser.Scene` and registers with a unique string key.

```javascript
export class MyScene extends Phaser.Scene {
  constructor(config = { key: 'MyScene' }) {
    super(config);
  }

  init(data) {
    // Called when the scene starts, receives transition parameters
    this.customParam = data.param || 0;
  }

  preload() {
    // Queue asset downloads
    this.load.image('logo', 'assets/logo.png');
  }

  create(data) {
    // Initialize Game Objects, tweens, physics, and input
    this.add.image(100, 100, 'logo');
  }

  update(time, delta) {
    // Called every animation frame (approx. 60 FPS)
    // time: current runtime in ms; delta: elapsed time since last frame in ms
  }
}
```

---

## 2. Key Scene Systems

- `this.add`: `Phaser.GameObjects.GameObjectFactory`
- `this.make`: `Phaser.GameObjects.GameObjectCreator`
- `this.cameras`: `Phaser.Cameras.Scene2D.CameraManager`
- `this.input`: `Phaser.Input.InputPlugin`
- `this.load`: `Phaser.Loader.LoaderPlugin`
- `this.physics`: `Phaser.Physics.Arcade.ArcadePhysics`
- `this.scale`: `Phaser.Scale.ScaleManager`
- `this.sound`: `Phaser.Sound.BaseSoundManager`
- `this.time`: `Phaser.Time.Clock`
- `this.tweens`: `Phaser.Tweens.TweenManager`
