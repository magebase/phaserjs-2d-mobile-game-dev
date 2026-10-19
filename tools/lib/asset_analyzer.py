"""Asset analyzer module for Phaser 4 texture, spritesheet and audio audits."""

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image
except ImportError:
    Image = None

from tools.lib.common import compute_sha256, is_power_of_two


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTS = {".ogg", ".mp3", ".wav", ".m4a"}
FONT_EXTS = {".ttf", ".woff", ".woff2", ".fnt"}
DATA_EXTS = {".json", ".tmx", ".xml"}


def inspect_image(filepath: Path) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
    """Inspect image dimensions, POT compliance, and alpha channel."""
    if Image is None:
        return None, False, []
    
    defects = []
    try:
        with Image.open(filepath) as img:
            w, h = img.size
            has_alpha = img.mode in ("RGBA", "LA") or ("transparency" in img.info)
            pot_w = is_power_of_two(w)
            pot_h = is_power_of_two(h)
            is_pot = pot_w and pot_h
            
            # Check defects
            if not is_pot:
                defects.append(f"non_power_of_two ({w}x{h})")
            if w > 2048 or h > 2048:
                defects.append(f"oversized_texture ({w}x{h} exceeds 2048px limit)")
                
            dim_info = {
                "width": w,
                "height": h,
                "is_power_of_two": is_pot
            }
            return dim_info, has_alpha, defects
    except Exception as e:
        return None, False, [f"corrupt_or_unreadable: {str(e)}"]


def extract_art_intelligence(filepath: Path) -> Tuple[Optional[Dict[str, Any]], List[str], str, Dict[str, Any]]:
    """Extract transparent bounding box, dominant palette, facing direction, and suitability."""
    if Image is None:
        return None, [], "unknown", {"score": 5.0, "notes": "PIL not available"}

    try:
        with Image.open(filepath) as img:
            w, h = img.size
            rgba = img.convert("RGBA")
            bbox = rgba.getbbox()
            if bbox:
                min_x, min_y, max_x, max_y = bbox
                cw = max_x - min_x
                ch = max_y - min_y
                trim_ratio = round((cw * ch) / max(1, w * h), 3)
                bounds = {
                    "min_x": min_x,
                    "min_y": min_y,
                    "max_x": max_x,
                    "max_y": max_y,
                    "content_width": cw,
                    "content_height": ch,
                    "trim_ratio": trim_ratio
                }
            else:
                bounds = {
                    "min_x": 0, "min_y": 0, "max_x": w, "max_y": h,
                    "content_width": w, "content_height": h, "trim_ratio": 1.0
                }

            # Sample dominant palette
            small = rgba.resize((32, 32))
            colors = small.getcolors(maxcolors=1024) or []
            solid_colors = [(count, c) for count, c in colors if len(c) < 4 or c[3] > 64]
            solid_colors.sort(reverse=True, key=lambda x: x[0])
            hex_palette = []
            for _, c in solid_colors[:5]:
                hex_palette.append(f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}")

            if bbox:
                mid_x = (bbox[0] + bbox[2]) / 2.0
                img_mid_x = w / 2.0
                delta = (mid_x - img_mid_x) / max(1.0, w)
                if delta < -0.05:
                    facing = "left"
                elif delta > 0.05:
                    facing = "right"
                else:
                    facing = "centered"
            else:
                facing = "omni"

            suitability = {
                "score": 9.0 if bounds.get("trim_ratio", 1.0) >= 0.25 else 6.0,
                "notes": "Crisp non-empty silhouette" if bounds.get("trim_ratio", 1.0) >= 0.25 else "Significant empty padding"
            }
            return bounds, hex_palette, facing, suitability
    except Exception as e:
        return None, [], "unknown", {"score": 3.0, "notes": f"Error inspecting image: {e}"}


def infer_semantic_roles(rel_path: str, atype: str) -> List[str]:
    """Infer game semantic role from asset path and type."""
    p_lower = rel_path.lower()
    roles = []
    if any(k in p_lower for k in ["hero", "player", "knight", "mage", "archer", "protagonist"]):
        roles.extend(["hero", "playable_character"])
    if any(k in p_lower for k in ["enemy", "skeleton", "goblin", "slime", "demon", "monster", "orc"]):
        roles.extend(["enemy", "combatant"])
    if any(k in p_lower for k in ["boss", "dragon", "overlord", "reaper"]):
        roles.extend(["boss", "combatant"])
    if any(k in p_lower for k in ["bullet", "arrow", "projectile", "laser", "missile", "fireball"]):
        roles.extend(["projectile", "hazard"])
    if any(k in p_lower for k in ["tile", "dungeon", "wall", "floor", "terrain", "ground"]):
        roles.extend(["tile", "environment"])
    if any(k in p_lower for k in ["coin", "gem", "potion", "pickup", "chest", "loot", "item"]):
        roles.extend(["pickup", "economy"])
    if any(k in p_lower for k in ["fx", "vfx", "particle", "slash", "explosion", "smoke", "flash"]):
        roles.extend(["vfx", "feedback"])
    if any(k in p_lower for k in ["ui", "hud", "btn", "button", "icon", "bar", "dialog", "panel"]):
        roles.extend(["hud", "ui_control"])
    if atype == "audio":
        if any(k in p_lower for k in ["music", "bgm", "theme", "ambient"]):
            roles.append("audio_bgm")
        else:
            roles.append("audio_sfx")

    return roles or ["general_asset"]


