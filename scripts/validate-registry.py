#!/usr/bin/env python3
"""Validation script for capabilities.json registry and schema conformance."""

import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

try:
    import jsonschema
except ImportError:
    print("Warning: jsonschema not installed; please install it for full validation.")
    jsonschema = None


def main():
    print("Validating capability registry and playbook resolution...")
    registry_file = repo_root / "registry" / "capabilities.json"
    schema_file = repo_root / "registry" / "schema.json"

    if not registry_file.exists():
        print(f"Error: Registry file not found: {registry_file}", file=sys.stderr)
        sys.exit(1)

    if not schema_file.exists():
        print(f"Error: Schema file not found: {schema_file}", file=sys.stderr)
        sys.exit(1)

    registry_data = json.loads(registry_file.read_text(encoding="utf-8"))
    schema_data = json.loads(schema_file.read_text(encoding="utf-8"))

    # 1. JSON Schema validation
    if jsonschema:
        try:
            jsonschema.validate(instance=registry_data, schema=schema_data)
            print("✓ capabilities.json conforms to registry/schema.json")
        except jsonschema.ValidationError as e:
            print(f"Schema validation error: {e.message} at {e.json_path}", file=sys.stderr)
            sys.exit(1)

    # 2. Duplicate ID check and Playbook path resolution
    seen_ids = set()
    errors = []
    capabilities = registry_data.get("capabilities", [])

    for cap in capabilities:
        cid = cap["id"]
        if cid in seen_ids:
            errors.append(f"Duplicate capability ID: {cid}")
        seen_ids.add(cid)

        # Check playbook file on disk
        playbook_path = repo_root / cap["playbook"]
        if not playbook_path.exists():
            errors.append(f"Capability '{cid}': playbook file '{cap['playbook']}' does not exist on disk")

    if errors:
        print(f"\nFound {len(errors)} registry errors:", file=sys.stderr)
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ All {len(capabilities)} capabilities verified with valid playbooks on disk.")
    sys.exit(0)


if __name__ == "__main__":
    main()
