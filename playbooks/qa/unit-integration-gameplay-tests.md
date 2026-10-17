# Playbook: Headless Unit & Integration Gameplay Tests

> **Domain:** QA  
> **Capability ID:** `qa.unit_integration_gameplay_tests`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blockers:** RB-01 (Build Failure), RB-03 (Core Loop)

---

## 1. Purpose & Scope

This playbook guides writing and running fast, headless unit and integration tests for Phaser 4 game logic using Vitest or Jest. It verifies scene transitions, player movement math, damage systems, and state persistence without requiring a physical screen.

---

## 2. Test Configuration Setup (Vitest Example)

In `vitest.config.js`:
```javascript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['tests/**/*.test.js']
  }
});
```

---

## 3. Integration Gameplay Test Blueprint

```javascript
// tests/gameplay.test.js
import { describe, it, expect, beforeEach } from 'vitest';
import { SaveStateManager } from '../src/managers/SaveStateManager.js';
import { getXpRequiredForLevel } from '../src/utils/progression.js';

describe('Player Progression Logic', () => {
  it('calculates correct non-linear XP thresholds', () => {
    expect(getXpRequiredForLevel(1)).toBe(100);
    expect(getXpRequiredForLevel(2)).toBeGreaterThan(200);
    expect(getXpRequiredForLevel(5)).toBe(1118);
  });
});

describe('Save State Manager', () => {
  let saveManager;

  beforeEach(() => {
    localStorage.clear();
    saveManager = new SaveStateManager(null);
  });

  it('persists score mutations locally', () => {
    saveManager.saveLocal({ coins: 50, level: 2 });
    const loaded = saveManager.getLocalState();
    expect(loaded.coins).toBe(50);
    expect(loaded.level).toBe(2);
  });
});
```

---

## 4. Verification Checklist

- [ ] `npm test` runs cleanly and exits with code 0.
- [ ] Tests verify genuine business logic and state mutations (no empty placeholder tests).
- [ ] Tests execute in $< 5\text{s}$ locally.
