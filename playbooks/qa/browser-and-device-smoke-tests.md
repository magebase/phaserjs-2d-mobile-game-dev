# Playbook: Mobile Viewport & Browser Console Smoke Tests

> **Domain:** QA  
> **Capability ID:** `qa.browser_and_device_smoke_tests`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blockers:** RB-02 (Unhandled Exceptions), RB-04 (Touch Controls)

---

## 1. Purpose & Scope

This playbook guides executing automated browser smoke tests using Playwright to emulate mobile devices (iPhone 14, Pixel 7), capture browser console errors during clean boot, and verify touch interactions.

---

## 2. Automated Mobile Smoke Test Script (Playwright)

```javascript
// tests/e2e/smoke.spec.js
import { test, expect, devices } from '@playwright/test';

const targetDevices = [
  devices['iPhone 14'],
  devices['Pixel 7']
];

for (const device of targetDevices) {
  test(`Clean boot & zero console errors on ${device.name}`, async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    page.on('pageerror', err => {
      consoleErrors.push(err.message);
    });

    await page.goto('http://localhost:5173');

    // 1. Wait for canvas element to mount
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible({ timeout: 5000 });

    // 2. Allow game loop to cycle through Boot -> Preload -> MainMenu (2 seconds)
    await page.waitForTimeout(2000);

    // 3. Emulate touch tap to dismiss start overlay or tap play
    await page.touchscreen.tap(device.viewport.width / 2, device.viewport.height / 2);

    // 4. Assert zero unhandled console exceptions (RB-02)
    expect(consoleErrors).toEqual([]);
  });
}
```

---

## 3. Verification Checklist

- [ ] Game boots cleanly to MainMenu without throwing console errors on mobile viewports.
- [ ] Touch gestures correctly trigger menu buttons and movement.
- [ ] Canvas scales responsively to the device viewport without horizontal scrollbars.
