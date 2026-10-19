#!/usr/bin/env python3
"""Unified evaluation runner for phaserjs-2d-mobile-game-dev."""

import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent


def main():
    print("=== Running phaserjs-2d-mobile-game-dev Evaluation Corpus ===\n")
    evals_dir = repo_root / "evals"
    eval_scripts = [
        evals_dir / "test-router-selection.py",
        evals_dir / "test-asset-reuse-priority.py",
        evals_dir / "test-report-schema.py",
        evals_dir / "test-quality-contract.py",
        evals_dir / "test-priority-formula.py",
        evals_dir / "test-art-intelligence.py",
        evals_dir / "test-genre-profiles.py",
        evals_dir / "test-verify-command.py",
        evals_dir / "test-prove-improvements.py"
    ]

    failed = 0
    for script in eval_scripts:
        print(f"--- Running {script.name} ---")
        res = subprocess.call([sys.executable, str(script)])
        if res != 0:
            print(f"✗ {script.name} failed with exit code {res}\n", file=sys.stderr)
            failed += 1
        else:
            print(f"✓ {script.name} passed.\n")

    if failed > 0:
        print(f"ERROR: {failed} evaluation test(s) failed.", file=sys.stderr)
        sys.exit(1)

    print("=============================================================")
    print(f"✓ All {len(eval_scripts)} evaluation suites passed successfully!")
    print("=============================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
