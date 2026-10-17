# Playbook: Inspect & Profile Game Project

> **Domain:** Lifecycle  
> **Capability ID:** `lifecycle.inspect_project`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides an autonomous agent or developer through discovering the active game project structure, validating the Phaser version, mapping the scene graph, locating all assets, and identifying backend integration touchpoints without disrupting existing code.

---

## 2. Trigger Conditions

Run this playbook when:
- First entering a new or unfamiliar game repository.
- Generating or updating `game-profile.json`.
- Diagnosing scene routing or package manager conventions.

---

## 3. Step-by-Step Procedure

### Step 1: Run Automated Project Probe
Execute the native probe tool:
```bash
./tools/magebase-game probe /path/to/game --output game-profile.json
```

### Step 2: Verify Phaser 4 Matrix
Inspect the engine version in `game-profile.json`:
- Confirm `identity.engine.name == "Phaser"`.
- If `identity.engine.major == 3`, consult `PHASER_COMPATIBILITY.md` for the v3-to-v4 upgrade pathway.
- Pinned target is **Phaser 4.2.1**.

### Step 3: Map the Scene Graph
Examine `architecture.scene_graph`:
- Check for standard lifecycle scenes: `BootScene` (init, scale config) $\to$ `PreloadScene` (asset loading) $\to$ `MainMenuScene` (UI) $\to$ `GameScene` (active loop).
- Note missing transitions or scenes that fail to pass control.

### Step 4: Catalog Asset Directories
Check `art.asset_roots`:
- Verify directories exist (e.g. `public/assets/`, `assets/`).
- If custom asset directories are present, record them in `game-profile.json`.

### Step 5: Detect Backend Bindings
Examine `backend.mode`:
- `django`: Look for `manage.py` and session cookie configurations.
- `cloudflare`: Look for `wrangler.jsonc` and D1/R2/KV/Queues bindings.
- `none`: Client-only local storage persistence.

---

## 4. Verification & Output Artifacts

- **Output:** `game-profile.json` conforming to `schemas/game-profile.schema.json`.
- **Validation:**
```bash
python3 -c "from tools.lib.common import load_json, validate_schema; from pathlib import Path; p = load_json(Path('game-profile.json')); valid, err = validate_schema(p, Path('schemas/game-profile.schema.json')); assert valid, err; print('Profile valid!')"
```
