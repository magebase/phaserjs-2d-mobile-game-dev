# Playbook: Cloudflare Edge Primitives (D1, R2, KV, Queues & Durable Objects)

> **Domain:** Backend  
> **Capability ID:** `backend.d1_r2_kv_queues_durable_objects`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides leveraging Cloudflare's serverless edge primitives (D1 SQL, R2 Object Storage, KV, Queues, and Durable Objects) to power high-scale, low-cost backend game infrastructure.

---

## 2. Edge Primitive Mapping for Games

| Primitive | Primary Game Role | Key Operational Rule |
| :--- | :--- | :--- |
| **D1 (SQL)** | Relational player profiles, leaderboards, cloud saves | Index all lookup columns (`user_id`, `score`); D1 bills by rows touched. |
| **R2 (Storage)** | Progressive asset streaming, high-res audio, DLC packs | Serve through Custom Domains or Workers Cache to minimize egress hits. |
| **KV (Key-Value)**| LiveOps remote configs, maintenance flags, item catalogs | Cache heavily at edge; ideal for read-heavy, rarely-mutated configs. |
| **Queues** | Asynchronous analytics telemetry, combat logs | Always pair every queue with a Dead Letter Queue (DLQ). |
| **Durable Objects** | Real-time multiplayer rooms, active combat lobbies | Single-point-of-coordination for strongly consistent state. |

---

## 3. Implementation Patterns

### 3.1 D1 High Score Leaderboard Query
```sql
-- schema.sql
CREATE TABLE IF NOT EXISTS leaderboards (
  user_id TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  score INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_leaderboard_score ON leaderboards (score DESC);
```

```javascript
// Fetch top 10 players
const topPlayers = await env.GAME_DB.prepare(
  'SELECT username, score FROM leaderboards ORDER BY score DESC LIMIT 10'
).all();
```

### 3.2 Cloudflare Queues for Background Telemetry
```javascript
// Inside worker request handler:
await env.TELEMETRY_QUEUE.send({
  event: 'level_complete',
  userId: user.id,
  duration: 45,
  timestamp: Date.now()
});
```

---

## 4. Verification Checklist

- [ ] All D1 queries utilize indexed columns to avoid table-scan billing penalties.
- [ ] Telemetry ingestion utilizes Queues with an attached DLQ.
- [ ] Static game assets in R2 are served with appropriate caching headers.
