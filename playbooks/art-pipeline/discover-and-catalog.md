# Playbook: Discover & Catalog Existing Game Assets

> **Domain:** Art Pipeline  
> **Capability ID:** `art_pipeline.discover_and_catalog`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-05 (Missing Asset 404s)

---

## 1. Purpose & Scope

This playbook guides discovering, indexing, and cataloging all existing visual and audio files in a Phaser 4 game project. It calculates SHA256 hashes, detects duplicate files, identifies non-power-of-two (NPOT) textures, and generates `asset-catalog.json`.

---

## 2. Trigger Conditions

Run this playbook when:
- Booting a game audit or onboarding an existing game repository.
- Before generating or creating any new artwork or sound.
- Resolving missing asset 404 errors (**RB-05**).

---

## 3. Step-by-Step Procedure

### Step 1: Run Automated Asset Audit Tool
Execute the native audit tool:
```bash
./tools/magebase-game audit /path/to/game --output asset-catalog.json
```

### Step 2: Review Defect Summary
Inspect `summary.defect_count` in `asset-catalog.json`:
- **`non_power_of_two`**: Textures that are not powers of two ($32, 64, 128, 256, 512, 1024, 2048$). Note: in WebGL, repeating textures MUST be POT.
- **`oversized_texture`**: Textures exceeding $2048\times 2048\text{px}$, which crash mid-tier mobile WebGL viewports.
- **`duplicate_of:<path>`**: Identical files with different names wasting download bandwidth.

### Step 3: Match Scene Code with Physical Files
Verify that every asset referenced in `this.load.image(...)` and `this.load.spritesheet(...)` exists in `asset-catalog.json`. If a reference is missing, record it as a high-severity finding.

---

## 4. Output Artifacts

- `asset-catalog.json` conforming to `schemas/asset-catalog.schema.json`.
- List of verified asset keys and detected duplicate candidates.
