import Phaser from 'phaser';

export class GameScene extends Phaser.Scene {
  constructor() {
    super({ key: 'GameScene' });
  }

  create() {
    const { width, height } = this.scale;
    this.add.text(width / 2, 40, 'MINIMAL PHASER 4 MOBILE GAME', {
      fontSize: '18px',
      color: '#00ff88'
    }).setOrigin(0.5);

    this.player = this.add.image(width / 2, height / 2, 'player').setScale(2);

    // Simple touch control
    this.input.on('pointerdown', (pointer) => {
      this.tweens.add({
        targets: this.player,
        x: pointer.x,
        y: pointer.y,
        duration: 300,
        ease: 'Power2'
      });
    });
  }
}
