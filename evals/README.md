# Evaluation Corpus & Quality Benchmark

> **Repository:** `phaserjs-2d-mobile-game-dev`  
> **Target Engine:** Phaser 4.2.1

This directory contains the automated evaluation test corpus used to measure router capability selection, asset discovery & defect precision, JSON schema compliance, and hard release blocker enforcement.

---

## 1. Evaluation Suites Overview

| Suite | Category | Tested Behavior |
| :--- | :--- | :--- |
| `test-router-selection.py` | `routing/` | Evaluates natural language prompt matching against `registry/capabilities.json`. |
| `test-asset-reuse-priority.py` | `asset-qa/` | Verifies cryptographic duplicate detection and non-power-of-two (NPOT) texture defect discovery. |
| `test-report-schema.py` | `project-discovery/` | Validates end-to-end audit report generation and schema compliance against `schemas/audit-report.schema.json`. |
| `test-quality-contract.py` | `gameplay-quality/` | Asserts that hard release blockers (RB-01 through RB-08) correctly trigger when defects are injected. |

---

## 2. Running Evaluations

Run the entire evaluation corpus with one command:

```bash
python3 scripts/run-evals.py
```

All 4 test suites must pass with exit code 0 before any PR can be merged.
