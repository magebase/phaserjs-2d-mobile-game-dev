# GAME_QUALITY.md — Project Quality Tracker

> **Project:** `<Game Name>`  
> **Target Engine:** Phaser 4.2.1  
> **Last Audited:** `YYYY-MM-DD HH:MM:SS`  
> **Status:** `[ PASSED | WARNING | BLOCKED ]`  
> **Release Gate Achieved:** `[ NONE | ALPHA | BETA | GOLD ]`

---

## 1. The 8 Hard Release Blockers

| Blocker ID | Requirement | Status | Evidence / Notes |
| :--- | :--- | :---: | :--- |
| **RB-01** | Build & Compilation Clean | ⚪ UNVERIFIED | `npm run build` status |
| **RB-02** | Zero Clean Boot Exceptions | ⚪ UNVERIFIED | Console error log inspection |
| **RB-03** | Core Loop Operational | ⚪ UNVERIFIED | Boot -> Play -> End state test |
| **RB-04** | Touch Controls Ergonomic | ⚪ UNVERIFIED | Multi-touch & $44\times 44\text{px}$ targets |
| **RB-05** | Zero Asset 404s | ⚪ UNVERIFIED | Physical file matches in catalog |
| **RB-06** | Zero Save/Progress Data Loss | ⚪ UNVERIFIED | Reload persistence assertion |
| **RB-07** | Zero Secrets in Client Bundle | ⚪ UNVERIFIED | Regex entropy scan on distribution files |
| **RB-08** | Frame Rate $\ge 30$ FPS Baseline | ⚪ UNVERIFIED | 60s runtime profile runner |

---

## 2. The 8 Quality Dimension Scores (1–10)

| Dimension | Score (1–10) | Target | Assessment / Observations |
| :--- | :---: | :---: | :--- |
| **1. Fun & Core Loop** | `-` | $\ge 7$ | Pacing, objective clarity, micro-rewards |
| **2. Mobile Usability** | `-` | $\ge 8$ | Virtual stick, notch safe areas, hitboxes |
| **3. Game Feel & Juice** | `-` | $\ge 7$ | Screen shake, hit pauses, particle effects |
| **4. Art Cohesion** | `-` | $\ge 7$ | Palette harmony, frame pacing, no stretching |
| **5. Audio & Feedback** | `-` | $\ge 7$ | Mobile audio unlock, spatial SFX, BGM loops |
| **6. Technical Stability** | `-` | $\ge 8$ | Context-loss recovery, memory leak profile |
| **7. Load & Performance** | `-` | $\ge 8$ | Bundle size $\le 8\text{MB}$, sub-3s boot, 60 FPS |
| **8. Release Readiness** | `-` | $\ge 8$ | Web manifest, PWA icons, offline fallback |
| **Average Score** | **-** | **$\ge 7.5$** | *Overall Quality Average* |

---

## 3. Prioritized Improvement Backlog

| Priority | ID | Task Description | Blocker? | Impact | Effort | Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | `TASK-01` | *Description of highest impact gap* | Yes | 10 | 3 | PENDING |
| 2 | `TASK-02` | *Description of secondary gap* | No | 7 | 2 | PENDING |

---

## 4. Audit Run History

- **`YYYY-MM-DD`**: Initial baseline generated via `magebase-game report`.
