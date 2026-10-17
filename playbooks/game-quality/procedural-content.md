# Playbook: Deterministic Procedural Content Generation

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.procedural_content`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides implementing reproducible, seeded procedural generation for 2D levels (dungeons, endless runners) with guaranteed reachability checks so levels are never impassable.

---

## 2. Seeded PRNG (Mulberry32)

Never use raw `Math.random()` for procedural generation; use a seeded PRNG so bugs and runs can be reproduced:

```javascript
export function createRNG(seed = 1337) {
  let s = seed >>> 0;
  return function() {
    s |= 0; s = s + 0x6D2B79F5 | 0;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
```

---

## 3. Flood-Fill Reachability Verification

Before rendering tiles or spawning enemies, prove the level exit is reachable from player spawn:

```javascript
export function isLevelSolvable(grid, startX, startY, exitX, exitY) {
  const rows = grid.length;
  const cols = grid[0].length;
  const visited = Array.from({ length: rows }, () => Array(cols).fill(false));
  const queue = [[startX, startY]];
  visited[startY][startX] = true;

  const dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]];

  while (queue.length > 0) {
    const [cx, cy] = queue.shift();
    if (cx === exitX && cy === exitY) {
      return true; // Exit is reachable!
    }

    for (const [dx, dy] of dirs) {
      const nx = cx + dx;
      const ny = cy + dy;
      if (nx >= 0 && nx < cols && ny >= 0 && ny < rows) {
        if (!visited[ny][nx] && grid[ny][nx] === 0) { // 0 = floor, 1 = wall
          visited[ny][nx] = true;
          queue.push([nx, ny]);
        }
      }
    }
  }
  return false; // Trapped! Reject map and regenerate
}
```

---

## 4. Verification Checklist

- [ ] Same integer seed produces identical tile layouts, enemy placements, and item spawns.
- [ ] Level generation never yields a map where the exit or key objective is unreachable (reachability test passes 100/100 random seeds).
- [ ] Generation executes in $< 50\text{ms}$ to avoid mobile frame lag during transitions.
