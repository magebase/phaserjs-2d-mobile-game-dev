import Phaser from 'phaser';

export class PreloadScene extends Phaser.Scene {
  constructor() {
    super({ key: 'PreloadScene' });
  }

  preload() {
    this.load.image('player', 'assets/player.png');
    this.load.image('tileset', 'assets/tileset.png');
  }

  create() {
    this.scene.start('GameScene');
  }
}
