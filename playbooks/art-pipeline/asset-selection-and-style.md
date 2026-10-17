# Playbook: Asset Selection & Style Cohesion

> **Domain:** Art Pipeline  
> **Capability ID:** `art_pipeline.asset_selection_and_style`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides evaluating and enforcing artistic consistency across sprites, tilesets, UI elements, and effects, preventing the "asset flip" look of mismatched visual packs.

---

## 2. Style Cohesion Guidelines

### 2.1 The "Pixel Ratio" Rule
Never mix differing pixel resolutions within the same active scene:
- If terrain uses $16\times 16\text{px}$ tiles with integer pixel art scaling, player and enemy characters must also adhere to the same pixel density.
- Do NOT mix low-res pixel sprites with smooth anti-aliased vector illustrations.

### 2.2 Color Palette Harmony
- Standardize on a unified color palette (e.g. Endesga 32, Pico-8, or custom 16-color ramp).
- UI buttons should use accents from the game world palette rather than default browser hex codes (`#0000ff`, `#ff0000`).

### 2.3 Lighting Direction Consistency
- Ensure top-down or side-scrolling sprites share a uniform light source (e.g. top-left light source with subtle bottom-right drop shadows).

---

## 3. Step-by-Step Style Audit

1. **Review Asset Catalog**: Group visual assets by tags (`pixel-art`, `vector`, `realistic`).
2. **Flag Discrepancies**: Note any sprite where native pixel size deviates by more than $2\times$ from baseline game scale.
3. **Palette Harmonization**: If an imported asset has clashing saturated colors, apply a color grading shader pass or re-palette in `tools/asset-audit`.

---

## 4. Verification Checklist

- [ ] All in-game sprites share uniform pixel scaling.
- [ ] UI frames, buttons, and dialogue boxes visually match the game world aesthetic.
- [ ] Shadows and highlights follow a consistent directional angle across all character sheets.
