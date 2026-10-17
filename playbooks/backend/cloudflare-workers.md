# Playbook: Cloudflare Serverless Workers Integration

> **Domain:** Backend  
> **Capability ID:** `backend.cloudflare_workers`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides configuring and deploying ultra-low-latency serverless edge APIs for Phaser 4 games using Cloudflare Workers (JavaScript, TypeScript, or Python).

---

## 2. Serverless Edge API Worker Blueprint

In `workers/game-api.js` (or `.ts`):

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '*';

    // Standard Edge CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Allow-Credentials': 'true'
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Route: Save Game State
    if (url.pathname === '/api/v1/save' && request.method === 'POST') {
      const payload = await request.json();
      const userId = payload.userId || 'anonymous';

      // Save to D1 or KV
      if (env.GAME_DB) {
        await env.GAME_DB.prepare(
          'INSERT OR REPLACE INTO player_saves (user_id, state_json, updated_at) VALUES (?, ?, ?)'
        ).bind(userId, JSON.stringify(payload), Date.now()).run();
      }

      return new Response(JSON.stringify({ status: 'saved', updatedAt: Date.now() }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
};
```

---

## 3. Wrangler Configuration Reference

In `wrangler.jsonc`:
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "phaser-game-edge-api",
  "main": "workers/game-api.js",
  "compatibility_date": "2026-09-02",
  "limits": {
    "cpu_ms": 50
  }
}
```

---

## 4. Verification Checklist

- [ ] Worker responds to OPTIONS preflight with HTTP 200 and CORS headers.
- [ ] Save payloads persist to edge storage and return valid JSON.
- [ ] Worker execution completes well within the 50ms CPU ceiling.