def classify_asset(filepath: Path) -> Tuple[str, str]:
    """Classify asset type and format."""
    ext = filepath.suffix.lower()
    if ext in IMAGE_EXTS:
        return "image", ext.lstrip(".")
    if ext in AUDIO_EXTS:
        return "audio", ext.lstrip(".")
    if ext in FONT_EXTS:
        return "font", ext.lstrip(".")
    if ext in DATA_EXTS:
        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")[:500]
            if "tilewidth" in text or "layers" in text:
                return "tilemap", "json"
            if "frames" in text or "textures" in text:
                return "atlas", "json"
        except Exception:
            pass
        return "json", ext.lstrip(".")
    return "other", ext.lstrip(".")


def analyze_assets(root_dir: str | Path, asset_roots: Optional[List[str]] = None) -> Dict[str, Any]:
    """Scan and catalog all game assets in the repository with art intelligence."""
    root = Path(root_dir).resolve()
    
    if not asset_roots:
        candidates = ["public/assets", "assets", "public", "static/assets"]
        asset_roots = [c for c in candidates if (root / c).is_dir()]
        if not asset_roots:
            asset_roots = ["."]
            
    items: List[Dict[str, Any]] = []
    seen_hashes: Dict[str, str] = {}
    
    images_count = 0
    audio_count = 0
    atlases_count = 0
    fonts_count = 0
    tilemaps_count = 0
    total_defects = 0
    total_bytes = 0
    
    for rel_root in asset_roots:
        scan_dir = root / rel_root
        if not scan_dir.exists():
            continue
            
        for f in scan_dir.rglob("*"):
            if not f.is_file():
                continue
            if any(part in f.parts for part in ["node_modules", ".git", "dist", "build"]):
                continue
                
            atype, aformat = classify_asset(f)
            if atype == "other" and f.suffix.lower() not in {".txt", ".csv"}:
                continue
                
            fsize = f.stat().st_size
            total_bytes += fsize
            sha = compute_sha256(f)
            rel_path = str(f.relative_to(root))
            
            dim_info = None
            has_alpha = False
            item_defects = []
            bounds = None
            palette: List[str] = []
            facing = "unknown"
            suitability: Optional[Dict[str, Any]] = None
            
            # Duplicate detection
            if sha in seen_hashes:
                item_defects.append(f"duplicate_of:{seen_hashes[sha]}")
            else:
                seen_hashes[sha] = rel_path
                
            if atype == "image":
                images_count += 1
                dim_info, has_alpha, img_defects = inspect_image(f)
                item_defects.extend(img_defects)
                bounds, palette, facing, suitability = extract_art_intelligence(f)
            elif atype == "audio":
                audio_count += 1
            elif atype == "atlas":
                atlases_count += 1
            elif atype == "font":
                fonts_count += 1
            elif atype == "tilemap":
                tilemaps_count += 1
                
            total_defects += len(item_defects)
            roles = infer_semantic_roles(rel_path, atype)
            
            item_entry: Dict[str, Any] = {
                "path": rel_path,
                "type": atype,
                "format": aformat,
                "size_bytes": fsize,
                "sha256": sha,
                "semantic_roles": roles,
                "tags": [atype, aformat] + roles,
                "defects": item_defects
            }
            if dim_info:
                item_entry["dimensions"] = dim_info
                item_entry["alpha_channel"] = has_alpha
            if bounds:
                item_entry["transparent_bounds"] = bounds
            if palette:
                item_entry["dominant_palette"] = palette
            if facing != "unknown":
                item_entry["facing_direction"] = facing
            if suitability:
                item_entry["suitability"] = suitability
                
            items.append(item_entry)
            
    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_files": len(items),
        "total_bytes": total_bytes,
        "items": items,
        "summary": {
            "images_count": images_count,
            "audio_count": audio_count,
            "atlases_count": atlases_count,
            "fonts_count": fonts_count,
            "tilemaps_count": tilemaps_count,
            "defect_count": total_defects
        }
    }
