import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene.js';
import { PreloadScene } from './scenes/PreloadScene.js';
import { GameScene } from './scenes/GameScene.js';

export const config = {
  type: Phaser.AUTO,
  width: 390,
  height: 844,
  parent: 'game-container',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  render: {
    pixelArt: true
  },
  scene: [BootScene, PreloadScene, GameScene]
};

export const game = new Phaser.Game(config);
