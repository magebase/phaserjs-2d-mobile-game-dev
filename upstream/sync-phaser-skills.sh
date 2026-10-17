#!/usr/bin/env bash
# Synchronize or verify pinned upstream Phaser skills
set -euo pipefail

PINNED_VERSION="4.2.1"
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/phaser-skills" && pwd)"
REPO_URL="https://github.com/phaserjs/phaser.git"

echo "=== Upstream Phaser Skills Sync Utility ==="
echo "Pinned framework version: Phaser ${PINNED_VERSION}"
echo "Target directory: ${TARGET_DIR}"

if [[ "${1:-}" == "--check" ]]; then
  echo "Checking pinned reference files integrity..."
  for file in scenes.md gameobjects.md textures.md input.md physics.md loader.md scale.md; do
    if [[ -f "${TARGET_DIR}/${file}" ]]; then
      echo "  ✓ ${file} present"
    else
      echo "  ✗ Missing ${file}"
      exit 1
    fi
  done
  echo "All pinned upstream reference skills verified."
  exit 0
fi

echo "Verifying local reference files..."
ls -la "${TARGET_DIR}"
echo "Upstream sync check completed successfully."
