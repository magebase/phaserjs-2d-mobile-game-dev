# Quality Rubric — Dimensional Scoring Guidelines

> **Router Reference:** `phaser-mobile-game-dev`  
> **Reference:** `GAME_QUALITY_CONTRACT.md`

This rubric provides evaluation benchmarks for scoring the 8 Quality Dimensions on a 1–10 scale.

---

## 1. Fun & Core Loop
- **1–3 (Unplayable)**: No win/loss condition, objective is undefined, mechanics feel broken or non-responsive.
- **4–6 (Functional)**: Core mechanic works, but lacks pacing, micro-rewards, or escalating challenge. Player easily disengages after 60 seconds.
- **7–8 (Commercial Ready)**: Satisfying loop with clear objectives, micro-goals (score, combos, unlocks), balanced difficulty curve, and clear restart cycle.
- **9–10 (Mastery)**: Deep flow state, emergent gameplay interactions, high replayability, multiple tactical choices.

---

## 2. Mobile Usability & Ergonomics
- **1–3 (Unplayable)**: Relies on desktop keyboard/mouse. No touch input. UI clipped by screen borders.
- **4–6 (Functional)**: Basic touch buttons, but fixed positions cause hand strain; virtual stick escapes thumb zone; no safe-area notch margins.
- **7–8 (Commercial Ready)**: Floating or adaptive virtual joystick, responsive touch targets ($\ge 44\times 44\text{px}$), safe area margins on modern iPhone/Android displays, multi-touch enabled.
- **9–10 (Mastery)**: Flawless one-handed and two-thumb ergonomics, haptic feedback on impact, customizable control positions, gesture shortcuts.

---

## 3. Game Feel & "Juice"
- **1–3 (Lifeless)**: Zero reaction on hit or score; sprites vanish abruptly; static linear movement.
- **4–6 (Basic)**: Sounds play on hit, but lack visual reinforcement; explosions are static sprites without particles.
- **7–8 (Tactile)**: Camera screen shake with decay, hit freezes (freeze-frames for 2–4 frames), impact particle bursts, squash-and-stretch on jumps/collisions, floating damage numbers.
- **9–10 (Visceral)**: Every interaction feels dynamic and rewarding; subtle camera zooms, dynamic lighting flashes on explosions, layered particle trails, recoil knockback.

---

## 4. Art Cohesion & Animation Quality
- **1–3 (Incoherent)**: Mixed asset resolutions (e.g. $16\text{px}$ pixel art mixed with $512\text{px}$ vector art), clashing color palettes, visible sprite seams or stretching.
- **4–6 (Passable)**: Single consistent style, but animations have missing frames, jumpy anchor points, or uneven frame rates.
- **7–8 (Commercial Ready)**: Unified color palette, clean spritesheet alignment with fixed pivots, smooth frame pacing, multi-layered parallax backgrounds.
- **9–10 (Mastery)**: Custom post-processing shader passes, seamless state blending, dynamic secondary animations (cloth sway, hair, dust particles), ambient environmental VFX.

---

## 5. Audio & Feedback
- **1–3 (Broken)**: Audio fails to play on mobile due to locked Web Audio context; harsh clipping; no mute controls.
- **4–6 (Passable)**: Web Audio unlocks, but sounds lack normalization; music loop has noticeable pop; no volume sliders.
- **7–8 (Commercial Ready)**: Instant unlock on first touch gesture, clear sound spatialization/panning, normalized sound levels, seamless music loops, independent BGM/SFX mute toggles.
- **9–10 (Mastery)**: Dynamic adaptive music (stems change with game intensity), rich procedural sound effects, Web Audio low-pass filtering on pause/underwater states.

---

## 6. Technical Stability & Error Recovery
- **1–3 (Fragile)**: Unhandled exceptions cause white-screen lockups; tab crashes after 5 minutes of play due to texture memory leaks.
- **4–6 (Passable)**: Error boundaries present, but network drops cause desynchronization or permanent loading spinners.
- **7–8 (Commercial Ready)**: Graceful WebGL context-loss recovery, resilient offline fallbacks, zero memory leaks across 30-minute stress runs, safe null checks on all game entities.
- **9–10 (Mastery)**: Self-healing error telemetry, optimistic client-side prediction with rollback, seamless reconnects without gameplay interruption.

---

## 7. Load & Runtime Performance
- **1–3 (Sluggish)**: Initial download $>25\text{MB}$; initial load $>10\text{s}$; frame rate frequently drops below 30 FPS.
- **4–6 (Passable)**: Initial bundle $\le 15\text{MB}$; maintains 60 FPS on desktop, but drops frames on mid-tier mobile phones.
- **7–8 (Commercial Ready)**: Initial bundle $\le 8\text{MB}$; load time $\le 2.5\text{s}$; solid 60 FPS on iPhone 11 and Snapdragon 7xx devices using Phaser 4 GPU batching.
- **9–10 (Mastery)**: Ultra-compact initial bundle ($\le 3\text{MB}$) with progressive asset streaming; sub-second boot; consistent 60–120 FPS utilizing `SpriteGPULayer` and `TilemapGPULayer`.

---

## 8. Release Readiness & Store Compliance
- **1–3 (Unready)**: No Web App Manifest; missing icons; unhandled back-button navigation; desktop-only layout.
- **4–6 (Passable)**: Manifest present, but icons are blurry or splash screen shows browser white flash.
- **7–8 (Commercial Ready)**: Valid Web App Manifest, crisp PWA icons ($192\text{px}$, $512\text{px}$), viewport meta tags locked (`viewport-fit=cover`), Capacitor/Cordova packaging compatibility.
- **9–10 (Mastery)**: Production-ready PWA with offline Service Worker caching; zero store policy compliance warnings; ready for Google Play TWA and Apple App Store packaging.
