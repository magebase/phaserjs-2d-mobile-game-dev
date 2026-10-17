# Playbook: FPS & Memory Performance Profiling

> **Domain:** QA  
> **Capability ID:** `qa.performance_budget`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-08 (Critical FPS Degradation)

---

## 1. Purpose & Scope

This playbook defines quantitative performance budgets for mobile 2D games and provides verification procedures to enforce frame rate stability, bundle size limits, and memory leak prevention.

---

## 2. Mobile Performance Budget Table

| Metric | Target Budget | Hard Block Ceiling | Measurement Tool |
| :--- | :--- | :--- | :--- |
| **Median Frame Rate** | $\ge 58$ FPS | $< 30$ FPS (**RB-08**) | In-engine delta timer / Chrome DevTools |
| **Initial Bundle Size** | $\le 5\text{MB}$ | $> 15\text{MB}$ | Bundler build stats / `du -sh dist` |
| **JavaScript Heap Memory**| $\le 64\text{MB}$ | $> 128\text{MB}$ | `performance.memory.usedJSHeapSize` |
| **WebGL Draw Calls** | $\le 15$ calls | $> 50$ calls | WebGL Spector / in-engine inspector |
| **Boot to Interactive** | $\le 2.0\text{s}$ | $> 6.0\text{s}$ | Lighthouse mobile 4G throttle |

---

## 3. In-Game Performance Monitor

Embed a lightweight performance tracker during dev and automated runs:

```javascript
export class PerformanceProfiler {
  constructor(game) {
    this.game = game;
    this.frameDeltas = [];
    this.maxFrames = 120;
  }

  recordFrame(delta) {
    this.frameDeltas.push(delta);
    if (this.frameDeltas.length > this.maxFrames) {
      this.frameDeltas.shift();
    }
  }

  getMetrics() {
    const avgDelta = this.frameDeltas.reduce((a, b) => a + b, 0) / this.frameDeltas.length;
    const currentFps = 1000 / avgDelta;
    const memoryMb = window.performance?.memory
      ? Math.round(window.performance.memory.usedJSHeapSize / (1024 * 1024))
      : 0;

    return {
      fps: Math.round(currentFps),
      avgDeltaMs: Math.round(avgDelta * 10) / 10,
      memoryMb
    };
  }
}
```

---

## 4. Verification Checklist

- [ ] Automated profiling run over 60 seconds records median FPS $\ge 58$ FPS.
- [ ] No single frame delta exceeds $33.3\text{ms}$ during normal gameplay.
- [ ] Total distribution size (`/dist`) is within the declared bundle budget.
