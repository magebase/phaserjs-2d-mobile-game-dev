# GAME_QUALITY_CONTRACT.md — Quality Definition of Done & Release Gates

> **Authoritative Specification:** `magebase/phaserjs-2d-mobile-game-dev`  
> **Status:** Active Release Contract

This document defines the strict, non-negotiable quality contract that every Phaser 4 mobile game must satisfy before it can be qualified as **Release-Ready**.

The contract operates on two distinct layers:
1. **The 8 Hard Release Blockers**: Absolute binary pass/fail criteria. If even one blocker fails, the build is disqualified.
2. **The 8 Dimensional Quality Scores**: Qualitative and quantitative ratings on a 1–10 scale.

---

## 1. The 8 Hard Release Blockers (Binary Gates)

A game is immediately marked **RELEASE BLOCKED** if any of the following conditions are present:

| ID | Blocker Name | Failure Condition | Verification Method |
| :--- | :--- | :--- | :--- |
| **RB-01** | **Build & Compilation Failure** | Bundler/build command (`npm run build`, `vite build`, etc.) exits with non-zero code or TypeScript compiler emits blocking errors. | Run automated build check in clean environment. |
| **RB-02** | **Unhandled Runtime Exceptions** | Uncaught `Error` or unhandled promise rejection occurs during scene lifecycle (`Boot`, `Preload`, `MainMenu`, or `GameScene` clean start). | Headless browser console log audit (`error` event listener). |
| **RB-03** | **Broken Core Gameplay Loop** | Core loop fails to start, progress through active gameplay, or reach a valid end state (win, loss, score screen, retry). | Automated gameplay test or deterministic bot run through one full loop. |
| **RB-04** | **Unplayable Touch Controls** | Key game actions cannot be triggered via single-finger touch or multitouch; interactive UI touch targets are smaller than $44\times 44\text{px}$ or off-screen. | Automated viewport touch event emulation on $390\times 844\text{px}$ and $412\times 915\text{px}$. |
| **RB-05** | **Missing Asset 404s** | Any visual texture, spritesheet frame, audio file, or bitmap font referenced in code fails to load or emits a loader warning. | Asset audit scan matching scene `this.load.*` calls with physical files. |
| **RB-06** | **Save / Progress Data Loss** | Reloading or killing the browser session causes player state or progression to silently reset without intentional local/remote persistence. | Save-state test: write state, reload scene, assert restored state. |
| **RB-07** | **Leaked Secrets in Bundle** | Client distribution bundle contains private API keys, Cloudflare admin tokens, database credentials, or sensitive secrets. | Secret scanner regex grep over `/dist` or `/public` output. |
| **RB-08** | **Critical FPS Degradation** | Median frame rate drops below 30 FPS for $\ge 3$ consecutive seconds during normal gameplay on the baseline tier device profile. | Performance profile runner measuring frame delta times over 60 seconds. |

---

## 2. The 8 Dimensional Quality Scores (1–10 Scale)

In addition to clearing all 8 Hard Blockers, games are evaluated across 8 dimensions. Each dimension is scored from 1 (broken/absent) to 10 (exceptional/mastery).

```
Score Tiers:
  1–3: Critical deficiencies / Unplayable
  4–6: Functional prototype / Needs significant polish
  7–8: Solid commercial release candidate
  9–10: Exemplary market-leading execution
```

### Dimension 1: Fun & Core Loop (Target: $\ge 7$)
- **1–3**: Confusing objectives; no clear failure or victory condition; player has no agency or engagement.
- **4–6**: Core loop functions, but pacing drags or mechanics feel repetitive without meaningful reward loops.
- **7–8**: Clear pacing, satisfying micro-rewards, clear goals, escalating challenge curve that respects player skill.
- **9–10**: Deeply compelling flow state, multiple tactical decisions, emergent gameplay, high replayability.

### Dimension 2: Mobile Usability & Ergonomics (Target: $\ge 8$)
- **1–3**: Requires desktop keyboard/mouse; UI elements clipped by iPhone notch/island or home indicator.
- **4–6**: Basic touch buttons work, but buttons feel stiff; virtual stick wanders off-screen; no safe-area insets.
- **7–8**: Smooth thumb-zone ergonomics, adaptive virtual joystick or intuitive gestures, safe areas honored across aspect ratios ($16:9$, $19.5:9$, $21:9$).
- **9–10**: Zero input lag, haptic feedback integration (where supported), accessibility scaling options, effortless one-handed or comfortable two-thumb play.

### Dimension 3: Game Feel & "Juice" (Target: $\ge 7$)
- **1–3**: Zero tactile feedback; objects disappear instantly without reaction; static, lifeless interactions.
- **4–6**: Basic particle effects or sounds, but timing feels detached; collisions lack weight or punch.
- **7–8**: Well-timed screen shake, hit-pauses (freeze frames for 2–4 frames on heavy impact), squash-and-stretch on jumps/landings, floating combat text.
- **9–10**: Visceral kinetic feedback across every interaction; every tap produces delight through particle bursts, dynamic lighting, and camera recoil.

