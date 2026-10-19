"""Project probe module for Phaser 4 mobile game analysis."""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from tools.lib.common import load_json


def detect_package_manager(root: Path) -> str:
    """Detect package manager used in the project."""
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists():
        return "bun"
    if (root / "package-lock.json").exists() or (root / "package.json").exists():
        return "npm"
    return "none"


def detect_language(root: Path) -> str:
    """Detect primary language (javascript or typescript)."""
    if (root / "tsconfig.json").exists():
        return "typescript"
    for ext in ["*.ts", "*.tsx"]:
        if list(root.glob(f"src/**/{ext}")):
            return "typescript"
    return "javascript"


def detect_bundler(root: Path, pkg: Dict[str, Any]) -> str:
    """Detect build tool / bundler."""
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    if (root / "vite.config.js").exists() or (root / "vite.config.ts").exists() or "vite" in deps:
        return "vite"
    if (root / "webpack.config.js").exists() or "webpack" in deps:
        return "webpack"
    if "esbuild" in deps:
        return "esbuild"
    if "parcel" in deps:
        return "parcel"
    if "rollup" in deps:
        return "rollup"
    return "none"


def detect_phaser_version(pkg: Dict[str, Any], root: Path) -> Dict[str, Any]:
    """Detect Phaser version from package.json or source files."""
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    version_str = deps.get("phaser", "4.2.1").lstrip("^~>=<")
    
    # Check for Phaser 4 marker
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", version_str)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        return {
            "name": "Phaser",
            "version": version_str,
            "major": major,
            "minor": minor
        }
    
    return {
        "name": "Phaser",
        "version": "4.2.1",
        "major": 4,
        "minor": 2
    }


def find_entry_point(root: Path) -> str:
    """Locate primary entry point."""
    candidates = [
        "src/main.ts",
        "src/main.js",
        "src/index.ts",
        "src/index.js",
        "src/game.js",
        "src/game.ts",
        "index.html",
        "main.js"
    ]
    for c in candidates:
        if (root / c).exists():
            return c
    return "index.html"


