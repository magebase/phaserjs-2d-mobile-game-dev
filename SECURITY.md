# SECURITY.md — Security Policy & Client Bundle Hygiene

> **Security Policy for:** `magebase/phaserjs-2d-mobile-game-dev`

---

## 1. Zero Secrets in Client Bundles (Hard Blocker RB-07)

Browser-based and mobile web games are client-executed code. All client assets and bundled JavaScript files can be easily decompiled, inspected, and extracted by end users.

### Strict Rules:
1. **Never embed secret credentials** in client-side game code:
   - No database connection strings (`postgres://`, `sqlite://`).
   - No Cloudflare API tokens, Global Keys, or Account IDs.
   - No Stripe or payment processor Secret Keys (only Publishable Keys).
   - No private JWT signing keys or admin passwords.
2. **Environment Variable Separation**:
   - Only variables prefixed with public markers (e.g. `VITE_PUBLIC_`, `NEXT_PUBLIC_`) may be referenced in client game scripts.
   - All sensitive writes and transaction validations must occur on the backend (Django / Cloudflare Worker).
3. **Automated Bundle Audits**:
   - Tool `project-probe` scans bundles for regex patterns matching AWS, Cloudflare, OpenAI, Stripe, and generic API key entropy patterns.

---

## 2. Content Security Policy (CSP) for Phaser 4

When deploying Phaser 4 web games, enforce a strict Content Security Policy to prevent cross-site scripting (XSS) and asset injection:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' data: blob:; connect-src 'self' https://api.yourdomain.com;
```

> **Note on WebAssembly**: Phaser 4 features and physics engines utilizing WebAssembly require `'wasm-unsafe-eval'` in modern CSP specifications. Never use generic `'unsafe-eval'`.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability in this repository or its tools, please disclose it responsibly:
- **Email:** `security@magebase.dev`
- **Response SLA:** Vulnerability reports are triaged within 48 hours, and patches are published within 7 days.
- Please do not open public GitHub issues for security vulnerabilities until a patch has been coordinated.
