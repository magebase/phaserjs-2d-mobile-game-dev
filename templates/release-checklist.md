# Release Checklist — Mobile 2D Game Release Gate

> **Phaser 4 Mobile Release Gate Checklist**

---

## 1. Technical Hard Gates (RB-01 through RB-08)
- [ ] **RB-01**: Clean production build with zero warnings/errors (`npm run build`).
- [ ] **RB-02**: Clean boot in headless browser; zero uncaught exceptions in console.
- [ ] **RB-03**: Core loop verified end-to-end (start $\to$ gameplay $\to$ victory/defeat $\to$ restart).
- [ ] **RB-04**: Touch controls functional; hitboxes $\ge 44\times 44\text{px}$; safe area notch respected.
- [ ] **RB-05**: Zero asset 404s in network tab and loader queue.
- [ ] **RB-06**: Progress persists across hard browser refresh and tab close.
- [ ] **RB-07**: Zero leaked secrets, internal URLs, or private tokens in `/dist`.
- [ ] **RB-08**: Stable $\ge 30$ FPS (target 60 FPS) on baseline test device.

---

## 2. Mobile Web & PWA Compliance
- [ ] `manifest.json` configured:
  - `name`, `short_name`, `theme_color`, `background_color`.
  - `display: "standalone"`, `orientation: "portrait"` (or `"landscape"`).
  - High-res PNG icons: $192\times 192$, $512\times 512$, and maskable icons.
- [ ] Apple touch icon declared: `<link rel="apple-touch-icon" href="...">`.
- [ ] Viewport meta tag locked: `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">`.
- [ ] Service worker registered for offline asset caching (if offline play enabled).

---

## 3. Audio & Interaction Polling
- [ ] Audio unlocks gracefully on first user touch gesture without latency.
- [ ] Music loops smoothly without stutter or audible pop.
- [ ] Sound mute toggle accessible from in-game settings.
- [ ] Browser backgrounding (tab hidden) automatically mutes or pauses audio context.

---

## 4. Native Wrapper Packaging (Capacitor / Cordova / TWA)
- [ ] Splash screen transitions smoothly to game canvas without white flash.
- [ ] Hardware back-button on Android navigates to pause menu instead of exiting app.
- [ ] Status bar style set to light/dark/transparent matching game palette.
- [ ] App permissions minimized (only network/storage if strictly needed).
