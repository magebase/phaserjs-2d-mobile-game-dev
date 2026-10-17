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
        # Check if tilemap or atlas
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
    """Scan and catalog all game assets in the repository."""
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
            
            # Duplicate detection
            if sha in seen_hashes:
                item_defects.append(f"duplicate_of:{seen_hashes[sha]}")
            else:
                seen_hashes[sha] = rel_path
                
            if atype == "image":
                images_count += 1
                dim_info, has_alpha, img_defects = inspect_image(f)
                item_defects.extend(img_defects)
            elif atype == "audio":
                audio_count += 1
            elif atype == "atlas":
                atlases_count += 1
            elif atype == "font":
                fonts_count += 1
            elif atype == "tilemap":
                tilemaps_count += 1
                
            total_defects += len(item_defects)
            
            item_entry: Dict[str, Any] = {
                "path": rel_path,
                "type": atype,
                "format": aformat,
                "size_bytes": fsize,
                "sha256": sha,
                "tags": [atype, aformat],
                "defects": item_defects
            }
            if dim_info:
                item_entry["dimensions"] = dim_info
                item_entry["alpha_channel"] = has_alpha
                
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
