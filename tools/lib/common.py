"""Shared common utilities for phaserjs-2d-mobile-game-dev tools."""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import jsonschema
except ImportError:
    jsonschema = None


def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_json(filepath: Path) -> Dict[str, Any]:
    """Safely load and parse a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
    """Write data as formatted JSON."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def validate_schema(data: Dict[str, Any], schema_path: Path) -> tuple[bool, Optional[str]]:
    """Validate JSON data against a JSON schema."""
    if jsonschema is None:
        return True, "jsonschema package not installed; skipping validation"
    
    try:
        schema = load_json(schema_path)
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except jsonschema.ValidationError as err:
        return False, f"Validation error at {err.json_path}: {err.message}"
    except Exception as e:
        return False, str(e)


def is_power_of_two(n: int) -> bool:
    """Check if an integer is a positive power of two."""
    return n > 0 and (n & (n - 1)) == 0
