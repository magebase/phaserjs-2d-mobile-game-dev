# Playbook: Store & Production Release Verification

> **Domain:** QA  
> **Capability ID:** `qa.build_store_release_checklist`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides executing the final release checklist across web manifests, mobile store wrapper compatibility (Capacitor, Cordova, Google Play TWA), and production asset caching.

---

## 2. Web App Manifest Audit Checklist

Verify `manifest.json` contains:
```json
{
  "name": "Game Title",
  "short_name": "Game",
  "start_url": "./index.html",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#000000",
  "theme_color": "#000000",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
```

---

## 3. Native Wrapper Compatibility Check

If packaging via Capacitor or Cordova:
1. **Android Hardware Back Button**: Verify pressing Android back button pauses the game instead of closing the app:
   ```javascript
   document.addEventListener('backbutton', () => {
     if (game.scene.isActive('GameScene')) {
       game.scene.pause('GameScene');
       game.scene.launch('PauseMenuScene');
     }
   }, false);
   ```
2. **Prevent Accidental Swipe-Down Refresh**:
   Ensure CSS contains `overscroll-behavior: none` on `body` and `canvas`.

---

## 4. Final Sign-Off Run

Run the unified report evaluator:
```bash
./tools/magebase-game report /path/to/game --output GAME_QUALITY.md
```

Confirm:
- Hard Blockers RB-01 through RB-08 are all marked `PASS`.
- Overall Status is `PASSED`.
- Release Tier is `GOLD`.
