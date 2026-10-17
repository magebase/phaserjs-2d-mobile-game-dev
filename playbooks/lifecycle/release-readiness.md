# Playbook: Evaluate Release Readiness Gates

> **Domain:** Lifecycle  
> **Capability ID:** `lifecycle.release_readiness`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook evaluates whether a Phaser 4 game is ready for commercial or preview release based on the release gates defined in `GAME_QUALITY_CONTRACT.md`.

---

## 2. Release Gate Criteria

| Gate | Hard Blockers Allowed | Minimum Average Score | Minimum Lowest Dimension |
| :--- | :---: | :---: | :---: |
| **Alpha Gate** (Internal playtest) | 0 on RB-01 through RB-05 | $\ge 5.0$ | $\ge 4$ |
| **Beta Gate** (Public preview) | 0 on RB-01 through RB-07 | $\ge 6.5$ | $\ge 6$ |
| **Gold / Production Gate** (Commercial release) | **0 on all (RB-01 to RB-08 must pass)** | **$\ge 7.5$** | **$\ge 7$** |

---

## 3. Step-by-Step Procedure

### Step 1: Run Full Audit & Report
```bash
./tools/magebase-game report /path/to/game --output GAME_QUALITY.md
```

### Step 2: Check Hard Blocker Status
Inspect `audit-report.json`:
- If `overall_status == "BLOCKED"`, the game CANNOT release. Identify remaining blockers.

### Step 3: Verify Mobile Manifest & Assets
Check for:
- `manifest.json` with `display: "standalone"`, `orientation`, and valid icon paths.
- Viewport meta tags locked in `index.html`.
- Touch target compliance ($\ge 44\times 44\text{px}$).

### Step 4: Generate Release Sign-Off
If all Gold Gate criteria are met, update `GAME_QUALITY.md` to state:
```markdown
> **Status:** `PASSED`  
> **Release Gate Achieved:** `GOLD`
```
