# CONTRIBUTING.md — Contributor Guidelines

Thank you for contributing to `phaserjs-2d-mobile-game-dev`! This repository acts as an agent-first engineering operating system, which requires high standards for consistency, schema adherence, and verifiable automated tests.

---

## 1. Development Principles

1. **Schema-First**: Every new data structure, profile field, or report output must be declared in `schemas/` and validated.
2. **Registry-Driven**: Every new playbook must be cataloged in `registry/capabilities.json` with clear trigger keywords, prerequisites, inputs, and outputs.
3. **No Dead Links**: Every markdown link and cross-reference between playbooks and tools must be valid and verified by `scripts/validate-skills.py`.
4. **Offline Resilience**: Tests and evaluation suites must not rely on live third-party network services. Use local mock fixtures in `fixtures/`.

---

## 2. Setting Up the Local Environment

Ensure you have Python 3.10+ and Node.js 18+ installed:

```bash
# Clone the repository
git clone https://github.com/magebase/phaserjs-2d-mobile-game-dev.git
cd phaserjs-2d-mobile-game-dev

# Install Python validation dependencies
python3 -m pip install -r scripts/requirements.txt
```

---

## 3. Running Validation & Tests

Before submitting any Pull Request, all three validation scripts must pass cleanly:

```bash
# 1. Validate all skill files and markdown links
python3 scripts/validate-skills.py

# 2. Validate capability registry against schema and check playbook paths
python3 scripts/validate-registry.py

# 3. Run the evaluation test suite against fixtures
python3 scripts/run-evals.py
```

---

## 4. Adding a New Playbook

When adding a playbook:
1. Place the markdown file in the appropriate domain folder under `playbooks/<domain>/`.
2. Follow the standardized playbook structure:
   - Purpose & Scope
   - When to Use (Triggers)
   - Step-by-Step Procedure
   - Code Patterns & Best Practices
   - Verification Commands
   - Common Pitfalls
3. Register the playbook in `registry/capabilities.json`.
4. Run `python3 scripts/validate-registry.py` to confirm path resolution and syntax.

---

## 5. Pull Request Checklist

- [ ] All new capabilities registered in `registry/capabilities.json`.
- [ ] Schema changes reflected in `schemas/` and sample templates in `templates/`.
- [ ] Added or updated test cases in `evals/`.
- [ ] `validate-skills.py`, `validate-registry.py`, and `run-evals.py` all return exit code 0.
- [ ] `CHANGELOG.md` updated with your changes.
