# Phaser 4 Loader Reference (Pinned v4.2.1)

> **Source:** Upstream Phaser Skills Reference  
> **Package:** `phaser`

---

## 1. Class: `Phaser.Loader.LoaderPlugin`

Accessed via `this.load` inside `preload()`.

```javascript
// Image
this.load.image('key', 'assets/image.png');

// Spritesheet
this.load.spritesheet('hero', 'assets/hero.png', {
  frameWidth: 32,
  frameHeight: 32,
  margin: 0,
  spacing: 0
});

// Texture Atlas (TexturePacker JSON)
this.load.atlas('characters', 'assets/chars.png', 'assets/chars.json');

// Audio (Multiple formats for browser compatibility)
this.load.audio('bgm', ['assets/music.ogg', 'assets/music.mp3']);

// Tilemaps
this.load.tilemapTiledJSON('level1', 'assets/level1.json');

// Lifecycle events
this.load.on('progress', (val) => console.log(`Loading: ${Math.round(val * 100)}%`));
this.load.on('filecomplete', (key) => console.log(`Loaded: ${key}`));
this.load.on('loaderror', (file) => console.error(`Error loading: ${file.key}`));
```
