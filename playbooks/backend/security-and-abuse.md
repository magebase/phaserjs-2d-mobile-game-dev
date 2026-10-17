# Playbook: Anti-Cheat, Rate Limiting & Secret Hygiene

> **Domain:** Backend  
> **Capability ID:** `backend.security_and_abuse`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-07 (Leaked Secrets in Client Bundle)

---

## 1. Purpose & Scope

This playbook guides preventing client-side secret exposure in distribution bundles (**RB-07**), mitigating leaderboard tampering through server-side score validation, and applying edge rate limits.

---

## 2. Zero Secrets in Client Bundles (RB-07)

Client game JavaScript is public code. Any private key bundled into `/dist` or `/build` is instantly compromised.

### Automated Bundle Audit Command:
```bash
# Scan output for private keys, AWS tokens, Stripe secrets
./tools/magebase-game probe /path/to/game
```

**Guardrail Rules**:
- Client variables must only reference public variables (`VITE_PUBLIC_*`, `NEXT_PUBLIC_*`).
- Database credentials and private JWT keys belong exclusively in server environments (`.env.local`, Cloudflare Secrets).

---

## 3. Server-Side Score Validation (Anti-Cheat)

Never allow the client to submit an arbitrary integer score without validation:

```javascript
// Edge validation function in Worker or Django view
export function validateSubmittedScore(payload) {
  const { score, elapsedSeconds, enemiesDefeated } = payload;

  // Sanity check 1: Impossible score rate
  const maxPossibleScorePerSecond = 500;
  if (score > elapsedSeconds * maxPossibleScorePerSecond) {
    return { valid: false, reason: 'Score exceeds theoretical maximum rate' };
  }

  // Sanity check 2: Enemy kill consistency
  if (enemiesDefeated > elapsedSeconds * 5) {
    return { valid: false, reason: 'Kill rate exceeds physical limits' };
  }

  return { valid: true };
}
```

---

## 4. Edge Rate Limiting

Protect backend endpoints against spamming bots using Cloudflare edge rate limits:

```javascript
// Inside worker request handler:
const clientIp = request.headers.get('CF-Connecting-IP') || 'unknown';
const rateLimitKey = `rate_${clientIp}`;

// Reject if client makes > 10 save requests per minute
```

---

## 5. Verification Checklist

- [ ] Secret scanner returns zero findings on production `/dist` bundles.
- [ ] Submitting impossible score values is rejected with HTTP 400.
- [ ] Endpoints reject burst spam over declared rate-limit thresholds.