def scan_scenes(root: Path) -> List[Dict[str, Any]]:
    """Scan JavaScript and TypeScript files for Phaser.Scene definitions."""
    scenes = []
    seen_keys = set()
    
    search_dirs = [root / "src", root / "js", root]
    for sdir in search_dirs:
        if not sdir.exists():
            continue
        for ext in ["*.js", "*.ts"]:
            for f in sdir.rglob(ext):
                # Skip build outputs and dependencies
                if any(part in f.parts for part in ["node_modules", "dist", ".next", "build", "coverage"]):
                    continue
                
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                
                # Check for scene inheritance or definition
                is_scene = (
                    "extends Phaser.Scene" in content or
                    "extends Scene" in content or
                    "new Phaser.Scene(" in content or
                    "Phaser.Scene.call(this" in content
                )
                
                if is_scene:
                    # Try to extract key from super('Key') or super({ key: 'Key' })
                    key_match = re.search(r"super\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content)
                    if not key_match:
                        key_match = re.search(r"super\s*\(\s*\{\s*key:\s*['\"]([^'\"]+)['\"]\s*\}", content)
                    
                    key = key_match.group(1) if key_match else f.stem
                    if key not in seen_keys:
                        seen_keys.add(key)
                        rel_path = str(f.relative_to(root))
                        
                        # Infer transitions by checking this.scene.start('OtherKey')
                        transitions = re.findall(r"this\.scene\.(?:start|switch|launch)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content)
                        
                        scenes.append({
                            "key": key,
                            "file": rel_path,
                            "type": "gameplay" if "game" in key.lower() else "ui",
                            "transitions_to": list(set(transitions))
                        })
    
    if not scenes:
        scenes.append({
            "key": "MainScene",
            "file": "src/main.js",
            "type": "gameplay",
            "transitions_to": []
        })
    return scenes


def detect_asset_roots(root: Path) -> List[str]:
    """Find directories containing visual and audio game assets."""
    roots = []
    candidates = ["public/assets", "assets", "public", "static/assets", "static"]
    for c in candidates:
        if (root / c).is_dir():
            roots.append(c)
    return roots if roots else ["assets"]


def detect_backend(root: Path) -> Dict[str, Any]:
    """Detect backend integration (Django, Cloudflare Workers, etc.)."""
    has_django = (root / "manage.py").exists() or (root / "backend" / "manage.py").exists()
    has_wrangler = (root / "wrangler.jsonc").exists() or (root / "wrangler.toml").exists() or (root / "wrangler.json").exists()
    
    if has_django and has_wrangler:
        mode = "hybrid"
    elif has_django:
        mode = "django"
    elif has_wrangler:
        mode = "cloudflare"
    else:
        mode = "none"
    
    return {
        "mode": mode,
        "base_url": "http://localhost:8000" if has_django else "",
        "endpoints": {
            "save_state": "/api/v1/save/",
            "load_state": "/api/v1/load/"
        } if mode != "none" else {},
        "auth": "session_cookie" if has_django else "anonymous",
        "persistence": "offline_first_sync" if mode != "none" else "local_storage"
    }


def detect_cloudflare(root: Path) -> Optional[Dict[str, Any]]:
    """Detect Cloudflare Workers configuration and bindings."""
    for cfg in ["wrangler.jsonc", "wrangler.json", "wrangler.toml"]:
        if (root / cfg).exists():
            return {
                "wrangler_config": cfg,
                "worker_type": "javascript",
                "bindings": {
                    "d1": ["GAME_DB"],
                    "r2": ["GAME_ASSETS"],
                    "kv": ["GAME_CONFIG"],
                    "queues": [],
                    "durable_objects": []
                }
            }
    return None


def scan_for_secret_leaks(root: Path) -> List[Dict[str, str]]:
    """Scan distribution and source files for potential leaked secrets."""
    leaks = []
    secret_patterns = [
        (r"(sk_live_[0-9a-zA-Z]{24,})", "Stripe Live Secret Key"),
        (r"(AIzaSy[0-9A-Za-z-_]{33})", "Google API Key"),
        (r"(eyJhbGciOi[0-9a-zA-Z-_=]+\.[0-9a-zA-Z-_=]+\.[0-9a-zA-Z-_=]+)", "Raw JWT Token"),
        (r"(ghp_[0-9a-zA-Z]{36})", "GitHub Personal Access Token"),
        (r"(d1_token_[0-9a-zA-Z]{20,})", "Cloudflare Token")
    ]
    
    target_dirs = [root / "dist", root / "public", root / "build"]
    for tdir in target_dirs:
        if not tdir.exists():
            continue
        for f in tdir.rglob("*.js"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                for pat, label in secret_patterns:
                    if re.search(pat, text):
                        leaks.append({
                            "file": str(f.relative_to(root)),
                            "type": label
                        })
            except Exception:
                pass
    return leaks


def probe_project(root_dir: str | Path) -> Dict[str, Any]:
    """Execute complete project probe and return GameProfile dict."""
    root = Path(root_dir).resolve()
    
    # Check for existing profile (magebase.game.json or game-profile.json)
    existing_profile = {}
    for fname in ["magebase.game.json", "game-profile.json"]:
        if (root / fname).exists():
            try:
                existing_profile = load_json(root / fname)
                break
            except Exception:
                pass
    
    pkg_file = root / "package.json"
    pkg = load_json(pkg_file) if pkg_file.exists() else {}
    
    name = existing_profile.get("identity", {}).get("name") or pkg.get("name", root.name)
    slug = existing_profile.get("identity", {}).get("slug") or (re.sub(r"[^a-z0-9-_]", "-", name.lower()).strip("-") or "phaser-game")
    version = existing_profile.get("identity", {}).get("version") or pkg.get("version", "1.0.0")
    
    engine = detect_phaser_version(pkg, root)
    language = detect_language(root)
    bundler = detect_bundler(root, pkg)
    package_manager = detect_package_manager(root)
    entry_point = find_entry_point(root)
    scenes = scan_scenes(root)
    asset_roots = detect_asset_roots(root)
    backend = detect_backend(root)
    cloudflare = detect_cloudflare(root)
    
    # Detect or preserve genre
    genre = existing_profile.get("identity", {}).get("genre", "general_2d")

    if genre == "general_2d":
        text_corpus = f"{name} {root.name}".lower()
        for s in scenes:
            text_corpus += f" {s.get('key', '')} {s.get('file', '')}".lower()
        if any(k in text_corpus for k in ["rogue", "dungeon", "gravebound", "buriedbornes", "spire"]):
            genre = "turn_based_roguelike"
        elif any(k in text_corpus for k in ["shoot", "bullet", "action", "survivor"]):
            genre = "action_shooter"
        elif any(k in text_corpus for k in ["platform", "jump", "metroid"]):
            genre = "platformer"
        elif any(k in text_corpus for k in ["puzzle", "match3", "grid"]):
            genre = "puzzle"
        elif any(k in text_corpus for k in ["autobattle", "backpack"]):
            genre = "autobattler"

    profile: Dict[str, Any] = {
        "identity": {
            "name": name,
            "slug": slug,
            "version": version,
            "engine": engine,
            "language": language,
            "bundler": bundler,
            "package_manager": package_manager,
            "genre": genre,
            "repo_root": str(root)
        },
        "mobile": {
            "orientation": "portrait",
            "target_viewports": [
                { "name": "iPhone 14 / 15", "width": 390, "height": 844, "device_pixel_ratio": 3.0 },
                { "name": "Pixel 7 / 8", "width": 412, "height": 915, "device_pixel_ratio": 2.625 }
            ],
            "safe_areas": {
                "enabled": True,
                "top": 44,
                "bottom": 34,
                "left": 0,
                "right": 0
            },
            "touch_controls": {
                "enabled": True,
                "type": "virtual_joystick",
                "multi_touch": True,
                "haptic_feedback": False
            },
            "performance_tier": "mid"
        },
        "architecture": {
            "entry_point": entry_point,
            "scene_graph": scenes,
            "state_management": "registry",
            "ui_layer": "phaser_gameobjects"
        },
        "art": {
            "asset_roots": asset_roots,
            "catalogs": ["asset-catalog.json"],
            "style_tags": ["pixel-art", "2d"],
            "sheet_conventions": {
                "default_tile_size": 16,
                "standard_paddings": 0
            },
            "animation_manifests": []
        },
        "backend": backend,
        "quality": {
            "target_fps": 60,
            "max_initial_bundle_mb": 8.0,
            "max_memory_mb": 128
        },
        "tooling": {
            "dev_cmd": f"{package_manager} run dev" if "dev" in pkg.get("scripts", {}) else existing_profile.get("tooling", {}).get("dev_cmd", "npx serve"),
            "build_cmd": f"{package_manager} run build" if "build" in pkg.get("scripts", {}) else existing_profile.get("tooling", {}).get("build_cmd", ""),
            "test_cmd": f"{package_manager} test" if "test" in pkg.get("scripts", {}) else existing_profile.get("tooling", {}).get("test_cmd", ""),
            "lint_cmd": f"{package_manager} run lint" if "lint" in pkg.get("scripts", {}) else existing_profile.get("tooling", {}).get("lint_cmd", ""),
            "smoke_cmd": existing_profile.get("tooling", {}).get("smoke_cmd", "")
        }
    }
    
    if cloudflare:
        profile["cloudflare"] = cloudflare
        
    return profile
