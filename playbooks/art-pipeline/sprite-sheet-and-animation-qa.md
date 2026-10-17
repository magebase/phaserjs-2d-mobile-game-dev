# Playbook: Sprite Sheet Grid QA & Animation Slicing

> **Domain:** Art Pipeline  
> **Capability ID:** `art_pipeline.sprite_sheet_and_animation_qa`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides diagnosing and correcting spritesheet alignment errors, non-divisible frame grids, stray edge bleeding, and character foot jitter in Phaser 4 sprite animations.

---

## 2. Common Spritesheet Defects & Automated Fixes

### 2.1 The "Uneven Frame Division" Defect
If an image is $68\times 32\text{px}$ and sliced at $16\times 16\text{px}$, $68 \pmod{16} = 4$. The remaining 4 pixels cause frame indexing to drift, producing mangled animation frames.

**Verification Check**:
```python
def check_grid(width, height, frame_w, frame_h, margin=0, spacing=0):
    effective_w = width - (2 * margin)
    effective_h = height - (2 * margin)
    cols = (effective_w + spacing) / (frame_w + spacing)
    rows = (effective_h + spacing) / (frame_h + spacing)
    return cols.is_integer() and rows.is_integer()
```

### 2.2 Stray Alpha Edge Bleed
WebGL bilinear filtering can bleed neighboring sprite pixels into the current frame.
- **Fix in Phaser Game Config**:
  ```javascript
  render: {
    pixelArt: true,
    roundPixels: true
  }
  ```
- Or add 1px transparent extruded border to each frame using TexturePacker or spritesheet slicers.

---

## 3. Correcting Foot Jitter (Anchor Point Stabilization)

When cycling between `idle` and `walk` animations, characters often appear to "hop" or jitter if sprite frames have variable vertical padding.

**Solution**:
Always anchor character sprites at the bottom center $(0.5, 1.0)$:
```javascript
player.setOrigin(0.5, 1.0);
```
Ensure all frames in the spritesheet have their ground contact point aligned to the exact same bottom pixel row.

---

## 4. Verification Checklist

- [ ] All spritesheet dimensions divide evenly by declared frame sizes.
- [ ] No visible 1px seam or edge artifact appears during sprite animations.
- [ ] Walking animation keeps feet planted without erratic vertical hopping.
