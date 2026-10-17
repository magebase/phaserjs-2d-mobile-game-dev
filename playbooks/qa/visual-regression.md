# Playbook: Visual Regression & Canvas Screenshot Testing

> **Domain:** QA  
> **Capability ID:** `qa.visual_regression`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides configuring automated visual regression testing to capture deterministic canvas screenshots of key game screens and detect unintentional UI shifts, texture blurring, or letterboxing bugs.

---

## 2. Deterministic Canvas Capture Pattern

Canvas animations produce changing pixel buffers on every frame. To capture deterministic golden screenshots:
1. Freeze or pause physics/animations at an exact frame.
2. Seed the random number generator.
3. Compare snapshots using Playwright `toHaveScreenshot()`:

```javascript
// tests/visual.spec.js
import { test, expect } from '@playwright/test';

test('MainMenu visual snapshot aligns with golden image', async ({ page }) => {
  await page.goto('http://localhost:5173?test_seed=42&freeze_frame=true');

  const canvas = page.locator('canvas');
  await expect(canvas).toBeVisible();

  // Wait for initial loader fade to complete
  await page.waitForTimeout(1000);

  // Compare snapshot with 0.2% max pixel tolerance
  await expect(canvas).toHaveScreenshot('main-menu-golden.png', {
    maxDiffPixelRatio: 0.002
  });
});
```

---

## 3. Verification Checklist

- [ ] Golden baseline screenshots are stored in `tests/visual/baselines/`.
- [ ] Visual diffs highlight unintended font rendering or sprite misalignment clearly.
- [ ] Tests pass across multiple runs without false-positive subpixel jitter.
