# Playbook: RenderNodes, Filters & 2D Dynamic Lighting

> **Domain:** Phaser 4  
> **Capability ID:** `phaser4.rendering_filters_lighting`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides leveraging Phaser 4's modernized rendering pipeline: **RenderNodes**, hardware-accelerated post-processing filters, and 2D dynamic point lighting with normal maps on mobile devices.

---

## 2. Phaser 4 RenderNode Architecture

Phaser 4 replaces monolithic WebGL pipelines with modular **RenderNodes**. RenderNodes handle draw call batching and custom shader passes.

### Custom Glow / Color Shift RenderNode:
```javascript
const FragmentShader = `
precision mediump float;
uniform sampler2D uMainSampler;
varying vec2 outTexCoord;
uniform float uTime;

void main(void) {
  vec4 color = texture2D(uMainSampler, outTexCoord);
  // Add subtle pulse glow to highlighted entities
  color.rgb += vec3(0.1, 0.2, 0.1) * sin(uTime * 3.0);
  gl_FragColor = color;
}
`;

export function registerGlowNode(renderer) {
  if (!renderer.nodes) return;
  
  renderer.nodes.add('GlowNode', {
    fragmentShader: FragmentShader,
    uniforms: {
      uTime: { type: '1f', value: 0 }
    }
  });
}
```

---

## 3. PostFX Filters on Mobile

Full-screen mobile post-processing must be budget-aware. Limit post-processing passes to a single combined filter to avoid rendering multiple full-screen render textures.

### Ambient Vignette Filter:
```javascript
// In GameScene.create():
const camera = this.cameras.main;
if (camera.postFX) {
  const vignette = camera.postFX.addVignette(0.5, 0.5, 0.7, 0.4);
}
```

---

## 4. 2D Dynamic Point Lights with Normal Maps

Phaser 4 includes built-in 2D lighting:

```javascript
// 1. Enable lighting in scene
this.lights.enable();
this.lights.setAmbientColor(0x333344);

// 2. Add player torch / point light
const playerLight = this.lights.addLight(player.x, player.y, 180).setColor(0xffaa55).setIntensity(2.0);

// In update(): sync light position with player
playerLight.setPosition(player.x, player.y);

// 3. Mark sprites to receive dynamic lighting
player.setPipeline('Light2D');
enemies.getChildren().forEach(e => e.setPipeline('Light2D'));
```

> **Mobile Budget Warning**: Mobile GPUs (Mali, Adreno, Apple GPU) struggle when more than 8 dynamic lights intersect the same tile. Keep active lights $\le 6$ within the active camera view frustum.

---

## 5. Verification Checklist

- [ ] WebGL context loss is handled cleanly without memory leak.
- [ ] PostFX filters do not cause FPS drops below 60 FPS on baseline target.
- [ ] RenderNodes properly update uniforms without allocating memory in `update()`.