### Dimension 4: Art Cohesion & Animation Quality (Target: $\ge 7$)
- **1–3**: Clashing pixel resolutions (mix of $16\times 16$ and high-res vector), inconsistent lighting directions, distorted sprite stretching.
- **4–6**: Consistent art style, but animations are choppy or missing key transitional frames (e.g. idle-to-run).
- **7–8**: Unified color palette, clean sprite sheets with consistent pixel grids, smooth frame pacing, layered parallax backgrounds.
- **9–10**: Impeccable visual direction, seamless animation blending, subtle ambient particle effects (dust motes, foliage sway), custom shader post-processing.

### Dimension 5: Audio & Sound Feedback (Target: $\ge 7$)
- **1–3**: Mute or harsh un-normalized audio; sound effects play out of sync or cut each other off abruptly.
- **4–6**: Background music and SFX present, but volume balance is uneven; no mute toggle; iOS audio context unlock fails.
- **7–8**: Audio unlocks reliably on first user tap, distinct spatial or layered SFX, volume sliders, music loops cleanly without pops.
- **9–10**: Dynamic interactive music system (intensity shifts with gameplay), rich layered foley audio, full Web Audio ducking and filter effects.

### Dimension 6: Technical Stability & Error Recovery (Target: $\ge 8$)
- **1–3**: Game crashes silently when network drops or WebGL context is lost; memory leaks crash browser tab after 5 minutes.
- **4–6**: Basic error handling, but network reconnects cause duplicated entities or desynced game state.
- **7–8**: Clean WebGL context-loss recovery, graceful offline handling, safe bounds checking on all array indices and game object pointers.
- **9–10**: Zero memory leaks across 30-minute stress runs, automated crash telemetry reporting, robust optimistic state rollback.

### Dimension 7: Load & Runtime Performance (Target: $\ge 8$)
- **1–3**: Initial download $>25\text{MB}$; initial boot takes $>10\text{s}$; frame rate dips below 30 FPS frequently.
- **4–6**: Initial bundle $\le 15\text{MB}$; initial boot $\le 5\text{s}$; maintains 45–60 FPS on desktop, but throttles on mobile devices.
- **7–8**: Initial bundle $\le 8\text{MB}$; initial boot $\le 2.5\text{s}$ on 4G; rock-solid 60 FPS on mid-tier mobile (iPhone 11+, Snapdragon 7xx).
- **9–10**: Ultra-lean initial bundle ($\le 3\text{MB}$) with progressive asset streaming; sub-second boot; consistent 60–120 FPS utilizing Phaser 4 `SpriteGPULayer`.

### Dimension 8: Release Readiness & Store Compliance (Target: $\ge 8$)
- **1–3**: No manifest; missing icons; unhandled back-button on Android; desktop window sizing hardcoded.
- **4–6**: Web manifest exists, but splash screen is blank or orientation lock fails on mobile browsers.
- **7–8**: Complete Web App Manifest, crisp PWA icons ($192\text{px}$, $512\text{px}$), correct orientation locking, Capacitor/Cordova wrapper compatibility.
- **9–10**: Production-ready PWA with offline Service Worker caching; zero store policy compliance warnings; ready for Google Play TWA and Apple App Store packaging.

---

## 3. Remediation Prioritization Formula

When multiple gaps exist, agents must rank tasks using this deterministic priority score:

$$\text{Priority} = (\text{IsBlocker} \times 100) + (\text{Impact} \times 10) + (\text{Confidence} \times 5) - (\text{Effort} \times 3)$$

- **IsBlocker**: $1$ if task resolves any of RB-01 through RB-08; otherwise $0$.
- **Impact**: Expected improvement on dimensional score ($1$ to $10$).
- **Confidence**: Agent's certainty of completing the fix without regressions ($1$ to $10$).
- **Effort**: Estimated complexity and lines touched ($1$ = trivial, $10$ = multi-system refactor).

---

## 4. Release Tier Gates

| Release Gate | Hard Blockers Allowed | Minimum Dimension Average | Minimum Lowest Dimension |
| :--- | :--- | :--- | :--- |
| **Alpha Gate** (Internal testing) | $0$ blockers on RB-01 to RB-05 | $\ge 5.0$ | $\ge 4$ |
| **Beta Gate** (Public preview) | $0$ blockers on RB-01 to RB-07 | $\ge 6.8$ | $\ge 6$ |
| **Gold / Production Gate** (Commercial release) | **0 blockers (RB-01 through RB-08 must all pass)** | **$\ge 7.5$** | **$\ge 7$** |
